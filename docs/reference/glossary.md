---
title: "用語集"
description: "電気系・計装系・防爆用語の日英略語対応表"
tags:
  - 逆引き
  - 入門
audience:
  - 電気担当
last_verified: 2026-08-06
---

# 用語集

## 電気系用語（52語）

| 日本語 | English | 略語 | 説明 |
|-------|---------|------|------|
| 遮断器 | Circuit Breaker | CB / MCCB / VCB | 過電流・短絡電流を感知して回路を自動遮断する機器 |
| 電磁接触器 | Magnetic Contactor | MC | 電磁コイルで主接点を開閉する機器。モーター起動に使用 |
| サーマルリレー | Thermal Relay | THR | バイメタルの熱変形で過電流を検出しモーターを保護 |
| 漏電遮断器 | Earth Leakage Circuit Breaker | ELCB / RCCB | 漏洩電流を検出して遮断する安全装置 |
| 配線用遮断器 | Molded Case Circuit Breaker | MCCB | 樹脂成形ケース内に遮断機構を持つ遮断器 |
| アンペアトリップ | Ampere Trip | AT | MCCB の定格電流。超過が続くと引き外し動作する電流値 |
| アンペアフレーム | Ampere Frame | AF | MCCB のフレーム（外箱）の大きさの呼び。搭載できる最大 AT を表し、常に AF ≥ AT |
| 真空遮断器 | Vacuum Circuit Breaker | VCB | 真空バルブで電流を遮断する高圧用遮断器 |
| 断路器 | Disconnecting Switch | DS | 無負荷状態で回路を切り離す開閉器（負荷開閉不可） |
| 過電流継電器 | Overcurrent Relay | OCR | 設定電流値を超えると動作する保護継電器 |
| 地絡継電器 | Ground Fault Relay | GR | 地絡電流を検出して動作する保護継電器 |
| 地絡方向継電器 | Directional Ground Fault Relay | DGR | 地絡電流の方向を判別する継電器 |
| 変圧器 | Transformer | TR | 電圧・電流を変換する機器 |
| 主幹 | Main Breaker | — | 受電の最上流に設置する主開閉器 |
| 分岐 | Branch Circuit | — | 主幹から枝分かれした回路 |
| 需要率 | Demand Factor | — | 設備容量に対する実際の最大需要電力の比率 |
| 力率 | Power Factor | PF / cosθ | 有効電力 / 皮相電力の比。1 に近いほど効率的 |
| 高調波 | Harmonics | — | 基本周波数の整数倍成分。インバータ・整流回路から発生 |
| インバータ | Inverter | INV | 直流を任意の周波数の交流に変換する機器 |
| 無停電電源装置 | Uninterruptible Power Supply | UPS | 停電時にバッテリーで電源を供給する装置 |
| 接地 | Grounding / Earthing | — | 電気機器を大地に電気的に接続すること |
| 等電位ボンディング | Equipotential Bonding | EPB | 複数の金属部分を同電位にする接続 |
| 電圧降下 | Voltage Drop | — | ケーブルの抵抗・リアクタンスによる電圧の低下 |
| 短絡電流 | Short Circuit Current | Is | 短絡故障時に流れる大電流 |
| %インピーダンス | Percent Impedance | %Z | 定格電流を流したときのインピーダンス電圧降下率 |
| 遮断容量 | Interrupting Capacity | IC / kA | 遮断器が安全に遮断できる最大短絡電流 |
| 保護協調 | Protective Coordination | — | 系統内の保護機器が適切な順序で動作する設計 |
| 自己保持回路 | Self-Holding Circuit | — | 起動 PB を離しても動作を継続するリレー回路 |
| インターロック | Interlock | IL | 特定の条件が成立しないと動作を禁止する回路 |
| フェールセーフ | Fail-Safe | — | 故障時に安全な状態になるよう設計された原則 |
| 展開接続図 | Connection Diagram | — | 制御回路の接続を機能的に展開した図 |
| 単線結線図 | Single Line Diagram | SLD | 電源系統を 1 線で表現した系統図 |
| ケーブルリスト | Cable Schedule | — | ケーブルの起点・終点・仕様をまとめた一覧表 |
| ループ電源 | Loop Power | — | DCS・レシーバーから 24V を伝送器に供給する方式（[計装基礎](../03-keiso/basics.md)参照） |
| デマンド | Demand | — | 需要電力。一定時間内の平均電力 |
| 受変電設備 | Substation | — | 受電・変圧・配電を行う設備の総称 |
| ケーブルラック | Cable Tray | — | ケーブルを支持・整列する支持架台 |
| 金属管 | Conduit | — | ケーブルを収納・保護する金属製の管 |
| 電気室 | Electrical Room | E/R | 受変電設備・制御盤を設置する専用部屋 |
| MCC | Motor Control Center | MCC | 複数の電動機制御ユニットを集合させた配電盤 |
| PLCプログラム | PLC Program | — | プログラマブルロジックコントローラの制御プログラム |
| ラダー図 | Ladder Diagram | LD | リレー回路に類似したグラフィカルプログラミング言語 |
| タグ番号 | Tag Number | TAG | 設備・計装機器を識別する番号体系 |
| 電路 | Electric Circuit | — | 法令用語では「通常の使用状態で電気が通じているところ」（電技省令第1条）。現場では[電路設計](../04-sekkei/cable-route.md)のようにケーブルの物理的経路（ラック・管路）の意味でも使われる |
| 接続箱 | Junction Box | JB | フィールドケーブルを集約・接続する箱 |
| 端子台 | Terminal Block | TB | 電線接続のための端子の集合体 |
| コントロールバルブ | Control Valve | CV | 制御信号で開度を連続調節できる弁 |
| 緊急遮断弁 | Emergency Shut Down Valve | ESD Valve / ESDV | 緊急時に自動で閉鎖する安全弁 |
| ループチェック | Loop Check | — | 計装ループの点検・動作確認 |
| 試運転 | Commissioning | — | 設備の機能確認・調整を行う工程 |
| MOC | Management of Change | MOC | 設備・手順の変更を管理する仕組み |
| 定期修理 | Turnaround | T/A | プラント停止中に集中して行う大規模点検 |

