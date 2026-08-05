---
title: "規格一覧"
description: "電気・計装・防爆・安全計装の主要規格を表形式で整理"
tags:
  - 逆引き
audience:
  - 電気担当
last_verified: 2026-08-05
---

# 規格一覧

!!! info "計装現場での使いどころは別ページ"
    本ページは規格番号・タイトル・入手先の網羅表です。各JISが計装工事のどこに効くかは [電気計装工事で押さえるJIS規格](../03-keiso/jis-standards.md) を参照してください。

## 電気設備関連規格

| 規格番号 | タイトル | 適用場面 | 入手先 |
|---------|---------|---------|-------|
| 電気設備技術基準（電技） | 電気設備に関する技術基準を定める省令 | すべての電気設備設計・施工 | 経産省 HP（無料） |
| 電気設備技術基準の解釈（電技解釈） | 電技の具体的な技術基準 | 接地・絶縁・保護の設計 | 経産省 HP（無料） |
| 内線規程（JEAC 8001） | 屋内電気設備の標準技術基準 | 屋内配線設計・施工 | 電気技術規程（有償） |
| 高圧受電設備規程（JEAC 8011） | 自家用高圧受電設備の技術基準 | 高圧受変電設備設計 | 電気技術規程（有償） |
| JIS C 1010-1 | 測定・制御・試験室用電気機器の安全 | 測定器の安全規格 | JSA Web デジタルライブラリ |
| JIS C 60364 群 | 低圧電気設備（IEC 60364 対応） | 低圧電気設備の設計・検証 | JSA |
| IEC 60364 | Low-voltage electrical installations | 低圧電気設備の国際標準 | IEC |

---

## 機器・制御関連規格

| 規格番号 | タイトル | 適用場面 | 入手先 |
|---------|---------|---------|-------|
| JIS C 0617 | 電気用図記号（IEC 60617 対応） | 展開図・P&ID の図記号 | JSA |
| JIS C 0448 | 表示・操作機器の色（1997年制定が現行） | 押しボタン・表示灯の色。割当は [操作盤・表示灯](../02-teiatsu/panel-hmi.md) | JSA |
| JIS C 60529（旧 JIS C 0920） | 外郭による保護等級（IP コード） | 盤・端子箱・フィールド機器の防塵防水等級。新旧番号は同じ体系（[計装工事で押さえるJIS規格](../03-keiso/jis-standards.md)） | JSA |
| IEC 60204-1 | Safety of machinery - Electrical equipment | 制御盤・非常停止の設計 | IEC |
| IEC 61439 | Low-voltage switchgear and controlgear assemblies | 低圧制御盤の設計・試験 | IEC |
| IEC 60947-5-5 | Emergency stop devices with mechanical latching | 非常停止装置の規格 | IEC |
| JEM 1195 | 低圧コントロールセンタ | 低圧 MCC の仕様・形式 | JEMA |
| JIS C 4034 | 回転電気機械 | 電動機の設計・試験 | JSA |

---

## 防爆関連規格

| 規格番号 | タイトル | 適用場面 | 入手先 |
|---------|---------|---------|-------|
| JIS C 60079-0 | 爆発性雰囲気：一般要求事項 | 防爆機器の基本要件 | JSA |
| JIS C 60079-1 | 耐圧防爆 Ex d | 耐圧防爆機器の設計・試験 | JSA |
| JIS C 60079-7 | 安全増防爆 Ex e | 安全増防爆機器 | JSA |
| JIS C 60079-11 | 本質安全防爆 Ex i | 本質安全回路の設計 | JSA |
| JIS C 60079-14 | 危険場所への電気設備の設置 | 防爆エリアでの設置基準 | JSA |
| IEC 60079-10-1 | Classification of areas - Gas | ガス危険場所の区分方法 | IEC |
| IEC 60079-10-2 | Classification of areas - Dust | 粉塵危険場所の区分方法 | IEC |
| ATEX 114 Directive | Equipment for explosive atmospheres | 欧州防爆機器の販売・使用規制 | EU |
| 消防法 第10条第3項・第4項 | 技術上の基準を**政令に委任**する規定（基準そのものは条文にない） | 危険物施設の位置・構造・設備 | e-Gov（無料） |
| 危険物の規制に関する政令 第9条第1項第十七号 | **「電気設備は、電気工作物に係る法令の規定によること」** | 危険物施設の電気設備は電技・電技解釈側に戻る（下記「根拠」参照） | e-Gov（無料） |

