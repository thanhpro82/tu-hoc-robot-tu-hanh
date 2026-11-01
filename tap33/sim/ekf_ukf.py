"""Tập 3.3 - EKF & UKF: Kalman cho thế giới cong (series Tự Học Robot Tự Hành)

Theo Chương 12 (§12.3), Principles of Robot Autonomy:
  - Mô hình phi tuyến (Eq. 12.5): x_t = f(x_t-1, u_t) + ε, ε ~ N(0, Q); z_t = h(x_t) + δ, δ ~ N(0, R)
  - EKF (Thuật toán 2): F_t = ∂f/∂x tại μ_t-1, H_t = ∂h/∂x tại μ̄_t; μ̄ = f(μ, u), Σ̄ = FΣFᵀ + Q; K = Σ̄Hᵀ(HΣ̄Hᵀ + R)⁻¹
  - UKF (Thuật toán 3): 2n + 1 điểm sigma, λ = α²(n + κ) − n, trọng số W_m, W_c; đưa điểm qua f, h thật, gộp lại
  - Ví dụ 12.3.1: tư thế [p_x, p_y, θ], đo khoảng cách và góc tới mốc ℓ: h = [√(Δx² + Δy²), atan2(Δy, Δx) − θ]
Phần A: biến đổi một phân bố Gauss qua chuyển động cong khi hướng còn mơ hồ; "sự thật" = 100.000 mẫu Monte Carlo.
Phần B: định vị robot unicycle: tốc độ từ encoder, tốc độ quay từ IMU, đo khoảng cách + góc tới 2 mốc mỗi 1 s.
Mở rộng / giả định: mọi tham số nhiễu, quỹ đạo, vị trí mốc, α = 1, β = 2, κ = 0. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 ekf_ukf.py
"""
import numpy as np

RNG = np.random.default_rng(33)
ALPHA, BETA, KAPPA = 1.0, 2.0, 0.0


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def diem_sigma(mu, Sig):
    n = len(mu)
    lam = ALPHA ** 2 * (n + KAPPA) - n
    Lc = np.linalg.cholesky((n + lam) * Sig)
    X = [mu] + [mu + Lc[:, i] for i in range(n)] + [mu - Lc[:, i] for i in range(n)]
    Wm = np.full(2 * n + 1, 1 / (2 * (n + lam)))
    Wc = Wm.copy()
    Wm[0] = lam / (n + lam)
    Wc[0] = lam / (n + lam) + (1 - ALPHA ** 2 + BETA)
    return np.array(X), Wm, Wc


def tb_goc(Y, W, cot_goc):
    """Trung bình có trọng số, riêng cột góc lấy trung bình trên vòng tròn."""
    m = W @ Y
    for c in cot_goc:
        m[c] = np.arctan2(W @ np.sin(Y[:, c]), W @ np.cos(Y[:, c]))
    return m


# ---------------- Phần A: một bước chuyển động cong ----------------
def f(x, u, dt):
    """Unicycle (tập 1.1): x' = x + v·dt·cosθ, y' = y + v·dt·sinθ, θ' = θ + ω·dt."""
    px, py, th = x
    v, w = u
    return np.array([px + v * dt * np.cos(th), py + v * dt * np.sin(th), goc(th + w * dt)])


def F_jac(x, u, dt):
    th = x[2]
    v = u[0]
    return np.array([[1, 0, -v * dt * np.sin(th)], [0, 1, v * dt * np.cos(th)], [0, 0, 1]])


MU_A = np.array([0.0, 0.0, 0.0])
SIG_A = np.diag([0.05 ** 2, 0.05 ** 2, np.radians(35) ** 2])  # hướng mơ hồ ±35°
U_A, DT_A = (2.0, 0.0), 1.0  # đi thẳng 2 m

