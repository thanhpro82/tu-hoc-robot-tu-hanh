"""Vẽ: (trái) kho hàng và 20 lần chạy của mỗi chính sách khi ε = 0,1 (đỏ: đường tắt sát cầu thang, xanh: đường vòng);
(phải) chi phí kỳ vọng J(S) theo độ trơn ε, tính bằng danh_gia của bạn, so với J* tối ưu (tập 4.3).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import mdp as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    danh_gia = ns["danh_gia"] if isinstance(ns, dict) else getattr(ns, "danh_gia")
    fig, (a, b) = V.tao(1, 2, rong=13, cao=4.6, gridspec_kw={"width_ratios": [1.3, 1]})
    for x in range(goc.W):
        for y in range(goc.H):
            mau = "#7f1d1d" if (x, y) in goc.CAU_THANG else "#475569" if (x, y) in goc.KE else "#111827"
            a.add_patch(Rectangle((x, y), 1, 1, fc=mau, ec="#1e293b"))
    for (x, y), chu in [(goc.S, "S"), (goc.G, "G")]:
        a.text(x + 0.5, y + 0.5, chu, ha="center", va="center", color="white", fontsize=13, weight="bold")
    rng = np.random.default_rng(0)
    for pi, mau in [(goc.pi_tat, V.MAU["do"]), (goc.pi_an_toan, V.MAU["xanh"])]:
        for k in range(20):
            q = np.array(goc.quy_dao(pi, 0.1, 100 + k)) + 0.5 + rng.normal(0, 0.06, 2)
            a.plot(q[:, 0], q[:, 1], color=mau, lw=1, alpha=0.6)
    a.set_xlim(0, goc.W); a.set_ylim(0, goc.H); a.set_aspect("equal"); a.axis("off")
    a.set_title("Kho hàng: cầu thang (đỏ sẫm) ở hàng dưới, kệ ở giữa", color="white", fontsize=11.5, loc="left")
    eps = np.linspace(0, 0.35, 15)
    b.plot(eps, [danh_gia(goc.pi_tat, e)[goc.S] for e in eps], color=V.MAU["do"], lw=2.2, label="đường tắt")
    b.plot(eps, [danh_gia(goc.pi_an_toan, e)[goc.S] for e in eps], color=V.MAU["xanh"], lw=2.2, label="đường vòng")
    b.plot(eps, [goc.toi_uu(e)[0][goc.S] for e in eps], color="white", lw=1.4, ls="--", label="J* (tối ưu, tập 4.3)")
    V.trang_tri(b, "Chi phí kỳ vọng J(S)", "độ trơn ε", "J(S)")
    V.chu_giai(b, loc="upper left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import mdp_cua_ban
        ve(mdp_cua_ban)