---

## 計装系用語（30語）

| 日本語 | English | 略語 | 説明 |
|-------|---------|------|------|
| 伝送器 | Transmitter | TX | プロセス変数を 4-20mA 等の標準信号に変換する機器 |
| 変換器 | Converter / Transducer | — | 信号の種類・スケールを変換する機器 |
| 配管計装図 | Piping and Instrumentation Diagram | P&ID | 配管・バルブ・計装機器の系統を示す図面 |
| プロセス変数 | Process Variable | PV | 制御対象の物理量（温度・圧力・流量等） |
| 設定値 | Set Point | SP | 制御目標値 |
| 操作量 | Manipulated Variable | MV | コントローラが制御弁などに出力する制御信号 |
| 分散制御システム | Distributed Control System | DCS | 工場全体のプロセス制御を分散して行うシステム |
| 安全計装システム | Safety Instrumented System | SIS | 危険状態を検出し安全側に動作させる独立した制御系 |
| 安全完全性レベル | Safety Integrity Level | SIL | SIS の信頼性・安全性のレベル（SIL 1〜4。[安全計装 SIS/SIL](../03-keiso/sis-sil.md)参照） |
| 最終要素 | Final Element | — | 制御弁・電磁弁など制御出力を受ける機器 |
| フィールドバス | Fieldbus | — | フィールド機器とコントローラを接続するデジタル通信 |
| HART | Highway Addressable Remote Transducer | HART | 4-20mA にデジタル信号を重畳する通信プロトコル |
| Foundation Fieldbus | Foundation Fieldbus | FF | 全デジタルのフィールドバスプロトコル |
| Modbus | Modbus | — | シリアル通信のシンプルなプロトコル |
| NAMUR | NAMUR | — | プロセス産業のオートメーション技術ユーザー協会（ドイツ）。NE 勧告（NE43 等）を発行する |
| ループ図 | Loop Diagram | — | 1 制御ループの接続を詳細に示した図面 |
| 校正 | Calibration | — | 測定器の指示値を基準に合わせる作業 |
| ゼロトリム | Zero Trim | — | 入力ゼロ時の出力を 4mA（0%）に合わせる調整 |
| スパン | Span | — | 測定範囲の最大値 - 最小値 |
| ドリフト | Drift | — | 時間経過による指示値のずれ |
| 電流ループ | Current Loop | — | 4-20mA を使ったアナログ信号伝送方式（電流帯の区分は[計装基礎](../03-keiso/basics.md)が正典） |
| ソースモード | Source Mode | — | ループキャリブレーターが電流を出力するモード |
| シンクモード | Sink Mode | — | 外部電源からの電流を受けて測定するモード |
| ポジショナー | Positioner | — | 制御弁の開度を制御信号に合わせるフィードバック装置 |
| デッドウェイトテスター | Dead Weight Tester | DWT | 分銅の重力を利用した圧力一次標準器 |
| ループキャリブレーター | Loop Calibrator | — | 4-20mA の信号を発生・測定する携帯型校正器 |
| レンジャビリティ | Rangeability | — | 流量計等の測定範囲の広さ（最大 / 最小流量比） |
| タイムアウト | Time-Out | — | 通信や制御が規定時間内に完了しない場合の処理 |
| アラーム | Alarm | — | 異常検知時の警報信号 |
| トリップ | Trip | — | 異常時に設備を緊急停止させる動作 |

