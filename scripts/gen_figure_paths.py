#!/usr/bin/env python3
"""図（インラインSVG）の曲線パスを、記事本文の式・数値から生成する。

図の座標を手書きすると、同じページに載っている式や数値表と静かに矛盾する。
矛盾した図は「最も権威的な見た目をした誤り」になるため、曲線は必ず本スクリプトで
生成し、出力をそのまま Markdown の <svg> に貼る。

使い方:
    python scripts/gen_figure_paths.py valve   # 制御弁の固有流量特性
    python scripts/gen_figure_paths.py tcc     # 保護協調 TCC 曲線
    python scripts/gen_figure_paths.py --check # 生成値と記事の数値表の突合

典拠:
  valve … docs/03-keiso/control-valve.md「流量特性」節の3特性の定義
  tcc   … docs/01-koatsu/coordination.md:66-76 の IEC 60255-151 反限時特性
          t = K / (M^E - 1) * TMS  （SI: K=0.14, E=0.02）
          および同 143-148 行の整定例（下位 Ip=110A/TMS=0.10、上位 Ip=300A/TMS=0.12、
          短絡電流 1094A → 0.30秒 / 0.64秒、時限差 0.34秒）
"""
import math
import sys

# ---------------------------------------------------------------- 制御弁

# 制御弁 固有流量特性のプロット領域（viewBox 420x320 内）
V_LEFT, V_RIGHT, V_TOP, V_BOTTOM = 62.0, 396.0, 34.0, 258.0
# イコールパーセンテージのレンジアビリティ R。カタログ代表値で 30〜50。
# 図は R=50 の代表例であり、規格で一意に決まる値ではない（本文に併記すること）。
EQ_RANGEABILITY = 50.0


def v_x(h: float) -> float:
    """開度 h (0..1) → SVG x"""
    return V_LEFT + (V_RIGHT - V_LEFT) * h


def v_y(f: float) -> float:
    """流量比 f (0..1) → SVG y"""
    return V_BOTTOM - (V_BOTTOM - V_TOP) * f


def valve_curves():
    """3つの固有流量特性 f(h) を返す。h=リフト比, f=Q/Qmax。"""
    R = EQ_RANGEABILITY
    return {
        # 開度に比例
        "linear": ("リニア", lambda h: h),
        # 開度1%増でその時点の流量の一定割合が増える ⇒ df/dh ∝ f ⇒ 指数関数
        "equal_pct": ("イコールパーセンテージ", lambda h: R ** (h - 1.0)),
        # 少し開くだけで大流量。慣用的な近似として平方根特性を用いる
        "quick_open": ("クイックオープン", lambda h: math.sqrt(h)),
    }


def gen_valve():
    print("# 制御弁 固有流量特性（viewBox 420x320）")
    print(f"# イコールパーセンテージは R={EQ_RANGEABILITY:g} の代表例")
    for key, (label, fn) in valve_curves().items():
        pts = []
        steps = 25          # 25分割＝26点。曲率の緩い3特性ではこれで十分滑らか
        for i in range(0, steps + 1):
            h = i / steps
            f = min(max(fn(h), 0.0), 1.0)
            pts.append(f"{v_x(h):.1f},{v_y(f):.1f}")
        # 折れ線を1本のパスにする
        print(f'\n<!-- {label} -->')
        print(f'd="M {" L ".join(pts)}"')


# ---------------------------------------------------------------- TCC

K_SI, E_SI = 0.14, 0.02          # IEC 60255-151 標準反限時（SI）
LOWER = {"name": "下位（フィーダ）", "Ip": 110.0, "TMS": 0.10}
UPPER = {"name": "上位（母線）",     "Ip": 300.0, "TMS": 0.12}
I_FAULT = 1094.0                 # 短絡電流 [A]

# TCC のプロット領域（viewBox 420x330 内）。両対数。
T_LEFT, T_RIGHT, T_TOP, T_BOTTOM = 66.0, 396.0, 34.0, 262.0
I_MIN, I_MAX = 100.0, 2000.0     # 横軸: 一次電流 [A]
T_MIN, T_MAX = 0.05, 10.0        # 縦軸: 動作時間 [s]


