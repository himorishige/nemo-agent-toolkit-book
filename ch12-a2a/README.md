# 第 12 章 マルチエージェント②：A2A プロトコル

docker compose で 2 つの NAT プロセスを立て、一方を A2A サーバー・もう一方を A2A クライアントにしてエージェント間通信を見せます。

## 動かし方

```bash
cp .env.example .env

# Milvus + NAT docs を投入
docker compose up -d milvus
docker compose --profile ingest run --rm ingest

# A2A サーバー起動（NAT Docs Agent、port 10001）
docker compose up -d agent-nat-docs

# Agent Card を確認
curl -s http://localhost:10001/.well-known/agent-card.json | jq .

# A2A クライアント実行（per_user_react_agent が A2A 経由で agent-nat-docs を呼ぶ）
docker compose run --rm agent-main

# 後片付け
docker compose down
```

## ファイル構成

- `rag-agent.yml` — A2A サーバー側: RAG を `_type: a2a` front_end で公開
- `main-agent.yml` — A2A クライアント側: `function_groups.a2a_client` + `per_user_react_agent`
- `docker-compose.yml` — 6 service（etcd / minio / milvus / ingest / agent-nat-docs / agent-main）

## 備考

NAT 1.6.0 の `a2a_client` は per-user function group なので、workflow 側も `per_user_react_agent` を
使う必要があります。通常の `react_agent` では tool_names に A2A client を入れられません。

詳細は Zenn Book [第 12 章「マルチエージェント②：A2A プロトコル」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
