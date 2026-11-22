---
title: 電気の規模感（桁のはしご）
description: 容量・電圧・電流・抵抗・インピーダンス・力率の大きさを、身近な実物と現場の機器で並べた速引き表
tags:
  - 設計
  - 計算
  - 逆引き
audience:
  - 電気担当
  - 保全担当
  - 計装担当
last_verified: 2026-11-22
---

# 電気の規模感（桁のはしご）

図面や計算結果の数値を見て「大きいのか小さいのか」を一瞬で判断するための速引き表です。6つの量を、身近な実物と現場の機器で桁ごとに並べています。

## 概要（30秒まとめ）

- **1000倍ごとの目盛りに実物を当てて覚えます。** 容量なら 1 kW（ドライヤー）→ 1 MW（高圧受電の工場）→ 1 GW（原子力1基）です。LED電球（10 W）はその手前です。
- **計算結果の桁チェックに使います。** 家庭の負荷が数 MW、発電所の出力が数 kW になったら、単位か桁の誤りです。
- **量どうしはつながっています。** 同じ電力・同じ力率・同じ線路なら、電圧が10倍で電流は1/10、損失（I²R）は1/100です。容量が大きい需要家ほど高い電圧で受電するのはこのためです。

!!! warning "数値の性格"
    図と表の数値は、桁をつかむための**代表値・目安**です。設計や判定の基準値として使わないでください。法令で決まっている値は「法定」と書き、根拠の正典ページへリンクしています。接地抵抗・絶縁抵抗の判定値は、このページには書かず正典ページを参照します。図の色付きの棒は、法令や契約の境目、または判定値が別に決まっている行です。

## 容量（W・kVA）

<figure id="fig-scale-power" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 346" width="640" height="346" role="img" aria-labelledby="fig-scale-power-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-power-title">容量のはしご図。横軸は対数目盛りで、1 W から 100 GW まで1000倍ごとに太線を引いている。LED電球 10 W、ドライヤー 1 kW、小型電動機 3.7 kW、低圧と高圧の契約の境目の目安 50 kW、高圧受電の工場 1 MW、特高受電の目安 2 MW、風車1基 2〜4 MW、新幹線1編成 17 MW、大工場 40 MW、原子力1基 1 GW、東京エリアの最大需要 約55 GW を棒の長さで並べている。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="330"/>
    <line x1="155.5" y1="38" x2="155.5" y2="330" stroke-dasharray="2 3"/>
    <line x1="182.9" y1="38" x2="182.9" y2="330" stroke-dasharray="2 3"/>
    <line x1="210.4" y1="38" x2="210.4" y2="330"/>
    <line x1="237.8" y1="38" x2="237.8" y2="330" stroke-dasharray="2 3"/>
    <line x1="265.3" y1="38" x2="265.3" y2="330" stroke-dasharray="2 3"/>
    <line x1="292.7" y1="38" x2="292.7" y2="330"/>
    <line x1="320.2" y1="38" x2="320.2" y2="330" stroke-dasharray="2 3"/>
    <line x1="347.6" y1="38" x2="347.6" y2="330" stroke-dasharray="2 3"/>
    <line x1="375.1" y1="38" x2="375.1" y2="330"/>
    <line x1="402.5" y1="38" x2="402.5" y2="330" stroke-dasharray="2 3"/>
    <line x1="430.0" y1="38" x2="430.0" y2="330" stroke-dasharray="2 3"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="128.0" y="32">1 W</text>
    <text x="210.4" y="32">1 kW</text>
    <text x="292.7" y="32">1 MW</text>
    <text x="375.1" y="32">1 GW</text>
  </g>
  <rect x="128" y="49.0" width="27.5" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">10 W</text>
  <text x="161.5" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">LED電球</text>
  <rect x="128" y="75.0" width="82.4" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1 kW</text>
  <text x="216.4" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">ドライヤー</text>
  <rect x="128" y="101.0" width="98.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">3.7 kW</text>
  <text x="232.0" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">小型の電動機</text>
  <rect x="128" y="127.0" width="129.0" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">50 kW</text>
  <text x="263.0" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">低圧と高圧の境目の目安</text>
  <rect x="128" y="153.0" width="164.7" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1 MW</text>
  <text x="298.7" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">高圧受電の工場・ビル</text>
  <rect x="128" y="179.0" width="173.0" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="191.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">2 MW</text>
  <text x="307.0" y="191.0" font-size="12" style="fill: var(--md-default-fg-color)">特高受電の目安</text>
  <rect x="128" y="205.0" width="177.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="217.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">2〜4 MW</text>
  <text x="311.8" y="217.0" font-size="12" style="fill: var(--md-default-fg-color)">風車1基</text>
  <rect x="128" y="231.0" width="198.5" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="243.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">17 MW</text>
  <text x="332.5" y="243.0" font-size="12" style="fill: var(--md-default-fg-color)">新幹線1編成</text>
  <rect x="128" y="257.0" width="208.7" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="269.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">40 MW</text>
  <text x="342.7" y="269.0" font-size="12" style="fill: var(--md-default-fg-color)">大工場</text>
  <rect x="128" y="283.0" width="247.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="295.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1 GW</text>
  <text x="381.1" y="295.0" font-size="12" style="fill: var(--md-default-fg-color)">原子力1基</text>
  <rect x="128" y="309.0" width="294.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="321.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約55 GW</text>
  <text x="428.9" y="321.0" font-size="12" style="fill: var(--md-default-fg-color)">東京エリアの最大需要</text>
