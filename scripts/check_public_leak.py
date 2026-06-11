#!/usr/bin/env python3
"""公開ビルド成果物（site/）の私的情報・退避済みコンテンツ漏えい検査。

07-site（自工場固有）は private repo ei-wiki-private へ退避済み（PR #7/#8/#10）だが、
「漏れていないこと」の検証が目視・手動 grep 頼みだった。本スクリプトは build 後の
site/ を機械検査し、PR Build Check と deploy.yml の両方で漏えいを fail-closed に止める。

使い方:
  python scripts/check_public_leak.py              # site/ を検査（mkdocs build 後）
  python scripts/check_public_leak.py --site DIR   # 検査対象ディレクトリ指定
  python scripts/check_public_leak.py --self-test  # 検出器の生存証明（正対照）のみ

終了コード:
  0 = 漏えい 0 件かつ正対照すべて検出
  1 = 漏えい検出 / 正対照の検出失敗（=検出器または build の故障）
  2 = 引数・IO エラー（site/ が無い等）

設計（2026-06-11 search_index.json 空振りPASS事故の再発防止）:
  - 生バイト grep はしない。HTML 実体参照・URL エンコード・\\uXXXX（JSON
    ensure_ascii 形）を復号した「復号ビュー」と、NFKC 正規化＋ゼロ幅除去の
    シャドーも走査する（エンコード形に隠れた語を見落とさない）
  - sitemap.xml.gz は gzip 展開してから走査する（コンテナをスキップしない）。
    .gz 以外のコンテナ（zip/pdf）は site/ に存在した時点で NG（中身を検査できない）
  - 正対照（positive control）を 3 層で同梱:
      1) --self-test: 各 FORBIDDEN パターンが自分のサンプルを検出できるか＋
         エンコード形プローブ（\\uXXXX・HTML実体・URL%・全角・ゼロ幅・gzip）
      2) site 検査時: 「確実に存在するはずの公開語」（計装 等）が
         search_index.json / sitemap.xml.gz / index.html から検出できるか
      3) 1)2) のどちらが欠けても exit 1 ＝「漏えい 0 件」を空振りで報告しない
  - 「三菱」は意図的に FORBIDDEN に入れない（docs に機器メーカーとしての正当
    用途 16 件: MELPRO-D / NF125-SV / FR-A800 / MELSEC 等。2026-06-11 実測）

関連: .secretary 側 scripts/sanitize_public_html.py（同思想の実装・--self-test 由来）／
      memory: feedback_absence_check_positive_control
"""

import argparse
import gzip
import html
import io
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

# Windows cp932 で日本語エンコード失敗を回避
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# 禁止パターン（site/ に 1 件でもあれば公開不可）
# 2026-06-11 に docs/ 全数調査で各語の正当用途 0 件を確認してから採用。
# 第3列は正対照サンプル: そのパターンが「必ず検出できなければならない」最小文字列。
# --self-test が毎回スキャンし、検出失敗＝検出器故障として exit 1 にする
# （パターン追加時はサンプルも必須＝検証器と fixture のドリフトを構造的に防ぐ）。
# 正当用途が将来できた場合は、このテーブルを意識的に編集する（黙認エスケープ無し）。
# ---------------------------------------------------------------------------
FORBIDDEN = [
    (r"07-site", "退避済みディレクトリの参照（URL/検索index/ナビ）", "07-site"),
    (r"ei-wiki-private", "退避先 private repo 名", "ei-wiki-private"),
    (r"コンビナート", "自工場固有の機微語（2026-06-11 PR #8 残骸事故の対象語）", "コンビナート"),
    (r"古[舘館]", "実名（姓・舘/館 異体字とも）", "古舘"),
    (r"舘", "実名の単漢字指紋（タグ/ゼロ幅分断対策。常用『館』は別字で対象外）", "<b>舘</b>"),
    (r"主寿", "実名（名）", "主寿"),
    (r"(?i)furuta(?:te|chi|n)|furudate", "実名ローマ字", "Furutate"),
    (r"(?i)kazutoshi", "実名ローマ字（名）", "Kazutoshi"),
    (r"(?i)furu3291", "メールアドレス（ローカル部指紋）", "k.furu3291@gmail.com"),
    (r"(?i)kfuru(?!furu)", "ローカルユーザー名（kfurufuru=公開GitHubアカウントは許容）", "kfuru"),
    (r"(?i)C:[/\\]+Users", "ローカル Windows パス", r"C:\Users"),
    (r"(?i)AppData", "ローカル Windows パス", "AppData"),
    (r"鶴見", "勤務地", "鶴見"),
]

