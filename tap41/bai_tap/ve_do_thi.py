"""Vẽ: (trái) sơ đồ máy trạng thái bản C dựng từ bảng chuyển của bạn; (phải) một lần chạy 105 s của bản C (seed 6 như video):
đường robot tô màu theo trạng thái, và mức pin.

Chạy: python -X utf8 ve_do_thi.py            -> dùng bảng chuyển của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import fsm as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import may_tu_bang  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

VI_TRI = {"TUAN_TRA": (0.9, 3.0), "DUOI": (4.0, 4.4), "TIM": (4.0, 1.6), "VE_SAC": (7.1, 3.0), "SAC": (7.1, 0.6)}
MAU_S = {"TUAN_TRA": V.MAU["xanh"], "DUOI": V.MAU["do"], "TIM": V.MAU["vang"], "VE_SAC": V.MAU["tim"], "SAC": V.MAU["luc"]}
NHAN = {"TUAN_TRA": "TUẦN TRA", "DUOI": "ĐUỔI", "TIM": "TÌM", "VE_SAC": "VỀ SẠC", "SAC": "SẠC"}


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    chuyen = lay("them_sac")(lay("chuyen_B")())
    fig, (a, b) = V.tao(1, 2, rong=13.5, cao=5, gridspec_kw={"width_ratios": [1.15, 1]})
    a.set_xlim(-0.3, 8.3); a.set_ylim(-0.2, 5.2); a.axis("off")
    for s, (x, y) in VI_TRI.items():
        a.add_patch(Rectangle((x - 1.0, y - 0.32), 2.0, 0.64, fc=MAU_S[s], ec="white", alpha=0.85))
        a.text(x, y, NHAN[s], ha="center", va="center", color="white", fontsize=10.5, weight="bold")
    for (s, i), d in chuyen.items():
        if s == d:
            continue
        (x0, y0), (x1, y1) = VI_TRI[s], VI_TRI[d]
        a.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14, color="white", lw=1.3,
                                    connectionstyle="arc3,rad=0.18", shrinkA=26, shrinkB=26))
        a.text((x0 + x1) / 2 + 0.15 * (y1 - y0), (y0 + y1) / 2 - 0.15 * (x1 - x0), i, color=V.CHU, fontsize=7.5, ha="center")
    a.set_title(f"Máy trạng thái bản C: {len(chuyen)} mũi tên", color="white", fontsize=12, loc="left")
    cu = goc.tao_fsm
    may = may_tu_bang(chuyen, goc.S_ALL)
    goc.tao_fsm = lambda bb: may if bb == "C" else cu(bb)
    try:
        st, log = goc.chay("C", 6, T=105, co_pin=True, ghi=True)
    finally:
        goc.tao_fsm = cu
    for x0, y0, x1, y1, _ in goc.VAT:
        b.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#475569", ec="none"))
    r = np.array([q["r"][:2] for q in log])
    for k in range(len(log) - 1):
        b.plot(r[k:k + 2, 0], r[k:k + 2, 1], color=MAU_S[log[k]["s"]], lw=2)
    b.plot(*goc.DOC, "s", color=V.MAU["luc"], ms=10)
    b.set_xlim(0, goc.RONG); b.set_ylim(0, goc.DAI); b.set_aspect("equal")
    V.trang_tri(b, f"105 s: thấy mèo {st['ti_le_thay'] * 100:.0f}% · pin thấp nhất {st['pin_min']:.0f}% · sạc {st['lan_sac']} lần")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import fsm_cua_ban
        ve(fsm_cua_ban)
