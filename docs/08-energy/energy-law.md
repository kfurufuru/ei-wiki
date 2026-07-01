---
title: 省エネ法対応
description: エネルギーの使用の合理化等に関する法律（省エネ法）の概要・特定事業者の義務・自工場での適用
tags: [省エネ法, 特定事業者, エネルギー管理士, 定期報告]
last_verified: 2026-04-04
---

# 省エネ法対応

## 法律の概要

**正式名称**: エネルギーの使用の合理化等に関する法律（通称：省エネ法）

エネルギー資源の有効利用と温暖化対策を目的とし、工場・事業場でのエネルギー使用の合理化を義務付ける。
主管は**経済産業省**（資源エネルギー庁）。

> **当工場への適用**: 当工場は化学プラントであり、電気・蒸気・燃料の消費量が基準を超えるため**特定事業者**に該当する。

---

## 特定事業者・特定連鎖化事業者の定義

| 区分 | 基準 | 義務 |
|------|------|------|
| **特定事業者** | 工場等のエネルギー使用量が年間**原油換算1,500kL以上** | エネルギー管理統括者・管理企画推進者の選任、定期報告・中長期計画の提出 |
| **第一種エネルギー管理指定工場** | 工場単体で**原油換算3,000kL以上** | エネルギー管理士の選任（電気・熱それぞれ） |
| **第二種エネルギー管理指定工場** | 工場単体で**原油換算1,500kL以上3,000kL未満** | エネルギー管理員の選任 |

> **原油換算の計算**: 電力1kWh = 0.0258L（原油換算係数）。年間電力使用量から換算すると、約58GWhで1,500kL相当。

<svg viewBox="0 0 720 300" role="img" aria-label="原油換算量による事業者区分と指定工場区分の閾値。1,500kLと3,000kLが境界。" style="max-width:100%;height:auto;font-family:sans-serif">
  <!-- 縦の境界ガイド -->
  <line x1="240" y1="40" x2="240" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
  <line x1="480" y1="40" x2="480" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
  <text x="240" y="30" text-anchor="middle" fill="currentColor" font-size="14" font-weight="bold">1,500kL</text>
  <text x="480" y="30" text-anchor="middle" fill="currentColor" font-size="14" font-weight="bold">3,000kL</text>

  <!-- 事業者全体で判定する軸 -->
  <text x="20" y="70" fill="currentColor" font-size="13" font-weight="bold">事業者全体</text>
  <line x1="40" y1="95" x2="700" y2="95" stroke="currentColor" stroke-width="2"/>
  <text x="140" y="88" text-anchor="middle" fill="currentColor" font-size="12">非該当</text>
  <text x="140" y="115" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">1,500kL未満</text>
  <text x="470" y="88" text-anchor="middle" fill="currentColor" font-size="12" font-weight="bold">特定事業者</text>
  <text x="470" y="115" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">1,500kL以上</text>
  <text x="470" y="132" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">統括者・管理企画推進者を選任</text>

  <!-- 工場単体で判定する軸 -->
  <text x="20" y="185" fill="currentColor" font-size="13" font-weight="bold">工場単体</text>
  <line x1="40" y1="210" x2="700" y2="210" stroke="currentColor" stroke-width="2"/>
  <text x="140" y="203" text-anchor="middle" fill="currentColor" font-size="12">指定なし</text>
  <text x="360" y="203" text-anchor="middle" fill="currentColor" font-size="12" font-weight="bold">第二種指定工場</text>
  <text x="360" y="230" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">1,500kL以上3,000kL未満</text>
  <text x="360" y="247" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">エネルギー管理員を選任</text>
  <text x="590" y="203" text-anchor="middle" fill="currentColor" font-size="12" font-weight="bold">第一種指定工場</text>
  <text x="590" y="230" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">3,000kL以上</text>
  <text x="590" y="247" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.8">エネルギー管理士を選任</text>

  <!-- 境界注記 -->
  <text x="360" y="278" text-anchor="middle" fill="currentColor" font-size="11" opacity="0.7">事業者区分は事業者全体、指定工場区分は工場単体で判定（判定基準が異なる）</text>
