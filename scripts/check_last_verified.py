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

EXPIRED_DAYS = 365
DUE_SOON_DAYS = 300


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


def classify(days: int) -> str:
    if days > EXPIRED_DAYS:
        return "EXPIRED"
    if days >= DUE_SOON_DAYS:
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
        status = classify(days)
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
