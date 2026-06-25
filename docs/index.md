---
title: 電気計装 実務Wiki
description: 困ったらここを見る — 電気計装エンジニアのフィールドリファレンス
last_verified: 2026-05-20
hide:
  - navigation
  - toc
---

# 電気計装 実務Wiki

> :material-lifebuoy: **困ったらここを見る** — 現場で即時に開けるフィールドリファレンス

[:material-compass-outline: はじめての方へ — 読む順番ガイド](getting-started.md){ .ei-onboard }

## いま困っている？ — 症状TOP10

| 症状 | 最初に確認 | 詳細記事 |
|-----|-----------|---------|
| 遮断器がトリップした / OCRが動作した | トリップ表示灯の色・OCR表示窓を目視 | [保護継電器](01-koatsu/relay.md) |
| 地絡警報が出た | GR/DGRの動作表示・構外地絡か構内かを判定 | [保護継電器（GR/DGR）](01-koatsu/relay.md) |
| モーターが起動しない | 現場盤のサーマルリレーとMCの動作確認 | [モータートラブル](06-trouble/motor.md) |
| インバータがエラーコードを表示する | エラーコードをマニュアルで確認・過電流か過電圧かを判定 | [インバータトラブル](06-trouble/inverter.md) |
| 4-20mAが振り切れる（0mA / 20mA以上） | 0mAなら断線疑い、20mA以上なら電源側を確認 | [計装信号トラブル](06-trouble/signal.md) |
| 温度指示が実際と合わない | 基準接点補償回路の動作とTC/RTD断線アラームを確認 | [計装信号トラブル](06-trouble/signal.md) |
| 制御弁が動かない（全開/全閉固着） | エア圧力（0.14MPa以上）とI/P出力信号を確認 | [制御弁トラブル](06-trouble/valve.md) |
| PLC/DCSとの通信が切れた | 通信ケーブルの物理接続とリンクLEDの状態を確認 | [PLC/DCSトラブル](06-trouble/plc-dcs.md) |
| 計器の値がノイズで暴れる | ノイズ源（インバータ・溶接機）の稼働と連動するか確認 | [接地・ノイズ](06-trouble/grounding-noise.md) |
| 保護継電器が誤動作（不要動作）した | 動作した継電器の種別・整定値・動作前後の電流/電圧を記録 | [保護装置誤動作](06-trouble/protection.md) |

[症状逆引き全リストへ →](06-trouble/index.md){ .md-button }

!!! tip "まず何をすべきか迷ったら"
    症状が特定できない・どこから手をつけるか迷う場合は [トラブル初動対応フロー](guidelines/trouble-first-response.md) を開いてください。安全確保から切り分けまでの初動手順を現場でそのまま追えます。

## 仕事から探す

<div class="grid cards" markdown>

- :material-hammer-wrench: **新設・更新工事**

    ---

    工事の企画から竣工・検収までの全フロー。ベンダー完了後の確認実務も含む。

    [:octicons-arrow-right-24: 工事フローへ](03-koji-kenshu/index.md)

- :material-wrench-check: **点検・保全**

    ---

    定期点検・校正・寿命管理・故障予防。平常時の保全業務を網羅。

    [:octicons-arrow-right-24: 保全フローへ](05-hozen/index.md)

- :material-pencil-ruler: **設計・見積**

    ---

    仕様書から図面・計算・規格確認。新規導入・改造検討の判断軸。

    [:octicons-arrow-right-24: 設計フローへ](04-sekkei/investment-flow.md)

- :material-shield-alert: **安全・作業許可**

    ---

    LOTO・作業許可・特別教育・リスクアセスメント。安全業務の手順化。

    [:octicons-arrow-right-24: 安全管理へ](10-safety/index.md)

</div>

## 技術分野から探す

<div class="grid cards" markdown>

- :material-lightning-bolt: **[高圧](01-koatsu/index.md)**
  受変電・変圧器・保護継電器・高圧ケーブル

- :material-power-plug: **[低圧](02-teiatsu/index.md)**
  配電・モーター制御・インバータ・PLC

- :material-gauge: **[計装](03-keiso/index.md)**
  センサ・制御弁・PID・DCS・防爆

- :material-pencil-ruler: **[設計](04-sekkei/index.md)**
  仕様書・負荷計算・図面体系・規格

- :material-wrench: **[保全](05-hozen/index.md)**
  定期点検・校正・絶縁管理・停電作業

- :material-alert: **[トラブル](06-trouble/index.md)**
  症状から原因へ — 逆引き対応ガイド

</div>

## リファレンス

[用語集](reference/glossary.md) ・ [規格一覧](reference/standards-list.md) ・ [計算ツール](reference/calculators.md) ・ [読む順番ガイド](getting-started.md)

## 記事の見方

- :material-account-hard-hat: `対象: 電気担当` — 電気主任・電計エンジニア向け
- :material-account-wrench: `対象: 保全担当` — 保全作業者向け
- :material-account: `対象: 製造担当` — 運転オペレーター向け（専門用語を最小化）

---

!!! tip "使い始める前に"
    このWikiが初めての方は [読む順番ガイド](getting-started.md) から始めると全体像をつかめます。
    各記事のフロントマターに `last_verified` フィールドがあります。
    1年以上更新のない記事は内容を確認してから参照してください。
