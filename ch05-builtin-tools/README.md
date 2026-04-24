# 第 5 章 組み込みツールを束ねる

ReAct エージェントに `current_datetime` と `wikipedia_search` を持たせ、質問内容に応じて自分でツールを選ぶ様子を観察します。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

docker compose run --rm nat
```

既定の質問は「Who is the current CEO of NVIDIA, and what date is it today?」です。`wikipedia_search` と `current_datetime` を両方呼ぶ挙動を期待しています。

## ファイル構成

- `workflow.yml` — 2 ツール構成（current_datetime + wiki_search）の ReAct
- `docker-compose.yml` — nat-nim-handson:1.6.0 イメージ + env_file + volumes
- `.env.example` — NGC API key 記入用

## 違う質問を試したいとき

```bash
docker compose run --rm nat \
  run --config_file /app/workflows/workflow.yml \
  --input "Give me a short summary of Apollo 11 mission."
```

詳細は Zenn Book [第 5 章「組み込みツールを束ねる」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
