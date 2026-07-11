#!/usr/bin/env python3
"""docs/ コンテンツ規約 lint（数値矛盾・frontmatter・boost・コードブロック言語）。

Phase 4 の中核 lint。過去に人手で修正した誤り値（D種接地10Ω 等）の再発と、
frontmatter 必須キー欠落・06-trouble の search.boost 欠落を fail-closed で止める。
コードブロック言語未指定は WARN（exit に影響させない）。

設計は scripts/check_public_leak.py の「正対照つき自己診断」を踏襲:
  - 禁止パターンは (id, regex_or_predicate, desc, sample) のテーブルに一元定義。
    self-test が毎回サンプルをスキャンし、検出失敗＝検出器故障として exit 1。
    サンプル未定義のパターンを作れない構造＝検証器と fixture のドリフト防止。
  - canary: 正典値（正しい値）の黙った削除を検知（3 件）。

使い方:
  python scripts/check_content_rules.py             # self-test → 全検査
  python scripts/check_content_rules.py --self-test # self-test のみ

終了コード（check_public_leak.py に合わせる）:
  0 = FAIL 違反なし（WARN は含んでよい）
  1 = FAIL 違反あり or self-test 失敗
  2 = IO エラー（docs/ 無し等）

誤検知回避（lint-ok 機構）:
  違反行と同一行の末尾、または直前行に `<!-- lint-ok: <ID> 任意理由 -->` が
  あれば、その <ID> に限りその違反行を免除する。ID 必須・ID 照合厳格
  （別 ID の lint-ok では免除しない）。複数 ID は `<!-- lint-ok: N1,N4 -->`。
"""

import argparse
import io
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows cp932 で日本語出力が化けるのを回避（check_public_leak.py と同処理）
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# 走査除外ディレクトリ（テンプレは意図的に誤り例を含む・includes は本文でない）
EXCLUDE_DIRS = {"templates", "includes"}

# frontmatter 必須キー
REQUIRED_FM_KEYS = ["title", "description", "tags", "audience", "last_verified"]


# ---------------------------------------------------------------------------
# 検査1: 数値矛盾 lint（禁止パターン・行単位共起）
# 各エントリ (id, matcher, desc, sample)。matcher は正規表現(compiled) か
# 述語関数(line->bool) のどちらか。sample は self-test が必ず検出できねばならぬ
# 最小文字列（サンプル未定義のパターンを作れない構造にする）。
# ---------------------------------------------------------------------------
def _both(pat_a: str, pat_b: str):
    """同一行に pat_a と pat_b の両方（順不同）を含めば True の述語を作る。"""
    ra, rb = re.compile(pat_a), re.compile(pat_b)
    return lambda line: bool(ra.search(line)) and bool(rb.search(line))


# 単位「Ω」の表記揺れ（記号 Ω とカタカナ「オーム」）を両方拾う断片。
# 事後監査で「10オーム」等のカタカナ単位が Ω 限定パターンをすり抜けた穴を塞ぐ。
_OHM = r"(?:Ω|オーム)"


FORBIDDEN = [
    ("N1", _both(r"D\s*種", r"(?<![0-9])10(?![0-9])\s*" + _OHM),
     "D種接地は100Ω以下（10Ωは誤り）", "D種接地は10Ω以下"),
    ("N2", _both(r"C\s*種", r"混触"),
     "混触時電位抑制はB種の役割（C種ではない）", "C種は混触時の電圧を抑制"),
    # N3: %の位置揺れ（150〜200% / 150%〜200% の両方）を許容。先頭の%を任意化。
    ("N3", _both(r"瞬時", r"150\s*[%％]?\s*[〜～\-]\s*200\s*[%％]"),
     "変圧器OCR瞬時整定150〜200%は誤り（600〜1000%）", "瞬時整定は150〜200%"),
    ("N4", _both(r"40\s*" + _OHM, r"(接地|アース)"),
     "本安IS接地40Ωは誤り（1Ω以下）", "IS接地抵抗は40Ω以下"),
    ("N5", re.compile(r"500\s*kW\s*以上.{0,30}(選任|主任技術者)"),
     "主任技術者選任は規模不問（500kW以上は誤り）", "500kW以上は主任技術者の選任義務"),
    ("N6", re.compile(r"5\s*万\s*kW|50,?000\s*kW"),
     "電験3種は電圧5万V未満（5万kWは誤り）", "電験3種の範囲は5万kW未満"),
    ("N7", re.compile(r"施行規則\s*第?\s*99\s*条"),
     "事故報告根拠は電気関係報告規則第3条", "電気事業法施行規則第99条"),
    ("N8", re.compile(r"5\.583"),
     "R型熱電対500℃は約4.471mV（5.583は600℃値）", "500℃で5.583mV"),
    ("N9", re.compile(r"片道.{0,15}(?<![0-9])28(?![0-9.])\s*" + _OHM),
     "1.25sq片道は約14.6Ω/km（片道28は誤り）", "1.25sqは片道28Ω/km"),
    ("N10", re.compile(r"サイノス"),
     "非実在語（正: サイフォン）", "サイノス型スナッバー"),
    ("N11", re.compile(r"コルマン"),
     "誤記（正: カルマン渦）", "コルマンの渦"),
    ("N12", re.compile(r"ルアー"),
     "計装配管の誤用語（正: ねじ込み接続）", "ルアー接続"),
]

