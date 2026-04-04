---
title: 読む順番ガイド
description: 経験レベル別に「何から読むか」を示すナビゲーションページ。OJT初日から中堅まで対応。
tags:
  - ガイド
  - 入門
  - ナビゲーション
audience:
  - 新入社員・派遣（電気計装ほぼ未経験）
  - 中堅・転換配属（電気OK・計装弱め）
  - 実務経験者（設計・電験対策も視野）
---

# 読む順番ガイド

このページは「どのページを、どの順番で読むか」を示すナビゲーションです。
自分の経験レベルに合ったタブを選んで、上から順に読み進めてください。
すべてを読む必要はありません。**今の仕事に必要なところから始めるのが正解です。**

---

=== "Lv.1 電気計装がほぼ初めての人"

    派遣・新入社員・他職種からの転換配属で「電気も計装もほぼゼロ」という方向けです。
    最初の3ヶ月でここまで読めれば十分です。

    ---

    ### Step 1 — まず読む（1〜2週目）

    現場で最低限の会話ができるようになるための3本柱。

    <div class="grid cards" markdown>

    - :fontawesome-solid-gauge: **計装の基礎**

        ---

        センサー・信号・ループの考え方。「計装とは何か」の出発点。

        [:octicons-arrow-right-24: 03-keiso/basics.md](03-keiso/basics.md)

    - :fontawesome-solid-plug: **低圧配電の基礎**

        ---

        動力盤・分電盤・ブレーカーの役割と読み方。

        [:octicons-arrow-right-24: 02-teiatsu/distribution.md](02-teiatsu/distribution.md)

    - :fontawesome-solid-screwdriver-wrench: **保全体系の概要**

        ---

        PM・CBM・BM の違い。現場での保全の考え方。

        [:octicons-arrow-right-24: 05-hozen/maintenance-system.md](05-hozen/maintenance-system.md)

    </div>

    ---

    ### Step 2 — 次に読む（1〜2ヶ月目）

    日常点検・設備操作に必要な知識。

    <div class="grid cards" markdown>

    - :fontawesome-solid-rotate: **モーター制御**

        ---

        スターデルタ・インバーター・保護回路の基本。

        [:octicons-arrow-right-24: 02-teiatsu/motor-control.md](02-teiatsu/motor-control.md)

    - :fontawesome-solid-clipboard-check: **定期点検の進め方**

        ---

        点検手順・チェックシート・絶縁測定の読み方。

        [:octicons-arrow-right-24: 05-hozen/periodic-inspection.md](05-hozen/periodic-inspection.md)

    </div>

    ---

    ### Step 3 — トラブル対応を覚える前に（2〜3ヶ月目）

    !!! warning "いきなりトラブルシューティングに入らないこと"
        原因を知らないまま対処法だけ覚えても応用が利きません。
        Step 1・2 を終えてからここへ来てください。

    <div class="grid cards" markdown>

    - :fontawesome-solid-triangle-exclamation: **トラブル対応の基本**

        ---

        現象の切り分け方・記録の書き方・エスカレーションの判断基準。

        [:octicons-arrow-right-24: 06-trouble/basics.md](06-trouble/basics.md)

    </div>

    ---

    !!! tip "3ヶ月の目安"
        Step 1〜3 を一通り読み終えたら、次のステップとして **Lv.2 の計装パート** に進むか、
        日々のトラブル記録を見ながら [06-trouble/](06-trouble/index.md) を深掘りしていくのがおすすめです。

