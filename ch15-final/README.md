# 第 15 章 題材アプリ総仕上げ

本書で作ってきた要素をすべて 1 つの docker compose に統合した「NVIDIA NAT docs & 一般知識ハイブリッド Q&A」エージェントです。

## アーキテクチャ

- **Milvus + etcd + minio**（第 9-10 章） - NAT 公式 docs のベクトルストア
- **Phoenix**（第 7 章） - OTLP トレース可視化
- **agent-nat-docs**（A2A サーバー、第 12 章） - RAG ReAct を 10001 番で公開

## NAT 1.6.0 の制約

- `router_agent` の `branches:` は `function_groups:` を展開しない（`function` 名のみ）。そのため本章では `per_user_react_agent` を採用
- `per_user_react_agent` は JWT の `sub` / `user_id` claim が必須
- A2A client が Agent Card から展開したスキルを呼ぶ際、引数スキーマの型変換エラー（`Cannot convert type <str> to <InputArgsSchema>`）が発生することがある（既知課題）
- **agent-main**（FastAPI フロント、第 14 章） - `per_user_react_agent` が `/v1/chat` 経由で 3 tool を使い分け
  - `nat_docs_a2a`（A2A client 経由で NAT docs Agent）
  - `wiki_lookup`（Wikipedia）
  - `current_datetime`

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# Milvus + ingest（初回のみ）
docker compose up -d milvus
# ingest は entrypoint override で実行
docker run --rm --network ch15-final_default \
  -v $PWD/scripts:/app/scripts:ro -v $PWD/../datasets:/app/datasets:ro \
  --env-file .env -e MILVUS_URI=http://milvus:19530 \
  --entrypoint python nat-nim-handson:1.6.0 /app/scripts/ingest.py

# 全 service 起動（Phoenix + A2A サーバー + FastAPI フロント）
docker compose up -d phoenix agent-nat-docs agent-main
sleep 15
docker compose logs -f agent-main | tail -20

# ダミー JWT 生成（per_user_react_agent は user_id 必須）
JWT=$(python3 -c "
import base64, json
h=base64.urlsafe_b64encode(json.dumps({'alg':'none','typ':'JWT'}).encode()).decode().rstrip('=')
p=base64.urlsafe_b64encode(json.dumps({'sub':'test','user_id':'test'}).encode()).decode().rstrip('=')
print(f'{h}.{p}.')")

# 動作確認（OpenAI 互換エンドポイント）
curl -s -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"messages":[{"role":"user","content":"Who founded NVIDIA?"}]}' | jq '.choices[0].message.content'

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
