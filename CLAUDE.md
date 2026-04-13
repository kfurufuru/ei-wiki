# ei-wiki

電気計装の実務知識を集約したWikiサイト。

## プロジェクト概要

- **サイト**: https://kfurufuru.github.io/ei-wiki/
- **リポジトリ**: kfurufuru/ei-wiki
- **目的**: 化学プラントの電気計装実務ナレッジベース（高圧受変電、保護協調、計装、トラブルシューティング等）
- **対象**: 電気主任技術者、計装エンジニア、電験学習者

## 技術スタック

- MkDocs + Material for MkDocs（静的サイトジェネレータ）
- GitHub Pages（ホスティング）
- GitHub Actions（自動デプロイ: `.github/workflows/deploy.yml`）
- MathJax（数式）/ Mermaid（図表）
- Python（MkDocs依存。`mkdocs-material` のみ）

## ファイル構造

```
ei-wiki/
├── mkdocs.yml              # サイト設定・ナビゲーション（nav約200エントリ）
├── docs/
│   ├── index.md            # トップページ
│   ├── getting-started.md  # 読み方ガイド
│   ├── 01-koatsu/          # 高圧受変電（11ページ）
│   ├── 02-teiatsu/         # 低圧設備（11ページ）
│   ├── 03-keiso/           # 計装・プロセス制御（13ページ）
│   ├── 04-sekkei/          # 電気設計（11ページ）
│   ├── 05-hozen/           # 保全・点検（9ページ）
│   ├── 06-trouble/         # トラブルシューティング（9ページ）
│   ├── 07-tsurumi/         # 鶴見工場固有（5ページ）
│   ├── 08-energy/          # 省エネ・エネルギー管理（6ページ）
│   ├── 09-hoantokei/       # 電気主任技術者業務（5ページ）
│   ├── 10-safety/          # 安全管理・作業許可（5ページ）
│   ├── 11-genai/           # 生成AI業務活用（7ページ）
│   ├── reference/          # 用語集・規格一覧・計算ツール
│   ├── templates/          # ページテンプレート（reference/procedure/trouble）
│   ├── includes/           # abbreviations.md（略語ツールチップ、全ページ自動付与）
│   ├── stylesheets/        # custom.css
│   ├── javascripts/        # cable-calc.js 等
│   └── overrides/          # MkDocsテーマオーバーライド
├── .github/workflows/deploy.yml
└── .claude/
    ├── commands/           # add-wiki-page, add-calculator, deploy-wiki
    └── rules/              # japanese-content, mkdocs-rules
```

## よく使うコマンド

```bash
mkdocs serve              # ローカルプレビュー（http://127.0.0.1:8000）
mkdocs build              # 静的サイトビルド
# デプロイはmainブランチへのpushでGitHub Actions自動実行
```

## コンテンツ規約

### フロントマター（全ページ必須）
```yaml
---
title: ページタイトル
description: 1行説明
tags: [高圧, 受変電]
audience: [電気主任, 保全担当]
last_verified: 2026-01-15
---
```
- トラブルシューティングページは `search: boost: 2` を追加

### Markdown規約
- H1はページに1つ。`##` 以下で階層構成
- リストは `-`（`*` 不可）
- コードブロックは言語指定必須
- 数式: インライン `$I = V/R$` / ブロック `$$P = VI\cos\theta$$`
- Admonition多用: `!!! tip`, `!!! warning`, `!!! danger`
- タブ: `=== "タブ名"`

### 日本語表記
- 「です・ます」調
- 専門用語は初出時に英語併記（例: 遮断器（Circuit Breaker））
- SI単位は半角スペース区切り（例: `100 V`, `50 A`）
- JIS/JEC準拠の用語を使用

### ページテンプレート
新規ページ作成時は `docs/templates/` の該当テンプレートをベースにする:
- `template-reference.md` — 仕様・選定ガイド系
- `template-procedure.md` — 作業手順系
- `template-trouble.md` — トラブルシューティング系

### HTMLツール（計算機等）
- docs内にHTML/JS/CSS埋め込み（単一ファイル完結）
- レスポンシブデザイン・入力バリデーション必須

## 命名規則

- ファイル名: ケバブケース（例: `motor-control.md`）
- フォルダ: 2桁プレフィックス+英語名（例: `01-koatsu`）
- ブランチ: `feature/ページ名` または `fix/修正内容`
- コミット: 日本語可。`add:`, `fix:`, `update:`, `feat:` プレフィックス推奨

## mkdocs.yml 編集時の注意

- navツリーは既存の階層構造を維持（約200エントリ）
- 新ページ追加時はnavへの追加 + index.mdの更新を忘れずに
- searchプラグインの日本語トークナイザ設定を維持
- abbreviations.mdのsnippets設定を維持
