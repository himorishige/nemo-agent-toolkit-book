# 第 7 章 Phoenix で観測する

docker compose に Arize Phoenix service を追加し、NAT ワークフローのトレースを可視化します。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# Phoenix を先に起動
docker compose up -d phoenix

# NAT を実行（トレースは phoenix service に送信される）
docker compose run --rm nat

# ブラウザで http://localhost:6006 を開き、Project 「nat-handson-ch07」を確認
```

## ファイル構成

- `workflow.yml` — `general.telemetry.tracing.phoenix` を追加して OTLP 送信
- `docker-compose.yml` — phoenix + nat の 2 service
- `.env.example`

## 後片付け

```bash
docker compose down
```

Phoenix のデータは永続化していません（検証用途）。長期運用したい場合は volume をマウントしてください。

詳細は Zenn Book [第 7 章「Phoenix で観測する」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
