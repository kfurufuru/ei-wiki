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
import os
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


def plan_record(data: dict, used: dict, pages: dict, anchor_pages: dict, anchors_of, revinfo_of):
    """--record の中身。通信は anchors_of / revinfo_of に委ねる（self-test で偽物を差し込む）。

    docs が使う**全**アンカーを現行 XML と照合する（新しく足した分だけでなく、記録済みの分も）。
    記録済みでも現行 XML に無くなったものは記録から外し、拒否として報告する。こうすると
    以後の本走査・--offline が「未記録のアンカー」として赤くし続けるので、黙って緑にならない。
    返り値: (書き込む JSON, 報告行, 拒否したアンカー)。既存法令の revision_id は**決して変えない**。
    """
    new = copy.deepcopy(data)
    laws = new.setdefault("laws", {})
    report: list[str] = []
    rejected: list[str] = []
    for lid in sorted(used):
        entry = laws.get(lid)
        known = set(entry.get("anchors") or []) if entry else set()
        valid = anchors_of(lid)
        for a in sorted(used[lid] - valid):
            rejected.append(f"{lid}: {a}（{'・'.join(sorted(anchor_pages[(lid, a)]))}）")
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
        anchors = (known | used[lid]) & valid
        added, dropped = sorted(anchors - known), sorted(known - anchors)
        if added:
            report.append(f"アンカー追加 {lid}（{entry['title']}）: {', '.join(added)}")
        if dropped:
            report.append(f"アンカー削除 {lid}（{entry['title']}）: 現行 XML に無い {', '.join(dropped)}")
        entry["anchors"] = sorted(anchors)
        if sorted(pages[lid]) != entry.get("pages"):
            report.append(f"引用ページ更新 {lid}（{entry['title']}）: {len(entry.get('pages') or [])} → {len(pages[lid])} 件")
            entry["pages"] = sorted(pages[lid])
    for lid in sorted(set(laws) - set(used)):
        report.append(f"注意 {lid}（{laws[lid]['title']}）: docs から引用が無くなった（記録は残す）")
    return new, report, rejected


def plan_update(data: dict, ids: list[str], used: dict, revinfo_of, anchors_of):
    """--update の中身。指定した法令の revision_id だけを進める。ID なし・未登録 ID は ValueError。

    進める法令は、記録済みと docs のアンカーを**進め先の版（現行）の XML** で照合し、1件でも
    無ければ進めない（改正で章・節が繰り下がると、旧版で正しかったアンカーが実在しなくなる）。
    返り値: (書き込む JSON, 報告行, 進めなかった法令の理由)。
    """
    if not ids:
        raise ValueError("法令 ID を指定してください（全件一括の前進はできません）")
    unknown = [i for i in ids if i not in (data.get("laws") or {})]
    if unknown:
        raise ValueError(f"JSON に無い法令 ID: {', '.join(unknown)}（新しい法令は --record で登録する）")
    new = copy.deepcopy(data)
    report: list[str] = []
    blocked: list[str] = []
    advanced = False
    for lid in ids:
        v, cur = new["laws"][lid], revinfo_of(lid)
        if v["revision_id"] == cur["law_revision_id"]:
            report.append(f"変化なし {lid}（{v['title']}）: {v['revision_id']}")
            continue
        missing = sorted((set(v.get("anchors") or []) | used.get(lid, set())) - anchors_of(lid))
        if missing:
            blocked.append(f"{lid}（{v['title']}）: 進め先の版 {cur['law_revision_id']} に無いアンカー {', '.join(missing)}")
            continue
        report.append(f"前進 {lid}（{v['title']}）: {v['revision_id']} → {cur['law_revision_id']}")
        v["revision_id"] = cur["law_revision_id"]
        v["amendment_enforcement_date"] = cur["amendment_enforcement_date"]
        v["title"] = cur["law_title"]
        advanced = True
    if advanced:
        # checked は「最後に見張りの基準を進めた日」。何も進めていないのに日付だけ動かさない
        new["checked"] = _dt.date.today().isoformat()
    return new, report, blocked


