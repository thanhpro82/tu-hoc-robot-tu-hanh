"""Bài tập tập 1.4: bám quỹ đạo số 8 bằng phẳng vi phân (Ví dụ 3.1.2 của sách).

Robot: unicycle mở rộng, trạng thái (x, y, v, θ), lệnh (a, ω) với a là gia tốc tới, ω là tốc độ quay.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/bam_quy_dao.py và loi_giai.py (tự làm trước đã).
"""
import math


def tinh_san(dx, dy, ddx, ddy):
    """Bài 1 (phẳng vi phân): biết vận tốc (ẋ, ẏ) và gia tốc (ẍ, ÿ) của điểm cần đi qua, suy ra v, θ, a, ω.

        v = √(ẋ² + ẏ²)                θ = atan2(ẏ, ẋ)
        a = (ẋ·ẍ + ẏ·ÿ) / v           ω = (ẋ·ÿ − ẏ·ẍ) / v²
    Trả về (v, theta, a, omega)."""
    raise NotImplementedError("TODO Bài 1: trả về (v, theta, a, omega)")


def dieu_khien_ao(xd, yd, dxd, dyd, ddxd, ddyd, x, y, v, th, kp, kd):
    """Bài 2: điều khiển ảo (feedforward + feedback) cho hai đầu ra x, y.

    (xd, yd), (dxd, dyd), (ddxd, ddyd): vị trí, vận tốc, gia tốc của robot ảo trên hình số 8.
    (x, y, v, th): trạng thái robot thật; vận tốc thật là (v·cos θ, v·sin θ).
        w1 = ẍ_d + kp·(x_d − x) + kd·(ẋ_d − ẋ)
        w2 = ÿ_d + kp·(y_d − y) + kd·(ẏ_d − ẏ)
    Trả về (w1, w2)."""
    raise NotImplementedError("TODO Bài 2: trả về (w1, w2)")


def doi_lenh(w1, w2, th, v):
    """Bài 3: đổi (w1, w2) về lệnh thật (a, ω) bằng cách giải  J·[a, ω] = [w1, w2],

        J = [[cos θ, −v·sin θ],
             [sin θ,  v·cos θ]]
    Gợi ý: J⁻¹ có công thức gọn:  a = cos θ·w1 + sin θ·w2,   ω = (−sin θ·w1 + cos θ·w2) / v.
    Trả về (a, omega)."""
    raise NotImplementedError("TODO Bài 3: trả về (a, omega)")
