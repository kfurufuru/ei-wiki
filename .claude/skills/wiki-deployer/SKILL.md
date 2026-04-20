---
name: wiki-deployer
description: MkDocs Wikiのデプロイ確認を行う。ビルドエラー・nav整合・GitHub Pages反映を順に検証し、問題があれば修正方法を提示する。「デプロイ確認」「deploy」「wikiをデプロイして」で発動。
---

# Wiki Deployer Skill

## Why（存在理由）

Wiki記事追加後のデプロイ確認（ビルド成功・nav整合・GitHub Pages反映）に都度コマンドを手打ちしていた。このスキルが確認フローを自動化し、エラー時の修正方法まで提示することで、デプロイ完了を確実にする。

## いつ発動するか

- 「デプロイ確認」「deploy」「wikiをデプロイして」
- 「mkdocs buildが通るか確認して」
- wiki-editor でページ追加後の確認フェーズ

発動しないケース:
- 記事の内容作成 → wiki-editor スキル
- GitHub Actions の設定変更 → 直接 .github/workflows/ を編集

---

## 実行フロー（Sequential パターン）

### Step 1: mkdocs.yml 整合チェック

```bash
# nav に新規ページが登録されているか確認
```

`mkdocs.yml` を Read → nav セクションと `docs/` 配下のファイルを照合:
- navに記載されているが存在しないファイル → エラー報告
- ファイルが存在するがnavに未登録 → 警告（デプロイ後に404）

### Step 2: ローカルビルド

```bash
cd [プロジェクトルート] && mkdocs build --strict 2>&1
```

- SUCCESS → Step 3へ
- ERROR → エラー内容を解析して修正方法を提示してから停止

よくあるエラー:
| エラー | 原因 | 修正 |
|-------|------|------|
| `Doc file not found` | navのパス誤り | mkdocs.yml のパスを修正 |
| `MathJax tag not closed` | 数式記法誤り | `$$...$$` の対応確認 |
| `Admonition content missing` | admonitionインデント不足 | 4スペースインデント確認 |

### Step 3: Git コミット確認

```bash
git status && git diff --stat
```

未コミットファイルがあれば: 「以下のファイルがコミット待ちです。コミットしますか？」と確認。
承認後: `git add [ファイル] && git commit -m "add: [記事名]"` を実行。

### Step 4: GitHub Pages 反映確認

```bash
git push origin main
```

push後、GitHub Actions のワークフロー状態を確認（gh コマンド）:

```bash
gh run list --limit 3
```

- 実行中 → 「デプロイ中です。2〜3分後に確認してください」
- 成功 → 「デプロイ完了。[サイトURL] で確認してください」
- 失敗 → ログを取得して原因を提示

---

## 制約

- **コミット前確認必須**: 承認なしでgit commitしない
- **push前確認**: mainブランチへのpushは必ず確認を取る
- **build --strict**: 警告をエラーとして扱い、警告ゼロを目標とする

## 完了宣言

「デプロイ完了。[サイトURL] に反映されました。」または「ビルドエラー: [原因]。修正後に再実行してください。」

## 参照

- MkDocsルール: `.claude/rules/mkdocs-rules.md`
- デプロイワークフロー: `.github/workflows/deploy.yml`
- Wiki Editor: `.claude/skills/wiki-editor/SKILL.md`（記事作成→デプロイの連携）
