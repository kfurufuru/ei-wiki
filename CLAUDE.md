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
- Mermaid（図表）。数式レンダラ（MathJax/KaTeX）は**未導入**＝数式はユニコード表記（下記Markdown規約）
- Python（MkDocs依存。`mkdocs-material` のみ）

## ファイル構造

```
ei-wiki/
├── mkdocs.yml              # サイト設定・ナビゲーション（nav約200エントリ）
├── requirements.txt        # mkdocs-material バージョン固定（pip install -r requirements.txt）
├── docs/
│   ├── index.md            # トップページ
│   ├── getting-started.md  # 読み方ガイド
│   ├── 01-koatsu/          # 高圧受変電
│   ├── 02-teiatsu/         # 低圧設備
│   ├── 03-keiso/           # 計装・プロセス制御
│   ├── 03-koji-kenshu/     # 工事・検収
│   ├── 04-sekkei/          # 電気設計
│   ├── 05-hozen/           # 保全・点検
│   ├── 06-trouble/         # トラブルシューティング
│   ├── (07-site/)          # 自工場固有 → private repo ei-wiki-private へ退避済み（2026-06-11）。本repoに置かないこと（mkdocs.ymlのexclude_docsは再追加事故ガードとして残置）
│   ├── 08-energy/          # 省エネ・エネルギー管理
│   ├── 09-hoantokei/       # 電気主任技術者業務
│   ├── 10-safety/          # 安全管理・作業許可
│   ├── 11-genai/           # 生成AI業務活用
│   ├── guidelines/         # 現場作業ガイドライン・チェックリスト
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
- 数式: **`$..$`/`$$..$$` のLaTeX記法は使用禁止**（レンダラ未配線のため文字のまま公開される。2026-06-11 PR #5で実害確認）。ユニコード表記で書く（例: `Io = √(Ioc² + Ior²)`、上付き²³・√・Δ・Ω等）。式の多いページが実際に必要になった時点でKaTeX配線を検討（AI社員諮問 2026-06-11 全員一致でYAGNI判断）
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

### タグ運用ルール（Phase 2-K4 タグ統制で確立）
- タグは**統制語彙30語のみ**使用。新タグ追加・表記揺れ禁止（定義: `docs/reference/tags.md`）
- 内訳: 分野11（高圧/低圧/計装/設計/保全/トラブル/工事管理/安全/法規・保安/省エネ/生成AI）＋主題14＋用途5
- 1ページ**2〜4個**。**分野1個必須**（所属ディレクトリで機械的に決定）＋主題0〜2個＋用途0〜1個
- 順序は 分野 → 主題 → 用途。1ページにしか付かない粒度の細かい語は付けず本文検索に委ねる
- 新語を足したくなったら語彙拡張ではなく `reference/tags.md` の既存語へのマッピングで対応

### HTMLツール（計算機等）
- docs内にHTML/JS/CSS埋め込み（単一ファイル完結）
- レスポンシブデザイン・入力バリデーション必須

## Skill配置ルール

| 配置 | パス | 対象Skill |
|------|------|----------|
| グローバル | `~/.claude/skills/` | ai-architect, ai-reviewer, inbox-manager, morning-reporter |
| ローカル | `.claude/skills/` | mkdocs-writer, wiki-deployer |

## 命名規則

- ファイル名: ケバブケース（例: `motor-control.md`）
- フォルダ: 2桁プレフィックス+英語名（例: `01-koatsu`）
- `03-keiso` と `03-koji-kenshu` はプレフィックスが重複しているが、公開URL維持のため既知のまま許容する
- ブランチ: `feature/ページ名` または `fix/修正内容`
- コミット: 日本語可。`add:`, `fix:`, `update:`, `feat:` プレフィックス推奨

## mkdocs.yml 編集時の注意

- navツリーは既存の階層構造を維持（約200エントリ）
- 新ページ追加時はnavへの追加 + index.mdの更新を忘れずに
- searchプラグインの日本語トークナイザ設定を維持
- abbreviations.mdのsnippets設定を維持
