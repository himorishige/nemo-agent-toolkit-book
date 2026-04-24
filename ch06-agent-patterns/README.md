# 第 6 章 エージェントパターンの使い分け

同じツール集合（`current_datetime` + `wikipedia_search`）を、異なるエージェントパターンで動かして挙動を比較します。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# ReAct
docker compose run --rm nat-react

# ReWOO
docker compose run --rm nat-rewoo

# Tool Calling
docker compose run --rm nat-tool-calling
```

docker compose の YAML アンカー（`x-nat-common`）で共通設定をまとめ、各 service は `workflow.yml` と command の差分だけを持ちます。

## ファイル構成

- `workflow-react.yml` — `_type: react_agent`
- `workflow-rewoo.yml` — `_type: rewoo_agent`
- `workflow-tool-calling.yml` — `_type: tool_calling_agent`
- `docker-compose.yml` — 3 service（nat-react / nat-rewoo / nat-tool-calling）
- `.env.example`

詳細は Zenn Book [第 6 章「エージェントパターンの使い分け」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
