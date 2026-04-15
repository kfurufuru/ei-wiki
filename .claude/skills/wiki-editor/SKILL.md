---
name: wiki-editor
description: ei-wiki（電気計装 実務Wiki）に記事を追加・更新するときに使う。ファイル作成・frontmatter付与・mkdocs.yml nav登録・内部リンク整合の4工程を順に実行し、記事の品質と構造整合を保証する。
---

# Wiki Editor — ei-wiki

## いつ使うか

- 新規ページを作成するとき（`add-wiki-page` コマンドの上位版 / 対話形式で内容も生成する場合）
- 既存ページを更新して frontmatter の `last_verified` やリンクを直すとき
- nav に記事が漏れていることに気づいたとき

> `add-wiki-page` は「場所とタイトルが確定している単純追加」向け。このSkillは内容まで対話生成し品質チェックまで行う。

## ワークフロー

1. **配置カテゴリを確定する**
   - mkdocs.yml の nav を Read して既存セクション（`01-koatsu` 〜 `reference`）を確認
   - 新セクションが必要かどうか判断し、必要なら提案する

2. **テンプレートを選ぶ**（`docs/templates/` から Read）
   - `template-reference.md` — 仕様・選定ガイド系
   - `template-procedure.md` — 作業手順系
   - `template-trouble.md` — トラブルシューティング系
   - トラブル系は frontmatter に `search: boost: 2` を追加

3. **ファイルを作成する**
   - パス: `docs/<カテゴリ>/kebab-case.md`
   - frontmatter は下記「frontmatter 形式」に従う
   - 本文は `mkdocs-rules.md` と `japanese-content.md` のルールに従う（Read 済みの場合は再Read不要）

4. **mkdocs.yml の nav を更新する**
   - Read → Edit で該当セクションに1行追加
   - インデントと既存順序を維持する

5. **内部リンク整合を確認する**
   - 新ページからリンクしている `docs/` 内パスが実在するか確認
   - 既存ページから新ページへのリンクが必要な場合は提案する

6. **完了報告**
   - 作成/更新したファイルパスと行数を列挙
   - `mkdocs serve` で確認するよう案内する

## 命名規約

- ファイル名: `kebab-case.md`（小文字・ハイフンのみ）
- 配置: `docs/<カテゴリ>/`（カテゴリは `01-koatsu` 〜 `reference` の既存フォルダ）

## frontmatter 形式

```yaml
---
title: ページタイトル（日本語可）
description: 1行説明
tags: [タグ1, タグ2]
audience: [電気主任, 保全担当]
last_verified: YYYY-MM-DD
---
```

トラブルシューティングページは `search: boost: 2` を追加する。

## チェックリスト

- [ ] mkdocs.yml の nav に追加済み
- [ ] frontmatter の必須キー（title / description / tags / audience / last_verified）が揃っている
- [ ] 内部リンクのパスが `docs/` 基準で実在する
- [ ] 日本語組版 → `japanese-content.md` に従っている（専門用語英語併記・単位半角スペース）
- [ ] Markdown 記法 → `mkdocs-rules.md` に従っている（見出し・admonition・コードブロック言語指定）

## 参照

- 命名・Markdown記法: `.claude/rules/mkdocs-rules.md`
- 日本語組版・用語統一: `.claude/rules/japanese-content.md`
- 単純追加（場所確定済み）: `.claude/commands/add-wiki-page.md`
- カテゴリ構造: `mkdocs.yml` の nav セクション（01-koatsu 〜 reference）