</svg>

*図: 原油換算量の閾値と区分。事業者全体で「特定事業者」を、工場単体で「第一種／第二種指定工場」を判定する（表と同じ数値・義務）。*

---

## エネルギー管理士の選任義務と職務

### 選任要件

- **第一種指定工場**は電気担当・熱担当それぞれ1名以上のエネルギー管理士を選任
- 選任後は経済産業大臣（地方産業保安監督部）への**届出が必要**
- 兼任は工場内に限り認められる

### 主な職務

1. エネルギーの使用方法の改善・監視
2. 設備・装置の維持・管理
3. エネルギー管理に関する記録の作成・保管
4. 省エネに関する計画・目標の策定への参画
5. 定期報告書への署名（工場長との連名）

> **注意**: エネルギー管理士は「エネルギーの合理化」の監督者であり、電気主任技術者（保安監督）とは役割が異なる。兼任は資格さえあれば可能。

---

## 定期報告書と中長期計画書の提出

### 定期報告書

| 項目 | 内容 |
|------|------|
| 提出期限 | 毎年**7月末日** |
| 提出先 | 経済産業局（中部・近畿・関東等、所轄地域による） |
| 内容 | 前年度のエネルギー使用量・原単位・設備情報・省エネ実施状況 |
| 提出方法 | 省エネ法電子報告システム（ESIMS）経由 |

!!! warning "提出遅延・虚偽報告のペナルティ"
    定期報告の不提出・虚偽報告は**100万円以下の罰金**（法人）。報告内容の精度管理が重要。

### 中長期計画書

| 項目 | 内容 |
|------|------|
| 提出周期 | 定期報告と同じく毎年7月末（内容は5年先の計画） |
| 内容 | 省エネ投資計画・目標原単位・主要設備の更新計画 |
| 求められる目標 | 年平均**1%以上**のエネルギー原単位改善 |

---

## 電気・熱のエネルギー計量義務

省エネ法第9条に基づき、指定工場はエネルギーの使用量を**計量・記録**しなければならない。

### 計量対象

- **電気**: 受電点の電力量（kWh）、主要設備の分岐電力量
- **燃料（重油・ガス等）**: 積算流量計または仕入れ伝票
- **蒸気**: 積算流量計（kg/h → GJ換算）

### 実務上のポイント

- 計量器は**検定済み**のものを使用（電力量計は電気計量法対象）
- データはPIヒストリアン等に自動収集→月次集計→定期報告書に転記
- 計量器の故障・異常時は代替計量の記録を残す

---

## ベンチマーク制度の概要

業種別に設定された**省エネ基準（ベンチマーク）**を達成することが求められる制度。

| 項目 | 内容 |
|------|------|
| 対象業種 | 化学工業（エチレン・アンモニア等の主要製品別） |
| 指標 | 製品1tあたりのエネルギー消費量（原油換算） |
| 目標水準 | 業界上位10%相当のエネルギー効率 |
| 未達時 | 勧告・命令・公表（罰則あり） |

> **化学工場の特徴**: 製品が多品種にわたるため、ベンチマーク対象製品を特定し、その生産に紐づくエネルギーを分離計量することが重要。

---

## 関連リンク・参考

- 省エネ法（e-Gov法令検索）
- 資源エネルギー庁「省エネ法に基づく定期報告書等の手引き」（毎年改訂）
- ESIMS（省エネ法電子報告システム）: https://esims.eccj.or.jp/

## 関連記事

- [demand-management.md](demand-management.md) — デマンド管理
- [energy-monitoring.md](energy-monitoring.md) — エネルギー計量・監視の実務
- [../09-hoantokei/legal-duties.md](../09-hoantokei/legal-duties.md) — 電気主任技術者の法定業務との整理
