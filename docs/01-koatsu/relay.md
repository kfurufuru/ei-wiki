---
title: "保護継電器"
description: "OCR/GR/DGR/UVR・整定計算・試験"
tags:
  - 高圧
  - 保護継電器
audience:
  - 電気担当
last_verified: 2026-04-16
status: published
---

# 保護継電器

## 30秒まとめ

OCR（過電流）・GR/DGR（地絡）が高圧回路保護の基本2本柱。整定は「保護したい設備の定格電流」と「上位との時限協調」で決まる。CT 二次回路を開路すると高電圧が発生する危険があるので絶対に開放しない。

---

## OCR（過電流継電器）整定計算

### 電流整定

変圧器一次側 OCR の整定電流は変圧器定格電流を基に設定する。

```
CT 二次換算電流 = 変圧器定格電流（A） / CT 変流比

例：1000 kVA、6.6kV 変圧器の場合
   定格電流 = 1000kVA / (√3 × 6.6kV) = 87.5 A
   CT 変流比：100/5A の場合
   CT 二次換算電流 = 87.5 / 20 = 4.375 A

限時電流整定値 = 4.375 × 1.2 = 5.25 A → 5.5 A タップに設定
瞬時電流整定値 = 4.375 × (6〜10) = 26〜44 A → 最大短絡電流を超えないよう設定
```

### 時限整定

上位変電所との**協調**を確保するため、下位の時限 < 上位の時限（最低 0.3 秒以上の差）。

| 階層 | 時限設定の目安 |
|------|------------|
| 最下位（モーター/変圧器直近） | 0.1〜0.3 秒 |
| 中間（フィーダー） | 0.4〜0.7 秒 |
| 上位（母線側） | 0.8〜1.2 秒 |

---

## GR と DGR の違い

| 項目 | GR（地絡継電器） | DGR（地絡方向継電器） |
|------|------------|-----------------|
| 検出方式 | 零相電流（I₀）の大きさのみ | 零相電流（I₀）＋零相電圧（V₀）の方向 |
| 判定 | 地絡の有無のみ | 地絡の発生方向（自回線 or 他回線） |
| 誤動作 | 他回線地絡で誤動作の可能性あり | 他回線地絡での誤動作を防げる |
| 使用箇所 | 単一フィーダー | 複数フィーダーが並列の系統 |

<svg viewBox="0 0 560 320" role="img" aria-label="零相電圧V0を基準軸とし、自回線地絡時と他回線地絡時の零相電流I0ベクトルを位相で描き分けた図。DGRの動作領域を扇形で示す。" style="max-width:100%;height:auto;font-family:sans-serif">
  <!-- reference axis V0 (horizontal) -->
  <line x1="280" y1="160" x2="530" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="530,160 520,155 520,165" fill="currentColor"/>
  <text x="534" y="164" fill="currentColor" font-size="15" font-weight="bold">V₀</text>
  <text x="332" y="152" fill="currentColor" font-size="11" opacity="0.75">基準軸（零相電圧）</text>
  <!-- vertical guide -->
  <line x1="280" y1="30" x2="280" y2="300" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3 4" opacity="0.4"/>
  <text x="280" y="24" fill="currentColor" font-size="11" text-anchor="middle" opacity="0.6">同一母線・共通基準</text>

  <!-- DGR operating region: fan sector around V0 axis (self-line side) -->
  <path d="M280,160 L500,90 A233,233 0 0,1 500,230 Z" fill="currentColor" opacity="0.12"/>
  <text x="470" y="200" fill="currentColor" font-size="12" text-anchor="middle" opacity="0.8">DGR 動作領域</text>
  <text x="470" y="216" fill="currentColor" font-size="10" text-anchor="middle" opacity="0.6">（位相角 θ の範囲）</text>

  <!-- I0 self-line fault: within operating region -->
  <line x1="280" y1="160" x2="465" y2="118" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="465,118 453,117 458,128" fill="currentColor"/>
  <text x="352" y="100" fill="currentColor" font-size="13" font-weight="bold">I₀（自回線地絡）</text>
  <text x="352" y="116" fill="currentColor" font-size="10" opacity="0.7">V₀ と特定の位相関係 → 動作</text>

  <!-- I0 other-line fault: opposite direction, outside operating region -->
  <line x1="280" y1="160" x2="90" y2="220" stroke="currentColor" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="90,220 102,219 95,209" fill="currentColor"/>
  <text x="20" y="248" fill="currentColor" font-size="13" font-weight="bold">I₀（他回線地絡）</text>
  <text x="20" y="264" fill="currentColor" font-size="10" opacity="0.7">位相が逆側 → 不動作</text>

  <!-- angle arc marker at origin -->
  <path d="M320,160 A40,40 0 0,0 306,132" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="322" y="138" fill="currentColor" font-size="12" opacity="0.8">θ</text>

  <!-- origin dot -->
  <circle cx="280" cy="160" r="3" fill="currentColor"/>

  <!-- GR note: magnitude only -->
  <text x="20" y="300" fill="currentColor" font-size="11" opacity="0.85">GR：I₀ の大きさのみ判定 → 自回線・他回線を区別できず、他回線地絡でも誤動作しうる</text>