</svg>
</figure>

| 規模 | 実物・機器の例 | 現場での使いどころ |
|---|---|---|
| 10 W 級 | LED電球 | 照明回路の負荷 |
| 1 kW 級 | ドライヤー・電子レンジ（100 V で約 10 A） | 家庭の 30 A 契約は 3 kVA |
| 数 kW〜数十 kW | 小型電動機（3.7 kW・11 kW・22 kW）、EV急速充電（約 50 kW） | 低圧の動力負荷 |
| 50 kW | 低圧契約と高圧契約の境目の目安（電力会社の契約区分） | 法令の値ではありません |
| 数百 kW〜2,000 kW | 高圧受電のビル・工場、変圧器 300〜1,000 kVA | 6.6 kV 受電の範囲 |
| 2,000 kW | 特高受電の目安（電力会社の契約区分） | 法令の値ではありません |
| 数 MW | 風車1基（2〜4 MW） | 出力 5,000 kW 以上の発電所・蓄電所は第三種電気主任技術者の範囲外（[資格一覧](../10-safety/special-education.md)） |
| 数十 MW | 新幹線1編成（約 17 MW）、大工場（40 MW は新幹線2〜3編成の全力加速・約10万世帯の平均消費） | 66 kV〜154 kV の特高受電 |
| 1 GW 級 | 火力1ユニット（数百 MW〜1,000 MW）、原子力1基（約 100 万 kW） | 電力系統の電源 |
| 数十 GW | 東京エリアの夏の最大需要（約 5,000 万〜6,000 万 kW） | 系統全体 |

- 換算: 1 万 kW ＝ 10 MW、100 万 kW ＝ 1 GW。電力系統の資料は「万 kW」で書かれることが多いです。
- 変圧器・発電機は kVA（皮相電力）、負荷は kW（有効電力）で書かれることが多いです。力率を掛けると kVA から kW になります。

## 電圧（V）