---

## 計装・プロセス制御関連規格

| 規格番号 | タイトル | 適用場面 | 入手先 |
|---------|---------|---------|-------|
| ISA-5.1 | Instrumentation Symbols and Identification | P&ID の計装記号 | ISA（有償） |
| ISA-5.4 | Instrument Loop Diagrams | ループ図の作成標準 | ISA（有償） |
| ISA-18.2 | Management of Alarm Systems | アラーム管理（実務は [アラーム管理](../03-keiso/alarm-management.md)） | ISA（有償） |
| ISA-88 | Batch Control | バッチプロセス制御 | ISA（有償） |
| NAMUR NE 43 | Standardization of Signal Level | 4-20mA の障害検出信号（3.6/21mA） | NAMUR |
| NAMUR NE 107 | Self-monitoring and Diagnosis | HART 機器の診断情報活用 | NAMUR |
| IEC 61158 | Fieldbus for use in industrial control systems | フィールドバスの国際標準 | IEC |
| IEC 61784 | Profile sets for continuous and discrete manufacturing | フィールドバスプロファイル | IEC |

---

## 安全計装関連規格

| 規格番号 | タイトル | 適用場面 | 入手先 |
|---------|---------|---------|-------|
| IEC 61511-1 | Safety instrumented systems for the process industry | 化学・石油化学プロセスの SIS 設計 | IEC |
| IEC 61511-2 | Guidelines for the application of IEC 61511-1 | 61511-1 の適用ガイド | IEC |
| IEC 61511-3 | Guidance for the determination of the required safety integrity levels | **必要 SIL の決定**（HAZOP・LOPA 等のリスク評価手法の例示） | IEC |
| IEC 61508 | Functional safety of E/E/PE safety-related systems | SIS の基礎規格（SIL の定義） | IEC |
| IEC 62061 | Safety of machinery - SIL | 機械向け安全計装 | IEC |

安全計装の規格は番号が近く混同しやすいため、上表の関係を図にすると次のとおりです。

<figure>
<svg viewBox="0 0 640 344" width="640" height="344" role="img"
     aria-labelledby="fig-fsafety-hierarchy-title" xmlns="http://www.w3.org/2000/svg">
  <title id="fig-fsafety-hierarchy-title">機能安全規格の関係。SILを定義する基礎規格 IEC 61508 の下に、プロセス産業向けの IEC 61511 と機械向けの IEC 62061 が分かれる。IEC 61511 はさらにパート1（SIS設計）、パート2（61511-1の適用ガイド）、パート3（必要SILの決定）に分かれる。</title>
  <g style="stroke: var(--md-default-fg-color); fill: none" stroke-width="1.6">
    <rect x="180" y="16" width="280" height="56" rx="6"/>
    <line x1="320" y1="72" x2="320" y2="96"/>
    <line x1="170" y1="96" x2="470" y2="96"/>
    <line x1="170" y1="96" x2="170" y2="110"/>
    <line x1="470" y1="96" x2="470" y2="110"/>
    <rect x="36" y="124" width="268" height="56" rx="6"/>
    <rect x="356" y="124" width="228" height="56" rx="6"/>
  </g>
  <g style="stroke: none; fill: var(--md-default-fg-color)">
    <path d="M 170,120 L 164,109 L 176,109 Z"/>
    <path d="M 470,120 L 464,109 L 476,109 Z"/>
  </g>
  <!-- 61511 のパート構成 -->
  <g style="stroke: var(--md-default-fg-color--light); fill: none" stroke-width="1.2">
    <line x1="170" y1="180" x2="170" y2="190"/>
    <line x1="170" y1="190" x2="52" y2="190"/>
    <line x1="52" y1="190" x2="52" y2="304"/>
    <line x1="52" y1="216" x2="64" y2="216"/>
    <line x1="52" y1="260" x2="64" y2="260"/>
    <line x1="52" y1="304" x2="64" y2="304"/>
    <rect x="64" y="200" width="240" height="32" rx="4"/>
    <rect x="64" y="244" width="240" height="32" rx="4"/>
    <rect x="64" y="288" width="240" height="32" rx="4"/>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="15">
    <text x="320" y="42" text-anchor="middle">IEC 61508</text>
    <text x="170" y="150" text-anchor="middle">IEC 61511</text>
    <text x="470" y="150" text-anchor="middle">IEC 62061</text>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11">
    <text x="320" y="62" text-anchor="middle">SIS の基礎規格（SIL の定義）</text>
    <text x="170" y="170" text-anchor="middle">化学・石油化学プロセスの SIS</text>
    <text x="470" y="170" text-anchor="middle">機械向け安全計装</text>
  </g>
  <g style="fill: var(--md-default-fg-color--light)" font-size="10">
    <text x="180" y="112" text-anchor="start">プロセス産業向け</text>
    <text x="460" y="112" text-anchor="end">機械向け</text>
  </g>
  <g style="fill: var(--md-default-fg-color)" font-size="11">
    <text x="76" y="221">-1　化学・石油化学プロセスの SIS 設計</text>
    <text x="76" y="265">-2　61511-1 の適用ガイド</text>
    <text x="76" y="309">-3　必要 SIL の決定（リスク評価）</text>
  </g>
