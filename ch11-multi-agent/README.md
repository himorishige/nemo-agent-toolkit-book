# 第 11 章 マルチエージェント 1：Router で振り分ける

NAT 1.6.0 の `router_agent` を使い、3 種類の tool に質問を振り分けるマルチエージェント構成です。

## 動かし方

```bash
cp .env.example .env

# Milvus スタック起動 + データ投入
docker compose up -d milvus
docker compose --profile ingest run --rm ingest

# ルーター実行（既定: NAT docs について質問）
docker compose run --rm nat

# 違う質問で branch を切り替える
docker compose run --rm nat \
  run --config_file /app/workflows/workflow.yml \
  --input "Who founded NVIDIA?"

docker compose run --rm nat \
  run --config_file /app/workflows/workflow.yml \
  --input "What is today's date?"

# 後片付け
docker compose down
```

## 3 つの branch

- `search_nat_docs` — NAT 公式 docs の RAG（Milvus）
- `wiki_lookup` — Wikipedia 検索
- `current_datetime` — 現在時刻

## 備考

NAT 1.6.0 の router_agent は、サブエージェント（react_agent）を直接 branches に入れると
`ChatRequestOrMessage` のスキーマ不一致で失敗します。本章では **tool / retriever 単位**で
branches を構成する形を採用しました。エージェント間通信は次章（A2A プロトコル）で扱います。

詳細は Zenn Book [第 11 章「マルチエージェント 1：Router で振り分ける」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
