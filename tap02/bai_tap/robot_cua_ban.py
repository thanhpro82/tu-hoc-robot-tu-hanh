"""Bài tập tập 0.2: tự viết robot 2 bánh đầu tiên.

Làm lần lượt Bài 1 → 2 → 3 (các chỗ `raise NotImplementedError`), xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/robot_dau_tien.py và loi_giai.py (tự làm trước đã).
"""
import math

dt = 0.01  # mỗi bước 0.01 giây = 100 lần mỗi giây


def step(x, y, theta, v, omega):
    """Bài 1: từ trạng thái (x, y, θ) và lệnh (v, ω), tính trạng thái sau dt giây.

    Robot chạy theo hướng mũi xe θ với tốc độ v, và quay với tốc độ ω:
        x mới = x + v·cos θ·dt,   y mới = y + v·sin θ·dt,   θ mới = θ + ω·dt
    Trả về tuple (x, y, theta)."""
    raise NotImplementedError("TODO Bài 1: cập nhật x, y, theta")


def omega_so_8(t):
    """Bài 2: lệnh quay ω tại thời điểm t (giây) để robot chạy hình số 8 với v = 0,5 m/s.

    Gợi ý: một vòng tròn với ω = 1 rad/s mất 2π giây. Vòng đầu quay trái (ω = +1), vòng sau quay phải (ω = −1)."""
    raise NotImplementedError("TODO Bài 2: trả về +1.0 hoặc -1.0 tuỳ t")


def lenh_vong_tron(R, T):
    """Bài 3: muốn robot chạy đúng 1 vòng tròn bán kính R (m) trong T giây, cần lệnh (v, ω) bao nhiêu?

    Gợi ý: quãng đường 1 vòng là 2πR, góc quay 1 vòng là 2π. Trả về tuple (v, omega)."""
    raise NotImplementedError("TODO Bài 3: trả về (v, omega)")
