"""Vẽ chính sách tối ưu π*_t (mũi tên) và J*_t (màu) ở t = 0 và t = 26, tính bằng quy_hoach_dong của bạn.
Gần hết giờ (t = 26), robot không kịp đi vòng nữa nên chọn liều đường tắt hoặc chịu phạt.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[2] / "tap42" / "sim"), str(_D.parents[1])]
import qhd as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

M = goc.M
MUI = {"len": (0, 0.32), "xuong": (0, -0.32), "trai": (-0.32, 0), "phai": (0.32, 0)}


def ve(ns, ra="ket_qua.png"):
    f = ns["quy_hoach_dong"] if isinstance(ns, dict) else getattr(ns, "quy_hoach_dong")
    J, PI = f(goc.EPS)
    fig, axes = V.tao(1, 2, rong=13, cao=4.2)
    for ax, t in zip(axes, [0, 26]):
        lon = np.zeros((M.H, M.W))
        for x in range(M.W):
            for y in range(M.H):
                if (x, y) in M.KE:
                    ax.add_patch(Rectangle((x, y), 1, 1, fc="#475569"))
                    continue
                v = J[t][(x, y)]
                lon[y, x] = v
                ax.add_patch(Rectangle((x, y), 1, 1, fc=V.plt.cm.magma(min(v, 100) / 100 * 0.85), ec="#0b1220"))
                if (x, y) not in M.CAU_THANG and (x, y) != M.G:
                    dx, dy = MUI[PI[t][(x, y)]]
                    ax.annotate("", xy=(x + 0.5 + dx, y + 0.5 + dy), xytext=(x + 0.5 - dx, y + 0.5 - dy),
                                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.6))
                ax.text(x + 0.08, y + 0.08, f"{v:.0f}", color="white", fontsize=7)
        for (x, y), chu in [(M.S, "S"), (M.G, "G")]:
            ax.text(x + 0.85, y + 0.8, chu, color=V.MAU["luc"], fontsize=11, weight="bold", ha="center")
        ax.set_xlim(0, M.W); ax.set_ylim(0, M.H); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(f"t = {t}: J*_t(S) = {J[t][M.S]:.2f}, còn {M.T - t} bước", color="white", fontsize=12, loc="left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import qhd_cua_ban
        ve(qhd_cua_ban)