=== "Lv.2 計装が弱い人（電気はOK）"

    電気系の経験はあるが計装（センサー・信号・制御弁・DCS）が手薄な方向けです。
    電気の基礎は読み飛ばして、計装に集中してください。

    ---

    ### 優先度 高（まずここから）

    <div class="grid cards" markdown>

    - :fontawesome-solid-gauge: **計装の基礎**

        ---

        4-20mA / HART / フィールドバスの考え方を整理する。

        [:octicons-arrow-right-24: 03-keiso/basics.md](03-keiso/basics.md)

    - :fontawesome-solid-signal: **計装信号トラブル（4-20mA）**

        ---

        断線・ノイズ・ループ電源の切り分け手順。現場で一番使う。

        [:octicons-arrow-right-24: 06-trouble/signal.md](06-trouble/signal.md)

    - :fontawesome-solid-faucet: **制御弁**

        ---

        空気作動弁・電動弁の構造・ポジショナー・キャリブレーション。

        [:octicons-arrow-right-24: 03-keiso/control-valve.md](03-keiso/control-valve.md)

    - :fontawesome-solid-sliders: **PID制御**

        ---

        比例・積分・微分の意味とチューニングの考え方。

        [:octicons-arrow-right-24: 03-keiso/pid.md](03-keiso/pid.md)

    </div>

    ---

    ### 深掘り（余裕ができたら）

    <div class="grid cards" markdown>

    - :fontawesome-solid-server: **DCS の基礎**

        ---

        I/O カード・コントローラー・冗長構成の概念。

        [:octicons-arrow-right-24: 03-keiso/dcs.md](03-keiso/dcs.md)

    - :fontawesome-solid-shield-halved: **防爆の基礎**

        ---

        Ex 区分・機器選定・配線ルールの要点。設備改造時に必須。

        [:octicons-arrow-right-24: 03-keiso/explosion-proof.md](03-keiso/explosion-proof.md)

    </div>

    ---

    ### 設計視点を持つ

    <div class="grid cards" markdown>

    - :fontawesome-solid-file-lines: **仕様書の書き方**

        ---

        計装仕様書（データシート）の構成と記入ポイント。

        [:octicons-arrow-right-24: 04-sekkei/spec-writing.md](04-sekkei/spec-writing.md)

    </div>

=== "Lv.3 設計・電験対策も視野に"

    実務経験があり、設備設計・法規対応・電験3種取得を目指している方向けです。

    ---

    ### 設計全般

    <div class="grid cards" markdown>

    - :fontawesome-solid-drafting-compass: **設計セクション トップ**

        ---

        図面体系・設備投資フロー・メーカー選定の流れを俯瞰する。

        [:octicons-arrow-right-24: 04-sekkei/index.md](04-sekkei/index.md)

    </div>

    ---

    ### 計算系（電験・設計共通）

    <div class="grid cards" markdown>

    - :fontawesome-solid-calculator: **負荷計算**

        ---

        需要率・力率・変圧器容量の計算手順。

        [:octicons-arrow-right-24: 04-sekkei/load-calc.md](04-sekkei/load-calc.md)

    - :fontawesome-solid-bolt: **短絡電流計算**

        ---

        %インピーダンス法・遮断器選定への接続。

        [:octicons-arrow-right-24: 04-sekkei/fault-current.md](04-sekkei/fault-current.md)

    - :fontawesome-solid-arrow-trend-down: **電圧降下計算**

        ---

        ケーブルサイズ選定と電圧降下の許容値の考え方。

        [:octicons-arrow-right-24: 04-sekkei/voltage-drop.md](04-sekkei/voltage-drop.md)

    </div>

    ---

    ### 法規対応

    !!! info "当工場固有の規制を含みます"
        石油コンビナート法対応は当工場製造所固有の運用です。
        他拠点の方は規格一覧のみ参照してください。

    <div class="grid cards" markdown>

    - :fontawesome-solid-book: **規格一覧**

        ---

        JIS・JEC・NECA・IEC の適用範囲まとめ。

        [:octicons-arrow-right-24: reference/standards-list.md](reference/standards-list.md)

    - :fontawesome-solid-industry: **石油コンビナート法対応**

        ---

        特定防災施設・電気設備の届出・検査ポイント。

        [:octicons-arrow-right-24: 04-sekkei/standards.md](04-sekkei/standards.md)

    </div>

---

## 困ったときは

「症状から調べたい」「用語の意味を確認したい」場合は逆引きインデックスを使ってください。

| 目的 | リンク |
|------|--------|
| 症状・現象から原因を探す | [トラブル逆引き](06-trouble/index.md) |
| 用語・略語を調べる | [用語集](reference/glossary.md) |
| 計算ツールをすぐ使いたい | [計算ツール集](reference/calculators.md) |
| 規格番号で探す | [規格一覧](reference/standards-list.md) |

!!! note "このページへのフィードバック"
    「ここが分かりにくかった」「このページを先に読んでおきたかった」という気づきは
    チームリーダーまたは Wiki 管理者に伝えてください。随時改訂します。
