---
title: "保護協調"
description: "協調曲線・時限設定・保護協調図の読み方"
tags:
  - 高圧
  - 保護協調
audience:
  - 電気担当
last_verified: 2026-04-04
status: published
---

# 保護協調

## 30秒まとめ

保護協調の目的は「事故点に最も近い遮断器だけが開放し、停電範囲を最小にすること」。TCC（時間-電流特性曲線）で上位と下位の特性が重ならないことを確認する。変圧器増設時に協調が崩れるケースに注意。

---

## 保護協調の目的

化学プラントでは停電範囲の最小化が連続生産維持の観点から非常に重要。

```
理想の動作：事故点→最近傍遮断器（最下位）のみトリップ
避けるべき動作：上位の遮断器がトリップして広範囲停電
```

### 保護協調が成立している状態

```
上位（母線側） [時限 0.8秒] ─┐
                              │
下位（フィーダー） [時限 0.4秒] ─┤ 差：0.4秒 → 協調成立
                              │
最下位（負荷直近） [時限 0.1秒] ─┘ 差：0.3秒 → 協調成立
```

---

## TCC（時間-電流特性曲線）の読み方

TCC は横軸に電流倍数（整定電流に対する比）、縦軸に動作時間をとったグラフ。

- **各保護継電器の特性曲線が縦方向に重ならないこと**が協調の条件
- 0.3秒以上の時限差が推奨（VCB の動作時間 + 余裕）

<svg viewBox="0 0 640 420" role="img" aria-label="TCC協調曲線。両対数グラフで上位（母線側）と下位（フィーダー）の反限時特性曲線を示し、同一電流で上位が下位より0.3〜0.4秒上にあり縦方向に重ならないこと、および大電流側の瞬時要素を図示する。" style="max-width:100%;height:auto;font-family:sans-serif;">
  <!-- 外枠（プロット領域） -->
  <rect x="70" y="30" width="500" height="320" fill="none" stroke="currentColor" stroke-width="1"/>
  <!-- 縦グリッド（対数目盛：倍数 1,2,5,10,20 を等間隔配置で近似） -->
  <line x1="70"  y1="30" x2="70"  y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="195" y1="30" x2="195" y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="320" y1="30" x2="320" y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="445" y1="30" x2="445" y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="570" y1="30" x2="570" y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <!-- 横グリッド（対数目盛：0.05,0.1,0.5,1,5,10秒） -->
  <line x1="70" y1="30"  x2="570" y2="30"  stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="70" y1="94"  x2="570" y2="94"  stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="70" y1="158" x2="570" y2="158" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="70" y1="222" x2="570" y2="222" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="70" y1="286" x2="570" y2="286" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <line x1="70" y1="350" x2="570" y2="350" stroke="currentColor" stroke-width="0.5" opacity="0.35"/>
  <!-- 軸ラベル：X -->
  <text x="70"  y="368" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <text x="195" y="368" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="320" y="368" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <text x="445" y="368" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <text x="570" y="368" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <text x="320" y="390" font-size="12" fill="currentColor" text-anchor="middle">電流倍数（整定電流に対する比）／対数目盛</text>
  <!-- 軸ラベル：Y -->
  <text x="62" y="34"  font-size="11" fill="currentColor" text-anchor="end">10</text>
  <text x="62" y="98"  font-size="11" fill="currentColor" text-anchor="end">5</text>
  <text x="62" y="162" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="62" y="226" font-size="11" fill="currentColor" text-anchor="end">0.5</text>
  <text x="62" y="290" font-size="11" fill="currentColor" text-anchor="end">0.1</text>
  <text x="62" y="354" font-size="11" fill="currentColor" text-anchor="end">0.05</text>
  <text x="20" y="190" font-size="12" fill="currentColor" text-anchor="middle" transform="rotate(-90 20 190)">動作時間［秒］／対数目盛</text>
  <!-- 上位（母線側）反限時曲線：常に下位より上（動作が遅い） -->
  <path d="M110,70 C200,110 300,150 400,175 S520,200 560,208" fill="none" stroke="currentColor" stroke-width="2.4"/>
  <text x="132" y="62" font-size="11" fill="currentColor">上位（母線側）</text>
  <!-- 下位（フィーダー）反限時曲線：破線で区別 -->
  <path d="M110,150 C200,190 300,228 400,250 S520,272 560,280" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="7 4"/>
  <text x="118" y="146" font-size="11" fill="currentColor">下位（フィーダー）</text>
  <!-- 時限差の縦連結（同一電流での縦方向間隔＝0.3〜0.4秒） -->
  <line x1="400" y1="175" x2="400" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
  <circle cx="400" cy="175" r="3" fill="currentColor"/>
  <circle cx="400" cy="250" r="3" fill="currentColor"/>
  <text x="410" y="216" font-size="11" fill="currentColor">時限差 0.3〜0.4秒</text>
  <!-- 瞬時要素（大電流側の縦の直線） -->
  <line x1="500" y1="30" x2="500" y2="350" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3" opacity="0.8"/>
  <text x="506" y="46" font-size="11" fill="currentColor">瞬時要素</text>
  <!-- 大電流側の向き注記（数値は特定せず定性的に） -->
  <text x="500" y="336" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.85">大電流（短絡）側→</text>
