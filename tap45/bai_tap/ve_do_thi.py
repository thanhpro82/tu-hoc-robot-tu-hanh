"""Vẽ: (trái) đường học của mạng luyện 500 lần trong video (đọc ../sim/pi_sach_0.pt);
(phải) 8 robot cùng bố cục vật cản: chưa học (đi bừa) và đã học. Tham số `ns` không dùng (mạng đã luyện sẵn).

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png
"""
import sys
from pathlib import Path

import numpy as np
import torch

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import deeprl as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import nap  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402


def _quy_dao(pi, layout, n=8, seed=7):
    torch.manual_seed(seed)
    env = goc.MoiTruong(n, np.random.default_rng(seed))
    with torch.no_grad():
        _, _, _, xs = goc.chay_tap(pi, env, layout=layout, ghi=True)
    return np.array(xs), env.ket


def ve(ns=None, ra="ket_qua.png"):
    ls = torch.load(_D.parent / "sim" / "pi_sach_0.pt", weights_only=False)["lich_su"]
    env0 = goc.MoiTruong(40, np.random.default_rng(29))
    env0.reset()
    layout = env0.layout(29)
    fig, (a, b, c) = V.tao(1, 3, rong=15, cao=4.6, gridspec_kw={"width_ratios": [1.2, 1, 1]})
    k = [x[0] for x in ls]
    a.plot(k, [x[1] * 100 for x in ls], color=V.MAU["luc"], lw=2.2, label="tới đích")
    a.plot(k, [x[2] * 100 for x in ls], color=V.MAU["do"], lw=2.2, label="va chạm")
    V.trang_tri(a, "Luyện 500 lần cập nhật (64 robot mỗi lần)", "lần cập nhật", "% số robot")
    V.chu_giai(a, loc="center right")
    torch.manual_seed(0)
    for ax, (ten, pi) in zip((b, c), [("Chưa học", goc.ChinhSach()), ("Đã học", nap("pi_sach_0.pt"))]):
        xs, ket = _quy_dao(pi, layout)
        for (cx, cy), r in zip(layout[0], layout[1]):
            if r > 0:
                ax.add_patch(Circle((cx, cy), r, fc="#475569", ec="none"))
        for i in range(xs.shape[1]):
            ax.plot(xs[:, i, 0], xs[:, i, 1], color=V.MAU["luc"] if ket[i] == 1 else V.MAU["do"], lw=1.4)
        ax.plot(*layout[2][:2], "o", color="white", ms=7)
        ax.add_patch(Circle(layout[3], goc.R_DICH, fc="none", ec=V.MAU["vang"], lw=2))
        ax.set_xlim(0, goc.RONG); ax.set_ylim(0, goc.RONG); ax.set_aspect("equal")
        V.trang_tri(ax, f"{ten}: {int((ket == 1).sum())}/8 tới đích")
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
