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
  python scripts/check_law_revisions.py --record    # docs のアンカー・引用ページを JSON に記録（revision_id は触らない）
  python scripts/check_law_revisions.py --update <法令ID>...  # 再検証が済んだ法令だけ revision_id を進める

--record と --update を分けた理由（2026-10-23・残件台帳 R24）:
  旧 --update は、案内文では「未記録アンカーを記録する」ことになっていたが、実際には
  アンカーもページも記録せず、**全法令の revision_id を現在値へ進めた**。そのため
  「アンカーを1件足したので --update」とすると、再検証が済んでいない改正（2026-10-01 の
  安衛法ほか3法令）まで黙って見張りから消えた（2026-10-22 に実際に起き、手で巻き戻した）。
  記録（日常の作業）と前進（再検証の完了宣言）は別の操作なので、別のオプションにした。
  --update は法令 ID の指定を必須にし、全件一括の前進をできなくしてある。
  --record は、記録するアンカーを現行の法令 XML の章・節・款から算出した値と照合し、
  一致しないものは記録しない（R22: 誤ったアンカーでもリンクは開くので、人の目では気づけない）。

外部依存なし（標準ライブラリのみ）。ネットワークに出られない環境では
--offline で JSON の自己整合性だけを検査する。
"""
from __future__ import annotations

import argparse
import base64
import copy
import datetime as _dt
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "https://laws.e-gov.go.jp/api/2/laws?law_id={}"
API_DATA = "https://laws.e-gov.go.jp/api/2/law_data/{}?law_full_text_format=xml"

# 法令 XML の階層要素 → e-Gov のアンカー部品。条（Article）の上にあるものだけを辿る。
_ANCHOR_PARTS = {"Part": "Pa", "Chapter": "Ch", "Section": "Se", "Subsection": "Ss", "Division": "Di"}
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


def fetch_xml(law_id: str) -> bytes:
    """現行の法令本文 XML。API v2 は JSON の law_full_text に base64 で入れて返す。"""
    with urllib.request.urlopen(API_DATA.format(law_id), timeout=TIMEOUT) as r:
        d = json.load(r)
    return base64.b64decode(d["law_full_text"])


def xml_anchors(xml_bytes: bytes) -> set[str]:
    """本則（MainProvision）の全条について、e-Gov の条アンカーを算出する。

    例: 第5章第1節の第44条の2 → Mp-Ch_5-Se_1-At_44_2、章の無い法令の第14条の2 → Mp-At_14_2。
    取得元は e-Gov（政府の API）で、外部実体を含まないので標準の ElementTree で読む。
    """
    out: set[str] = set()

    def walk(elem, path: list[str]) -> None:
        for child in elem:
            num = child.get("Num")
            if child.tag == "Article":
                out.add("-".join(["Mp", *path, f"At_{num}"]))
            elif child.tag in _ANCHOR_PARTS:
                walk(child, [*path, f"{_ANCHOR_PARTS[child.tag]}_{num}"])
            else:
                walk(child, path)

    mp = ET.fromstring(xml_bytes).find(".//MainProvision")
    if mp is None:
        raise RuntimeError("法令 XML に MainProvision が無い")
    walk(mp, [])
    return out


def plan_record(data: dict, used: dict, pages: dict, anchors_of, revinfo_of) -> tuple[dict, list[str], list[str]]:
    """--record の中身。通信は anchors_of / revinfo_of に委ね、self-test で偽物を差し込めるようにする。

    返り値: (書き込む JSON, 報告行, 拒否したアンカー)。既存法令の revision_id は**決して変えない**。
    """
    new = copy.deepcopy(data)
    laws = new.setdefault("laws", {})
    report: list[str] = []
    rejected: list[str] = []
    for lid in sorted(used):
        entry = laws.get(lid)
        known = set(entry.get("anchors") or []) if entry else set()
        to_add = used[lid] - known
        valid = anchors_of(lid) if to_add else set()
        bad = sorted(to_add - valid)
        rejected += [f"{lid}: {a}（{'・'.join(sorted(pages[lid])[:2])}）" for a in bad]
        good = sorted(to_add & valid)
        if entry is None:
            info = revinfo_of(lid)
            entry = laws[lid] = {
                "title": info["law_title"],
                "revision_id": info["law_revision_id"],
                "amendment_enforcement_date": info["amendment_enforcement_date"],
                "pages": [],
                "anchors": [],
            }
            report.append(f"新規登録 {lid}（{entry['title']}）: 現行の版 {entry['revision_id']} を基準にする")
        entry["anchors"] = sorted(known | set(good))
        if good:
            report.append(f"アンカー追加 {lid}（{entry['title']}）: {', '.join(good)}")
        if sorted(pages[lid]) != entry.get("pages"):
            report.append(f"引用ページ更新 {lid}（{entry['title']}）: {len(entry.get('pages') or [])} → {len(pages[lid])} 件")
            entry["pages"] = sorted(pages[lid])
    for lid in sorted(set(laws) - set(used)):
        report.append(f"注意 {lid}（{laws[lid]['title']}）: docs から引用が無くなった（記録は残す）")
    return new, report, rejected


def plan_update(data: dict, ids: list[str], revinfo_of) -> tuple[dict, list[str]]:
    """--update の中身。指定した法令の revision_id だけを進める。ID なし・未登録 ID は ValueError。"""
    if not ids:
        raise ValueError("法令 ID を指定してください（全件一括の前進はできません）")
    unknown = [i for i in ids if i not in (data.get("laws") or {})]
    if unknown:
        raise ValueError(f"JSON に無い法令 ID: {', '.join(unknown)}（新しい法令は --record で登録する）")
    new = copy.deepcopy(data)
    report: list[str] = []
    advanced = False
    for lid in ids:
        v, cur = new["laws"][lid], revinfo_of(lid)
        if v["revision_id"] == cur["law_revision_id"]:
            report.append(f"変化なし {lid}（{v['title']}）: {v['revision_id']}")
            continue
        report.append(f"前進 {lid}（{v['title']}）: {v['revision_id']} → {cur['law_revision_id']}")
        v["revision_id"] = cur["law_revision_id"]
        v["amendment_enforcement_date"] = cur["amendment_enforcement_date"]
        v["title"] = cur["law_title"]
        advanced = True
    if advanced:
        # checked は「最後に見張りの基準を進めた日」。何も進めていないのに日付だけ動かさない
        new["checked"] = _dt.date.today().isoformat()
    return new, report


def save(data: dict) -> None:
    manifest_path().write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


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
                f"（{'・'.join(sorted(pages[lid])[:3])} ほか）。--record で登録すること"
            )
            continue
        known = set(laws[lid].get("anchors") or [])
        for anc in sorted(used[lid] - known):
            problems.append(
                f"{lid}: 未記録のアンカー {anc}"
                f"（{'・'.join(sorted(p for p in pages[lid])[:2])}）。"
                "--record で記録すること（現行の法令 XML から算出した値と一致しないアンカーは記録を拒否する）"
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

    # R24 の陽性対照（通信しない）。偽の法令 XML と revision_info を差し込む。
    fake_xml = (
        "<Law><LawBody><MainProvision><Chapter Num=\"5\"><Section Num=\"1\">"
        "<Article Num=\"44_2\"/></Section></Chapter><Article Num=\"9\"/>"
        "</MainProvision></LawBody></Law>"
    ).encode("utf-8")
    if xml_anchors(fake_xml) != {"Mp-Ch_5-Se_1-At_44_2", "Mp-At_9"}:
        print(f"[FAIL] アンカー算出が壊れている: {sorted(xml_anchors(fake_xml))}")
        return 1
    fake_info = {"law_title": "偽法令", "law_revision_id": "X_NEW", "amendment_enforcement_date": "2099-01-01"}
    probe = {"laws": {lid: copy.deepcopy(data["laws"][lid])}}
    used = {lid: {"Mp-Ch_5-Se_1-At_44_2", "Mp-Ch_9-At_44_2"}, "NEWLAW": {"Mp-At_9"}}
    pg = {lid: {"docs/a.md"}, "NEWLAW": {"docs/b.md"}}
    rec, _, rejected = plan_record(probe, used, pg, lambda _l: xml_anchors(fake_xml), lambda _l: fake_info)
    if rec["laws"][lid]["revision_id"] != stored:
        print("[FAIL] --record が既存法令の revision_id を変えた（R24 の再発）")
        return 1
    if "Mp-Ch_5-Se_1-At_44_2" not in rec["laws"][lid]["anchors"] or "Mp-Ch_9-At_44_2" in rec["laws"][lid]["anchors"]:
        print("[FAIL] --record が正しいアンカーを記録しない、または XML に無いアンカーを記録した")
        return 1
    if not any("Mp-Ch_9-At_44_2" in r for r in rejected):
        print("[FAIL] --record が XML に無いアンカーを拒否として報告しない")
        return 1
    if rec["laws"].get("NEWLAW", {}).get("revision_id") != "X_NEW":
        print("[FAIL] --record が未登録の法令を登録しない")
        return 1
    try:
        plan_update(probe, [], lambda _l: fake_info)
        print("[FAIL] 法令 ID なしの --update が通った（全件一括の前進＝R24 の再発）")
        return 1
    except ValueError:
        pass
    two = {"laws": {k: copy.deepcopy(data["laws"][k]) for k in sorted(data["laws"])[:2]}}
    a, b = sorted(two["laws"])
    upd, _ = plan_update(two, [a], lambda _l: fake_info)
    if upd["laws"][a]["revision_id"] != "X_NEW" or upd["laws"][b]["revision_id"] != two["laws"][b]["revision_id"]:
        print("[FAIL] --update が指定外の法令を進めた、または指定した法令を進めない")
        return 1

    print(
        f"[OK] self-test: 法令 {len(data['laws'])} 件・"
        f"アンカー {sum(len(v.get('anchors') or []) for v in data['laws'].values())} 件・"
        f"引用ページ {sum(len(v['pages']) for v in data['laws'].values())} 件、"
        "陽性対照（revision_id 改ざん）を検出、JSON 自己検査＋docs アンカー照合パス、"
        "--record／--update の陽性対照 6 件パス（revision_id 不変・XML 外アンカー拒否・新規登録・"
        "ID なし拒否・指定外を進めない・アンカー算出）"
    )
    return 0


def _differs(current: str, stored: str) -> bool:
    return current != stored


def main() -> int:
    ap = argparse.ArgumentParser(description="法令改正の見張り")
    ap.add_argument("--self-test", action="store_true", help="検出器の生存証明")
    ap.add_argument("--offline", action="store_true", help="通信せず JSON の自己整合性のみ検査")
    ap.add_argument("--record", action="store_true",
                    help="docs のアンカー・引用ページを JSON に記録（revision_id は触らない）")
    ap.add_argument("--update", nargs="*", metavar="LAW_ID",
                    help="再検証が済んだ法令の revision_id だけを現在値へ進める（法令 ID の指定が必須）")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.record:
        return record()
    if args.update is not None:
        return update(args.update)

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
            "確認が済んだ法令だけを `--update <法令ID>` で現在値に進める"
            f"（今回の候補: {' '.join(lid for lid, _, _ in changed)}）。"
        )

    if changed or errors:
        return 1

    print(
        f"[OK] 法令 {len(data['laws'])} 件・引用ページ "
        f"{sum(len(v['pages']) for v in data['laws'].values())} 件、"
        f"改正なし（前回記録 {data.get('checked')}）"
    )
    return 0


def record() -> int:
    """docs のアンカー・引用ページを記録する。アンカーは現行 XML と一致したものだけ。"""
    data = load()
    used, pages = scan_docs()
    cache: dict[str, set[str]] = {}

    def anchors_of(lid: str) -> set[str]:
        if lid not in cache:
            cache[lid] = xml_anchors(fetch_xml(lid))
        return cache[lid]

    new, report, rejected = plan_record(data, used, pages, anchors_of, fetch)
    for r in report:
        print(f"  {r}")
    if rejected:
        print("[FAIL] 現行の法令 XML に無いアンカーがあるため、その分は記録しませんでした（docs 側を直す）:")
        for r in rejected:
            print(f"  - {r}")
    if new != data:
        save(new)
        print(f"[OK] 記録しました（revision_id は変えていません）。e-Gov から XML を取得した法令 {len(cache)} 件")
    else:
        print("[OK] 記録の変更なし")
    return 1 if rejected else 0


def update(ids: list[str]) -> int:
    """指定した法令の revision_id だけを進める。ID なしなら改正中の法令を示して止まる。"""
    data = load()
    try:
        new, report = plan_update(data, ids, fetch)
    except ValueError as e:
        print(f"[NG] --update: {e}")
        if not ids:
            pending = [lid for lid, v in sorted(data["laws"].items())
                       if _differs(fetch(lid)["law_revision_id"], v["revision_id"])]
            print("  改正を検出中の法令: " + (" ".join(pending) if pending else "なし"))
            print("  引用ページの再検証が済んだものだけを指定してください。JSON は書き換えていません。")
        return 2
    for r in report:
        print(f"  {r}")
    if new != data:
        save(new)
    print(f"[OK] 指定した {len(ids)} 件を処理（checked={new.get('checked')}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
