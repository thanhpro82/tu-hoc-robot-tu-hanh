"""Vẽ ngôi nhà dựng lại nhìn từ trên xuống (trục x, z): trước và sau bundle adjustment, so với điểm thật và tâm camera thật.
(Phần ghép tuần tự + bundle adjustment là code video; bài tập của bạn là bước hai ảnh đầu tiên.)

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import sfm as goc  # noqa: E402
from chung import ve as V  # noqa: E402


def ve(ns=None, ra="ket_qua.png"):
    fig, axes = V.tao(1, 2, rong=12, cao=5.4)
    for ax, (ten, A, loi, tam, rms) in zip(axes, [("Ghép tuần tự", goc.A0, goc.LOI0, goc.TAM0, goc.RMS_TRUOC),
                                                   ("Sau bundle adjustment", goc.A1, goc.LOI1, goc.TAM1, goc.RMS_SAU)]):
        P = np.array(list(A.values()))
        ax.scatter(goc.P_THAT[:, 0], goc.P_THAT[:, 2], s=7, color=V.MAU["xam"], label="điểm thật")
        ax.scatter(P[:, 0], P[:, 2], s=7, color=V.MAU["luc"], alpha=0.8, label="điểm dựng lại")
        ax.plot(goc.TAM_CAM[:, 0], goc.TAM_CAM[:, 2], "o", color="white", ms=6, mfc="none", label="camera thật")
        ax.plot(tam[:, 0], tam[:, 2], "x", color=V.MAU["cam"], ms=8, mew=2, label="camera ước lượng")
        V.trang_tri(ax, f"{ten}: lệch {loi.mean() * 100:.1f} cm, {rms:.2f} px", "x (m)", "z (m)")
        ax.set_aspect("equal")
        V.chu_giai(ax, loc="lower left", fontsize=8.5)
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
