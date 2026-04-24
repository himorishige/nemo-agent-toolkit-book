# 第 15 章 題材アプリ総仕上げ

本書で作ってきた要素をすべて 1 つの docker compose に統合した「NVIDIA NAT docs & 一般知識ハイブリッド Q&A」エージェントです。

## アーキテクチャ

- **Milvus + etcd + minio**（第 9-10 章） - NAT 公式 docs のベクトルストア
- **Phoenix**（第 7 章） - OTLP トレース可視化
- **agent-nat-docs**（A2A サーバー、第 12 章） - RAG ReAct を 10001 番で公開
- **agent-main**（FastAPI フロント、第 14 章） - Router が `/v1/chat` 経由で 3 branch に振り分け
  - `nat_docs_a2a`（A2A client 経由で NAT docs Agent）
  - `wiki_lookup`（Wikipedia）
  - `current_datetime`

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# Milvus + ingest（初回のみ）
docker compose up -d milvus
docker compose --profile ingest run --rm ingest

# 全 service 起動（Phoenix + A2A サーバー + FastAPI フロント）
docker compose up -d phoenix agent-nat-docs agent-main
sleep 10
docker compose logs -f agent-main | tail -20

# 動作確認（OpenAI 互換エンドポイント）
curl -s -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"How do I configure a Milvus retriever in NAT?"}]}' | jq .

# Phoenix UI
open http://localhost:6006   # macOS

# 後片付け
docker compose down
```

## ファイル構成

- `rag-agent.yml` — A2A サーバー側（RAG ReAct）
- `main-agent.yml` — FastAPI フロント側（Router + A2A client + tool）
- `docker-compose.yml` — 8 service（etcd / minio / milvus / ingest / phoenix / agent-nat-docs / agent-main）
- `scripts/ingest.py` — ch10 のカテゴリ付き ingest
- `.env.example`

詳細は Zenn Book [第 15 章「題材アプリ総仕上げ」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