# site/ に「確実に存在するはずの公開語」。検出できなければ検出器か build の故障
# （＝「漏えい 0 件」が空振りの疑い）として exit 1。
# (相対パス, パターン, 説明)。パスは mkdocs build の固定出力。
SITE_POSITIVE_CONTROLS = [
    ("search/search_index.json", r"計装", "検索インデックス復号後に本文語が見えること"),
    ("sitemap.xml.gz", r"03-keiso", "gzip 展開後に公開 URL パスが見えること"),
    ("index.html", r"計装", "トップページ本文が見えること"),
]

# エンコード形プローブ（--self-test 用）: 復号・正規化・gzip 展開の各層の生存証明
_ENCODED_PROBES = [
    ("JSON \\uXXXX 形（ensure_ascii・search_index 事故と同型）", "\\u53e4\\u8218"),
    ("HTML 10進実体", "&#21476;&#33304;"),
    ("HTML 16進実体", "&#x53e4;&#x8218;"),
    ("URL エンコード", "%E5%8F%A4%E8%88%98"),
    ("NFKC 全角英字", "ＫＦＵＲＵ"),
    ("ゼロ幅挿入", "古\u200b舘"),
]

# テキスト走査しない拡張子（画像・フォント）。コンテナ（zip/pdf）は走査除外では
# なく「存在自体を NG」。gz はここに含めず gzip 展開して走査する。
BINARY_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".svg",
               ".woff", ".woff2", ".ttf", ".eot"}
CONTAINER_EXTS = {".zip", ".pdf"}

CONTEXT_CHARS = 35
MAX_SHOW = 8

# ZWSP / ZWNJ / ZWJ / WORD JOINER / ZWNBSP(BOM) — 不可視のため必ず明示エスケープで書く
_ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff"))


def shadow_normalize(text: str) -> str:
    """ゼロ幅文字を除去し NFKC 正規化したシャドーコピー。"""
    return unicodedata.normalize("NFKC", text.translate(_ZERO_WIDTH))


def decoded_view(text: str) -> str:
    """HTML 実体参照・URL エンコード・\\uXXXX を素朴に復号した検査用ビュー。"""
    t = html.unescape(text)
    try:
        t = unquote(t)
    except Exception:
        pass
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), t)


def scan_text(text: str) -> list[tuple[str, str, str]]:
    """生・NFKC シャドー・復号ビュー（とその NFKC）を走査し
    (パターン, ラベル+検出層, context) を返す。"""
    seen: set[tuple[str, int]] = set()
    out = []
    sources = [("", text)]
    shadow = shadow_normalize(text)
    if shadow != text:
        sources.append(("・正規化後検出", shadow))
    dec = decoded_view(text)
    if dec != text:
        sources.append(("・復号後検出", dec))
        dec_shadow = shadow_normalize(dec)
        if dec_shadow != dec:
            sources.append(("・復号+正規化後検出", dec_shadow))
    for suffix, t in sources:
        for pat, label, _sample in FORBIDDEN:
            for m in re.finditer(pat, t):
                key = (pat, m.start())
                if key in seen:
                    continue
                seen.add(key)
                s, e = m.start(), m.end()
                ctx = t[max(0, s - CONTEXT_CHARS): e + CONTEXT_CHARS].replace("\n", "⏎")
                out.append((pat, label + suffix, ctx))
    return out


def read_artifact(path: Path) -> str | None:
    """検査用テキストを返す。gz は展開、バイナリ拡張子は None（スキップ）。
    UTF-8 で読めないテキスト系ファイルは例外を上げる（呼び出し側で NG 扱い）。"""
    suffix = path.suffix.lower()
    if suffix in BINARY_EXTS:
        return None
    if suffix == ".gz":
        data = gzip.decompress(path.read_bytes())
        return data.decode("utf-8")
    return path.read_text(encoding="utf-8")