</svg>

*V₀ を基準軸に I₀ の位相を見るのが DGR。自回線地絡と他回線地絡で I₀ の向きが逆側になり、動作領域（位相角 θ の範囲）の内か外かで判別する。GR は I₀ の大きさしか見ないため両者を区別できない。*

!!! tip "化学プラントでの選定"
    複数の 6.6kV フィーダーが同一母線から出ている場合は DGR を採用し、
    他回線地絡による不必要停電を防止する。

---

## デジタル継電器の設定画面の見方

主要メーカーのデジタル継電器で確認する主要パラメータ。

| パラメータ | 三菱（MELPRO-D） | 東芝（GRL） | オムロン |
|----------|--------------|---------|--------|
| 限時電流整定 | PICKUP | I₁ | IS |
| 瞬時電流整定 | INST | I₂ | Ih |
| 時限 | TIME | TL | T |
| 位相角（DGR） | θ | θ | θ |

設定変更後は必ず**設定値の記録**と**試験（注入試験）による動作確認**を実施する。

---

## CT 二次回路の開路禁止

!!! danger "CT 二次回路を開路すると危険"
    CT（変流器）は一次電流を強制的に二次側に流そうとする。
    二次回路を開路すると、一次電流がすべて二次コイルの磁化に使われ、
    **数 kV の高電圧が二次端子に発生する**。感電・機器破損の危険がある。

    CT の二次回路で作業する際のルール：
    1. CT 短絡（shorting）端子で二次回路を短絡してから作業する
    2. 作業完了後に短絡を外す
    3. 停電状態での作業が最も安全

---

## トリップ確認試験の実施手順

定期点検時に継電器の動作を確認する試験。

```
【注入試験手順】
1. 対象フィーダーの VCB を開路し、停電状態にする
2. CT 二次側に試験電流注入装置を接続
3. 整定値の 1.1 倍の電流を注入し、規定時限内でトリップ出力が出ることを確認
4. 瞬時要素については整定値以上の電流を注入してトリップ確認
5. トリップ確認後、VCB の解放動作を確認
6. 試験記録（電流値・時限・担当者・日時）を作成
```

!!! note "無電圧試験（継電器単体試験）"
    VCB のトリップ回路を含めた一連の動作確認を「トリップ試験」と呼ぶ。
    継電器単体の特性確認だけでなく、トリップコイル・VCB 機構部も含めた総合確認が重要。

!!! warning "試験前の連絡と異常時の報告フロー"
    注入試験は誤トリップ・波及停電・感電のリスクを伴うため、実施前後の連絡と異常時の報告経路を定めておく。

    **試験前（事前連絡・承認）**

    - 停電範囲・時間帯・対象フィーダーを運転部門へ通知する
    - 電気主任技術者（試験責任者）の立会または承認を得る

    **異常発生時（誤操作・感電・意図せぬ波及停電）**

    1. 直ちに電流注入を停止する
    2. CT 二次側は短絡端子で短絡し、開路状態を残さない
    3. 試験責任者（電気主任技術者）へ即報し、作業を中断する
    4. 波及停電が生じた場合は、社内規定に従い運転部門・電力会社・保安監督部門へ速やかに連絡する

    連絡先・順序・時限は社内規定および各事業場の保安規程に従う。

---

## 関連ページ

- [遮断器・断路器](breaker.md) — VCB 動作・トリップ信号・インターロック
- [変圧器](transformer.md) — OCR・ブッフホルツ継電器の配置
- [保護協調](coordination.md) — 多段階保護・時限協調設定
- [保護リレー試験手順](../guidelines/protective-relay-test.md) — OCR/GR/DGR の動作試験・整定値確認を現場で行う実務手順
- [高圧カテゴリ](index.md) — より広い高圧知識へ