---

## 防爆用語（10語）

| 日本語 | English | 略語 | 説明 |
|-------|---------|------|------|
| 防爆 | Explosion Protection | Ex | 爆発性雰囲気での点火を防ぐための構造・方式 |
| 危険場所 | Hazardous Area | — | 爆発性ガスまたは粉塵が存在する可能性のある場所 |
| Zone 0 | Zone 0 | — | 爆発性雰囲気が連続して存在する場所 |
| Zone 1 | Zone 1 | — | 爆発性雰囲気が断続的に生じる可能性のある場所 |
| Zone 2 | Zone 2 | — | 爆発性雰囲気が生じる可能性が低い場所 |
| 耐圧防爆 | Flameproof | Ex d | 内部爆発を封じ込め外部に火炎を伝えない構造 |
| 安全増防爆 | Increased Safety | Ex e | スパーク・高温部を排除した構造 |
| 本質安全防爆 | Intrinsic Safety | Ex ia/ib | 回路エネルギーを点火能力以下に制限する方式 |
| 温度クラス | Temperature Class | T1〜T6 | 機器の最高表面温度を分類（T6 が最も低温：85℃。対応表は[防爆照明](../02-teiatsu/lighting.md)が正典） |
| ガスグループ | Gas Group | IIA/IIB/IIC | 爆発性ガスを点火のしやすさで分類。IIC が最も点火感度が高い（[防爆](../03-keiso/explosion-proof.md)参照） |

## 根拠

### 本ページが正典の範囲

本ページは**用語の和英対応と1行定義のみ**の正典です。数値・条文・判定基準は各正典ページが持ち、本ページの定義に数値が含まれる場合は正典リンクを併記します（定義のずれは全ページに波及するため、正典と食い違う定義を書かないことを最優先とします）。

### 一次照合済みの条項号（e-Gov 法令 API 照合）

- **「電路」の定義**: 電気設備に関する技術基準を定める省令（平成9年通商産業省令第52号）**第1条第一号**「『電路』とは、通常の使用状態で電気が通じているところをいう。」を e-Gov 法令 API の現行条文で逐語確認。あわせて同条第九号「電線路」（電線＋支持・保蔵する工作物）が別の定義語であることも確認

