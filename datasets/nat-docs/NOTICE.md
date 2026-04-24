# NOTICE

このディレクトリに含まれる Markdown ファイル（`LICENSE` と本 `NOTICE.md` を除く）は、以下のオープンソースプロジェクトの公式ドキュメントを収録したものです。

- **Project**: NVIDIA NeMo Agent Toolkit
- **Repository**: https://github.com/NVIDIA/NeMo-Agent-Toolkit
- **License**: Apache License 2.0
- **Copyright**: Copyright (c) NVIDIA Corporation

本書 [Zenn Book「クラウド NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン」](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson) の第 9-10 章 で RAG のナレッジソースとして扱うために、2026-04-24 時点のリポジトリから `docs/source/` 配下の一部の `.md` ファイルを改変なしでコピーしています。

Apache License 2.0 の全文は同ディレクトリの `LICENSE` を参照してください。

## 取得コマンド

```bash
git clone --depth 1 https://github.com/NVIDIA/NeMo-Agent-Toolkit /tmp/nat-source
cp /tmp/nat-source/docs/source/{get-started,build-workflows,run-workflows,improve-workflows,components}/*.md ./
cp /tmp/nat-source/docs/source/index.md ./
cp /tmp/nat-source/README.md ./nat-readme.md
cp /tmp/nat-source/LICENSE.md ./LICENSE
```

## 変更の有無

- 改変なし（ファイル名はソースの basename をそのまま利用、内容はコピー元と同一）

## 再配布

読者が手元で動作確認できるよう、このリポジトリ（Apache 2.0 ライセンス）に含めています。
元のライセンスと著作権表示（Apache 2.0 + NVIDIA Corporation）を維持したうえでの再配布です。
