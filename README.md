# NeMo Agent Toolkit NIM + Docker ハンズオン サンプルコード

Zenn Book **[NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson)** のサンプルコード配布リポジトリです。

各章の完成コードを `chNN-{topic}/` ディレクトリに置いています。章ごとに `docker compose up` または `docker compose run` だけで動作確認できる構成です。

## Prerequisites

- Docker（Colima 推奨 / Docker Desktop / native Docker Engine のいずれか）
- NGC API key（[build.nvidia.com](https://build.nvidia.com) で取得、Developer 無料枠あり）
- Python は不要（Docker コンテナ内で完結）

## クイックスタート（第 3 章の Hello Agent）

```bash
git clone https://github.com/himorishige/nemo-agent-toolkit-book.git
cd nemo-agent-toolkit-book

# まずベースイメージをビルド（章を跨いで使い回します）
docker build -t nat-nim-handson:1.6.0 docker/nat/

cd ch03-hello-agent
cp .env.example .env
# .env に NGC_API_KEY=nvapi-... を記入

docker compose run --rm nat
```

## 章別ディレクトリ

| 章   | ディレクトリ            | 内容                                                    |
| ---- | ----------------------- | ------------------------------------------------------- |
| 03   | `ch03-hello-agent/`     | `docker compose run nat` で ReAct 1 回実行              |
| 05   | `ch05-builtin-tools/`   | current_datetime / wikipedia_search 2 ツール ReAct      |
| 06   | `ch06-agent-patterns/`  | ReAct / ReWOO / Tool Calling 比較                       |
| 07   | `ch07-phoenix/`         | Phoenix service 追加 + OTLP トレース                    |
| 08   | `ch08-mcp/`             | MCP クライアント + `nat mcp serve`                      |
| 09   | `ch09-rag-milvus/`      | Milvus standalone + NIM Embedding で NAT docs RAG       |
| 10   | `ch10-rag-operations/`  | カテゴリ別フィルタ + top_k チューニング                 |
| 11   | `ch11-multi-agent/`     | `router_agent` で 3 branch 振り分け                     |
| 12   | `ch12-a2a/`             | `nat a2a serve` + `a2a_client` で 2 コンテナ連携        |
| 13   | `ch13-nat-eval/`        | 20 問データセット + trajectory / langsmith evaluator    |
| 14   | `ch14-nat-serve/`       | `nat serve` FastAPI 化（`/v1/chat` OpenAI 互換）        |
| 15   | `ch15-final/`           | 全 8 service 統合 compose（RAG + A2A + Router + 可視化） |

## 共通構成

- `docker/nat/` — 全章共通の NAT 実行コンテナ（`python:3.12-slim` + `nvidia-nat[langchain,mcp,eval,phoenix,a2a]==1.6.0`）
- `datasets/nat-docs/` — 第 9 章以降の RAG 用ソース（NVIDIA/NeMo-Agent-Toolkit docs 24 ファイル、Apache 2.0）
- `ch13-nat-eval/dataset/` — 第 13 章の評価用 20 問

## バージョン

| コンポーネント | バージョン                                  |
| -------------- | ------------------------------------------- |
| nvidia-nat     | 1.6.0                                       |
| Python         | 3.12（Docker イメージ側）                   |
| workflow LLM   | `nvidia/llama-3.3-nemotron-super-49b-v1`    |
| Embedding      | `nvidia/nv-embedqa-e5-v5`                   |
| Phoenix        | 14.8.0                                      |
| Milvus         | `milvusdb/milvus:v2.5.4`（Docker standalone）|

NAT 1.7 以降で動作が変わる箇所は、Zenn Book 側の章末または本リポの各章 README に差分メモを追記していきます。

## Python コードの lint / format

本書で Python コードが登場する章（第 9 章の ingest スクリプトなど）向けに、リポジトリルートの `pyproject.toml` で ruff を設定しています。

```bash
# lint
uvx ruff check .

# format（書き換え）
uvx ruff format .

# format 確認のみ（CI 向け）
uvx ruff format --check .
```

`uvx` は [uv](https://github.com/astral-sh/uv) のツールランナーで、Python 環境を汚さずに ruff を実行できます。`pip install ruff` で手元に入れて `ruff check .` でも同じことができます。

## License

Apache License 2.0。詳細は [LICENSE](./LICENSE) を参照してください。

`datasets/nat-docs/` 配下の Markdown は NVIDIA/NeMo-Agent-Toolkit リポジトリ（Apache 2.0）から抜粋したもので、同じく Apache 2.0 に従います。再利用時は `datasets/nat-docs/NOTICE.md` の引用条件を参照してください。