def save(data: dict) -> None:
    """一時ファイルに書いてから置き換える。書き込み途中の失敗で JSON が切れて壊れないように。"""
    path = manifest_path()
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def scan_docs():
    """docs の e-Gov リンクから (法令ID→アンカー集合, 法令ID→引用ページ集合, (法令ID, アンカー)→ページ集合) を集める。

    アンカーの文字に `:` を含める（範囲で削除された条は Num が「323:324」の形になる）。
    """
    root = Path(__file__).resolve().parent.parent / "docs"
    used: dict[str, set[str]] = {}
    pages: dict[str, set[str]] = {}
    anchor_pages: dict[tuple[str, str], set[str]] = {}
    pat = re.compile(r"laws\.e-gov\.go\.jp/law/(\w+)#([\w:-]+)")
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root.parent).as_posix()
        for law, anc in pat.findall(md.read_text(encoding="utf-8")):
            used.setdefault(law, set()).add(anc)
            pages.setdefault(law, set()).add(rel)
            anchor_pages.setdefault((law, anc), set()).add(rel)
    return used, pages, anchor_pages


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

    used, pages, anchor_pages = scan_docs()
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
                f"{lid}: 未記録のアンカー {anc}（{'・'.join(sorted(anchor_pages[(lid, anc)]))}）。"
                "--record で記録すること（現行の法令 XML から算出した値と一致しないアンカーは記録を拒否する）"
            )
    return problems


# ---------------------------------------------------------------------------
# self-test 用の偽の世界（通信もファイル書き込みもしない）
# ---------------------------------------------------------------------------
_FAKE_XML = (
    '<Law><LawBody><MainProvision>'
    '<Part Num="1"><Chapter Num="2"><Section Num="3"><Subsection Num="4"><Division Num="5">'
    '<Article Num="6"/></Division></Subsection></Section></Chapter></Part>'
    '<Chapter Num="5"><Section Num="1"><Article Num="44_2"/><Article Num="323:324"/></Section></Chapter>'
    '<Article Num="9"/>'
    '</MainProvision><SupplProvision><Article Num="1"/></SupplProvision></LawBody></Law>'
).encode("utf-8")
_FAKE_XML_ANCHORS = {
    "Mp-Pa_1-Ch_2-Se_3-Ss_4-Di_5-At_6", "Mp-Ch_5-Se_1-At_44_2", "Mp-Ch_5-Se_1-At_323:324", "Mp-At_9",
}


def _fake_world(xml: bytes, used: dict, anchor_pages: dict):
    """main() を偽の load/save/fetch/fetch_xml/scan_docs で動かす。saved に書き込み内容が残る。"""
    data = {
        "checked": "2000-01-01",
        "laws": {
            "A": {"title": "法令A", "revision_id": "A_OLD", "amendment_enforcement_date": "2000-01-01",
                  "pages": ["docs/a.md"], "anchors": ["Mp-Ch_5-Se_1-At_44_2", "Mp-At_9"]},
            "B": {"title": "法令B", "revision_id": "B_CUR", "amendment_enforcement_date": "2000-01-01",
                  "pages": ["docs/b.md"], "anchors": ["Mp-At_9"]},
        },
    }
    info = {"A": "A_NEW", "B": "B_CUR", "N": "N_1"}
    pages: dict[str, set[str]] = {}
    for (lid, _a), ps in anchor_pages.items():
        pages.setdefault(lid, set()).update(ps)
    saved: list[dict] = []
    fakes = {
        "load": lambda: copy.deepcopy(data),
        "save": lambda d: saved.append(copy.deepcopy(d)),
        "fetch": lambda lid: {"law_title": f"法令{lid}", "law_revision_id": info[lid],
                              "amendment_enforcement_date": "2099-01-01"},
        "fetch_xml": lambda _lid: xml,
        "scan_docs": lambda: (used, pages, anchor_pages),
    }
    return data, saved, fakes


def _run_main(argv: list[str], fakes: dict) -> int:
    """偽物を差し込んで main(argv) を実行し、出力を捨てる。終わったら必ず元に戻す。"""
    import contextlib
    import io

    g = globals()
    orig = {k: g[k] for k in fakes}
    g.update(fakes)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                return main(argv)
            except SystemExit as e:  # argparse のエラーは SystemExit(2)
                return int(e.code or 0)
    finally:
        g.update(orig)