</svg>
<figcaption>SIL を定義する基礎規格が IEC 61508、そこからプロセス産業向けに具体化したものが IEC 61511、機械向けが IEC 62061。化学プラントの SIS 設計で直接参照するのは IEC 61511 の 3 パート。</figcaption>
</figure>

---

## 日本固有の法規（参考）

| 法規名 | 主管省庁 | 主な適用 | 参照先 |
|-------|---------|---------|-------|
| 電気事業法 | 経済産業省 | 自家用電気工作物の設置・変更 | 経産省 HP |
| 高圧ガス保安法 | 経済産業省 | 高圧ガス設備の変更・検査 | 経産省 HP |
| 労働安全衛生法 | 厚生労働省 | 停電作業・特別教育 | 厚労省 HP |
| 消防法 | 総務省 | 防爆機器・非常電源・危険物 | 消防庁 HP |
| 計量法 | 経済産業省 | 取引・証明用計量器の校正 | 経産省 HP |

---

## 根拠

### 本ページの位置づけ

**規格番号とタイトルの索引**であり、規格の要求内容を書くページではありません。要求内容は各正典ページ（[電気計装工事で押さえるJIS規格](../03-keiso/jis-standards.md)・[防爆](../03-keiso/explosion-proof.md)・[安全計装 SIS/SIL](../03-keiso/sis-sil.md)・[アラーム管理](../03-keiso/alarm-management.md)）にあり、本ページからは番号でたどるだけです。

### 一次照合済みの条項号（e-Gov 現行条文・2026-08-05 照合）

| 条項 | 確認した内容 |
|---|---|
| 消防法 第10条第3項 | 製造所・貯蔵所・取扱所における危険物の貯蔵・取扱いは「**政令で定める技術上の基準**」に従う |
| 消防法 第10条第4項 | 位置・構造及び設備の技術上の基準は「**政令でこれを定める**」。**第10条自体には基準の中身がない** |
| 危険物の規制に関する政令 第9条第1項第十七号 | 製造所の基準として「**電気設備は、電気工作物に係る法令の規定によること**」 |
| 同 第10条第1項第十三号ほか | 屋内貯蔵所・屋外タンク貯蔵所・地下タンク貯蔵所等は「**第9条第1項第十七号に掲げる製造所の電気設備の例による**」と準用 |

### 委任チェーン（危険物施設の電気設備をどこで調べるか）

**消防法 第10条第3項・第4項 →（委任）→ 危険物の規制に関する政令 第9条第1項第十七号 →（丸ごと参照）→ 電気工作物に係る法令（電気事業法・電技・電技解釈）**

危険物施設の電気設備に固有の技術基準を**消防法の中で探しても見つかりません**。政令が電気工作物側の法令に戻しているためで、防爆の実体は電技解釈側（法令から JIS C 60079-14 への名指しは [計装工事で押さえるJIS規格](../03-keiso/jis-standards.md)・[規格・法規](../04-sekkei/standards.md) が正典）にあります。

### 是正の記録（2026-08-05）

索引ページの誤りは**参照先を丸ごと間違えさせる**ため、番号とタイトルの対応を洗い直しました。