</svg>

*上位（母線側）の曲線が同一電流で常に下位（フィーダー）より上にあり、縦方向に 0.3〜0.4秒の間隔を保って重ならないのが協調成立の状態。右側の瞬時要素より大電流側では時限差を待たず遮断する。*

```
時限差 = 下位機器の動作時間 + VCB 動作時間（0.05秒）+ 協調余裕（0.1〜0.2秒）
       ≒ 0.3〜0.4秒
```

!!! tip "協調確認の実務"
    設備変更前に協調図（TCC）を更新し、変更後も協調が成立していることを確認する。
    TCC の作成はメーカー（三菱電機・富士電機等）の保護協調検討ソフトを活用するか、
    メーカー技術部門に依頼するのが現実的。

    メーカー技術部門へ依頼する際に用意する入力データ：

    - 単線結線図（対象系統の全体構成）
    - 各変圧器・系統の %Z と基準容量
    - CT の変流比（CT 比）
    - 既設 OCR の整定タップと時限
    - VCB の遮断時間

---

## %Z 法による短絡電流計算（概要）

系統のインピーダンスを基準容量（MVA ベース）に揃えた「%インピーダンス（%Z）」で短絡電流を求める方法。

### 計算ステップ

```
1. 基準容量（Sb）を決める（例：1000 kVA = 1 MVA）
2. 各機器の %Z を基準容量に換算
   %Z_new = %Z_rated × (Sb / S_rated)
3. 電源から事故点までの %Z を合計
4. 短絡電流を算出：
   Is = 100 / (%Z_total) × I_base
   I_base = Sb / (√3 × Vb)
```

### 計算例（6.6kV フィーダーの短絡電流）

```
系統：系統インピーダンス %Zs = 3%（1MVA ベース）
変圧器：%Z = 5%（1MVA ベース）
合計 %Z = 3 + 5 = 8%

基準電流 I_base[A] = Sb[VA] / (√3 × Vb[V])
       = 1,000,000 / (√3 × 6600) = 87.5 A   ← 基準容量 Sb=1MVA に対する 6.6kV 母線の基準電流
Is = (100 / 8) × 87.5 = 1094 A
```

---

## 上位-下位の時限協調

| 時限差の目安 | 条件 |
|-----------|------|
| 0.3秒 | VCB + OCR の最低限の時限差 |
| 0.4秒 | 余裕を持たせた標準的な時限差 |
| 0.5秒以上 | 大型系統・古い機器での推奨 |

---

## 変圧器増設時に協調が崩れやすいケース

!!! warning "変圧器増設時の協調再確認"
    変圧器を増設・並列運転すると以下の変化が生じる：

    | 変化 | 影響 |
    |------|------|
    | 短絡電流の増加 | 既設遮断器の遮断容量を超える可能性 |
    | 需要電流の増加 | OCR の整定電流との乖離（誤動作リスク） |
    | 複数変圧器の並列 | 変圧器間を流れる循環電流による誤動作 |

    変圧器増設前には必ず保護協調を再計算し、TCC で上位・下位の協調が崩れていないことを確認する。

---

## 保護協調図（TCC）の保管

保護協調図は以下の変更が発生したときに必ず更新する：

- [ ] 変圧器の増設・変更
- [ ] 高圧モーターの増設・変更
- [ ] 系統構成変更（母線分割等）
- [ ] 保護継電器の更新・整定変更
- [ ] 進相コンデンサの増設
