#!/usr/bin/env python3
"""記事鮮度監査スクリプト

docs/**/*.md のフロントマター `last_verified` をスキャンし、
今日からの経過日数で EXPIRED / DUE_SOON / OK / WARN に分類して
Markdown 表で標準出力に出す。

--ci フラグ時、EXPIRED が 1 件以上あれば exit 1。

外部依存なし（標準ライブラリのみ）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

EXPIRED_DAYS = 365
DUE_SOON_DAYS = 300


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

    print(f"# 記事鮮度監査レポート（基準日: {today.isoformat()}）")
    print()
    print(
        f"- EXPIRED: {counts['EXPIRED']}件 / "
        f"DUE_SOON: {counts['DUE_SOON']}件 / "
        f"OK: {counts['OK']}件 / "
        f"WARN: {counts['WARN']}件"
    )
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