<figure id="fig-scale-voltage" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 398" width="640" height="398" role="img" aria-labelledby="fig-scale-voltage-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-voltage-title">電圧のはしご図。横軸は対数目盛りで、1 V から 1 MV まで。乾電池 1.5 V、自動車 12 V、家庭 100 V、工場の動力 400 V、低圧の上限 交流 600 V、直流電化 1,500 V、高圧配電 6.6 kV、高圧の上限 7,000 V、特高受電 22 kV、第三種の範囲（50 kV 未満）、大工場の受電 66 kV、154 kV、基幹送電 500 kV を並べ、法令の境目3本を色付きで示している。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="382"/>
    <line x1="178.3" y1="38" x2="178.3" y2="382" stroke-dasharray="2 3"/>
    <line x1="228.7" y1="38" x2="228.7" y2="382" stroke-dasharray="2 3"/>
    <line x1="279.0" y1="38" x2="279.0" y2="382"/>
    <line x1="329.3" y1="38" x2="329.3" y2="382" stroke-dasharray="2 3"/>
    <line x1="379.7" y1="38" x2="379.7" y2="382" stroke-dasharray="2 3"/>
    <line x1="430.0" y1="38" x2="430.0" y2="382"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="128.0" y="32">1 V</text>
    <text x="279.0" y="32">1 kV</text>
    <text x="430.0" y="32">1 MV</text>
  </g>
  <rect x="128" y="49.0" width="8.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1.5 V</text>
  <text x="142.9" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">乾電池</text>
  <rect x="128" y="75.0" width="54.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">12 V</text>
  <text x="188.3" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">自動車のバッテリー</text>
  <rect x="128" y="101.0" width="100.7" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">100 V</text>
  <text x="234.7" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">家庭のコンセント</text>
  <rect x="128" y="127.0" width="131.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">400 V級</text>
  <text x="265.0" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">工場の動力</text>
  <rect x="128" y="153.0" width="139.8" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">600 V</text>
  <text x="273.8" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">低圧の上限（交流）</text>
  <rect x="128" y="179.0" width="159.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="191.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1,500 V</text>
  <text x="293.9" y="191.0" font-size="12" style="fill: var(--md-default-fg-color)">直流電化（750 V 超で高圧）</text>
  <rect x="128" y="205.0" width="192.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="217.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">6.6 kV</text>
  <text x="326.3" y="217.0" font-size="12" style="fill: var(--md-default-fg-color)">高圧配電線</text>
  <rect x="128" y="231.0" width="193.5" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="243.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">7,000 V</text>
  <text x="327.5" y="243.0" font-size="12" style="fill: var(--md-default-fg-color)">高圧の上限</text>
  <rect x="128" y="257.0" width="218.6" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="269.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">22 kV</text>
  <text x="352.6" y="269.0" font-size="12" style="fill: var(--md-default-fg-color)">特高受電の工場</text>
  <rect x="128" y="283.0" width="236.5" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="295.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">50 kV</text>
  <text x="370.5" y="295.0" font-size="12" style="fill: var(--md-default-fg-color)">第三種の監督範囲（未満）</text>
  <rect x="128" y="309.0" width="242.6" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="321.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">66 kV</text>
  <text x="376.6" y="321.0" font-size="12" style="fill: var(--md-default-fg-color)">大工場の受電</text>
  <rect x="128" y="335.0" width="261.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="347.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">154 kV</text>
  <text x="395.1" y="347.0" font-size="12" style="fill: var(--md-default-fg-color)">一次変電所への送電</text>
  <rect x="128" y="361.0" width="286.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="373.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">500 kV</text>
  <text x="420.8" y="373.0" font-size="12" style="fill: var(--md-default-fg-color)">基幹送電線</text>
</svg>
</figure>

| 電圧 | 区分 | 実物・機器の例 |
|---|---|---|
| 1.5 V〜12 V | — | 乾電池、自動車のバッテリー |
| 100 V／200 V | 低圧 | 家庭のコンセント（単相3線式 100/200 V） |
| 200 V〜400 V 級 | 低圧 | 工場の動力・三相電動機 |
| 交流 600 V 以下／直流 750 V 以下 | 低圧の上限（法定） | — |
| 直流 1,000 V〜1,500 V | **高圧** | 大型太陽光の直流側、在来線の直流電化 |
| 3.3 kV／6.6 kV | 高圧 | 電柱の一番上の配電線、高圧受電の工場、大型電動機 |
| 7,000 V | 高圧の上限（法定・交流直流共通） | 7,000 V ちょうどは高圧 |
| 22 kV／33 kV | 特高 | 特高受電の中規模工場、都市部の配電 |
| 50,000 V 未満 | 第三種電気主任技術者の監督範囲（法定） | — |
| 66 kV／77 kV | 特高 | 数十 MW 級の大工場の受電（第三種の範囲外） |
| 154 kV | 特高 | 一次変電所への送電、大工場の受電 |
| 275 kV／500 kV | 特高 | 基幹送電線 |

電力の流れは、発電機（十数 kV〜20 kV 台）→ 昇圧して基幹送電（500 kV・275 kV）→ 超高圧変電所（154 kV）→ 一次変電所（66 kV）→ 配電用変電所（6.6 kV）→ 柱上変圧器（100/200 V）です。

!!! tip "つまずきやすい点"
    - 直流は 750 V を超えると高圧です。在来線の直流 1,500 V や大型太陽光の直流側は高圧に入ります。
    - 特高でも第三種の範囲とは限りません。66 kV 受電の工場は第二種以上の電気主任技術者が要ります。

## 電流（A）