mc = np.array([f(x, U_A, DT_A) for x in RNG.multivariate_normal(MU_A, SIG_A, 100_000)])
MC_MU, MC_COV = mc[:, :2].mean(0), np.cov(mc[:, :2].T)
EKF_MU = f(MU_A, U_A, DT_A)[:2]
Fa = F_jac(MU_A, U_A, DT_A)
EKF_COV = (Fa @ SIG_A @ Fa.T)[:2, :2]
Xs, Wm, Wc = diem_sigma(MU_A, SIG_A)
Ys = np.array([f(x, U_A, DT_A) for x in Xs])
UKF_MU = Wm @ Ys[:, :2]
UKF_COV = sum(Wc[i] * np.outer(Ys[i, :2] - UKF_MU, Ys[i, :2] - UKF_MU) for i in range(len(Xs)))
MC_MAU = mc[RNG.choice(len(mc), 1500, replace=False), :2]

# ---------------- Phần B: định vị robot ----------------
DT, T = 0.1, 60.0
MOC = np.array([[4.0, 6.0], [-4.0, -2.0]])
SIG_V, SIG_W = 0.08, np.radians(3)  # nhiễu encoder (m/s), IMU (rad/s)
LECH_W = np.radians(1.0)  # IMU lệch nhẹ
SIG_R, SIG_B = 0.15, np.radians(4)  # cảm biến khoảng cách, góc
Q = np.diag([(SIG_V * DT) ** 2, (SIG_V * DT) ** 2, (SIG_W * DT) ** 2]) * 2
R = np.diag([SIG_R ** 2, SIG_B ** 2])


def h(x, l):
    dx, dy = l[0] - x[0], l[1] - x[1]
    return np.array([np.hypot(dx, dy), goc(np.arctan2(dy, dx) - x[2])])


def H_jac(x, l):
    dx, dy = l[0] - x[0], l[1] - x[1]
    q = dx ** 2 + dy ** 2
    r = np.sqrt(q)
    return np.array([[-dx / r, -dy / r, 0], [dy / q, -dx / q, -1]])


def lenh(t):
    """Quỹ đạo: vòng tròn rồi số 8 nhẹ."""
    return 0.6, 0.25 * np.sin(2 * np.pi * t / 30) + 0.12


def ekf_buoc(mu, Sig, u, zs):
    F = F_jac(mu, u, DT)
    mu = f(mu, u, DT)
    Sig = F @ Sig @ F.T + Q
    for z, l in zs:
        H = H_jac(mu, l)
        S = H @ Sig @ H.T + R
        K = Sig @ H.T @ np.linalg.inv(S)
        y = z - h(mu, l); y[1] = goc(y[1])
        mu = mu + K @ y; mu[2] = goc(mu[2])
        IKH = np.eye(3) - K @ H
        Sig = IKH @ Sig @ IKH.T + K @ R @ K.T
    return mu, Sig


def ukf_buoc(mu, Sig, u, zs):
    X, Wm_, Wc_ = diem_sigma(mu, Sig)
    Y = np.array([f(x, u, DT) for x in X])
    mu = tb_goc(Y, Wm_, [2])
    d = Y - mu; d[:, 2] = goc(d[:, 2])
    Sig = (Wc_[:, None] * d).T @ d + Q
    for z, l in zs:
        X, Wm_, Wc_ = diem_sigma(mu, Sig)
        Z = np.array([h(x, l) for x in X])
        zh = tb_goc(Z, Wm_, [1])
        dz = Z - zh; dz[:, 1] = goc(dz[:, 1])
        dx = X - mu; dx[:, 2] = goc(dx[:, 2])
        S = (Wc_[:, None] * dz).T @ dz + R
        Pxz = (Wc_[:, None] * dx).T @ dz
        K = Pxz @ np.linalg.inv(S)
        y = z - zh; y[1] = goc(y[1])
        mu = mu + K @ y; mu[2] = goc(mu[2])
        Sig = Sig - K @ S @ K.T
        Sig = (Sig + Sig.T) / 2
    return mu, Sig