### 是正の記録（2026-08-06）

- **「電路＝ケーブルが通る物理的経路（ラック・管路）」の定義を是正**: 電技省令第1条第一号の法令定義（通常の使用状態で電気が通じているところ）と食い違っていた。省令第58条「低圧電路の絶縁抵抗」等の法令記述を物理経路の意味で読むと誤読になるため、法令定義を第一義とし、現場での「物理経路」の用法（本Wikiの「電路設計」ページ等）は併記に格下げした
- **「NAMUR＝計装機器標準化団体」を是正**: NAMUR はプロセス産業のオートメーション技術**ユーザー協会**であり、標準化機関ではない（NE は「勧告」）
- **「ガスグループ＝最小点火エネルギーで分類。IIC が最も危険」を是正**: 分類指標を単一の物性値に断定せず「点火のしやすさで分類」とし、「危険」ではなく「点火感度が高い」に変更（[防爆](../03-keiso/explosion-proof.md)の記述と整合）
- **数値を含む定義に正典リンクを追加**: 温度クラス（T6=85℃→[防爆照明](../02-teiatsu/lighting.md)）・SIL 1〜4（→[安全計装 SIS/SIL](../03-keiso/sis-sil.md)）・電流ループ／ループ電源 24V（→[計装基礎](../03-keiso/basics.md)）

### 正典と全数照合した結果（ずれ無しを確認した定義）

上記の是正以外の定義は、2026-08-06 に各正典ページ（[計装基礎](../03-keiso/basics.md)・[防爆](../03-keiso/explosion-proof.md)・[防爆照明](../02-teiatsu/lighting.md)・[安全計装 SIS/SIL](../03-keiso/sis-sil.md)・[絶縁管理](../05-hozen/insulation-management.md)）と突き合わせ、食い違いがないことを確認しました。

### 二次資料で一致を確認（原本未照合）

- NAMUR の組織性格（ユーザー協会）は NAMUR 公式サイトの自己紹介文と複数の計装メーカー資料で一致を確認（定款等の原文は未照合）
- Zone 0/1/2・防爆構造記号（Ex d/e/ia/ib）・温度クラスの各定義は IEC 60079 系規格の原本未照合（本Wiki内の照合状態は[防爆](../03-keiso/explosion-proof.md)・[防爆照明](../02-teiatsu/lighting.md)の根拠節による）

### 限界の明示

- 英語表記・略語は現場・メーカーで揺れがある（例: 漏電遮断器の ELCB/RCCB/ELB、短絡電流の Is/Isc）。本表は代表的な表記であり、図面・仕様書では**その文書の凡例・定義**が優先
- 本表の1行定義は入口であり、設計・判定に使う数値はリンク先の正典で確認すること

### 正典参照

| 項目 | 正典 |
|---|---|
| 4-20mA・HART・フィールドバスの数値 | [計装基礎](../03-keiso/basics.md) |
| 防爆構造・ガスグループ・Zone | [防爆](../03-keiso/explosion-proof.md) |
| 温度クラスと最高表面温度の対応表 | [防爆照明](../02-teiatsu/lighting.md) |
| SIL・安全計装 | [安全計装 SIS/SIL](../03-keiso/sis-sil.md) |
| 絶縁抵抗の法定値・実務管理値 | [絶縁管理](../05-hozen/insulation-management.md) |
| 用語の根拠となる規格の一覧 | [規格一覧](standards-list.md) |

照合日: 2026-08-06（電技省令第1条の定義を e-Gov 法令 API で逐語照合、全定義を上記正典ページと突き合わせ）。

## 関連ページ

- [規格一覧](standards-list.md) — 用語の根拠となる規格を引く
- [読む順番ガイド](../getting-started.md) — 初めての人はここから
- [リファレンス](index.md) — 他の参照資料へ