<figure id="fig-scale-current" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 398" width="640" height="398" role="img" aria-labelledby="fig-scale-current-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-current-title">電流のはしご図。横軸は対数目盛りで、1 mA から 100 kA まで。感じ始める 1 mA、計装信号 20 mA、漏電遮断器の高感度 30 mA、地絡継電器の整定 0.2 A、100 W電球 1 A、ドライヤー 10 A、22 kW電動機 80 A、1,000 kVA変圧器の一次 87 A、40 MW を 66 kV で受けた 350 A、同じ変圧器の二次 2,750 A、40 MW を 6.6 kV で受けた 3,500 A、遮断器の遮断電流 12.5 kA、雷 数十 kA を並べている。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="382"/>
    <line x1="165.8" y1="38" x2="165.8" y2="382" stroke-dasharray="2 3"/>
    <line x1="203.5" y1="38" x2="203.5" y2="382" stroke-dasharray="2 3"/>
    <line x1="241.2" y1="38" x2="241.2" y2="382"/>
    <line x1="279.0" y1="38" x2="279.0" y2="382" stroke-dasharray="2 3"/>
    <line x1="316.8" y1="38" x2="316.8" y2="382" stroke-dasharray="2 3"/>
    <line x1="354.5" y1="38" x2="354.5" y2="382"/>
    <line x1="392.2" y1="38" x2="392.2" y2="382" stroke-dasharray="2 3"/>
    <line x1="430.0" y1="38" x2="430.0" y2="382" stroke-dasharray="2 3"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="128.0" y="32">1 mA</text>
    <text x="241.2" y="32">1 A</text>
    <text x="354.5" y="32">1 kA</text>
  </g>
  <rect x="128" y="49.0" width="2.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1 mA</text>
  <text x="134.0" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">感じ始める（目安）</text>
  <rect x="128" y="75.0" width="49.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">4〜20 mA</text>
  <text x="183.1" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">計装信号</text>
  <rect x="128" y="101.0" width="55.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">30 mA</text>
  <text x="189.8" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">漏電遮断器（高感度）</text>
  <rect x="128" y="127.0" width="86.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.2 A</text>
  <text x="220.9" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">地絡継電器の整定（目安）</text>
  <rect x="128" y="153.0" width="113.2" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1 A</text>
  <text x="247.2" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">100 W電球</text>
  <rect x="128" y="179.0" width="151.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="191.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">10 A</text>
  <text x="285.0" y="191.0" font-size="12" style="fill: var(--md-default-fg-color)">ドライヤー 1 kW</text>
  <rect x="128" y="205.0" width="185.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="217.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約80 A</text>
  <text x="319.1" y="217.0" font-size="12" style="fill: var(--md-default-fg-color)">22 kW電動機（200 V）</text>
  <rect x="128" y="231.0" width="186.6" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="243.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約87 A</text>
  <text x="320.6" y="243.0" font-size="12" style="fill: var(--md-default-fg-color)">1,000 kVA 変圧器の一次</text>
  <rect x="128" y="257.0" width="209.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="269.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約350 A</text>
  <text x="343.3" y="269.0" font-size="12" style="fill: var(--md-default-fg-color)">40 MW を 66 kV で受電（力率1）</text>
  <rect x="128" y="283.0" width="243.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="295.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約2,750 A</text>
  <text x="377.1" y="295.0" font-size="12" style="fill: var(--md-default-fg-color)">1,000 kVA 変圧器の二次</text>
  <rect x="128" y="309.0" width="247.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="321.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約3,500 A</text>
  <text x="381.0" y="321.0" font-size="12" style="fill: var(--md-default-fg-color)">40 MW を 6.6 kV で受電（力率1）</text>
  <rect x="128" y="335.0" width="267.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="347.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">12.5 kA</text>
  <text x="401.9" y="347.0" font-size="12" style="fill: var(--md-default-fg-color)">遮断器の定格遮断電流</text>
  <rect x="128" y="361.0" width="282.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="373.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">数十 kA</text>
  <text x="416.3" y="373.0" font-size="12" style="fill: var(--md-default-fg-color)">雷</text>
</svg>
</figure>

| 電流 | 実物・機器の例 | 現場での使いどころ |
|---|---|---|
| 1 mA | 人が感じ始める目安 | 低圧の漏えい電流の管理値の桁 |
| 4〜20 mA | 計装の統一信号（[計装の基礎](../03-keiso/basics.md)） | LED 1個も数 mA〜20 mA |
| 30 mA | 漏電遮断器の高感度形（[低圧配電](../02-teiatsu/distribution.md)） | 感度の数値は法令ではなく実務標準 |
| 0.2 A 程度 | 高圧受電設備の地絡継電器（GR）の整定の目安 | 地絡保護 |
| 数 A 程度 | 高圧配電線の1線地絡電流 Ig | B種接地抵抗の計算に使う |
| 10 A〜15 A | ドライヤー 1 kW（100 V）、コンセント1口 15 A | 分岐回路 |
| 約 80 A | 三相 200 V・22 kW 電動機（効率 0.9・力率 0.85 で計算） | 低圧動力の幹線 |
| 約 87 A／約 2,750 A | 1,000 kVA 変圧器の一次側（6.6 kV）／二次側（210 V） | 同じ変圧器で約30倍違う |
| 約 350 A／約 3,500 A | 40 MW を 66 kV／6.6 kV で受電（力率 1） | 特高で受電する理由 |
| 12.5 kA | 高圧受電用の真空遮断器でよく見る定格遮断電流 | 短絡電流の桁（[短絡電流計算](../04-sekkei/fault-current.md)） |
| 数十 kA〜 | 雷 | 避雷設備 |

