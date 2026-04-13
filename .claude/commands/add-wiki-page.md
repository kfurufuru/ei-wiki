# 新規Wikiページ追加

ei-wikiに新しいページを追加する手順。

## 引数

- `$ARGUMENTS`: 配置場所/ファイル名 ページタイトル（例: "01-koatsu/relay-test 保護リレー試験"）

## 手順

1. ページ種別に応じたテンプレートを `docs/templates/` から読み込む:
   - `template-reference.md` — 仕様・選定ガイド系
   - `template-procedure.md` — 作業手順系
   - `template-trouble.md` — トラブルシューティング系

2. `docs/` 配下の適切なディレクトリにMarkdownファイルを作成
   - ファイル名はケバブケースで命名
   - フロントマターは必須:
     ```yaml
     ---
     title: ページタイトル
     description: 1行説明
     tags: [タグ1, タグ2]
     audience: [電気主任, 保全担当]
     last_verified: 2026-04-13
     ---
     ```
   - トラブルシューティングページは `search: boost: 2` を追加

3. `mkdocs.yml` の `nav` セクションに新ページを追加
   - 既存の階層構造とインデントを維持すること
   - 適切なセクション配下に配置

4. `docs/index.md` に新ページへのリンクを追加（必要な場合）

5. `mkdocs serve` でローカルプレビューして確認

## 注意事項

- 数式は MathJax 記法を使用
- 図はMermaid記法またはHTML埋め込み
- admonition（`!!! tip`, `!!! warning`, `!!! danger`）を活用
- 略語は `docs/includes/abbreviations.md` に自動登録済み（追加が必要なら更新）
