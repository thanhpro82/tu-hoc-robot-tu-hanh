"""Bài tập tập 3.2: bộ lọc Kalman (Thuật toán 1, Mục 12.2 của sách, Ví dụ 12.2.1). Dùng numpy.

Trạng thái x = [vị trí p, vận tốc v]; điều khiển u = gia tốc đo được (gia tốc kế); đo z = vị trí (cảm biến khoảng cách).
    x_t = A·x_{t−1} + B·u_t + ε,  ε ~ N(0, Q)          z_t = C·x_t + δ,  δ ~ N(0, R)
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/kalman.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

DT = 0.1
SIGMA_A, SIGMA_Z = 0.3, 0.3
A = np.array([[1, DT], [0, 1]])
B = np.array([DT ** 2 / 2, DT])
C = np.array([[1.0, 0.0]])
Q = np.outer(B, B) * SIGMA_A ** 2
R = np.array([[SIGMA_Z ** 2]])


def du_doan(mu, Sig, u):
    """Bài 1 (dự đoán): đẩy niềm tin (μ, Σ) tới một bước.

        μ̄ = A·μ + B·u          Σ̄ = A·Σ·Aᵀ + Q
    Trả về (mu_b, Sig_b)."""
    raise NotImplementedError("TODO Bài 1: dự đoán")


def cap_nhat(mu_b, Sig_b, z):
    """Bài 2 (cập nhật): trộn dự đoán với số đo z (một số, vị trí đo được).

        S = C·Σ̄·Cᵀ + R           K = Σ̄·Cᵀ·S⁻¹            (K hình 2×1)
        μ = μ̄ + K·(z − C·μ̄)
        Σ = (I − K·C)·Σ̄·(I − K·C)ᵀ + K·R·Kᵀ                (dạng Joseph, giữ Σ đối xứng, dương)
    Trả về (mu, Sig, K)."""
    raise NotImplementedError("TODO Bài 2: cập nhật")


def loc_kalman(ds_u, ds_z, mu0, Sig0):
    """Bài 3: chạy bộ lọc qua cả chuỗi. Mỗi bước k: du_doan với ds_u[k], rồi cap_nhat với ds_z[k].

    Trả về list các μ (mỗi bước một mảng 2 số: vị trí, vận tốc) sau cập nhật."""
    raise NotImplementedError("TODO Bài 3: vòng lặp Kalman")