!!! danger "感電の数値は目安"
    感電の危険は数十 mA から高まると言われますが、個人差・通電時間・通電経路で大きく変わります。安全の判断基準には使わず、停電・検電・接地の手順（[ロックアウト・タグアウト](../10-safety/lockout-tagout.md)）で守ってください。

人が感じる電流（mA）・高圧の地絡電流（数 A）・短絡電流（kA）は、それぞれ桁が違います。低圧の漏電遮断器は mA、高圧の地絡継電器は 1 A 未満、遮断器は kA 単位の電流を扱います。6.6 kV の非接地系統では地絡電流が短絡電流より桁違いに小さいので、地絡は過電流継電器ではなく、零相電流を見る地絡継電器で検出します。

## 抵抗（Ω）

<figure id="fig-scale-resistance" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 320" width="640" height="320" role="img" aria-labelledby="fig-scale-resistance-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-resistance-title">抵抗のはしご図。横軸は対数目盛りで、10 マイクロオームから 10 ギガオームまで。母線の接続部 0.1 ミリオーム級、屋内配線 2.0 mm の銅線 1 m で 5.5 ミリオーム、100 平方ミリの銅線 1 km で 0.17 オーム、1 kW電熱器 10 オーム、接地抵抗 10〜100 オーム級、測温抵抗体 Pt100 100 オーム、計装の受信抵抗 250 オーム、人体 約1 キロオーム、低圧の絶縁抵抗 メガオーム級、良好な高圧ケーブルの絶縁 ギガオーム級を並べている。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="304" stroke-dasharray="2 3"/>
    <line x1="148.1" y1="38" x2="148.1" y2="304" stroke-dasharray="2 3"/>
    <line x1="168.3" y1="38" x2="168.3" y2="304"/>
    <line x1="188.4" y1="38" x2="188.4" y2="304" stroke-dasharray="2 3"/>
    <line x1="208.5" y1="38" x2="208.5" y2="304" stroke-dasharray="2 3"/>
    <line x1="228.7" y1="38" x2="228.7" y2="304"/>
    <line x1="248.8" y1="38" x2="248.8" y2="304" stroke-dasharray="2 3"/>
    <line x1="268.9" y1="38" x2="268.9" y2="304" stroke-dasharray="2 3"/>
    <line x1="289.1" y1="38" x2="289.1" y2="304"/>
    <line x1="309.2" y1="38" x2="309.2" y2="304" stroke-dasharray="2 3"/>
    <line x1="329.3" y1="38" x2="329.3" y2="304" stroke-dasharray="2 3"/>
    <line x1="349.5" y1="38" x2="349.5" y2="304"/>
    <line x1="369.6" y1="38" x2="369.6" y2="304" stroke-dasharray="2 3"/>
    <line x1="389.7" y1="38" x2="389.7" y2="304" stroke-dasharray="2 3"/>
    <line x1="409.9" y1="38" x2="409.9" y2="304"/>
    <line x1="430.0" y1="38" x2="430.0" y2="304" stroke-dasharray="2 3"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="168.3" y="32">1 mΩ</text>
    <text x="228.7" y="32">1 Ω</text>
    <text x="289.1" y="32">1 kΩ</text>
    <text x="349.5" y="32">1 MΩ</text>
    <text x="409.9" y="32">1 GΩ</text>
  </g>
  <rect x="128" y="49.0" width="20.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.1 mΩ級</text>
  <text x="154.1" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">母線の接続部</text>
  <rect x="128" y="75.0" width="55.2" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">5.5 mΩ</text>
  <text x="189.2" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">屋内配線 2.0 mm × 1 m</text>
  <rect x="128" y="101.0" width="85.2" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.17 Ω</text>
  <text x="219.2" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">銅線 100 mm² × 1 km</text>
  <rect x="128" y="127.0" width="120.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">10 Ω</text>
  <text x="254.8" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">電熱器 1 kW（100 V）</text>
  <rect x="128" y="153.0" width="130.9" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">10〜100 Ω級</text>
  <text x="264.9" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">接地抵抗（種類で違う）</text>
  <rect x="128" y="179.0" width="140.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="191.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">100 Ω</text>
  <text x="274.9" y="191.0" font-size="12" style="fill: var(--md-default-fg-color)">Pt100（0 ℃）</text>
  <rect x="128" y="205.0" width="148.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="217.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">250 Ω</text>
  <text x="282.9" y="217.0" font-size="12" style="fill: var(--md-default-fg-color)">計装の受信抵抗</text>
  <rect x="128" y="231.0" width="161.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="243.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">約1 kΩ</text>
  <text x="295.1" y="243.0" font-size="12" style="fill: var(--md-default-fg-color)">人体（目安）</text>
  <rect x="128" y="257.0" width="210.9" height="16" style="fill: var(--ei-fig-warn)" fill-opacity="0.55"/>
  <text x="120" y="269.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.1〜1 MΩ級</text>
  <text x="344.9" y="269.0" font-size="12" style="fill: var(--md-default-fg-color)">低圧の絶縁抵抗</text>
  <rect x="128" y="283.0" width="281.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="295.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">GΩ級</text>
  <text x="415.9" y="295.0" font-size="12" style="fill: var(--md-default-fg-color)">良好な高圧ケーブル</text>
