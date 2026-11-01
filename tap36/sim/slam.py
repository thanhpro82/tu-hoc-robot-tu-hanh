"""Tập 3.6 - SLAM: con gà hay quả trứng? (series Tự Học Robot Tự Hành)

Theo Chương 14, Principles of Robot Autonomy:
  - Full SLAM (Định nghĩa 14.2, Eq. 14.2): ước lượng cả quỹ đạo và bản đồ; định vị cần bản đồ, vẽ bản đồ cần định vị
  - Front-end (§14.2): khép vòng = tìm lại chỗ cũ + kiểm tra hình học; căn quét bằng ICP (§14.2.5)
  - Graph SLAM (§14.7): nút = tư thế, cạnh = ràng buộc tương đối (odometry, khép vòng);
    r_ij = z_ij ⊖ h_ij(x_i, x_j), Ω_ij = R_ij⁻¹, x* = argmin Σ r_ijᵀ Ω_ij r_ij, giải bằng Gauss–Newton / LM, cố định tư thế đầu
  - Khép vòng nối hai đầu xa nhau của quỹ đạo, sai số dồn lại được rải đều dọc đường
Mở rộng / giả định: hành lang vòng quanh khối nhà 20 × 14 m, LiDAR 90 tia, nhiễu odometry (2% quãng đường, 1°/m, lệch hướng
nhẹ), coi như đã nhận ra chỗ cũ (bước tìm lại chỗ cũ không mô phỏng), ICP điểm–điểm, giải bằng scipy least_squares (LM).
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 slam.py
"""
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import cKDTree

RNG = np.random.default_rng(36)
O = 0.1
RONG, DAI = 20.0, 14.0
NX, NY = int(RONG / O), int(DAI / O)
SO_TIA, TAM, SIG_LIDAR = 90, 8.0, 0.02
BUOC_NUT = 1.0  # mỗi nút cách nhau 1 m
SIG_D, SIG_TH = 0.02, np.radians(1.0)  # nhiễu odometry mỗi mét
LECH_TH = np.radians(0.5)  # lệch hướng mỗi mét (odometry quay hụt)


def tao_ban_do():
    m = np.zeros((NY, NX), dtype=bool)
    m[:3, :] = m[-3:, :] = True
    m[:, :3] = m[:, -3:] = True

    def khoi(x0, y0, x1, y1):
        m[int(y0 / O):int(y1 / O), int(x0 / O):int(x1 / O)] = True

    khoi(3.0, 3.0, 17.0, 11.0)   # khối nhà ở giữa -> hành lang vòng quanh rộng 2,7 m
    for x0, y0, x1, y1 in [(5, 0.3, 5.4, 1.2), (10, 12.8, 10.6, 13.7), (18.8, 6, 19.7, 6.5), (0.3, 8, 1.4, 8.4), (13, 0.3, 13.5, 1.0)]:
        khoi(x0, y0, x1, y1)     # vài hốc, cột để hành lang có đặc điểm
    return m


BAN_DO = tao_ban_do()
GOC_TIA = np.linspace(-np.pi, np.pi, SO_TIA, endpoint=False)


def chiem(x, y):
    ix = np.clip((x / O).astype(int), 0, NX - 1)
    iy = np.clip((y / O).astype(int), 0, NY - 1)
    return BAN_DO[iy, ix] | (x < 0) | (x >= RONG) | (y < 0) | (y >= DAI)


def quet(p):
    th = p[2] + GOC_TIA
    ra = np.full(SO_TIA, TAM)
    da = np.zeros(SO_TIA, dtype=bool)
    for d in np.arange(0.05, TAM, 0.03):
        t = chiem(p[0] + d * np.cos(th), p[1] + d * np.sin(th)) & ~da
        ra[t] = d
        da |= t
    ra = ra + RNG.normal(0, SIG_LIDAR, SO_TIA)
    ok = ra < TAM - 0.1
    return np.column_stack([ra * np.cos(GOC_TIA), ra * np.sin(GOC_TIA)])[ok]  # điểm trong hệ robot


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def cong(a, b):
    """a ⊕ b: ghép tư thế tương đối b vào a (SE(2))."""
    c, s = np.cos(a[2]), np.sin(a[2])
    return np.array([a[0] + c * b[0] - s * b[1], a[1] + s * b[0] + c * b[1], goc(a[2] + b[2])])


def tru(a, b):
    """a⁻¹ ⊕ b: tư thế b nhìn từ a."""
    c, s = np.cos(a[2]), np.sin(a[2])
    dx, dy = b[0] - a[0], b[1] - a[1]
    return np.array([c * dx + s * dy, -s * dx + c * dy, goc(b[2] - a[2])])


def quy_dao_that():
    """Đi một vòng hành lang ngược chiều kim đồng hồ, mỗi 1 m một nút, quay lại gần chỗ xuất phát."""
    goc_den = [(1.6, 1.6), (18.4, 1.6), (18.4, 12.4), (1.6, 12.4), (1.6, 1.6)]
    pts = []
    for (x0, y0), (x1, y1) in zip(goc_den[:-1], goc_den[1:]):
        L = np.hypot(x1 - x0, y1 - y0)
        n = int(round(L / BUOC_NUT))
        for i in range(1, n + 1):
            pts.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, np.arctan2(y1 - y0, x1 - x0)))
    pts.append((1.6, 1.6, 0.0))  # quay tại chỗ về hướng ban đầu: trở lại đúng tư thế xuất phát
    P = [np.array([1.6, 1.6, 0.0])] + [np.array(p) for p in pts]
    return P


THAT = quy_dao_that()
N = len(THAT)
QUET = [quet(p) for p in THAT]

