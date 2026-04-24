# NeMo Agent Toolkit Cloud NIM + Docker ハンズオン サンプルコード

Zenn Book **[クラウド NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson)**（執筆中）のサンプルコード配布リポジトリです。

各章の完成コードを `ch0N-{topic}/` ディレクトリに置いています。章ごとに `docker compose up` または `docker compose run` だけで動作確認できる構成を目指しています。

## Prerequisites

- Docker（Colima 推奨 / Docker Desktop / native Docker Engine のいずれか）
- NGC API key（[build.nvidia.com](https://build.nvidia.com) で取得、無料枠あり）
- Python は不要（Docker コンテナ内で完結）

## クイックスタート（第 3 章の Hello Agent）

```bash
git clone https://github.com/himorishige/nemo-agent-toolkit-book.git
cd nemo-agent-toolkit-book/ch03-hello-agent

cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

docker compose run --rm nat
```

## 章別ディレクトリ

（執筆進捗に合わせて追加していきます）

| 章    | ディレクトリ                    | 内容                                           |
| ----- | ------------------------------- | ---------------------------------------------- |
| 02    | `ch02-environment/`             | Colima + Docker + NGC セットアップ             |
| 03    | `ch03-hello-agent/`             | `docker compose run nat` で ReAct 1 回実行     |
| 05    | `ch05-builtin-tools/`           | current_datetime / wikipedia_search / web_search |
| 06    | `ch06-agent-patterns/`          | ReAct / ReWOO / Tool Calling / Router 比較     |
| 07    | `ch07-phoenix/`                 | docker compose に phoenix service 追加         |
| 08    | `ch08-mcp/`                     | MCP クライアント + `nat mcp serve`             |
| 09    | `ch09-rag-faiss/`               | NIM Embedding + FAISS in-memory                |
| 10    | `ch10-rag-milvus/`              | Milvus Lite（ファイル DB）                     |
| 11    | `ch11-multi-agent/`             | Router + Wiki Agent + RAG Agent                |
| 12    | `ch12-a2a/`                     | agent-a / agent-b の 2 コンテナ A2A 通信       |
| 13    | `ch13-eval/`                    | 20 問データセット + LLM-as-Judge               |
| 14    | `ch14-serve/`                   | `nat serve` FastAPI 化                         |
| 15    | `ch15-final/`                   | 全 service 統合 compose                        |

## 共通構成

- `docker/nat/` — 全章共通の NAT 実行コンテナ（`python:3.12-slim` + `nvidia-nat==1.6.0`）
- `datasets/` — RAG / eval 用のソースデータ

## バージョン

- **NAT**: `nvidia-nat==1.6.0`
- **Python**: 3.12
- **クラウド NIM モデル**: `meta/llama-3.1-8b-instruct`（workflow）、`nvidia/llama-3.3-nemotron-super-49b-v1`（judge）
- **Embedding**: `nvidia/nv-embedqa-e5-v5`

NAT 1.7 以降で動作が変わる箇所は各章の README に差分メモを追記します。

## License

Apache License 2.0。詳細は [LICENSE](./LICENSE) を参照してください。

## Related

- 原稿リポジトリ: [himorishige/zenn-contents](https://github.com/himorishige/zenn-contents)
- 著者: [@himorishige](https://github.com/himorishige)
- 本書の企画プラン: ai-workspace 内の `plans/zenn-book-nemo-agent-tool-mutable-pebble.md`（private）