</svg>
</figure>

| 抵抗 | 実物・機器の例 | 現場での使いどころ |
|---|---|---|
| 数十 µΩ〜数 mΩ | 母線の接続部、遮断器の接触抵抗 | 接続部の発熱管理 |
| 約 5.5 mΩ/m | 屋内配線の銅線 2.0 mm（断面積約 3.14 mm²） | 10 m で約 0.055 Ω |
| 約 0.17 Ω/km | 断面積 100 mm² の銅線（アルミは銅の約 1.6 倍） | 電圧降下の計算（[電圧降下](../04-sekkei/voltage-drop.md)） |
| 10 Ω | 100 V・1 kW の電熱器（R ＝ V²/P） | — |
| 10〜100 Ω 級 | 接地抵抗（種類で値が違う） | 判定値は[接地点検ガイドライン](../guidelines/grounding-inspection.md) |
| 100 Ω／250 Ω | 測温抵抗体 Pt100（0 ℃）／計装の受信抵抗（4〜20 mA → 1〜5 V） | 計装ループ |
| 約 1 kΩ | 人体の抵抗の目安（濡れると下がる） | — |
| MΩ 級 | 低圧の絶縁抵抗 | 判定値は[絶縁管理](../05-hozen/insulation-management.md) |
| GΩ 級 | 良好な高圧ケーブルの絶縁抵抗 | 判定値は[絶縁管理](../05-hozen/insulation-management.md) |

オームの法則でつなぐと、100 V が人体の約 1 kΩ にかかれば約 100 mA、絶縁抵抗 0.1 MΩ にかかれば 1 mA です。「流したい所（電線・接地）は小さく、流したくない所（絶縁）は大きく」です。電線（mΩ〜Ω）と低圧の電路の絶縁（0.1 MΩ 以上）は10万倍以上、接地（10〜100 Ω 級）と低圧の電路の絶縁でも数百倍以上離れています。

## インピーダンス（%Z・Ω）

<figure id="fig-scale-impedance" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 190" width="640" height="190" role="img" aria-labelledby="fig-scale-impedance-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-impedance-title">パーセントインピーダンスのはしご図。横軸は対数目盛りで、1 % から 10,000 % まで。配電用変圧器 4〜6 %、直列リアクトル 6 %、特高の大型変圧器 10〜15 %、同期発電機の同期リアクタンス 100〜200 %、変圧器の励磁インピーダンス 数千 % を並べている。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="174"/>
    <line x1="203.5" y1="38" x2="203.5" y2="174" stroke-dasharray="2 3"/>
    <line x1="279.0" y1="38" x2="279.0" y2="174" stroke-dasharray="2 3"/>
    <line x1="354.5" y1="38" x2="354.5" y2="174"/>
    <line x1="430.0" y1="38" x2="430.0" y2="174" stroke-dasharray="2 3"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="128.0" y="32">1 %</text>
    <text x="354.5" y="32">1 k%</text>
  </g>
  <rect x="128" y="49.0" width="52.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">4〜6 %</text>
  <text x="186.8" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">配電用変圧器の %Z</text>
  <rect x="128" y="75.0" width="58.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">6 %</text>
  <text x="192.8" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">直列リアクトル</text>
  <rect x="128" y="101.0" width="81.5" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">10〜15 %</text>
  <text x="215.5" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">特高の大型変圧器</text>
  <rect x="128" y="127.0" width="164.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">100〜200 %</text>
  <text x="298.3" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">同期リアクタンス</text>
  <rect x="128" y="153.0" width="262.5" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">数千 %</text>
  <text x="396.5" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">変圧器の励磁インピーダンス</text>
