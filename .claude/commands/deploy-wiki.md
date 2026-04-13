# Wikiデプロイ確認

GitHub Actionsによるデプロイ状況を確認する。

## 手順

1. `gh run list --repo kfurufuru/ei-wiki --limit 5` で最新のワークフロー実行を確認
2. 失敗している場合は `gh run view <run-id> --log` でログを確認
3. デプロイ成功後、https://kfurufuru.github.io/ei-wiki/ でサイト表示を確認

## トラブルシューティング

- ビルドエラー: `mkdocs build` をローカルで実行し、エラー箇所を特定
- nav エラー: `mkdocs.yml` のインデントとファイルパスを確認
- 404エラー: ファイル名とnavの対応を確認
