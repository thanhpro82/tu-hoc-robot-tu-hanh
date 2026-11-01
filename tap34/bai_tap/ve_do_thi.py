"""Vẽ đám hạt ở 4 thời điểm (bộ lọc chạy bằng hàm của bạn): ban đầu, bước 1 (2 cụm soi gương), bước 9 (tin nhầm), bước 12 (đã rẽ, gom về đúng chỗ).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import hat as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import chay_lai  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    log = chay_lai(lay("trong_so"), lay("ess"), lay("lay_mau_lai"))
    chon = [log[0]] + [[r for r in log if r["k"] == k and r["buoc"] == "trọng số"][0] for k in (1, 9, 12)]
    duong = np.array([r["x"][:2] for r in log])
    fig, axes = V.tao(1, 4, rong=16, cao=3.9)
    for ax, r in zip(axes, chon):
        w = r["w"] / r["w"].max()
        mau = np.tile([0.976, 0.451, 0.086, 0.0], (len(w), 1))
        mau[:, 3] = 0.08 + 0.8 * w      # hạt càng nặng càng đậm
        ax.scatter(r["P"][:, 0], r["P"][:, 1], s=4 + 20 * w, color=mau)
        ax.plot(duong[: 2 * r["k"] + 1, 0], duong[: 2 * r["k"] + 1, 1], color="white", lw=1.2)
        ax.plot(*r["x"][:2], "o", color="white", ms=8, mfc="none", mew=2)
        ax.plot(r["x"][0], 2 * goc.MOC[0, 1] - r["x"][1], "x", color=V.MAU["lam"], ms=9, mew=2)
        ax.scatter(goc.MOC[:, 0], goc.MOC[:, 1], marker="*", s=200, color=V.MAU["vang"], zorder=5)
        ax.axhline(goc.MOC[0, 1], color=V.MAU["xam"], ls=":", lw=1)
        gan, guong, _ = goc.thong_ke(r)
        V.trang_tri(ax, f"bước {r['k']}: thật {gan * 100:.0f}% · gương {guong * 100:.0f}%")
        ax.set_xlim(0, goc.RONG)
        ax.set_ylim(0, goc.DAI)
        ax.set_aspect("equal")
    fig.suptitle("○ vị trí thật · × vị trí soi gương qua đường nối 2 mốc ★ (đo khoảng cách không phân biệt được hai chỗ này)",
                 color=V.CHU, fontsize=10.5, x=0.01, ha="left", y=0.99)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import hat_cua_ban
        ve(hat_cua_ban)
