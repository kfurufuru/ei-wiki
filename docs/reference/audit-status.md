---
title: "記事鮮度監査ダッシュボード"
description: "last_verified による記事鮮度の3バケット運用と CI 連動の仕組み"
last_verified: 2026-05-19
tags:
  - リファレンス
  - 監査
---

# 記事鮮度監査ダッシュボード

本Wikiでは各記事のフロントマターに `last_verified: YYYY-MM-DD` を記録し、最終確認日からの経過日数で **EXPIRED / DUE_SOON / OK** の3バケットに分類して鮮度を管理します。バケット境界は EXPIRED が365日超、DUE_SOON が300〜365日、OK が300日未満で、月初に GitHub Actions で自動スキャンし、EXPIRED が1件でも残っていれば CI が失敗するように連動させています。これにより、放置記事の検出と更新タイミングの可視化を運用コストゼロで継続できます。

最新スキャン日: 2026-05-19

## ローカル実行方法

リポジトリルートから以下を実行すると、Markdown 表形式で鮮度レポートが標準出力に出ます。

```bash
# 全件一覧
python scripts/check_last_verified.py

# CI モード（EXPIRED があれば exit 1）
python scripts/check_last_verified.py --ci

# 基準日を指定して試算（例: 半年後の状態）
python scripts/check_last_verified.py --today 2026-11-19
```

外部ライブラリ依存はなく、Python 3.11 標準ライブラリのみで動作します。

!!! tip "更新ルール"
    - 記事を実質修正した際は、フロントマターの `last_verified` を必ず当日日付に更新する
    - 365日経過した記事が残っていると CI（月初実行）が失敗する
    - DUE_SOON（300〜365日）に入ったら、次回編集機会に優先的に再確認する
