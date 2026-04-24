# 第 9 章 RAG アドオン：Milvus に NAT docs を入れる

NVIDIA/NeMo-Agent-Toolkit の公式 docs（Apache 2.0）を Milvus に投入し、NAT の RAG として検索する構成です。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# 1. Milvus スタック（milvus + etcd + minio）を起動
docker compose up -d milvus

# 2. NAT docs を chunk + embedding + Milvus に投入
docker compose --profile ingest run --rm ingest

# 3. RAG エージェントを実行
docker compose run --rm nat

# 後片付け（volume まで消したい場合は `-v` を付ける）
docker compose down
```

## ファイル構成

- `docker-compose.yml` — 5 service（etcd / minio / milvus / ingest / nat）
- `workflow.yml` — `embedders` / `retrievers` / `retriever_tool` を使う ReAct 構成
- `scripts/ingest.py` — NAT docs を chunk → NIM Embedding → Milvus 投入
- `.env.example`

## データソース

`../datasets/nat-docs/` 配下の 24 Markdown ファイル（NVIDIA/NeMo-Agent-Toolkit リポから抜粋、Apache 2.0）。
詳細は `../datasets/nat-docs/NOTICE.md` を参照してください。

## 実測（2026-04-24、DGX Spark）

- 24 files → 1,034 chunks（size=500, overlap=100）
- NIM `nv-embedqa-e5-v5` で 1,034 embedding 生成
- Milvus 投入後、`search_nat_docs` tool が 3 records を返し ReAct が正しく要約

詳細は Zenn Book [第 9 章「RAG アドオン：Milvus に NAT docs を入れる」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
