"""Bài tập tập 3.4: bộ lọc hạt, ngàn phỏng đoán (Thuật toán 5, Mục 12.4.2 của sách). Dùng numpy.

Niềm tin là K = 1000 hạt; P là mảng (K, 3), mỗi hàng một phỏng đoán (x, y, θ); W là trọng số của các hạt (tổng = 1).
Robot đo khoảng cách tới 2 mốc: z = [d1, d2], nhiễu σ = 0,2 m.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/hat.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

MOC = np.array([[2.0, 4.0], [8.0, 4.0]])
SIG_Z = 0.2


def trong_so(P, z, W):
    """Bài 1 (bước 2 của thuật toán): trọng số mới = W · p(z | hạt), rồi chuẩn hoá cho tổng = 1.

    Với mỗi hạt: d_j = khoảng cách từ hạt tới mốc j − z_j  (j = 1, 2)
                 p(z | hạt) ∝ exp(−½ · Σ_j (d_j / SIG_Z)²)
    Trả về mảng K trọng số."""
    raise NotImplementedError("TODO Bài 1: trọng số")


def ess(w):
    """Bài 2: cỡ mẫu hiệu dụng ESS = 1 / Σ w_k². Mọi hạt nặng bằng nhau thì ESS = K; dồn hết vào 1 hạt thì ESS = 1."""
    raise NotImplementedError("TODO Bài 2: ESS")


def lay_mau_lai(w, r):
    """Bài 3 (bước 3): lấy mẫu lại kiểu hệ thống (low-variance), r là MỘT số ngẫu nhiên trong [0, 1).

    c = tổng dồn của w;  K mốc u_i = (r + i) / K, i = 0..K−1;  hạt được chọn cho mốc u_i là chỉ số đầu tiên có c ≥ u_i
    (gợi ý: np.searchsorted(c, u), rồi kẹp không vượt K − 1). Trả về mảng K chỉ số (hạt nặng được chọn nhiều lần)."""
    raise NotImplementedError("TODO Bài 3: lấy mẫu lại")
