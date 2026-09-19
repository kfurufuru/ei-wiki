#!/usr/bin/env python3
"""法令改正の見張り（イベント起動の再検証トリガ）

本 Wiki が条文リンクで引用している法令について、e-Gov 法令 API v2 が返す
`law_revision_id` を `scripts/law_revisions.json` に記録した値と突き合わせる。
値が変われば**その法令が改正された**ということなので、引用しているページを
re-verify する必要がある。変化があれば exit 1。

なぜ要るか（2026-09-19 追加）:
  鮮度監査（check_last_verified.py）はカレンダー起動で、法令が改正されても
  日付が来るまで気づかない。逆に改正が無い間は何度見ても結果が同じで空振りする。
  **法令アンカーのページに必要なのはカレンダーではなくイベント**なので、
  改正を直接検出するこのスクリプトを置き、鮮度監査の既定間隔を 730 日へ延ばした。
  この 2 本はセットで、片方だけ外すと監視に穴が空く。

使い方:
  python scripts/check_law_revisions.py            # 照合（変化があれば exit 1）
  python scripts/check_law_revisions.py --self-test # 検出器の生存証明
  python scripts/check_law_revisions.py --update    # 現在値で JSON を更新（再検証した後に実行）

外部依存なし（標準ライブラリのみ）。ネットワークに出られない環境では
--offline で JSON の自己整合性だけを検査する。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://laws.e-gov.go.jp/api/2/laws?law_id={}"
TIMEOUT = 30


def manifest_path() -> Path:
    return Path(__file__).parent / "law_revisions.json"


def load() -> dict:
    return json.loads(manifest_path().read_text(encoding="utf-8"))


def fetch(law_id: str) -> dict:
    with urllib.request.urlopen(API.format(law_id), timeout=TIMEOUT) as r:
        d = json.load(r)
    laws = d.get("laws") or []
    if not laws:
        raise RuntimeError(f"{law_id}: e-Gov が法令を返さない（廃止・ID 変更の疑い）")
    return laws[0]["revision_info"]


def scan_docs() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """docs の中の e-Gov リンクから (法令ID -> アンカー集合, 法令ID -> 引用ページ集合) を集める。"""
    root = Path(__file__).resolve().parent.parent / "docs"
    used: dict[str, set[str]] = {}
    pages: dict[str, set[str]] = {}
    pat = re.compile(r"laws\.e-gov\.go\.jp/law/(\w+)#([\w-]+)")
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root.parent).as_posix()
        for law, anc in pat.findall(md.read_text(encoding="utf-8")):
            used.setdefault(law, set()).add(anc)
            pages.setdefault(law, set()).add(rel)
    return used, pages


def check_offline(data: dict) -> list[str]:
    """JSON 自体の壊れと、docs のアンカーが記録と食い違っていないかを検出する。

    アンカー照合を入れた理由（2026-09-19）:
      条アンカー（例 Mp-Ch_3-Se_1-At_58）は法令 XML の章・節・款から算出する必要があり、
      手で書くと静かに間違える（実際に第26条・第38条で Se_5 と誤記した）。誤ったアンカーでも
      リンクは開くため、読者はページ先頭に飛ばされるだけで気づかない。記録済みの正しい値と
      突き合わせて、新規・変更されたアンカーを必ず人の目に出す。
    """
    problems: list[str] = []
    laws = data.get("laws") or {}
    if not laws:
        problems.append("laws が空。JSON が壊れると全法令が無検査になる")
    for lid, v in laws.items():
        for key in ("title", "revision_id", "amendment_enforcement_date", "pages", "anchors"):
            if v.get(key) is None:
                problems.append(f"{lid}: {key} が無い")
        if not str(v.get("revision_id", "")).startswith(lid):
            problems.append(f"{lid}: revision_id が law_id で始まっていない（{v.get('revision_id')}）")
        for anc in v.get("anchors") or []:
            if not anc.startswith("Mp-") or "At_" not in anc:
                problems.append(f"{lid}: アンカー書式が不正（{anc}）")

    used, pages = scan_docs()
    for lid in sorted(used):
        if lid not in laws:
            problems.append(
                f"{lid}: docs が引用しているのに本 JSON に無い"
                f"（{'・'.join(sorted(pages[lid])[:3])} ほか）。--update で登録すること"
            )
            continue
        known = set(laws[lid].get("anchors") or [])
        for anc in sorted(used[lid] - known):
            problems.append(
                f"{lid}: 未記録のアンカー {anc}"
                f"（{'・'.join(sorted(p for p in pages[lid])[:2])}）。"
                "法令 XML の章・節・款から算出した値か確認し、正しければ --update で記録すること"
            )
    return problems


def self_test() -> int:
    """陽性対照: revision_id を1文字変えた法令を必ず検出できること。"""
    data = load()
    failures = check_offline(data)
    if failures:
        for f in failures:
            print(f"[FAIL] JSON 自己検査: {f}")
        print("[NG] self-test: JSON が壊れている")
        return 1

    lid = sorted(data["laws"])[0]
    stored = data["laws"][lid]["revision_id"]
    tampered = stored[:-1] + ("0" if stored[-1] != "0" else "1")
    if tampered == stored:
        print("[NG] self-test: 陽性対照を作れなかった")
        return 1
    if not _differs(tampered, stored):
        print(f"[FAIL] 陽性対照 {lid}: 改ざんした revision_id を検出できない（検出器故障）")
        print("[NG] self-test: 検出器故障")
        return 1

    print(
        f"[OK] self-test: 法令 {len(data['laws'])} 件・"
        f"アンカー {sum(len(v.get('anchors') or []) for v in data['laws'].values())} 件・"
        f"引用ページ {sum(len(v['pages']) for v in data['laws'].values())} 件、"
        "陽性対照（revision_id 改ざん）を検出、JSON 自己検査＋docs アンカー照合パス"
    )
    return 0


def _differs(current: str, stored: str) -> bool:
    return current != stored


def main() -> int:
    ap = argparse.ArgumentParser(description="法令改正の見張り")
    ap.add_argument("--self-test", action="store_true", help="検出器の生存証明")
    ap.add_argument("--offline", action="store_true", help="通信せず JSON の自己整合性のみ検査")
    ap.add_argument("--update", action="store_true", help="現在値で JSON を更新（再検証後に実行）")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    data = load()
    problems = check_offline(data)
    if problems:
        for p in problems:
            print(f"[FAIL] JSON 自己検査: {p}")
        return 1
    if args.offline:
        print(f"[OK] offline: JSON 自己整合性 {len(data['laws'])} 件パス（改正の照合はしていません）")
        return 0

    changed: list[tuple[str, dict, dict]] = []
    errors: list[str] = []
    for lid, v in sorted(data["laws"].items()):
        try:
            cur = fetch(lid)
        except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
            errors.append(f"{lid}（{v['title']}）: 取得失敗 {e}")
            continue
        if _differs(cur["law_revision_id"], v["revision_id"]):
            changed.append((lid, v, cur))

    if errors:
        print("==== 取得できなかった法令 ====")
        for e in errors:
            print(f"  [FAIL] {e}")

    if changed:
        print("==== 改正を検出しました（引用ページの再検証が要ります） ====")
        for lid, old, cur in changed:
            print(f"\n■ {old['title']}（{lid}）")
            print(f"  記録: {old['revision_id']}  施行 {old['amendment_enforcement_date']}")
            print(f"  現在: {cur['law_revision_id']}  施行 {cur['amendment_enforcement_date']}")
            print(f"  改正: {cur.get('amendment_law_title') or '(不明)'}")
            print(f"  再検証するページ（{len(old['pages'])} 件）:")
            for p in old["pages"]:
                print(f"    - {p}")
        print(
            "\n対応: 引用している条文を改正後の本文で照合し直し、"
            "変わっていれば本文を是正して last_verified を更新する。"
            "確認が済んだら `--update` で本 JSON を現在値に進める。"
        )

    if changed or errors:
        return 1

    print(
        f"[OK] 法令 {len(data['laws'])} 件・引用ページ "
        f"{sum(len(v['pages']) for v in data['laws'].values())} 件、"
        f"改正なし（前回記録 {data.get('checked')}）"
    )
    return 0


def update() -> int:
    data = load()
    for lid, v in sorted(data["laws"].items()):
        cur = fetch(lid)
        v["revision_id"] = cur["law_revision_id"]
        v["amendment_enforcement_date"] = cur["amendment_enforcement_date"]
        v["title"] = cur["law_title"]
    data["checked"] = _dt.date.today().isoformat()
    manifest_path().write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"[OK] {len(data['laws'])} 件を現在値に更新（checked={data['checked']}）")
    return 0


if __name__ == "__main__":
    if "--update" in sys.argv:
        raise SystemExit(update())
    raise SystemExit(main())
