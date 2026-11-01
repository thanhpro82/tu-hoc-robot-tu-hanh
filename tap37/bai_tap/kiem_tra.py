"""Tự chấm bài tập tập 3.7. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Dữ liệu là lần chạy slam_toolbox THẬT trong ROS 2 (../ws/out/), đọc bằng ../sim/phan_tich.py; không cần cài ROS.
"""
import math
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import phan_tich as goc  # noqa: E402  (đọc ws/out: tư thế thật / odometry / slam_toolbox và ảnh /map)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

LOG_THO = goc.LOG          # mỗi 0,5 s: "that", "odo" (hệ thế giới), "slam" (hệ map của slam_toolbox)


def bai_1(ns):
    q, g = ham(ns, "goc_sang_quat"), ham(ns, "quat_sang_goc")
    for th in [0.0, 0.7, -2.5, math.pi / 2, 3.1]:
        assert gan(q(th), goc.R.quat(th)), f"goc_sang_quat({th}) phải ra {goc.R.quat(th)}, bạn ra {q(th)}"
        assert gan(g(*q(th)), th, 1e-9), f"quat_sang_goc(goc_sang_quat({th})) phải quay về {th}"
    return "đổi qua lại góc ↔ quaternion đúng (TF của ROS 2 dùng quaternion cho hướng)"


def bai_2(ns):
    f = ham(ns, "ve_goc")
    X0 = goc.X0
    THAT = np.array([f(r["that"], X0) for r in LOG_THO])
    ODO = np.array([f(r["odo"], X0) for r in LOG_THO])
    assert gan(THAT, goc.THAT) and gan(ODO, goc.ODO), "đổi hệ toạ độ chưa khớp (trừ X0 rồi xoay ngược X0_θ, bọc góc)"
    e_odo = np.hypot(*(ODO[:, :2] - THAT[:, :2]).T)
    e_slam = np.hypot(*(goc.SLAM[:, :2] - THAT[:, :2]).T)
    return (f"trong hệ gốc: odometry cuối lệch {e_odo[-1]:.2f} m, slam_toolbox chỉ lệch {e_slam[-1] * 100:.1f} cm "
            f"(trung bình {e_slam.mean() * 100:.1f} cm) như video")


def bai_3(ns):
    f = ham(ns, "ty_le_dung_tuong")
    tuong = np.zeros((10, 10), dtype=bool); tuong[2, :] = True
    M = np.zeros((10, 10)); M[2, 3] = M[2, 5] = M[7, 7] = 100
    assert gan(f(M, 0.0, 0.0, 0.1, tuong, 0.1), 2 / 3), "ví dụ nhỏ: 3 ô vật cản, 2 ô nằm trên hàng tường → 2/3"
    M, INFO = goc.MAPS[-1]
    ty = f(M, INFO["ox"] + goc.X0[0], INFO["oy"] + goc.X0[1], INFO["res"], goc.TUONG, goc.R.O)
    assert gan(ty, goc.NET_SLAM_MAP, 1e-9), f"bản đồ cuối của slam_toolbox: phải ra {goc.NET_SLAM_MAP * 100:.1f}%, bạn ra {ty * 100:.1f}%"
    return f"bản đồ slam_toolbox tự vẽ: {ty * 100:.1f}% ô tường nằm đúng tường thật (±10 cm), như video"


BAI = [("Bài 1 · góc và quaternion", bai_1), ("Bài 2 · đổi hệ toạ độ", bai_2), ("Bài 3 · chấm bản đồ /map", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "phan_tich_cua_ban", loi_giai)
