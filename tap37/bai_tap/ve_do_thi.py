"""Vẽ lần chạy slam_toolbox thật: (trái) bản đồ /map cuối cùng slam_toolbox tự vẽ, cùng quỹ đạo thật, odometry và slam
(đổi hệ bằng ve_goc của bạn); (phải) sai số vị trí theo thời gian.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import phan_tich as goc  # noqa: E402
from chung import ve as V  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    f = ns["ve_goc"] if isinstance(ns, dict) else getattr(ns, "ve_goc")
    THAT = np.array([f(r["that"], goc.X0) for r in goc.LOG])
    ODO = np.array([f(r["odo"], goc.X0) for r in goc.LOG])
    M, INFO = goc.MAPS[-1]
    fig, (a, b) = V.tao(1, 2, rong=13, cao=4.8, gridspec_kw={"width_ratios": [1.35, 1]})
    hien = np.where(M == 100, 1.0, np.where(M == 0, 0.0, 0.45))
    ny, nx = M.shape
    a.imshow(hien, origin="lower", cmap="gray_r", extent=[INFO["ox"], INFO["ox"] + nx * INFO["res"], INFO["oy"], INFO["oy"] + ny * INFO["res"]])
    a.plot(THAT[:, 0], THAT[:, 1], color=V.MAU["luc"], lw=2.4, label="thật")
    a.plot(ODO[:, 0], ODO[:, 1], color=V.MAU["do"], lw=1.6, label="odometry")
    a.plot(goc.SLAM[:, 0], goc.SLAM[:, 1], color=V.MAU["xanh"], lw=1.6, ls="--", label="slam_toolbox")
    a.set_title(f"Bản đồ /map slam_toolbox tự vẽ ({goc.NET_SLAM_MAP * 100:.1f}% ô đúng tường)", color="white", fontsize=11.5, loc="left")
    a.set_xticks([]); a.set_yticks([]); a.grid(False)
    V.chu_giai(a, loc="upper right", fontsize=8.5)
    e_odo = np.hypot(*(ODO[:, :2] - THAT[:, :2]).T)
    e_slam = np.hypot(*(goc.SLAM[:, :2] - THAT[:, :2]).T)
    b.plot(goc.T, e_odo * 100, color=V.MAU["do"], lw=2, label=f"odometry: cuối {e_odo[-1] * 100:.0f} cm")
    b.plot(goc.T, e_slam * 100, color=V.MAU["xanh"], lw=2, label=f"slam_toolbox: cuối {e_slam[-1] * 100:.1f} cm")
    V.trang_tri(b, "Sai số vị trí (ROS 2 chạy thật)", "thời gian (s)", "sai số (cm)")
    V.chu_giai(b, loc="upper left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import phan_tich_cua_ban
        ve(phan_tich_cua_ban)
