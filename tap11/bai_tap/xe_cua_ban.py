"""Bài tập tập 1.1: vì sao xe không đi ngang được?

Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/khong_di_ngang.py (tự làm trước đã).
"""
import math

dt = 0.01
L = 0.30                     # chiều dài cơ sở ô tô (trục trước tới trục sau), mét
PHI_MAX = math.radians(30)   # góc lái tối đa


def step_car(x, y, theta, v, phi):
    """Bài 1: mô hình ô tô (bicycle model), toạ độ (x, y) đặt ở giữa trục sau, phi = góc lái bánh trước.

    1. Kẹp phi trong khoảng [−PHI_MAX, PHI_MAX] (tay lái không quay quá 30°).
    2. Cập nhật:  x += v·cos θ·dt,  y += v·sin θ·dt,  θ += v·tan(φ)/L·dt
    Trả về (x, y, theta)."""
    raise NotImplementedError("TODO Bài 1: mô hình ô tô")


def van_toc_ngang(path):
    """Bài 2: kiểm tra ràng buộc "bánh xe không trượt ngang".

    path là danh sách (x, y, theta, ...) cách nhau dt giây. Với mỗi cặp điểm liền nhau a, b:
        vx = (b.x − a.x)/dt,  vy = (b.y − a.y)/dt
        vận tốc ngang thân xe = |vx·sin θ_a − vy·cos θ_a|
    Trả về giá trị LỚN NHẤT trên cả đường đi (m/s)."""
    raise NotImplementedError("TODO Bài 2: vận tốc ngang lớn nhất")


def ke_hoach_do_xe(d, L, phi_max):
    """Bài 3: đỗ xe song song, dời ngang d mét bằng cách lùi 2 cung tròn ngược chiều nhau.

    - Bán kính quay nhỏ nhất (đánh lái hết cỡ): R = L / tan(phi_max)
    - Mỗi cung quay góc α thì dời ngang R·(1 − cos α), hai cung dời 2R(1 − cos α) = d
    Trả về (R, alpha), alpha tính bằng radian."""
    raise NotImplementedError("TODO Bài 3: trả về (R, alpha)")