def _r24_checks() -> list[str]:
    """R24 の陽性対照（2026-10-23）。main() から record()/update() を通す端から端までの形で確かめる。"""
    fails: list[str] = []
    if xml_anchors(_FAKE_XML) != _FAKE_XML_ANCHORS:
        fails.append(f"アンカー算出（編・章・節・款・目・附則除外・範囲条）: {sorted(xml_anchors(_FAKE_XML))}")

    # --record: A に正 1・誤 1（A は改正検出中）、新法令 N に正 1・誤 1
    used = {"A": {"Mp-Ch_5-Se_1-At_44_2", "Mp-Pa_1-Ch_2-Se_3-Ss_4-Di_5-At_6", "Mp-Ch_9-At_44_2"},
            "N": {"Mp-At_9", "Mp-At_99"}}
    ap = {("A", "Mp-Ch_5-Se_1-At_44_2"): {"docs/a.md"}, ("A", "Mp-Pa_1-Ch_2-Se_3-Ss_4-Di_5-At_6"): {"docs/a.md"},
          ("A", "Mp-Ch_9-At_44_2"): {"docs/wrong.md"}, ("N", "Mp-At_9"): {"docs/n.md"}, ("N", "Mp-At_99"): {"docs/n.md"}}
    _, saved, fk = _fake_world(_FAKE_XML, used, ap)
    rc = _run_main(["--record"], fk)
    out = saved[-1] if saved else {}
    laws = out.get("laws", {})
    if rc != 1:
        fails.append(f"--record: 誤アンカーがあるのに exit {rc}（期待 1）")
    if laws.get("A", {}).get("revision_id") != "A_OLD":
        fails.append("--record: 改正検出中の法令の revision_id を変えた（R24 の再発）")
    if laws.get("A", {}).get("anchors") != sorted(["Mp-Ch_5-Se_1-At_44_2", "Mp-Pa_1-Ch_2-Se_3-Ss_4-Di_5-At_6", "Mp-At_9"]):
        fails.append(f"--record: A のアンカー記録が想定外 {laws.get('A', {}).get('anchors')}")
    if laws.get("N", {}).get("revision_id") != "N_1" or laws.get("N", {}).get("anchors") != ["Mp-At_9"]:
        fails.append(f"--record: 新法令の登録が想定外 {laws.get('N')}")
    if laws.get("B", {}).get("revision_id") != "B_CUR":
        fails.append("--record: 引用されていない法令の revision_id を変えた")
    # 法令 A を引くページは a / aa / wrong の3つ。誤アンカーを書いたのは wrong だけ。
    used2 = {"A": {"Mp-Ch_9-At_44_2", "Mp-At_9", "Mp-Ch_5-Se_1-At_44_2"}}
    ap2 = {("A", "Mp-Ch_9-At_44_2"): {"docs/wrong.md"}, ("A", "Mp-At_9"): {"docs/a.md"},
           ("A", "Mp-Ch_5-Se_1-At_44_2"): {"docs/aa.md"}}
    _, _, fk2 = _fake_world(_FAKE_XML, used2, ap2)
    import contextlib
    import io

    buf = io.StringIO()
    g = globals()
    orig = {k: g[k] for k in fk2}
    g.update(fk2)
    try:
        with contextlib.redirect_stdout(buf):
            record()
    finally:
        g.update(orig)
    line = next((ln for ln in buf.getvalue().splitlines() if "Mp-Ch_9-At_44_2" in ln), "")
    if "docs/wrong.md" not in line or "docs/a.md" in line:
        fails.append(f"--record: 拒否の報告が誤アンカーを書いたページを指さない（{line.strip()}）")

    # --record: 記録済みでも現行 XML に無くなったアンカーは外す（以後の検査で赤くし続ける）
    stale_xml = _FAKE_XML.replace(b'<Article Num="9"/>', b"")
    _, saved3, fk3 = _fake_world(stale_xml, {"B": {"Mp-At_9"}}, {("B", "Mp-At_9"): {"docs/b.md"}})
    rc3 = _run_main(["--record"], fk3)
    if rc3 != 1 or not saved3 or "Mp-At_9" in saved3[-1]["laws"]["B"]["anchors"]:
        fails.append("--record: 現行 XML から消えた記録済みアンカーを拒否・削除しない")

    # --update
    used4 = {"A": {"Mp-Ch_5-Se_1-At_44_2"}, "B": {"Mp-At_9"}}
    ap4 = {("A", "Mp-Ch_5-Se_1-At_44_2"): {"docs/a.md"}, ("B", "Mp-At_9"): {"docs/b.md"}}
    for argv, want_rc in ((["--update"], 2), (["--update", "ZZZ"], 2), (["--update", "A", "ZZZ"], 2),
                          (["--record", "--update", "A"], 2), (["--update", "A", "--record"], 2)):
        _, s, fk = _fake_world(_FAKE_XML, used4, ap4)
        rc = _run_main(argv, fk)
        if rc != want_rc or s:
            fails.append(f"{' '.join(argv)}: exit {rc}・書き込み {len(s)} 回（期待 exit {want_rc}・書き込みなし）")
    _, s, fk = _fake_world(_FAKE_XML, used4, ap4)
    rc = _run_main(["--update", "A"], fk)
    if rc != 0 or not s or s[-1]["laws"]["A"]["revision_id"] != "A_NEW" \
            or s[-1]["laws"]["B"]["revision_id"] != "B_CUR" or s[-1]["checked"] == "2000-01-01":
        fails.append("--update A: A だけを進めて checked を更新する、にならない")
    _, s, fk = _fake_world(_FAKE_XML, used4, ap4)
    rc = _run_main(["--update", "B"], fk)
    if rc != 0 or s:
        fails.append("--update B（変化なし）: JSON を書いた（checked だけ動かしてはいけない）")
    _, s, fk = _fake_world(stale_xml, used4, ap4)
    rc = _run_main(["--update", "A"], fk)
    if rc != 1 or (s and s[-1]["laws"]["A"]["revision_id"] != "A_OLD"):
        fails.append("--update A: 進め先の版に無いアンカーがあるのに進めた")
    return fails