# odometry có nhiễu và lệch
ODO = []
for i in range(N - 1):
    z = tru(THAT[i], THAT[i + 1])
    d = np.hypot(z[0], z[1])
    z = z + np.array([RNG.normal(0, SIG_D * d), RNG.normal(0, SIG_D * d), RNG.normal(LECH_TH * d, SIG_TH * max(d, 0.3))])
    ODO.append(z)
DR = [THAT[0].copy()]
for z in ODO:
    DR.append(cong(DR[-1], z))
DR = np.array(DR)


def icp(A, B, khoi_dau=np.zeros(3), lap=40):
    """Tìm T sao cho T ⊕ B khớp A (điểm–điểm). Trả về T và sai lệch trung bình."""
    T = khoi_dau.copy()
    cay = cKDTree(A)
    for _ in range(lap):
        c, s = np.cos(T[2]), np.sin(T[2])
        Bt = B @ np.array([[c, s], [-s, c]]) + T[:2]
        d, j = cay.query(Bt)
        giu = d < np.percentile(d, 80)
        P, Q = Bt[giu], A[j[giu]]
        mp, mq = P.mean(0), Q.mean(0)
        H = (P - mp).T @ (Q - mq)
        U, _, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T
        if np.linalg.det(R) < 0:
            Vt[1] *= -1
            R = Vt.T @ U.T
        dth = np.arctan2(R[1, 0], R[0, 0])
        dt = mq - R @ mp
        T = cong(np.array([dt[0], dt[1], dth]), T)
    c, s = np.cos(T[2]), np.sin(T[2])
    d, _ = cay.query(B @ np.array([[c, s], [-s, c]]) + T[:2])
    return T, float(np.median(d))


# Khép vòng: nút cuối quay về gần nút đầu -> ICP giữa quét cuối và quét đầu (coi như đã nhận ra chỗ cũ)
Z_VONG, LOI_ICP = icp(QUET[0], QUET[-1])
TH_VONG = tru(THAT[0], THAT[-1])

CANH = [(i, i + 1, ODO[i], np.diag([1 / (SIG_D * 1.0) ** 2] * 2 + [1 / SIG_TH ** 2])) for i in range(N - 1)]
CANH_VONG = (0, N - 1, Z_VONG, np.diag([1 / 0.03 ** 2] * 2 + [1 / np.radians(0.5) ** 2]))


def toi_uu(canh):
    """x* = argmin Σ r_ijᵀ Ω_ij r_ij, r_ij = z_ij ⊖ (x_i⁻¹ ⊕ x_j); tư thế 0 cố định (gauge)."""
    L = [np.linalg.cholesky(Om).T for *_, Om in canh]

    def phan_du(v):
        X = np.vstack([THAT[0], v.reshape(-1, 3)])
        r = []
        for (i, j, z, _), Lk in zip(canh, L):
            e = tru(X[i], X[j]) - z
            e[2] = goc(e[2])
            r.append(Lk @ e)
        return np.concatenate(r)

    kq = least_squares(phan_du, DR[1:].ravel(), method="lm")
    return np.vstack([THAT[0], kq.x.reshape(-1, 3)])


OPT = toi_uu(CANH + [CANH_VONG])


def ve_ban_do(P):
    """Ghép các lần quét theo tư thế P thành lưới chiếm chỗ (đếm số điểm rơi vào mỗi ô)."""
    g = np.zeros((NY, NX), dtype=int)
    for p, q in zip(P, QUET):
        c, s = np.cos(p[2]), np.sin(p[2])
        w = q @ np.array([[c, s], [-s, c]]) + p[:2]
        ix, iy = (w[:, 0] / O).astype(int), (w[:, 1] / O).astype(int)
        ok = (ix >= 0) & (ix < NX) & (iy >= 0) & (iy < NY)
        np.add.at(g, (iy[ok], ix[ok]), 1)
    return g


def do_net(g):
    """Tỉ lệ điểm quét rơi đúng vào tường thật (± 1 ô)."""
    from scipy.ndimage import binary_dilation
    tuong = binary_dilation(BAN_DO, iterations=1)
    return float(g[tuong].sum() / g.sum())


G_DR, G_OPT, G_THAT = ve_ban_do(DR), ve_ban_do(OPT), ve_ban_do(THAT)
loi = lambda P: np.hypot(*(np.array(P)[:, :2] - np.array(THAT)[:, :2]).T)

if __name__ == "__main__":
    print(f"Hành lang vòng quanh khối nhà {RONG} × {DAI} m · {N} nút (mỗi {BUOC_NUT} m) · LiDAR {SO_TIA} tia · {N - 1} cạnh odometry")
    e_dr, e_opt = loi(DR), loi(OPT)
    print(f"Chỉ odometry: về tới cuối lệch {e_dr[-1]:.2f} m, lớn nhất {e_dr.max():.2f} m, trung bình {e_dr.mean():.2f} m")
    print(f"Khép vòng bằng ICP: tìm được ({Z_VONG[0]:.2f}, {Z_VONG[1]:.2f}, {np.degrees(Z_VONG[2]):.1f}°), thật ({TH_VONG[0]:.2f}, {TH_VONG[1]:.2f}, {np.degrees(TH_VONG[2]):.1f}°), sai lệch điểm {LOI_ICP * 100:.1f} cm")
    print(f"Sau tối ưu đồ thị: cuối lệch {e_opt[-1]:.2f} m, lớn nhất {e_opt.max():.2f} m, trung bình {e_opt.mean():.2f} m")
    print(f"Độ nét bản đồ (điểm quét rơi đúng tường): odometry {do_net(G_DR) * 100:.1f}% · sau tối ưu {do_net(G_OPT) * 100:.1f}% · tư thế thật {do_net(G_THAT) * 100:.1f}%")
