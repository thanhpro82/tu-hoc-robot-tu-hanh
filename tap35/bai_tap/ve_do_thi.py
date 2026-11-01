"""Vẽ lần định vị của video trên bản đồ căn hộ (bộ lọc có thả hạt): bước 1 (rải khắp nhà), bước 4 (đã tìm ra),
bước 53 (vừa bị bắt cóc), bước 60 (tìm lại được). Tia LiDAR ở bước 4 vẽ bằng hàm quet của bạn.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import mcl as goc  # noqa: E402
from chung import ve as V  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    quet = ns["quet"] if isinstance(ns, dict) else getattr(ns, "quet")
    fig, axes = V.tao(1, 4, rong=16, cao=3.6)
    duong = np.array([r["x"][:2] for r in goc.LOG])
    for ax, k in zip(axes, [1, 4, 53, 60]):
        r = goc.LOG[k - 1]
        ax.imshow(goc.BAN_DO, origin="lower", extent=[0, goc.RONG, 0, goc.DAI], cmap="gray_r", vmin=0, vmax=1.6)
        P = r["tha"]["P"]
        ax.scatter(P[:, 0], P[:, 1], s=1.5, color=V.MAU["cam"], alpha=0.6)
        ax.plot(duong[:k, 0], duong[:k, 1], color=V.MAU["lam"], lw=1)
        ax.plot(*r["x"][:2], "o", color=V.MAU["luc"], ms=8, mfc="none", mew=2)
        if k == 4:
            d = np.asarray(quet(r["x"][None]))[0]
            for g, dd in zip(goc.GOC_TIA + r["x"][2], d):
                ax.plot([r["x"][0], r["x"][0] + dd * np.cos(g)], [r["x"][1], r["x"][1] + dd * np.sin(g)], color=V.MAU["vang"], lw=0.9)
        nhan = {1: "rải khắp nhà", 4: "đã tìm ra", 53: "vừa bị bắt cóc", 60: "tìm lại được"}[k]
        ax.set_title(f"bước {k}: {nhan} ({r['tha']['gan'] * 100:.0f}% hạt đúng chỗ)", color="white", fontsize=11, loc="left")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import mcl_cua_ban
        ve(mcl_cua_ban)
