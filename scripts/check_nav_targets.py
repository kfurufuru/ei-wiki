#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nav・セクションindex のリンク先が実在するかを検査する。

## なぜあるか — 2026-09-17 の事故

同一の作業ツリーを複数セッションが共有していたため、あるセッションの commit が
別セッションの未コミット編集（mkdocs.yml の nav 1行と index.md の表1行）を
巻き込んだ。**そのページ本体は含まれていない**ため、出来上がったのは
「nav には載っているがファイルが無い」コミットだった。

この汚染は後続の cherry-pick で別ブランチへ持ち越され、そちらの CI が落ちた。

`mkdocs build --strict` は CI で同じものを捕まえるが、**捕まえるのは push 後**。
この検査は pre-commit で走らせ、**壊れたコミットをそもそも作らせない**ことを狙う。
壊れたコミットさえ無ければ、cherry-pick で汚染が広がることもない。

## 使い方

    python scripts/check_nav_targets.py            # 作業ツリーを検査
    python scripts/check_nav_targets.py --staged   # index（staging）を検査。pre-commit 用
    python scripts/check_nav_targets.py --self-test  # 検査器自身の検査

exit 0 = 問題なし / exit 1 = ダングリング検出 / exit 2 = 検査不能
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = "docs"

# mkdocs.yml の nav 行: `      - 表示名: 11-genai/foo.md`  または `      - 11-genai/index.md`
NAV_RE = re.compile(r"^\s*-\s+(?:[^:\n]+:\s*)?([A-Za-z0-9_./-]+\.md)\s*$")
# Markdown の相対リンク: `[表示](foo.md)`。http(s)・アンカーのみは除く
LINK_RE = re.compile(r"\]\((?!https?:|#)([A-Za-z0-9_./-]+\.md)(?:#[^)]*)?\)")


def _git(args):
    return subprocess.run(
        ["git"] + args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )


def _read_worktree(path):
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    with open(full, encoding="utf-8") as f:
        return f.read()


def _batch_read_staged(paths):
    """index から複数ファイルの中身を git 1回で読む。

    1ファイルごとに `git show` を起動すると、この環境では1回あたり約1秒かかり、
    index.md が十数個あるだけで pre-commit が15秒級になる（2026-09-17 実測）。
    `git cat-file --batch` なら1プロセスで済む。
    """
    paths = list(paths)
    if not paths:
        return {}
    stdin = "".join(":" + p.replace(os.sep, "/") + "\n" for p in paths).encode("utf-8")
    p = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        input=stdin, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    if p.returncode != 0:
        return {}
    out, pos, result = p.stdout, 0, {}
    for path in paths:
        nl = out.find(b"\n", pos)
        if nl < 0:
            break
        header = out[pos:nl].decode("utf-8", "replace")
        if header.endswith("missing") or " " not in header:
            pos = nl + 1
            continue
        try:
            size = int(header.rsplit(" ", 1)[1])
        except ValueError:
            pos = nl + 1
            continue
        body = out[nl + 1: nl + 1 + size]
        result[path] = body.decode("utf-8", "replace")
        pos = nl + 1 + size + 1     # 本文の後ろの改行も飛ばす
    return result


_STAGED_CACHE = {}


def _read_staged(path):
    return _STAGED_CACHE.get(path.replace(os.sep, "/"))


def _exists_worktree(path):
    return os.path.isfile(os.path.join(ROOT, path))


# index（staging）の全パスを1回だけ読む。
# 1ファイルごとに git を起動すると Windows では約400回のプロセス生成になり、
# pre-commit が数分固まる（2026-09-17 に実測して作り直した）。
_STAGED_PATHS = None


def _staged_paths():
    global _STAGED_PATHS
    if _STAGED_PATHS is None:
        r = _git(["ls-files"])
        if r.returncode != 0:
            _STAGED_PATHS = set()
        else:
            _STAGED_PATHS = set(
                l.strip() for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()
            )
    return _STAGED_PATHS


def _exists_staged(path):
    return path.replace(os.sep, "/") in _staged_paths()


def _list_index_pages(staged):
    """docs/*/index.md を列挙する。"""
    if staged:
        return sorted(
            p for p in _staged_paths()
            if p.startswith(DOCS + "/") and p.endswith("/index.md") and p.count("/") == 2
        )
    out = []
    base = os.path.join(ROOT, DOCS)
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        p = os.path.join(base, name, "index.md")
        if os.path.isfile(p):
            out.append(DOCS + "/" + name + "/index.md")
    return out