</svg>
</figure>

インピーダンスは **Ω ではなく %Z（単位法）で比べます**。Ω の値は電圧で桁が変わるからです。1,000 kVA・%Z 5 % の変圧器は、6.6 kV 側で約 2.2 Ω、210 V 側で約 2.2 mΩ と、同じ 5 % が 1,000 倍違う Ω になります。短絡電流は「定格電流 × 100 / %Z」で、%Z 5 % なら定格の20倍です。

| 大きさ | 例（50 Hz） | 現場での使いどころ |
|---|---|---|
| 4〜6 % | 配電用変圧器の %Z | 短絡すると定格の約17〜25倍が流れる |
| 6 % | 進相コンデンサの直列リアクトル | 第5調波で 5² × 6 % ＝ 150 % となり誘導性（[高調波](../01-koatsu/harmonics.md)） |
| 10〜15 % 程度 | 特高の大型変圧器 | 短絡電流を抑えるため大きめに作る |
| 100〜200 % | 同期発電機の同期リアクタンス | 短絡比 ＝ 1／同期リアクタンス（単位法） |
| 数千 % | 変圧器の励磁インピーダンス | 無負荷電流が定格の数 % しか流れない理由 |
| 約 0.3 Ω | 6.6 kV で短絡電流 12.5 kA になる電源側（6,600 ÷ √3 ÷ 12,500） | 受電点の短絡電流の見積り |
| 約 0.4 Ω/km | 架空送電線の誘導リアクタンス | 抵抗（0.1〜0.2 Ω/km）より大きい |
| 約 436 Ω／約 26 Ω | 6.6 kV・100 kvar の進相コンデンサ（X ＝ V²/Q）／その直列リアクトル 6 % | コンデンサ設備 |
| 約 3.2 kΩ | 高圧配電系統の対地静電容量 1 µF（1相分） | 1線地絡電流 3ωCE ≒ 3.6 A |

50 Hz の換算の目安は、1 mH → 0.31 Ω、1 H → 314 Ω、1 µF → 3.2 kΩ、100 µF → 32 Ω です。60 Hz なら誘導性は 1.2 倍、容量性は 1/1.2 になります。

## 力率（cos θ）

