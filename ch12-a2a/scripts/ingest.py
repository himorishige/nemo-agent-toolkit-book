"""NAT docs をカテゴリ（source path 上位ディレクトリ）付きで Milvus に再投入する.

第 9 章の `ingest.py` との差分:
- metadata にカテゴリ（get-started / build-workflows / ...）を付けて検索フィルタできるようにする
- 既存コレクションを drop してから作り直す
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

# ファイル名の prefix でカテゴリを推定する簡易マッピング.
# 読者が自分のドキュメント構成に置き換えるときに同じ発想が使える.
CATEGORY_MAP = {
    "installation": "get-started",
    "quick-start": "get-started",
    "index": "get-started",
    "nat-readme": "get-started",
    "about-building-workflows": "build-workflows",
    "workflow-configuration": "build-workflows",
    "memory": "build-workflows",
    "object-store": "build-workflows",
    "embedders": "components",
    "retrievers": "components",
    "sharing-components": "components",
    "a2a-server": "run-workflows",
    "a2a-client": "run-workflows",
    "mcp-server": "run-workflows",
    "mcp-client": "run-workflows",
    "fastmcp-server": "run-workflows",
    "launching-ui": "run-workflows",
    "about-running-workflows": "run-workflows",
    "evaluate": "improve-workflows",
    "profiler": "improve-workflows",
    "optimizer": "improve-workflows",
    "sizing-calc": "improve-workflows",
    "test-time-compute": "improve-workflows",
    "about-improving-workflows": "improve-workflows",
}


def category_of(filename: str) -> str:
    stem = Path(filename).stem
    return CATEGORY_MAP.get(stem, "misc")


def load_documents() -> list:
    md_files = sorted(p for p in DOCS_DIR.glob("*.md") if p.name not in {"NOTICE.md"})
    print(f"Loading {len(md_files)} markdown files from {DOCS_DIR}")
    documents = []
    for md in md_files:
        loader = TextLoader(str(md), encoding="utf-8")
        for doc in loader.load():
            doc.metadata["source"] = md.name
            doc.metadata["category"] = category_of(md.name)
            documents.append(doc)
    return documents


def split_documents(documents: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def embed_chunks(chunks: list) -> list[list[float]]:
    api_key = os.environ.get("NGC_API_KEY")
    if not api_key:
        sys.exit("NGC_API_KEY が環境変数に設定されていません")
    embedder = NVIDIAEmbeddings(model=EMBED_MODEL, api_key=api_key)
    vectors = embedder.embed_documents([c.page_content for c in chunks])
    print(f"Embedded {len(vectors)} chunks with {EMBED_MODEL}")
    return vectors


def write_to_milvus(chunks: list, vectors: list[list[float]]) -> None:
    client = MilvusClient(uri=MILVUS_URI)

    if client.has_collection(COLLECTION):
        client.drop_collection(COLLECTION)

    schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=EMBED_DIM)
    schema.add_field("text", DataType.VARCHAR, max_length=4096)
    schema.add_field("source", DataType.VARCHAR, max_length=256)
    schema.add_field("category", DataType.VARCHAR, max_length=64)

    index_params = client.prepare_index_params()
    index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="L2")

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
            "category": chunk.metadata.get("category", "misc"),
        }
        for i, (vec, chunk) in enumerate(zip(vectors, chunks, strict=True))
    ]
    client.insert(collection_name=COLLECTION, data=payload)

    categories = {}
    for p in payload:
        categories[p["category"]] = categories.get(p["category"], 0) + 1
    print(f"Inserted {len(payload)} records into '{COLLECTION}' at {MILVUS_URI}")
    print("Per-category chunk counts:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")


def main() -> None:
    docs = load_documents()
    chunks = split_documents(docs)
    vectors = embed_chunks(chunks)
    write_to_milvus(chunks, vectors)
    print("Done.")


if __name__ == "__main__":
    main()
