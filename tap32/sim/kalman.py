"""Tập 3.2 - Kalman Filter dễ hiểu nhất (series Tự Học Robot Tự Hành)

Theo Principles of Robot Autonomy (Ch. 11 giới thiệu, công thức ở §12.2):
  - Mô hình (Eq. 12.3-12.4): x_t = A x_t-1 + B u_t + ε, ε ~ N(0, Q); z_t = C x_t + δ, δ ~ N(0, R)
  - Ví dụ 12.2.1: x = [p, v], A = [[1, Δt], [0, 1]], B = [Δt²/2, Δt], C = [1, 0] (đo vị trí)
  - Thuật toán 1: dự đoán μ̄ = Aμ + Bu, Σ̄ = AΣAᵀ + Q; S = CΣ̄Cᵀ + R; K = Σ̄CᵀS⁻¹;
    μ = μ̄ + K(z − Cμ̄), Σ = (I − KC)Σ̄(I − KC)ᵀ + KRKᵀ (dạng Joseph)
Mở rộng / giả định: hồ sơ gia tốc, nhiễu gia tốc kế σ_a = 0,3 m/s² và lệch 0,02 m/s², cảm biến khoảng cách σ = 0,3 m,
Δt = 0,1 s, chạy 20 s. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 kalman.py
"""
import numpy as np

RNG = np.random.default_rng(32)
DT, T = 0.1, 20.0
N = int(T / DT)
SIGMA_A, LECH_A = 0.3, 0.02  # gia tốc kế: nhiễu và lệch
SIGMA_Z = 0.3  # cảm biến khoảng cách
A = np.array([[1, DT], [0, 1]])
B = np.array([DT ** 2 / 2, DT])
C = np.array([[1.0, 0.0]])
Q = np.outer(B, B) * SIGMA_A ** 2  # nhiễu quá trình do gia tốc đo sai
R = np.array([[SIGMA_Z ** 2]])


def gia_toc(t):
    """Hồ sơ gia tốc thật: tăng tốc, chạy đều, phanh."""
    if t < 4:
        return 0.5
    if t < 12:
        return 0.0
    if t < 16:
        return -0.4
    return 0.1


def chay():
    x = np.array([0.0, 0.0])
    mu = np.array([0.0, 0.0]); Sig = np.diag([1.0, 0.5])
    dr = np.array([0.0, 0.0])  # chỉ tích phân gia tốc kế (không cảm biến)
    log = []
    for k in range(1, N + 1):
        t = k * DT
        a = gia_toc(t - DT)
        x = A @ x + B * a
        u = a + LECH_A + RNG.normal(0, SIGMA_A)  # gia tốc kế đo được
        z = x[0] + RNG.normal(0, SIGMA_Z)  # cảm biến khoảng cách
        dr = A @ dr + B * u
        # Kalman: dự đoán
        mu_b = A @ mu + B * u
        Sig_b = A @ Sig @ A.T + Q
        # cập nhật
        S = C @ Sig_b @ C.T + R
        K = Sig_b @ C.T @ np.linalg.inv(S)
        mu = mu_b + (K @ (np.array([z]) - C @ mu_b)).ravel()
        IKC = np.eye(2) - K @ C
        Sig = IKC @ Sig_b @ IKC.T + K @ R @ K.T
        log.append({"t": t, "p": x[0], "v": x[1], "z": z, "dr": dr[0], "mu_b": mu_b[0], "sig_b": float(np.sqrt(Sig_b[0, 0])),
                    "mu": mu[0], "sig": float(np.sqrt(Sig[0, 0])), "K": float(K[0, 0]), "u": u})
    return log


LOG = chay()

if __name__ == "__main__":
    p = np.array([r["p"] for r in LOG])
    z = np.array([r["z"] for r in LOG])
    mu = np.array([r["mu"] for r in LOG])
    dr = np.array([r["dr"] for r in LOG])
    rms = lambda e: float(np.sqrt(np.mean(e ** 2)))
    print(f"{N} bước × {DT} s · quãng đường thật {p[-1]:.2f} m · Q từ σ_a = {SIGMA_A}, R = σ_z² = {SIGMA_Z}²")
    print(f"Chỉ cảm biến khoảng cách: sai RMS {rms(z - p) * 100:.1f} cm, lớn nhất {np.max(np.abs(z - p)) * 100:.1f} cm")
    print(f"Chỉ tích phân gia tốc kế: cuối cùng lệch {abs(dr[-1] - p[-1]):.2f} m")
    print(f"Kalman: sai RMS {rms(mu - p) * 100:.1f} cm, lớn nhất {np.max(np.abs(mu - p)) * 100:.1f} cm · "
          f"tốt hơn cảm biến {rms(z - p) / rms(mu - p):.1f} lần")
    print(f"K (vị trí) bước 1 = {LOG[0]['K']:.3f}, bước 10 = {LOG[9]['K']:.3f}, cuối = {LOG[-1]['K']:.3f}")
    print(f"σ sau cập nhật cuối = {LOG[-1]['sig'] * 100:.1f} cm (cảm biến {SIGMA_Z * 100:.0f} cm, dự đoán {LOG[-1]['sig_b'] * 100:.1f} cm)")
    k = 50
    r = LOG[k]
    print(f"Ví dụ bước {k + 1} (t = {r['t']:.1f} s): dự đoán {r['mu_b']:.2f} ± {r['sig_b'] * 100:.1f} cm, đo {r['z']:.2f} ± {SIGMA_Z * 100:.0f} cm "
          f"-> sau {r['mu']:.2f} ± {r['sig'] * 100:.1f} cm (thật {r['p']:.2f}) · K = {r['K']:.3f}")
