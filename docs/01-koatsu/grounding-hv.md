---
title: "接地（高圧）"
description: "A/B/C/D種・接地抵抗測定"
tags:
  - 高圧
  - 接地
audience:
  - 電気担当
last_verified: 2026-04-04
status: published
---

# 接地（高圧）

## 30秒まとめ

A〜D種接地の目的と抵抗基準値を正確に覚えることが基本。接地抵抗測定は3電極法が標準。複数の接地極を「共用接地」とする場合は高電位上昇の影響が伝播しないか確認が必要。

---

## A/B/C/D 種接地の定義・基準値

| 種別 | 接地抵抗 | 主な対象 | 目的 |
|------|---------|---------|------|
| A 種 | **10 Ω 以下** | 高圧・特高機器の鉄台・外箱 | 地絡時の感電保護、アーク放電防止 |
| B 種 | **150/Ig Ω 以下**（最大 600 Ω） | 変圧器低圧側中性点 | 高低圧混触時の低圧側電位上昇抑制 |
| C 種 | **10 Ω 以下**（または 0.5秒で自動遮断なら 500 Ω） | 300V 超低圧機器の外箱 | 感電保護 |
| D 種 | **100 Ω 以下**（または 0.5秒で自動遮断なら 500 Ω） | 300V 以下低圧機器の外箱 | 感電保護 |

Ig = 1線地絡電流（A）。B種は系統の1線地絡電流から算出する。

!!! note "C 種・D 種の特例（漏電遮断器付き）"
    漏電遮断器（感度電流 30mA 以下、動作時間 0.1秒以内）が設置されている場合、
    C 種・D 種の抵抗値は 500 Ω 以下に緩和される（電技解釈 第17条）。

---

## 接地線サイズ（電気設備技術基準による）

| 接地種別 | 最小線径（銅線） |
|---------|--------------|
| A 種 | 2.6 mm（≒ 5.5 mm²） |
| B 種 | 4 mm²（計算値による）※ |
| C 種 | 1.6 mm（≒ 2 mm²） |
| D 種 | 1.6 mm（≒ 2 mm²） |

※ B種接地線は「高圧側電路の1線地絡電流の最大値」から算出する。詳細は電技解釈 第24条。

---

## 接地抵抗測定（3電極法）

### 機器と接続方法

```
被測定極（E）── 測定器 ── 補助電流極（C）
                    |
                補助電圧極（P）

E: 被測定接地極
P: E から 10m 程度離した補助電圧極
C: P からさらに 10m 程度離した補助電流極（E から 20〜30m）
```

### 測定手順

```
1. 測定器（接地抵抗計）の電池容量を確認
2. E・P・C 端子を上図の通り接続
3. 測定器の操作スイッチを押して測定
4. 表示値を読み取り記録（温度・天候も記録）
5. P 極の位置を変えて（±10%）再測定し、安定した値を採用
```

!!! warning "近傍の地中金属による誤差"
    近くに埋設配管・アース板が多い場合、補助極との間に影響が出て誤差が大きくなる。
    複数方向に補助極を設置して測定し、ばらつきの少ない値を採用する。

---

## 共用接地 vs 独立接地

| 項目 | 共用接地 | 独立接地 |
|------|---------|---------|
| コスト | 低い | 高い |
| 電位上昇の影響 | 他の機器に伝播する | 伝播しない |
| 本安バリアの IS アース | 共用不可（独立が必要） | 必要 |
| 計測器アース | 信号系は独立が望ましい | 推奨 |
| 一般接地 | 共用可 | — |

!!! danger "本安バリアの IS アースは独立させる"
    本質安全防爆回路の IS アース（IS グラウンド）は、通常のアースや建屋接地と**共用してはいけない**。
    IS アースの抵抗値（40 Ω 以下）と独立性を年1回確認する。

---

## 接地電位上昇と感電保護

地絡事故発生時、接地極周辺に電位勾配が生じる（ステップ電圧）。足の位置によって電位差が生じ感電する危険がある。

<svg viewBox="0 0 640 320" role="img" aria-label="接地極からの距離に対する地表電位分布曲線。接地極付近ほど勾配が急でステップ電圧が大きく、等電位メッシュ施工時は勾配が平坦化する。" style="max-width:100%;height:auto;" xmlns="http://www.w3.org/2000/svg">
  <!-- 軸 -->
  <line x1="70" y1="40" x2="70" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <line x1="70" y1="250" x2="600" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="30" fill="currentColor" font-size="13" text-anchor="middle">対地電位</text>
  <text x="600" y="275" fill="currentColor" font-size="13" text-anchor="end">接地極からの距離</text>
  <!-- 接地極 -->
  <line x1="70" y1="250" x2="70" y2="270" stroke="currentColor" stroke-width="3"/>
  <text x="70" y="288" fill="currentColor" font-size="12" text-anchor="middle">接地極</text>
  <!-- 急峻な電位分布曲線（未施工） -->
  <path d="M70 55 C 110 90, 150 175, 230 210 S 400 245, 600 249" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="250" y="150" fill="currentColor" font-size="12">地表電位分布（未施工）</text>
  <!-- 等電位メッシュ施工時：勾配が平坦化 -->
  <path d="M70 200 C 200 215, 400 235, 600 249" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="360" y="205" fill="currentColor" font-size="12">等電位メッシュ施工時（勾配が平坦化）</text>
  <!-- 両足位置とステップ電圧 -->
  <line x1="120" y1="250" x2="120" y2="82" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="165" y1="250" x2="165" y2="150" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>
  <circle cx="120" cy="250" r="4" fill="currentColor"/>
  <circle cx="165" cy="250" r="4" fill="currentColor"/>
  <text x="143" y="266" fill="currentColor" font-size="11" text-anchor="middle">両足間隔</text>
  <line x1="185" y1="82" x2="185" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <line x1="181" y1="82" x2="189" y2="82" stroke="currentColor" stroke-width="1.5"/>
  <line x1="181" y1="150" x2="189" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <text x="196" y="120" fill="currentColor" font-size="12">ステップ電圧</text>
  <!-- 2m 以内 立入禁止マーカー -->
  <line x1="215" y1="45" x2="215" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="2 4"/>
  <text x="219" y="60" fill="currentColor" font-size="11">2m 以内に近づかない</text>
</svg>

*接地極に近いほど勾配が急でステップ電圧が大きい。接地極から 2m 以内に近づかず、等電位メッシュ施工で勾配を平坦化する。*

### 対策

- 接地極の周囲に等電位メッシュを施工する（大型変電所）
- 接地極周囲の地表面に絶縁性材料（砂利・アスファルト）を敷設する
- 事故発生時は接地極から 2m 以内に近づかない（手順書への明記）
