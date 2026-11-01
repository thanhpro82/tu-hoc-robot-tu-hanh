"""Vẽ lần chạy của video: (trái) đường đi của người, robot và quả bóng nhìn từ trên xuống;
(phải) khoảng cách thật và khoảng cách robot ước lượng từ khung YOLO, tô màu theo trạng thái.

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png (chạy lại mô phỏng của video, 30–60 giây)
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
from chung import ve as V  # noqa: E402
from kiem_tra import goc  # noqa: E402

MAU_TT = {"theo": V.MAU["luc"], "dừng": V.MAU["do"], "tìm": V.MAU["vang"]}


def ve(ns=None, ra="ket_qua.png"):
    log = goc().LOG
    fig, (a, b) = V.tao(1, 2, rong=12.5, cao=4.8, gridspec_kw={"width_ratios": [1, 1.25]})
    ng = np.array([r["nguoi"] for r in log])
    rb = np.array([r["robot"][:2] for r in log])
    bo = np.array([r["bong"] for r in log if r["bong"] is not None])
    a.plot(ng[:, 0], ng[:, 1], color=V.MAU["xanh"], lw=2.2, label="người")
    a.plot(rb[:, 0], rb[:, 1], color="white", lw=2.2, label="robot")
    a.plot(bo[:, 0], bo[:, 1], color=V.MAU["do"], lw=2.2, ls="--", label="bóng lăn qua")
    a.plot(rb[0, 0], rb[0, 1], "o", color=V.MAU["luc"], ms=7)
    V.trang_tri(a, "Nhìn từ trên xuống (32 giây)", "x (m)", "y (m)")
    a.set_aspect("equal", adjustable="datalim")
    V.chu_giai(a, loc="best", fontsize=8.8)
    t = [r["t"] for r in log]
    for r in log:
        b.axvspan(r["t"] - 0.05, r["t"] + 0.05, color=MAU_TT[r["trang_thai"]], alpha=0.12, lw=0)
    b.plot(t, [r["kc_that"] for r in log], color="white", lw=2, label="khoảng cách thật")
    b.plot(t, [r["z_hat"] if r["z_hat"] is not None else np.nan for r in log], color=V.MAU["cam"], lw=1.4,
           label="ước lượng từ khung YOLO")
    b.axhline(2.0, color=V.MAU["xam"], ls=":", lw=1.2)
    for tt, m in MAU_TT.items():
        b.plot([], [], color=m, lw=6, alpha=0.4, label=f"trạng thái: {tt}")
    V.trang_tri(b, "Giữ cách người 2 m", "thời gian (s)", "khoảng cách (m)")
    V.chu_giai(b, loc="upper right", fontsize=8.3)
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
