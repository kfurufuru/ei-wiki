#!/usr/bin/env python3
"""記事鮮度監査スクリプト

docs/**/*.md のフロントマター `last_verified` をスキャンし、
今日からの経過日数で EXPIRED / DUE_SOON / OK / WARN に分類して
Markdown 表で標準出力に出す。

--ci フラグ時、EXPIRED が 1 件以上あれば exit 1。
--queue N フラグ時、「次に検証すべき順」に N 件を出す（被リンク数×古さ）。

なぜ --queue が要るか（2026-07-28 追加）:
  既定の出力はバケット別の平坦な一覧で、優先順位が付かない。加えて
  49ページが 2026-04-04 という同一の一括日付を持つため、EXPIRED は
  ある日いっきに数十件が同時発火する「崖」になる。日付を機械的に
  書き換えるのは禁止（実際に検証していないため）なので、代わりに
  「読まれている順 × 古い順」で少しずつ消化できる待ち行列を出す。

外部依存なし（標準ライブラリのみ）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

# 再検証の間隔（2026-09-19 に一律 365 日から区分制へ変更）
#
# 一律 365 日は両方向に間違っていた。生成AI のページは半年で陳腐化し（2026-08 に
# 旧ドメイン・月額料金など6件を是正）、法令アンカーのページは 1 年経っても
# 条番号が動かない（2026-07→09 の再照合で異同ゼロ）。加えて 136 ページを
# 365 日で1周するには週 2.6 ページ要り、運用の週2ページでは構造的に追いつかず
# 崖が解消しない（1周 476 日）。
#
# 区分を入れて必要ペースを 1.60 ページ/週 に下げ、週2ページで定常の EXPIRED が
# ゼロになることをシミュレーションで確認した（毎週いちばん超過率の高い2件を
# 消化する前提・260 週）。
#
# **730 日が許されるのは、カレンダーが唯一の見張りではないから。**
#   - scripts/check_law_revisions.py … 引用法令の改正を e-Gov API で直接検出（イベント起動）
#   - scripts/check_content_rules.py … 既知の誤り値を FORBIDDEN、正典値を canary で保護
#   - .github/pull_request_template.md … 新規の数値に一次照合表を要求
# この 3 本を外すなら間隔も 365 日に戻すこと。
DEFAULT_INTERVAL_DAYS = 730

# セクション別の上書き。変化が速い分野だけ短くする。
SECTION_INTERVAL_DAYS = {
    "11-genai": 180,   # 製品名・料金・機能が半年で変わる（実績あり）
}

# DUE_SOON は満了の 60 日前から
DUE_SOON_MARGIN_DAYS = 60


def interval_for(rel_path: str) -> int:
    """docs/<section>/... の section で再検証間隔を決める。"""
    parts = rel_path.split("/")
    section = parts[1] if len(parts) > 2 else ""
    return SECTION_INTERVAL_DAYS.get(section, DEFAULT_INTERVAL_DAYS)


def count_inbound_links(docs_dir: Path, repo_root: Path) -> dict[str, int]:
    """docs/ 内の相対 .md リンクを数え、被リンク数（そのページの読まれやすさの代理指標）を返す。"""
    import re as _re
    counts: dict[str, int] = {}
    link_re = _re.compile(r"\]\(([^)#]+\.md)")
    for md in docs_dir.rglob("*.md"):
        rel = md.relative_to(repo_root).as_posix()
        if "templates/" in rel or "includes/" in rel:
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for target in link_re.findall(text):
            resolved = (md.parent / target).resolve()
            try:
                key = resolved.relative_to(repo_root).as_posix()
            except ValueError:
                continue
            counts[key] = counts.get(key, 0) + 1
    return counts


def find_repo_root(start: Path) -> Path:
    """スクリプト位置から docs/ を含む親ディレクトリを探す。"""
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / "docs").is_dir():
            return p
    return start.parent.resolve()


def parse_frontmatter_last_verified(md_path: Path) -> str | None:
    """簡易 YAML フロントマターから last_verified の値を取り出す。

    YAMLライブラリは使わず、行単位の簡易パース。
    `---` で囲まれたブロック内の `last_verified: YYYY-MM-DD` を拾う。
    """
    try:
        with md_path.open("r", encoding="utf-8") as f:
            first = f.readline()
            if first.strip() != "---":
                return None
            for line in f:
                if line.strip() == "---":
                    return None
                # key: value（valueはクォート除去）
                if ":" not in line:
                    continue
                key, _, value = line.partition(":")
                if key.strip() == "last_verified":
                    v = value.strip().strip('"').strip("'")
                    return v or None
    except OSError:
        return None
    return None


def classify(days: int, interval: int = DEFAULT_INTERVAL_DAYS) -> str:
    if days > interval:
        return "EXPIRED"
    if days >= interval - DUE_SOON_MARGIN_DAYS:
        return "DUE_SOON"
    return "OK"


def main() -> int:
    parser = argparse.ArgumentParser(description="last_verified 鮮度監査")
    parser.add_argument("--ci", action="store_true", help="EXPIRED があれば exit 1")
    parser.add_argument(
        "--today",
        default=None,
        help="基準日（YYYY-MM-DD）。省略時は今日。",
    )
    parser.add_argument(
        "--queue", type=int, metavar="N", default=0,
        help="次に検証すべき順（被リンク数×古さ）に N 件だけ出す",
    )
    args = parser.parse_args()

    today = (
        _dt.date.fromisoformat(args.today)
        if args.today
        else _dt.date.today()
    )

    repo_root = find_repo_root(Path(__file__).parent)
    docs_dir = repo_root / "docs"
    if not docs_dir.is_dir():
        print(f"ERROR: docs/ not found under {repo_root}", file=sys.stderr)
        return 2

    rows: list[tuple[str, str, str, int | str]] = []
    counts = {"EXPIRED": 0, "DUE_SOON": 0, "OK": 0, "WARN": 0}

    for md_path in sorted(docs_dir.rglob("*.md")):
        rel = md_path.relative_to(repo_root).as_posix()
        # docs/templates/（テンプレ）と docs/includes/（snippet）は監査対象外
        if "templates/" in rel or "includes/" in rel:
            continue
        value = parse_frontmatter_last_verified(md_path)
        if value is None:
            counts["WARN"] += 1
            rows.append(("WARN", rel, "(なし)", "-"))
            continue
        try:
            d = _dt.date.fromisoformat(value)
        except ValueError:
            counts["WARN"] += 1
            rows.append(("WARN", rel, value, "-"))
            continue
        days = (today - d).days
        status = classify(days, interval_for(rel))
        counts[status] += 1
        rows.append((status, rel, value, days))

    # 出力順: EXPIRED → DUE_SOON → WARN → OK
    order = {"EXPIRED": 0, "DUE_SOON": 1, "WARN": 2, "OK": 3}
    rows.sort(key=lambda r: (order[r[0]], r[1]))

    if not args.queue:
        print(f"# 記事鮮度監査レポート（基準日: {today.isoformat()}）")
        print()
        print(
            f"- EXPIRED: {counts['EXPIRED']}件 / "
            f"DUE_SOON: {counts['DUE_SOON']}件 / "
            f"OK: {counts['OK']}件 / "
            f"WARN: {counts['WARN']}件"
        )
        print()
    # 同一 last_verified に多数が集中していないか（一括スタンプ＝将来の同時失効）
    from collections import Counter as _C
    stamp = _C(v for st, r, v, d in rows if st != "WARN")
    cliffs = [(v, n) for v, n in stamp.items() if n >= 10]

    if args.queue:
        inbound = count_inbound_links(docs_dir, repo_root)
        q = [(r, v, d, inbound.get(r, 0)) for st, r, v, d in rows if isinstance(d, int)]
        # 古い順 → 同じ古さなら読まれている順。
        # （被リンクを第1キーにすると「18日前に検証済みだが読まれている」ページが
        #   先頭に来てしまい、再検証の待ち行列として意味をなさない）
        q.sort(key=lambda t: (-t[2], -t[3]))
        print(f"# 次に検証すべき記事 上位 {args.queue} 件"
              f"（基準日: {today.isoformat()}・被リンク数×古さ順）")
        print()
        if cliffs:
            for v, n in sorted(cliffs, key=lambda t: -t[1]):
                print(f"> 注意: {v} の一括日付が {n} 件あります。"
                      f"放置すると同日にまとめて EXPIRED 化します。")
            print()
        print("| # | パス | last_verified | 経過日数 | 被リンク |")
        print("| --- | --- | --- | --- | --- |")
        for i, (r, v, d, ib) in enumerate(q[: args.queue], 1):
            print(f"| {i} | {r} | {v} | {d} | {ib} |")
        return 0

    if cliffs:
        for v, n in sorted(cliffs, key=lambda t: -t[1]):
            print(f"> 注意: {v} の一括日付が {n} 件（同日に EXPIRED 化します）")
        print()
    print("| 状態 | パス | last_verified | 経過日数 |")
    print("| --- | --- | --- | --- |")
    for status, rel, val, days in rows:
        print(f"| {status} | {rel} | {val} | {days} |")

    if args.ci and counts["EXPIRED"] > 0:
        print(
            f"\nCI: EXPIRED {counts['EXPIRED']}件のため失敗扱い",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
