"""Vẽ 4 ô: ảnh sàn có nhiễu · cạnh khi không làm mịn · cạnh sau làm mịn Gauss + vạch tìm được · lưới bỏ phiếu Hough.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import thi_giac as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import canh_voi  # noqa: E402


def _duong(ax, a_deg, r, mau, **kw):
    a = np.radians(a_deg)
    y = np.array([0, goc.H])
    ax.plot((r - y * np.sin(a)) / np.cos(a), y, color=mau, **kw)


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    e0 = canh_voi(lay("do_doc"), goc.ANH, False)
    e1 = canh_voi(lay("do_doc"), goc.ANH, True)
    acc, alphas, r_max = lay("hough")(e1)
    acc = np.asarray(acc)
    dinh = goc.tim_dinh(acc, alphas, r_max)
    fig, ax = V.tao(1, 4, rong=16, cao=3.6)
    ax[0].imshow(goc.ANH, cmap="gray", vmin=0, vmax=255)
    ax[0].set_title("Ảnh sàn (nhiễu σ = 28)", color="white", fontsize=11.5, loc="left")
    ax[1].imshow(e0, cmap="gray")
    ax[1].set_title(f"Không làm mịn: {int(e0.sum())} cạnh", color="white", fontsize=11.5, loc="left")
    ax[2].imshow(e1, cmap="gray")
    _duong(ax[2], np.mean([d[0] for d in dinh]), np.mean([d[1] for d in dinh]), V.MAU["cam"], lw=2.4)
    ax[2].set_xlim(0, goc.W)
    ax[2].set_ylim(goc.H, 0)
    ax[2].set_title(f"Gauss rồi Sobel: {int(e1.sum())} cạnh", color="white", fontsize=11.5, loc="left")
    for a in ax[:3]:
        a.set_xticks([])
        a.set_yticks([])
        a.grid(False)
    ax[3].imshow(np.sqrt(acc).T, aspect="auto", cmap="magma", origin="lower",
                 extent=[-90, 90, -r_max, r_max])
    for a_d, r, v in dinh:
        ax[3].plot(a_d, r, "o", mfc="none", mec=V.MAU["lam"], ms=11, mew=2)
    ax[3].set_ylim(-50, 420)
    V.trang_tri(ax[3], f"Hough: đỉnh α = {dinh[0][0]:.0f}°", "α (độ)", "r (px)")
    ax[3].grid(False)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import thi_giac_cua_ban
        ve(thi_giac_cua_ban)