# 追加正対照（回帰 fixture）: 過去に表記揺れで検出をすり抜けた実例。
# self-test が (id, sample) ごとに「その ID で確かに検出できる」ことを証明する。
# FORBIDDEN の 4 つ組（sample 1件/パターン）を壊さず、拡張の生存証明を上乗せする。
EXTRA_POSITIVE = [
    ("N1", "D種接地は10オーム以下"),      # Ω→カタカナ「オーム」でのすり抜け
    ("N3", "瞬時要素は150%〜200%"),        # %を各数値に付す位置違いでのすり抜け
    ("N4", "IS接地抵抗は40オーム以下"),    # 同上（Ω→オーム）
    ("N9", "1.25sqは片道28オーム/km"),     # 同上（Ω→オーム）
]

# canary: これらの正典値が消えていたら FAIL（黙った削除の検知）。
# (repo ルートからの相対パス, 必ず存在すべき文字列, 説明)
CANARIES = [
    ("docs/02-teiatsu/grounding-lv.md", "100Ω", "D種接地の正典値"),
    ("docs/01-koatsu/insulation-test.md", "10.35", "6.6kV竣工交流試験電圧の正典値"),
    ("docs/01-koatsu/juhenden.md", "規模によらず", "主任技術者選任の正典表現"),
]

_LINTOK = re.compile(r"<!--\s*lint-ok:\s*([\w,]+)")


def _matches(matcher, line: str) -> bool:
    """matcher（正規表現 or 述語）を line に適用。"""
    if callable(matcher):
        return bool(matcher(line))
    return bool(matcher.search(line))


def lintok_ids(line: str) -> set:
    """行内の lint-ok コメントが指す ID 集合。無ければ空集合。"""
    m = _LINTOK.search(line)
    if not m:
        return set()
    return {t for t in m.group(1).split(",") if t}


# ---------------------------------------------------------------------------
# 走査本体
# ---------------------------------------------------------------------------
def load_docs():
    """docs/ 配下の .md（templates/・includes/ 除外）を (相対パス, 行リスト) で返す。"""
    out = []
    for p in sorted(DOCS.rglob("*.md")):
        rel_parts = p.relative_to(DOCS).parts
        if rel_parts and rel_parts[0] in EXCLUDE_DIRS:
            continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        out.append((rel, p.read_text(encoding="utf-8").splitlines()))
    return out


def scan_lines(lines):
    """禁止パターンを行単位走査。lint-ok（同一行/直前行・ID照合）で免除。
    (行番号1始まり, ID, desc, 行内容) のリストを返す。"""
    out = []
    for i, line in enumerate(lines):
        exempt = lintok_ids(line)
        if i > 0:
            exempt |= lintok_ids(lines[i - 1])
        for pid, matcher, desc, _sample in FORBIDDEN:
            if pid in exempt:
                continue
            if _matches(matcher, line):
                out.append((i + 1, pid, desc, line))
    return out


def check_forbidden(docs):
    """検査1: 数値矛盾 lint。違反 (rel, 行番号, ID, desc, 行内容) のリスト。"""
    violations = []
    for rel, lines in docs:
        for lineno, pid, desc, content in scan_lines(lines):
            violations.append((rel, lineno, pid, desc, content))
    return violations


def parse_frontmatter(lines):
    """先頭 --- 〜 --- のフロントマター本文行を返す。無し/未終端なら None。"""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def _key_state(fm_lines, key):
    """frontmatter 内の key の状態を返す。
    (存在するか, インライン値 or None, 充足するか)。
    充足条件: キー行があり、同一行に非空値がある or 次行以降に `- ` 項目が1つ以上。"""
    kre = re.compile(rf"^{re.escape(key)}\s*:(.*)$")
    for idx, line in enumerate(fm_lines):
        m = kre.match(line)
        if not m:
            continue
        inline = m.group(1).strip()
        if inline and inline not in ("[]", "{}"):
            return True, inline, True
        # ブロックリスト形式の子項目を探す（次のトップレベルキーまで）
        for j in range(idx + 1, len(fm_lines)):
            nxt = fm_lines[j]
            if re.match(r"^\S.*:", nxt):  # 次のトップレベルキー
                break
            if re.match(r"^\s*-\s+\S", nxt):
                return True, None, True
        return True, inline, False  # キーはあるが値が空
    return False, None, False


