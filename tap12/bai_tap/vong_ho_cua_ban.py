"""Bài tập tập 1.2: nhắm mắt mà chạy, điều khiển vòng hở.

Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/vong_ho.py và loi_giai.py (tự làm trước đã).
"""
import math


def ke_hoach_vuong(canh, v, t_quay):
    """Bài 1: lập sẵn chuỗi lệnh cho robot 2 bánh chạy 1 vòng hình vuông cạnh `canh` mét, ngược chiều kim đồng hồ.

    Mỗi lệnh là tuple (số giây, v, ω). Mỗi cạnh gồm 2 lệnh:
      - chạy thẳng hết cạnh với tốc độ v (ω = 0),
      - đứng yên quay trái 90° (v = 0) trong đúng t_quay giây.
    Trả về list 8 lệnh (4 cạnh)."""
    raise NotImplementedError("TODO Bài 1: list 8 tuple (giây, v, ω)")


def thoi_gian_nhanh_nhat(d, v_max, a_max):
    """Bài 2: thời gian ngắn nhất để chạy d mét, xuất phát và dừng hẳn, với |v| ≤ v_max và |gia tốc| ≤ a_max.

    Cách nhanh nhất: tăng tốc hết cỡ → chạy đều v_max → phanh hết cỡ (đồ thị v là hình thang).
      - Tăng tốc tới v_max mất v_max/a_max giây và đi được v_max²/(2·a_max) mét; phanh cũng vậy.
      - Nếu d quá ngắn, chưa kịp tới v_max đã phải phanh: đồ thị thành hình tam giác, T = 2·√(d/a_max).
    Trả về T (giây)."""
    raise NotImplementedError("TODO Bài 2: trả về T")


def van_toc_luc(t, d, v_max, a_max):
    """Bài 3: tốc độ tại thời điểm t (giây) trên đồ thị hình thang của Bài 2.

    Gợi ý: với T = thoi_gian_nhanh_nhat(...), tốc độ là số nhỏ nhất trong 3 giới hạn:
    a_max·t (đang tăng tốc), v_max (chạy đều), a_max·(T − t) (đang phanh). Ngoài [0, T] thì bằng 0.
    Nhớ trường hợp hình tam giác: đỉnh lúc đó thấp hơn v_max."""
    raise NotImplementedError("TODO Bài 3: trả về v tại thời điểm t")