def scan(staged):
    """(問題リスト, 検査したnav件数, 検査したリンク件数) を返す。"""
    read = _read_staged if staged else _read_worktree
    exists = _exists_staged if staged else _exists_worktree
    problems, n_nav, n_link = [], 0, 0

    if staged:
        # 読むファイルを先に確定し、git cat-file 1回でまとめて取る
        _STAGED_CACHE.update(_batch_read_staged(["mkdocs.yml"] + _list_index_pages(True)))

    # 1) mkdocs.yml の nav
    text = read("mkdocs.yml")
    if text is None:
        return ([("mkdocs.yml", 0, "mkdocs.yml を読めません")], 0, 0)
    in_nav = False
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^nav:\s*$", line):
            in_nav = True
            continue
        if in_nav and line and not line[0].isspace():
            in_nav = False          # 次のトップレベルキーで nav は終わり
        if not in_nav:
            continue
        m = NAV_RE.match(line)
        if not m:
            continue
        target = DOCS + "/" + m.group(1)
        n_nav += 1
        if not exists(target):
            problems.append(("mkdocs.yml", i, "nav のリンク先が存在しません: " + target))

    # 2) docs/*/index.md の相対リンク
    for page in _list_index_pages(staged):
        body = read(page)
        if body is None:
            continue
        d = os.path.dirname(page)
        for m in LINK_RE.finditer(body):
            rel = m.group(1)
            target = os.path.normpath(os.path.join(d, rel)).replace(os.sep, "/")
            n_link += 1
            if not exists(target):
                line_no = body[: m.start()].count("\n") + 1
                problems.append((page, line_no, "リンク先が存在しません: " + target))

    return (problems, n_nav, n_link)


def self_test():
    """陽性対照 — 検査器が生きているかを確かめる。

    実在しない .md を指す nav 行と index リンクを合成し、**必ず検出されること**を
    確かめる。これが通ってしまうなら検査は黙って無検査になっている。
    """
    fake_nav = "      - 存在しないページ: 99-nonexistent/ghost-page.md"
    if not NAV_RE.match(fake_nav):
        print("[NG] self-test: nav 行の正規表現が陽性対照を拾えません", file=sys.stderr)
        return 1
    if NAV_RE.match(fake_nav).group(1) != "99-nonexistent/ghost-page.md":
        print("[NG] self-test: nav 行からパスを取り出せません", file=sys.stderr)
        return 1

    fake_link = "| [幽霊ページ](ghost-page.md) | 誰 | 何 |"
    ms = LINK_RE.findall(fake_link)
    if ms != ["ghost-page.md"]:
        print("[NG] self-test: index リンクの正規表現が陽性対照を拾えません", file=sys.stderr)
        return 1

    # 負対照 — 外部リンクとアンカーは拾ってはいけない
    if LINK_RE.findall("[外部](https://example.com/a.md) [節](#midashi)"):
        print("[NG] self-test: 外部リンク・アンカーを誤検出します", file=sys.stderr)
        return 1

    # 事故の再現 — nav にあるがファイルが無い状態を検出できること
    if _exists_worktree(DOCS + "/99-nonexistent/ghost-page.md"):
        print("[NG] self-test: 対照用のパスが実在してしまっています", file=sys.stderr)
        return 1

    print("[OK] self-test: 陽性対照3 + 負対照2 パス（検査器は生きています）")
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    staged = "--staged" in argv
    problems, n_nav, n_link = scan(staged)
    where = "staging" if staged else "作業ツリー"
    if problems:
        print("[FAIL] nav/index のリンク先が %d 件見つかりません（%s）" % (len(problems), where),
              file=sys.stderr)
        for path, line, msg in problems:
            print("  %s:%d  %s" % (path, line, msg), file=sys.stderr)
        print("", file=sys.stderr)
        print("nav・index にページを載せたのに本体ファイルが無い状態です。", file=sys.stderr)
        print("他セッションの編集を巻き込んだ commit でこれが起きます"
              "（2026-09-17 の事故）。", file=sys.stderr)
        print("該当ファイルを一緒に stage するか、nav/index の行を外してください。",
              file=sys.stderr)
        return 1
    print("[OK] nav %d 件・index リンク %d 件すべて実在（%s）" % (n_nav, n_link, where))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