def t_x(i: float) -> float:
    """一次電流 [A] → SVG x（対数軸）"""
    r = (math.log10(i) - math.log10(I_MIN)) / (math.log10(I_MAX) - math.log10(I_MIN))
    return T_LEFT + (T_RIGHT - T_LEFT) * r


def t_y(t: float) -> float:
    """動作時間 [s] → SVG y（対数軸・上が長時間）"""
    r = (math.log10(t) - math.log10(T_MIN)) / (math.log10(T_MAX) - math.log10(T_MIN))
    return T_BOTTOM - (T_BOTTOM - T_TOP) * r


def op_time(i: float, relay: dict) -> float:
    """一次電流 i における動作時間 [s]。M<=1 は動作しない（None）。"""
    m = i / relay["Ip"]
    if m <= 1.0:
        return None
    return K_SI / (m ** E_SI - 1.0) * relay["TMS"]


def tcc_points(relay: dict):
    """M>1 の領域だけ点列を返す（codex 指摘: M<=1 は描かない）。"""
    pts = []
    # ピックアップ直上から描き始める。M=1 は t→∞ なので、
    # 縦軸上限 T_MAX に収まる電流から開始する。
    # 対数等間隔で 60 点サンプリングする（反限時は立ち上がりが急なので密度を確保）。
    start, steps = relay["Ip"] * 1.005, 60
    ratio = (I_MAX / start) ** (1.0 / steps)
    i = start
    for _ in range(steps + 1):
        t = op_time(i, relay)
        if t is not None and t <= T_MAX:
            pts.append((i, t))
        i *= ratio
    return pts


def gen_tcc():
    print("# 保護協調 TCC（viewBox 420x330・両対数）")
    print(f"# 横軸=一次電流[A] {I_MIN}-{I_MAX} / 縦軸=動作時間[s] {T_MIN}-{T_MAX}")
    print(f"# t = {K_SI}/(M^{E_SI} - 1) * TMS   (IEC 60255-151 SI)")
    for relay in (LOWER, UPPER):
        pts = tcc_points(relay)
        d = " L ".join(f"{t_x(i):.1f},{t_y(t):.1f}" for i, t in pts)
        print(f'\n<!-- {relay["name"]} Ip={relay["Ip"]:g}A TMS={relay["TMS"]:g} -->')
        print(f'd="M {d}"')
    # 短絡点の縦線と動作時間マーカー
    print(f'\n<!-- 短絡電流 {I_FAULT:g}A の垂線 -->')
    print(f'x={t_x(I_FAULT):.1f}  (y {t_y(T_MAX):.1f} .. {t_y(T_MIN):.1f})')
    for relay in (LOWER, UPPER):
        t = op_time(I_FAULT, relay)
        print(f'<!-- {relay["name"]}: t={t:.3f}s -->  point {t_x(I_FAULT):.1f},{t_y(t):.1f}')


def check():
    """生成値が記事の数値表と一致するかを機械照合する。"""
    ok = True
    expect = [(LOWER, 0.30), (UPPER, 0.64)]
    for relay, want in expect:
        got = op_time(I_FAULT, relay)
        m = I_FAULT / relay["Ip"]
        # 記事は小数2桁で丸めて記載しているので許容差 0.005
        good = abs(got - want) <= 0.005
        ok &= good
        print(f'{"OK " if good else "NG "} {relay["name"]}: '
              f'M={m:.2f}, t={got:.4f}s (記事表={want}s)')
    diff = op_time(I_FAULT, UPPER) - op_time(I_FAULT, LOWER)
    good = abs(diff - 0.34) <= 0.005
    ok &= good
    print(f'{"OK " if good else "NG "} 時限差={diff:.4f}s (記事表=0.34s)')
    # 弁: 各特性が定義域の端で妥当か
    for key, (label, fn) in valve_curves().items():
        f0, f1 = fn(0.0), fn(1.0)
        good = abs(f1 - 1.0) < 1e-9 and 0.0 <= f0 <= 1.0
        ok &= good
        print(f'{"OK " if good else "NG "} {label}: f(0)={f0:.4f}, f(1)={f1:.4f}')
    return 0 if ok else 1


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if arg == "valve":
        gen_valve()
    elif arg == "tcc":
        gen_tcc()
    else:
        sys.exit(check())
