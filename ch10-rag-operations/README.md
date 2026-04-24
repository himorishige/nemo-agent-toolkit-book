# 第 10 章 RAG 運用：永続化・メタデータフィルタ・top_k チューニング

第 9 章の Milvus 構成を踏襲しつつ、実運用で効いてくる 3 つのテクニックを並べます。

## 動かし方

```bash
cp .env.example .env

# Milvus スタック起動
docker compose up -d milvus

# カテゴリ付きで再 ingest
docker compose --profile ingest run --rm ingest

# 複数 retriever が混在する ReAct を実行
docker compose run --rm nat

# 後片付け（-v を付けると Milvus データまで消える）
docker compose down        # コンテナだけ停止、data volume は保持
# docker compose down -v   # volume も削除（次回は再 ingest が必要）
```

## ファイル構成

- `workflow.yml` — 3 つの retriever（全体 / get-started フィルタ / top_k=8）+ 3 つの tool
- `scripts/ingest_with_category.py` — metadata に category 付き Milvus 投入
- `docker-compose.yml` — ch09 と同じスタックを別 project 名で起動

詳細は Zenn Book [第 10 章「RAG 運用」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
