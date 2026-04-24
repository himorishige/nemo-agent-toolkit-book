"""NAT docs を Milvus standalone に投入する ingest スクリプト.

実行:
    docker compose up -d milvus etcd minio
    docker compose --profile ingest run --rm ingest
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import DataType, MilvusClient

DOCS_DIR = Path("/app/datasets/nat-docs")
MILVUS_URI = os.environ.get("MILVUS_URI", "http://milvus:19530")
COLLECTION = "nat_docs"
EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"
EMBED_DIM = 1024
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_documents() -> list:
    """Markdown ファイルを読み込み LangChain Document 形式で返す."""
    md_files = sorted(p for p in DOCS_DIR.glob("*.md") if p.name not in {"NOTICE.md"})
    print(f"Loading {len(md_files)} markdown files from {DOCS_DIR}")

    documents = []
    for md in md_files:
        loader = TextLoader(str(md), encoding="utf-8")
        for doc in loader.load():
            doc.metadata["source"] = md.name
            documents.append(doc)
    return documents


def split_documents(documents: list) -> list:
    """Document を固定長チャンクに分割する."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def embed_chunks(chunks: list) -> list[list[float]]:
    """NIM Embedding API でチャンクをベクトル化する."""
    api_key = os.environ.get("NGC_API_KEY")
    if not api_key:
        sys.exit("NGC_API_KEY が環境変数に設定されていません")

    embedder = NVIDIAEmbeddings(model=EMBED_MODEL, api_key=api_key)
    texts = [chunk.page_content for chunk in chunks]
    vectors = embedder.embed_documents(texts)
    print(f"Embedded {len(vectors)} chunks with {EMBED_MODEL}")
    return vectors


def write_to_milvus(chunks: list, vectors: list[list[float]]) -> None:
    """Milvus standalone にコレクションを作成して書き込む."""
    client = MilvusClient(uri=MILVUS_URI)

    if client.has_collection(COLLECTION):
        client.drop_collection(COLLECTION)

    schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=EMBED_DIM)
    schema.add_field("text", DataType.VARCHAR, max_length=4096)
    schema.add_field("source", DataType.VARCHAR, max_length=256)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="L2",  # NAT 1.6.0 の milvus_retriever は既定で L2 で検索するため揃える
    )

    client.create_collection(
        collection_name=COLLECTION,
        schema=schema,
        index_params=index_params,
    )

    payload = [
        {
            "id": i,
            "vector": vec,
            "text": chunk.page_content[:4000],
            "source": chunk.metadata.get("source", ""),
        }
        for i, (vec, chunk) in enumerate(zip(vectors, chunks, strict=True))
    ]
    result = client.insert(collection_name=COLLECTION, data=payload)
    inserted = result.get("insert_count", len(payload))
    print(f"Inserted {inserted} records into collection '{COLLECTION}' at {MILVUS_URI}")


def main() -> None:
    docs = load_documents()
    chunks = split_documents(docs)
    vectors = embed_chunks(chunks)
    write_to_milvus(chunks, vectors)
    print("Done.")


if __name__ == "__main__":
    main()