def chay_B():
    x = np.array([0.0, 0.0, np.radians(30)])
    mu0 = np.array([0.4, -0.3, np.radians(-20)])  # đoán ban đầu sai: lệch 50 cm, hướng sai 50°
    Sig0 = np.diag([0.5 ** 2, 0.5 ** 2, np.radians(60) ** 2])
    me, Se = mu0.copy(), Sig0.copy()
    mu_, Su = mu0.copy(), Sig0.copy()
    dr = mu0.copy()
    log = []
    for k in range(1, int(T / DT) + 1):
        t = k * DT
        v, w = lenh(t)
        x = f(x, (v, w), DT)
        u = (v + RNG.normal(0, SIG_V), w + LECH_W + RNG.normal(0, SIG_W))
        zs = []
        if k % 10 == 0:
            for l in MOC:
                z = h(x, l) + RNG.normal(0, [SIG_R, SIG_B]); z[1] = goc(z[1])
                zs.append((z, l))
        dr = f(dr, u, DT)
        me, Se = ekf_buoc(me, Se, u, zs)
        mu_, Su = ukf_buoc(mu_, Su, u, zs)
        log.append({"t": t, "x": x.copy(), "dr": dr.copy(), "ekf": me.copy(), "ukf": mu_.copy(), "do": bool(zs),
                    "se": float(np.sqrt(Se[0, 0] + Se[1, 1])), "su": float(np.sqrt(Su[0, 0] + Su[1, 1]))})
    return log


LOG_B = chay_B()

if __name__ == "__main__":
    print("Phần A: hướng mơ hồ ±35°, đi thẳng 2 m")
    print(f"  Monte Carlo (sự thật): tâm ({MC_MU[0]:.3f}, {MC_MU[1]:.3f}) m")
    print(f"  EKF: tâm ({EKF_MU[0]:.3f}, {EKF_MU[1]:.3f}) -> lệch {np.linalg.norm(EKF_MU - MC_MU) * 100:.1f} cm")
    print(f"  UKF ({len(Xs)} điểm sigma): tâm ({UKF_MU[0]:.3f}, {UKF_MU[1]:.3f}) -> lệch {np.linalg.norm(UKF_MU - MC_MU) * 100:.1f} cm")
    print(f"  σx: MC {np.sqrt(MC_COV[0, 0]) * 100:.1f} cm · EKF {np.sqrt(EKF_COV[0, 0]) * 100:.1f} cm · UKF {np.sqrt(UKF_COV[0, 0]) * 100:.1f} cm")
    print(f"  σy: MC {np.sqrt(MC_COV[1, 1]) * 100:.1f} cm · EKF {np.sqrt(EKF_COV[1, 1]) * 100:.1f} cm · UKF {np.sqrt(UKF_COV[1, 1]) * 100:.1f} cm")
    L = LOG_B
    loi = lambda key, a=0, b=len(L): np.sqrt(np.mean([np.sum((r[key][:2] - r["x"][:2]) ** 2) for r in L[a:b]]))
    print(f"Phần B: {T:.0f} s, đo 2 mốc mỗi 1 s, đoán ban đầu lệch 50 cm, hướng sai 50°")
    print(f"  Chỉ odometry: RMS {loi('dr') * 100:.1f} cm · cuối lệch {np.linalg.norm(L[-1]['dr'][:2] - L[-1]['x'][:2]):.2f} m")
    print(f"  EKF: RMS {loi('ekf') * 100:.1f} cm · 10 s đầu {loi('ekf', 0, 100) * 100:.1f} cm · sau đó {loi('ekf', 100) * 100:.1f} cm")
    print(f"  UKF: RMS {loi('ukf') * 100:.1f} cm · 10 s đầu {loi('ukf', 0, 100) * 100:.1f} cm · sau đó {loi('ukf', 100) * 100:.1f} cm")
    for key in ("ekf", "ukf"):
        e = [np.linalg.norm(r[key][:2] - r["x"][:2]) for r in L]
        print(f"  {key}: lần đầu dưới 20 cm ở t = {next(r['t'] for r, v in zip(L, e) if v < 0.2):.1f} s")