def check_frontmatter(docs):
    """検査2: frontmatter 必須キー lint。違反メッセージ文字列のリスト。"""
    fails = []
    for rel, lines in docs:
        fm = parse_frontmatter(lines)
        if fm is None:
            for key in REQUIRED_FM_KEYS:
                fails.append(f"{rel}: frontmatter '{key}' 欠落")
            continue
        for key in REQUIRED_FM_KEYS:
            present, inline, ok = _key_state(fm, key)
            if not ok:
                fails.append(f"{rel}: frontmatter '{key}' 欠落/不正")
                continue
            if key == "last_verified":
                val = (inline or "").strip().strip('"').strip("'")
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", val):
                    fails.append(f"{rel}: frontmatter 'last_verified' 欠落/不正")
                    continue
                try:
                    datetime.strptime(val, "%Y-%m-%d")
                except ValueError:
                    fails.append(f"{rel}: frontmatter 'last_verified' 欠落/不正")
    return fails


def check_boost(docs):
    """検査3: 06-trouble/*.md は search.boost>=2 を要求。違反メッセージのリスト。"""
    fails = []
    for rel, lines in docs:
        if not rel.startswith("docs/06-trouble/"):
            continue
        fm = parse_frontmatter(lines)
        if fm is None:
            fails.append(f"{rel}: 06-trouble frontmatter 無し（search/boost 検証不能）")
            continue
        s_idx = None
        for idx, line in enumerate(fm):
            if re.match(r"^search\s*:", line):
                s_idx = idx
                break
        if s_idx is None:
            fails.append(f"{rel}: 06-trouble 'search:' ブロック欠落")
            continue
        found = None
        for j in range(s_idx + 1, len(fm)):
            line = fm[j]
            if re.match(r"^\S", line):  # search ブロックを抜けた
                break
            m = re.match(r"^\s+boost\s*:\s*(\d+)", line)
            if m:
                found = int(m.group(1))
                break
        if found is None:
            fails.append(f"{rel}: 06-trouble 'boost:' 欠落")
        elif found < 2:
            fails.append(f"{rel}: 06-trouble boost={found} が2未満")
    return fails


# コードブロック言語未指定の総数ラチェット基準。
# 既存の裸フェンス（ASCII図・数式ブロックの慣行）は R30（一括自動変換の教訓）を
# 避けて据え置くが、この基準を超える＝新規ページ/加筆で裸フェンスを増やしたら FAIL。
# 既存分は免罪しつつ増加だけを止める。既存を`text`化して減らしたらこの値も下げてよい。
CODEBLOCK_WARN_BASELINE = 242


def warn_codeblocks(docs):
    """検査4: コードブロック言語未指定を数える（WARN・exit 非影響）。
    開始/終了フェンスをトグルで追跡し、終了フェンスを開始と誤認しない。
    (総件数, ファイル別件数dict) を返す。"""
    total = 0
    per_file = {}
    fence = re.compile(r"^\s*```(\S*)")
    for rel, lines in docs:
        in_block = False
        for line in lines:
            m = fence.match(line)
            if not m:
                continue
            if not in_block:
                in_block = True
                if not m.group(1):  # 言語トークン無し
                    total += 1
                    per_file[rel] = per_file.get(rel, 0) + 1
            else:
                in_block = False  # 終了フェンス（トークンは無視）
    return total, per_file