def self_test() -> int:
    """陽性対照: revision_id を1文字変えた法令を必ず検出できること＋R24 の端から端までの試験。"""
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

    r24 = _r24_checks()
    if r24:
        for f in r24:
            print(f"[FAIL] R24 陽性対照: {f}")
        print("[NG] self-test: --record／--update が壊れている")
        return 1

    print(
        f"[OK] self-test: 法令 {len(data['laws'])} 件・"
        f"アンカー {sum(len(v.get('anchors') or []) for v in data['laws'].values())} 件・"
        f"引用ページ {sum(len(v['pages']) for v in data['laws'].values())} 件、"
        "陽性対照（revision_id 改ざん）を検出、JSON 自己検査＋docs アンカー照合パス、"
        "--record／--update の端から端までの陽性対照パス（通信・書き込みなし）"
    )
    return 0


def _differs(current: str, stored: str) -> bool:
    return current != stored


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="法令改正の見張り")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true", help="検出器の生存証明")
    mode.add_argument("--offline", action="store_true", help="通信せず JSON の自己整合性のみ検査")
    mode.add_argument("--record", action="store_true",
                      help="docs のアンカー・引用ページを JSON に記録（revision_id は触らない）")
    mode.add_argument("--update", nargs="*", metavar="LAW_ID",
                      help="再検証が済んだ法令の revision_id だけを現在値へ進める（法令 ID の指定が必須）")
    args = ap.parse_args(argv)

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


def _anchors_cached():
    cache: dict[str, set[str]] = {}

    def anchors_of(lid: str) -> set[str]:
        if lid not in cache:
            cache[lid] = xml_anchors(fetch_xml(lid))
        return cache[lid]

    return anchors_of, cache


def record() -> int:
    """docs のアンカー・引用ページを記録する。アンカーは現行 XML と一致したものだけ。"""
    data = load()
    used, pages, anchor_pages = scan_docs()
    anchors_of, cache = _anchors_cached()
    new, report, rejected = plan_record(data, used, pages, anchor_pages, anchors_of, fetch)
    for r in report:
        print(f"  {r}")
    if rejected:
        print("[FAIL] 現行の法令 XML に無いアンカーがあります。記録しませんでした（docs 側のリンクを直す）:")
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
    used, _pages, _ap = scan_docs()
    anchors_of, _cache = _anchors_cached()
    try:
        new, report, blocked = plan_update(data, ids, used, fetch, anchors_of)
    except ValueError as e:
        print(f"[NG] --update: {e}")
        if not ids:
            try:
                pending = [lid for lid, v in sorted(data["laws"].items())
                           if _differs(fetch(lid)["law_revision_id"], v["revision_id"])]
                print("  改正を検出中の法令: " + (" ".join(pending) if pending else "なし"))
            except (urllib.error.URLError, RuntimeError, TimeoutError) as err:
                print(f"  改正を検出中の法令は取得できませんでした（{err}）")
        print("  JSON は書き換えていません。")
        return 2
    for r in report:
        print(f"  {r}")
    for b in blocked:
        print(f"  [NG] 進めなかった {b}。docs のリンクを現行の条に直し --record してから再実行する")
    if new != data:
        save(new)
    print(f"[{'NG' if blocked else 'OK'}] 指定した {len(ids)} 件を処理（checked={new.get('checked')}）")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
