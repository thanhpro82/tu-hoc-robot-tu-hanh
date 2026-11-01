"""Bài tập tập 3.7: đọc và chấm kết quả slam_toolbox chạy thật trong ROS 2 (dữ liệu có sẵn ở ../ws/out/). Dùng numpy.

ROS 2 lưu hướng của robot bằng quaternion (x, y, z, w); bản đồ /map là lưới ô: −1 chưa biết, 0 trống, 100 có vật cản,
kèm toạ độ góc dưới trái (ox, oy) và cỡ ô res (mét).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../ws/robot_gia.py, ../sim/phan_tich.py và loi_giai.py (tự làm trước đã).
"""
import math

import numpy as np


def goc_sang_quat(th):
    """Bài 1a: robot quay quanh trục z một góc th → quaternion (x, y, z, w) = (0, 0, sin(th/2), cos(th/2))."""
    raise NotImplementedError("TODO Bài 1a")


def quat_sang_goc(x, y, z, w):
    """Bài 1b: quaternion → góc quay quanh z (yaw): atan2(2(w·z + x·y), 1 − 2(y² + z²))."""
    raise NotImplementedError("TODO Bài 1b")


def ve_goc(p, X0):
    """Bài 2: đổi tư thế p = (x, y, θ) trong hệ thế giới sang hệ gốc đặt tại điểm xuất phát X0 (hệ odom/map của ROS lúc đầu).

    dx = p_x − X0_x, dy = p_y − X0_y; xoay ngược một góc X0_θ:
        [cos(−X0_θ)·dx − sin(−X0_θ)·dy,  sin(−X0_θ)·dx + cos(−X0_θ)·dy,  góc(p_θ − X0_θ)]
    (góc bọc về [−π, π)). Trả về mảng 3 số."""
    raise NotImplementedError("TODO Bài 2: đổi hệ toạ độ")


def ty_le_dung_tuong(M, ox, oy, res, tuong, o_tuong):
    """Bài 3: bản đồ /map M (mảng cao × rộng) có bao nhiêu % ô vật cản (giá trị 100) nằm đúng tường thật?

    Ô (hàng i, cột j) của M có tâm ở (ox + (j + 0.5)·res,  oy + (i + 0.5)·res) mét.
    tuong là lưới tường thật (True/False) với cỡ ô o_tuong, góc ở (0, 0): điểm (x, y) rơi vào tuong[int(y/o_tuong), int(x/o_tuong)].
    Chỉ tính các ô rơi vào trong lưới tuong. Trả về tỉ lệ (0..1)."""
    raise NotImplementedError("TODO Bài 3: độ chính xác bản đồ")
