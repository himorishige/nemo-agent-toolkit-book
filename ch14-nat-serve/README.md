# 第 14 章 `nat serve` で Web API 化

NAT ワークフローを FastAPI として HTTP 公開し、curl / httpx / OpenAI 互換クライアントから叩けるようにします。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# FastAPI サーバー起動（port 8000）
docker compose up -d
docker compose logs -f nat-api   # 起動ログ追跡用

# 動作確認
curl -s http://localhost:8000/health
# => {"status":"healthy"}

curl -s -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is today date?"}]}'

# ブラウザで Swagger UI
open http://localhost:8000/docs    # macOS
# xdg-open http://localhost:8000/docs  # Linux

docker compose down
```

## 主要エンドポイント（OpenAPI 3.1）

| path             | 用途                                       |
| ---------------- | ------------------------------------------ |
| `/health`        | ヘルスチェック                             |
| `/docs`          | Swagger UI                                 |
| `/openapi.json`  | OpenAPI 3.1 schema                         |
| `/generate`      | 単発実行（input_message 1 つを渡す）       |
| `/generate/stream` | 同上、SSE ストリーミング                  |
| `/v1/chat`       | OpenAI Chat Completions 互換               |
| `/v1/chat/stream`| 同上、SSE ストリーミング                  |
| `/v1/workflow`   | workflow 単発実行                          |

詳細は Zenn Book [第 14 章「`nat serve` で Web API 化」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