# ---------------------------------------------------------------------------
# self-test（正対照・負対照・canary）
# ---------------------------------------------------------------------------
def self_test():
    """検出器の生存証明。1つでも失敗で exit 1。"""
    failures = []

    # 1) 正対照: 各パターンが自分のサンプルを検出できること
    for pid, matcher, _desc, sample in FORBIDDEN:
        if not _matches(matcher, sample):
            failures.append(f"正対照 {pid}: サンプル {sample!r} を検出できない（検出器故障）")

    # 1b) 追加正対照: 表記揺れですり抜けていた実例も、該当 ID で検出できること
    for pid, sample in EXTRA_POSITIVE:
        hits = {v[1] for v in scan_lines([sample])}
        if pid not in hits:
            failures.append(f"追加正対照 {pid}: すり抜け表記 {sample!r} を検出できない（拡張漏れ）")

    # 2) 負対照(a): 同一行 lint-ok: N1 で N1 が免除されること
    a = ["D種接地は10Ω以下 <!-- lint-ok: N1 -->"]
    if any(v[1] == "N1" for v in scan_lines(a)):
        failures.append("負対照(a): lint-ok: N1 が N1 を免除できていない")

    # 3) 負対照(b): 別 ID lint-ok: N2 では N1 が免除されない（ID照合の生存証明）
    b = ["D種接地は10Ω以下 <!-- lint-ok: N2 -->"]
    if not any(v[1] == "N1" for v in scan_lines(b)):
        failures.append("負対照(b): lint-ok: N2 が N1 を誤って免除している（ID照合破綻）")

    # 4) canary: 正典値の黙った削除検知
    for rel, needle, why in CANARIES:
        p = ROOT / rel
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            failures.append(f"canary: {rel} 読込不可 ({e})")
            continue
        if needle not in text:
            failures.append(f"canary: {rel} に {needle!r} が無い（{why}の削除疑い）")

    if failures:
        for msg in failures:
            print(f"[FAIL] {msg}")
        print(f"[NG] self-test: 検出器故障 {len(failures)} 件。この結果は信頼できません。")
        return 1
    print(f"[OK] self-test: 正対照{len(FORBIDDEN)} + 追加正対照{len(EXTRA_POSITIVE)} "
          f"+ 負対照2 + canary{len(CANARIES)} パス")
    return 0


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------
def run_all():
    """self-test → 全検査。FAIL 有りで 1、無しで 0（WARN は非影響）。"""
    if not DOCS.is_dir():
        print(f"[ERROR] docs ディレクトリがありません: {DOCS}", file=sys.stderr)
        return 2

    if self_test() != 0:
        return 1

    try:
        docs = load_docs()
    except Exception as e:
        print(f"[ERROR] docs 読込失敗: {e}", file=sys.stderr)
        return 2

    forbidden = check_forbidden(docs)
    fm_fails = check_frontmatter(docs)
    boost_fails = check_boost(docs)
    warn_total, warn_files = warn_codeblocks(docs)

    print("")
    # 検査1: 数値矛盾
    for rel, lineno, pid, desc, content in forbidden:
        print(f"[FAIL] {rel}:{lineno}: {pid}（{desc}）")
        print(f"    {content.strip()}")
    # 検査2: frontmatter
    for msg in fm_fails:
        print(f"[FAIL] {msg}")
    # 検査3: boost
    for msg in boost_fails:
        print(f"[FAIL] {msg}")

    # 検査4: WARN（既存の裸フェンスは免罪）＋総数ラチェット（増加は FAIL）
    if warn_total:
        print(f"\n[WARN] コードブロック言語未指定: {warn_total}箇所 / {len(warn_files)}ファイル")
        top = sorted(warn_files.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        for rel, n in top:
            print(f"    {rel}: {n}箇所")
    ratchet_fail = warn_total > CODEBLOCK_WARN_BASELINE
    if ratchet_fail:
        print(
            f"\n[FAIL] コードブロック言語未指定が基準を超過: {warn_total} > "
            f"{CODEBLOCK_WARN_BASELINE}（基準）。新規/加筆の裸フェンスに言語指定を付けること"
            f"（ASCII図・数式は ```text）。"
        )

    total_fail = len(forbidden) + len(fm_fails) + len(boost_fails) + (1 if ratchet_fail else 0)
    print("\n==== サマリ ====")
    print(f"  検査1 数値矛盾:        {len(forbidden)} 件")
    print(f"  検査2 frontmatter:    {len(fm_fails)} 件")
    print(f"  検査3 06-trouble boost: {len(boost_fails)} 件")
    print(f"  検査4 コードブロック(WARN): {warn_total} 箇所 / {len(warn_files)} ファイル")
    if total_fail:
        print(f"[NG] FAIL 合計 {total_fail} 件。")
        return 1
    print("[OK] FAIL 0 件（WARN は exit に影響しません）。")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="docs/ コンテンツ規約 lint（数値矛盾・frontmatter・boost・コードブロック）")
    ap.add_argument("--self-test", action="store_true",
                    help="self-test（正対照・負対照・canary）のみ実行")
    args = ap.parse_args()

    if args.self_test:
        if not DOCS.is_dir():
            print(f"[ERROR] docs ディレクトリがありません: {DOCS}", file=sys.stderr)
            return 2
        return self_test()
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