<figure id="fig-scale-pf" style="scroll-margin-top: 4rem">
<svg viewBox="0 0 640 268" width="640" height="268" role="img" aria-labelledby="fig-scale-pf-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-scale-pf-title">力率のはしご図。横軸は 0 から 1 までの等間隔目盛り。抵抗負荷 1.0、改善後の受電点 0.95〜1.0、改善の目標 0.9、誘導電動機の定格負荷時 0.8〜0.9、計算の定番 0.8、蛍光灯の磁気式安定器や電動機の軽負荷 0.5〜0.6、無負荷の電動機や変圧器 0.1〜0.2、リアクトルとコンデンサ 0 を並べ、右に同じ電力を送るときの電流倍率を書いている。</title>
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1" stroke-opacity="0.35">
    <line x1="128.0" y1="38" x2="128.0" y2="252"/>
    <line x1="188.4" y1="38" x2="188.4" y2="252"/>
    <line x1="248.8" y1="38" x2="248.8" y2="252"/>
    <line x1="309.2" y1="38" x2="309.2" y2="252"/>
    <line x1="369.6" y1="38" x2="369.6" y2="252"/>
    <line x1="430.0" y1="38" x2="430.0" y2="252"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11" text-anchor="middle">
    <text x="128.0" y="32">0</text>
    <text x="188.4" y="32">0.2</text>
    <text x="248.8" y="32">0.4</text>
    <text x="309.2" y="32">0.6</text>
    <text x="369.6" y="32">0.8</text>
    <text x="430.0" y="32">1</text>
  </g>
  <rect x="128" y="49.0" width="302.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="61.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">1.0</text>
  <text x="436.0" y="61.0" font-size="12" style="fill: var(--md-default-fg-color)">抵抗負荷（電流 1 倍）</text>
  <rect x="128" y="75.0" width="292.9" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="87.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.95〜1.0</text>
  <text x="426.9" y="87.0" font-size="12" style="fill: var(--md-default-fg-color)">改善後の受電点</text>
  <rect x="128" y="101.0" width="271.8" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="113.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.9</text>
  <text x="405.8" y="113.0" font-size="12" style="fill: var(--md-default-fg-color)">改善の目標（1.11 倍）</text>
  <rect x="128" y="127.0" width="256.7" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="139.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.8〜0.9</text>
  <text x="390.7" y="139.0" font-size="12" style="fill: var(--md-default-fg-color)">誘導電動機・定格負荷</text>
  <rect x="128" y="153.0" width="241.6" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="165.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.8</text>
  <text x="375.6" y="165.0" font-size="12" style="fill: var(--md-default-fg-color)">計算の定番（1.25 倍）</text>
  <rect x="128" y="179.0" width="166.1" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="191.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.5〜0.6</text>
  <text x="300.1" y="191.0" font-size="12" style="fill: var(--md-default-fg-color)">蛍光灯・軽負荷（約2 倍）</text>
  <rect x="128" y="205.0" width="45.3" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="217.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0.1〜0.2</text>
  <text x="179.3" y="217.0" font-size="12" style="fill: var(--md-default-fg-color)">無負荷の電動機・変圧器</text>
  <rect x="128" y="231.0" width="2.0" height="16" style="fill: var(--md-default-fg-color)" fill-opacity="0.22"/>
  <text x="120" y="243.0" font-size="12" text-anchor="end" style="fill: var(--md-default-fg-color)">0</text>
  <text x="134.0" y="243.0" font-size="12" style="fill: var(--md-default-fg-color)">リアクトル（遅れ）・コンデンサ（進み）</text>
</svg>
</figure>

同じ有効電力を送るとき、電流は 1/cos θ 倍、線路損失は 1/cos² θ 倍になります。力率 0.8 なら電流 1.25 倍・損失約 1.56 倍、0.5 なら電流2倍・損失4倍です。40 MW を 66 kV で受電するとき、力率 1 なら約 350 A、0.8 なら約 437 A です。

| 力率 | 実物・機器の例 | 現場での使いどころ |
|---|---|---|
| 1.0 | 電熱器・白熱電球などの抵抗負荷 | — |
| 0.95〜1.0 | 力率改善後の受電点 | 基本料金の力率割引（[力率改善ROI](../08-energy/power-factor-roi.md)） |
| 0.8〜0.9 | 誘導電動機の定格負荷時 | 計算では 0.8（sin θ ＝ 0.6）が定番 |
| 0.5〜0.6 | 磁気式安定器の蛍光灯、電動機の軽負荷時 | 軽負荷運転は力率が下がる |
| 0.1〜0.2 程度 | 無負荷の電動機・変圧器 | 電流のほとんどが磁化電流 |
| 0（遅れ／進み） | リアクトル／進相コンデンサ | 軽負荷時にコンデンサを入れたままだと進み力率で受電電圧が上がる |

力率改善に必要なコンデンサ容量は Qc ＝ P × (tan θ₁ − tan θ₂) です。tan θ は cos θ ＝ 0.95 で約 0.33、0.9 で約 0.48、0.8 で 0.75、0.6 で約 1.33 です。100 kW を 0.8 から 0.95 にすると約 42 kvar です（[力率改善](../01-koatsu/power-factor.md)）。

## よくある誤解

- **「特高なら電験3種で見られる」** — 第三種の範囲は 50,000 V 未満です。66 kV 受電は範囲外です。
- **「%Z が小さいほど良い変圧器」** — %Z が小さいと電圧降下は小さくなりますが、短絡電流が大きくなり遮断器の負担が増えます。トレードオフです。
- **「力率は 1.0 まで上げるほど得」** — 0.95 から 1.0 に上げるコンデンサは効果の割に大きくなります（tan θ 0.33 分が全部要る）。軽負荷時は進み力率の害も出ます。

## 関連記事

- [短絡電流計算](../04-sekkei/fault-current.md)
- [電圧降下](../04-sekkei/voltage-drop.md)
- [力率改善](../01-koatsu/power-factor.md)
- [高調波](../01-koatsu/harmonics.md)
- [接地点検ガイドライン](../guidelines/grounding-inspection.md)
- [絶縁管理](../05-hozen/insulation-management.md)
- [計算ツール集](calculators.md)