| 項目 | 旧記載 | 是正後 |
|---|---|---|
| JEM 1195 | 開放型電動機の騒音測定方法 | **低圧コントロールセンタ**（低圧 MCC の規格。メーカー各社の製品説明で一致） |
| JIS C 0364 | 建築電気設備 | **JIS C 60364 群「低圧電気設備」**。中核部は C60364 に採番替えされており、旧番号のまま引くと現行版に届かない |
| IEC 61511-3 | Guidance for functional safety assessment／SIL 評価の実施方法 | **Guidance for the determination of the required safety integrity levels**＝**必要 SIL の決定**。「評価の実施方法」ではなく「どの SIL が必要かを決める」パート |
| IEC 61511-2 | Application guidelines | **Guidelines for the application of IEC 61511-1** |
| NAMUR NE 43／NE 107 の入手先 | NAMUR（無料） | **NAMUR**（入手条件を未確認のため「無料」を削除） |
| 消防法第 10 条 | 危険物施設の技術上の基準 | **第10条は基準を政令に委任する規定**。基準の実体は危険物の規制に関する政令にあり、電気設備は同令第9条第1項第十七号で**電気工作物に係る法令へ戻される**（委任チェーンを飛ばした直接帰属を是正） |
| JIS C 0448 | 人間・機械インターフェース | **表示・操作機器の色（1997年制定が現行）**。repo 内の [計装工事で押さえるJIS規格](../03-keiso/jis-standards.md) が JSA カタログで番号・名称・現行有効を一次確認済みだったため、その記述に合わせた |

IEC 61511-3 の是正は**図（機能安全規格の階層）の中の文字・title・figcaption も同時に直しました**。本文だけ直すと図が旧記述のまま残ります。

### 二次資料で一致を確認（原本未照合）

- **IEC 61511-2／-3 の正式表題**は IEC webstore・ANSI webstore の書誌情報で一致を確認しました。**規格本文は未入手**です（2016 年版が第2版で 2003 年版を置き換えたことも書誌情報どまり）
- **JEM 1195 が低圧コントロールセンタである**ことは、複数メーカーの製品説明で一致を確認しました。**JEMA の規格本文は未入手**です
- **JIS C 0364 → C 60364 の採番替え**は JSA・規格本文の公開索引で確認しました。ただし**特殊設備・特殊場所を扱う第7部は JIS C 0364-7-xxx の採番が残っています**（例: JIS C 0364-7-714）。「すべてが C60364 に移った」わけではありません

### 原本未照合（honest-hold）

- **本表のすべての規格について、本文は未入手です。** タイトル・適用場面は書誌情報と公開索引に基づくもので、**条項番号は一切引用していません**
- **版年は書きません。** 過去に「JIS C 0448:2011」という**実在しない版年**を載せていた事案があるため、本ページは版年を持たない索引に統一しています。版が要る作業では JSA・IEC の現行版を直接確認してください
- ~~**JIS C 0448 の正式表題**は原本未照合~~ → **解消済み（2026-08-05）**。[計装工事で押さえるJIS規格](../03-keiso/jis-standards.md) が JSA カタログで「JIS C 0448:1997（2023-10-20 確認）」を一次確認済みだったため、その記述に揃えました。**honest-hold にする前に repo 内の既存照合を探すこと**（本件は探さずに hold を書いた取りこぼし）
- **入手先の欄は「どこが発行しているか」の目安**で、無償／有償の別は NAMUR ほか一部で未確認です

### 限界の明示

- **網羅表ではありません。** プラントで参照する規格のうち、本 Wiki の他ページから参照されるものを中心に並べたものです
- **索引の誤りは下流全体に伝播します。** 本表の番号を根拠として使う前に、実際の規格の表題を発行元で確認してください
- **法規の欄（日本固有）は主管省庁の目安**で、条項の特定は各正典ページ（[法定義務一覧](../09-hoantokei/legal-duties.md) ほか）によってください

### 正典参照

| 項目 | 正典 |
|---|---|
| 各 JIS が計装工事のどこに効くか | [電気計装工事で押さえるJIS規格](../03-keiso/jis-standards.md) |
| 防爆の規格体系・EPL・ガスグループ | [防爆](../03-keiso/explosion-proof.md) |
| SIL・安全計装の設計 | [安全計装 SIS/SIL](../03-keiso/sis-sil.md) |
| アラーム管理の実務 | [アラーム管理](../03-keiso/alarm-management.md) |
| 法定義務・届出の条項 | [法定義務一覧](../09-hoantokei/legal-duties.md) |

照合日: 2026-08-05（消防法・危険物政令は e-Gov 現行条文で一次照合。規格は書誌情報レベルの確認で本文はいずれも未入手）。
