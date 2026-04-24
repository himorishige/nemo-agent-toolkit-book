# 第 3 章 最短 Hello Agent

NAT の ReAct エージェントを `docker compose run` で 1 回実行します。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

docker compose run --rm nat
```

NGC API key と NIM クラウド（build.nvidia.com）の疎通が通っていれば、ReAct ループが 1 周回って今日の日付を答えます。

## ファイル構成

- `workflow.yml` — NAT の設定ファイル（`_type: nim` で Llama 3.1 8B を叩く）
- `docker-compose.yml` — `nat-nim-handson:1.6.0` イメージを起動、`What is today's date?` を入力
- `.env.example` — NGC API key 記入用

## 違う質問を試したいとき

compose ファイルの `command:` を書き換えるか、コマンドラインで上書きします。

```bash
docker compose run --rm nat \
  run --config_file /app/workflows/workflow.yml \
  --input "Tell me the current date in Japanese."
```

詳細は Zenn Book [第 3 章「最短 Hello Agent」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