def self_test() -> int:
    """正対照スキャンで検出器自体の生存を証明する（--self-test）。"""
    failures = []
    for pat, label, sample in FORBIDDEN:
        if not any(h[0] == pat for h in scan_text(sample)):
            failures.append(f"{pat!r} ({label}) が正対照 {sample!r} を検出できない")
    for name, probe in _ENCODED_PROBES:
        if not scan_text(probe):
            failures.append(f"エンコード形 {name} の正対照 {probe!r} が全層で未検出")
    # gzip 展開層の生存証明（sitemap.xml.gz と同経路）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        gz = Path(td) / "probe.xml.gz"
        gz.write_bytes(gzip.compress("<url>古舘</url>".encode("utf-8")))
        text = read_artifact(gz)
        if not (text and scan_text(text)):
            failures.append("gzip 展開層の正対照が未検出（sitemap.xml.gz 経路の故障）")
    if failures:
        for msg in failures:
            print(f"[FAIL] {msg}")
        print(f"[NG] self-test: 検出器故障 {len(failures)} 件。"
              "この状態の『漏えい 0 件』は信頼できません。")
        return 1
    print(f"[OK] self-test: 正対照 {len(FORBIDDEN)} パターン＋エンコード形 "
          f"{len(_ENCODED_PROBES)} 種＋gzip 展開層を全て検出（検出器は生きています）")
    return 0


def scan_site(site: Path, quiet: bool) -> int:
    if not site.is_dir():
        print(f"[ERROR] site ディレクトリがありません: {site}（先に mkdocs build）",
              file=sys.stderr)
        return 2

    # 検出器の生存証明を内蔵実行（CI の独立 step だけに頼らない）。
    # これが無いと scan_text の沈黙故障時に「漏えい 0 件＋site 正対照 PASS」の
    # 空振りが成立してしまう（site 正対照は re.search 直叩きで scan_text 非依存のため）
    if self_test() != 0:
        return 1

    # 構造ガード: 退避済みディレクトリが build に再混入していないか
    if (site / "07-site").exists():
        print(f"[FAIL] {site}/07-site が build 出力に存在（exclude_docs の退行）")
        return 1

    violations: list[tuple[str, str, str, str]] = []  # (rel, pat, label, ctx)
    n_files = 0
    for p in sorted(site.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(site)).replace("\\", "/")
        if p.suffix.lower() in CONTAINER_EXTS:
            print(f"[FAIL] 走査不能なコンテナ形式が site/ に存在: {rel}（中身を検査できない）")
            return 1
        try:
            text = read_artifact(p)
        except Exception as e:
            print(f"[FAIL] 読込/展開できないファイル: {rel} ({e})")
            return 1
        if text is None:
            continue
        n_files += 1
        for pat, label, ctx in scan_text(text):
            violations.append((rel, pat, label, ctx))

    if violations:
        for rel, pat, label, ctx in violations[:MAX_SHOW]:
            print(f"[FAIL] {rel}: {pat} ({label})")
            if not quiet:
                print(f"    …{ctx}…")
        if len(violations) > MAX_SHOW:
            print(f"    …他 {len(violations) - MAX_SHOW} 件")
        print(f"[NG] 漏えい {len(violations)} 件。公開不可（deploy を中止してください）。")
        return 1

    # site 正対照: 「確実にあるはずの公開語」が見えること（空振り PASS 防止）
    pc_failures = []
    for rel, pat, why in SITE_POSITIVE_CONTROLS:
        p = site / rel
        try:
            text = read_artifact(p) if p.is_file() else None
        except Exception:
            text = None
        if text is None or not re.search(pat, decoded_view(text)):
            pc_failures.append(f"{rel}: {pat!r} が未検出（{why}）")
    if pc_failures:
        for msg in pc_failures:
            print(f"[FAIL] site 正対照: {msg}")
        print("[NG] 正対照が見えない＝検出器か build の故障。"
              "『漏えい 0 件』は空振りの疑いがあり信頼できません。")
        return 1

    print(f"[OK] {n_files} ファイル走査・漏えい 0 件・site 正対照 "
          f"{len(SITE_POSITIVE_CONTROLS)}/{len(SITE_POSITIVE_CONTROLS)} 検出（公開可能な状態）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="公開ビルド成果物（site/）の私的情報漏えい検査（正対照つき）")
    ap.add_argument("--site", default="site", help="検査対象ディレクトリ（既定: site）")
    ap.add_argument("--self-test", action="store_true",
                    help="検出器の生存証明（正対照スキャン）のみ実行")
    ap.add_argument("--quiet", action="store_true", help="context 表示を抑制（CI 用）")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    return scan_site(Path(args.site), args.quiet)


if __name__ == "__main__":
    sys.exit(main())
