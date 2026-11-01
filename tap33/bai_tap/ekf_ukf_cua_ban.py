"""Bài tập tập 3.3: EKF và UKF, Kalman cho thế giới cong (Mục 12.3 của sách). Dùng numpy.

Trạng thái robot x = [p_x, p_y, θ]; lệnh u = (v, ω); mốc ℓ = (ℓ_x, ℓ_y).
Chuyển động (unicycle):  f(x, u) = [p_x + v·dt·cos θ,  p_y + v·dt·sin θ,  θ + ω·dt]
Đo tới mốc (Ví dụ 12.3.1): h(x, ℓ) = [√(Δx² + Δy²),  atan2(Δy, Δx) − θ],  với Δx = ℓ_x − p_x, Δy = ℓ_y − p_y
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/ekf_ukf.py (tự làm trước đã).
"""
import numpy as np

ALPHA, BETA, KAPPA = 1.0, 2.0, 0.0


def F_jac(x, u, dt):
    """Bài 1 (EKF): ma trận Jacobi F = ∂f/∂x (3×3) tại x. Chỉ θ làm vị trí đổi phi tuyến:

        F = [[1, 0, −v·dt·sin θ],
             [0, 1,  v·dt·cos θ],
             [0, 0,  1         ]]"""
    raise NotImplementedError("TODO Bài 1: Jacobi của chuyển động")


def H_jac(x, l):
    """Bài 2 (EKF): ma trận Jacobi H = ∂h/∂x (2×3) của phép đo khoảng cách + góc tới mốc l.

    Với Δx = l_x − p_x, Δy = l_y − p_y, q = Δx² + Δy², r = √q:
        H = [[−Δx/r, −Δy/r,  0],
             [ Δy/q, −Δx/q, −1]]"""
    raise NotImplementedError("TODO Bài 2: Jacobi của phép đo")


def diem_sigma(mu, Sig):
    """Bài 3 (UKF): 2n + 1 điểm sigma và trọng số (n = len(mu)).

    λ = α²(n + κ) − n;  L = cholesky((n + λ)·Σ)  (np.linalg.cholesky, cột i là L[:, i])
    Điểm: X_0 = μ,  X_i = μ + L[:, i],  X_{n+i} = μ − L[:, i]   (i = 0..n−1, xếp đúng thứ tự này)
    Trọng số: Wm = Wc = 1 / (2(n + λ)) cho mọi điểm, trừ Wm[0] = λ/(n + λ), Wc[0] = λ/(n + λ) + (1 − α² + β).
    Trả về (X dạng mảng (2n+1, n), Wm, Wc)."""
    raise NotImplementedError("TODO Bài 3: điểm sigma")
