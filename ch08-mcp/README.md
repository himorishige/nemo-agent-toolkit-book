# 第 8 章 MCP サーバー連携

`nat mcp serve` で NAT ワークフローを MCP サーバーとして公開し、`nat mcp client` や Claude Desktop などの MCP クライアントから呼び出せるようにします。

## 動かし方

```bash
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

# MCP サーバーを起動（9901 ポートで待ち受け）
docker compose up -d nat-server
docker compose logs -f nat-server   # 起動ログを追いたい場合

# 別シェルから NAT の MCP クライアントで ping / tool list
docker compose --profile client run --rm nat-client \
  ping --url http://nat-server:9901/mcp

docker compose --profile client run --rm nat-client \
  tool list --url http://nat-server:9901/mcp
```

## Claude Desktop から接続する

macOS / Windows 側の Claude Desktop から、手元のマシン（`localhost`、LAN IP、Tailscale などの remote IP のいずれでも可）で動かしている MCP サーバーに接続する設定例は Zenn Book 第 8 章を参照してください。

## ファイル構成

- `workflow.yml` — 章 5 と同じ 2 ツール ReAct（MCP 公開対象）
- `docker-compose.yml` — `nat-server`（9901 公開）と `nat-client`（profile: client）の 2 service
- `.env.example`

詳細は Zenn Book [第 8 章「MCP サーバー連携」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) を参照してください。
