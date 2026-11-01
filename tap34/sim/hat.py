"""Tập 3.4 - Particle Filter: ngàn phỏng đoán (series Tự Học Robot Tự Hành)

Theo Chương 12 (§12.4.2), Principles of Robot Autonomy:
  - Niềm tin = tập K hạt P_t = {x_t^[1], ..., x_t^[K]} (Eq. 12.11), K ≈ 10³ thường đủ dùng
  - Thuật toán 5: (1) dự đoán: rút x̄_t^[k] ~ p(x_t | x_t-1^[k], u_t); (2) trọng số w_t^[k] = p(z_t | x̄_t^[k]);
    (3) lấy mẫu lại có hoàn lại theo trọng số -> P_t
  - Không lấy mẫu lại thì trọng số dồn vào vài hạt (suy biến); hợp với định vị toàn cục, niềm tin nhiều đỉnh
Mở rộng / giả định: robot có la bàn biết hướng (±5°), phòng 10 × 8 m, 2 mốc phát sóng, robot chỉ đo khoảng cách tới 2 mốc (σ = 0,2 m) nên lúc đầu
có 2 vị trí "soi gương" đều khớp; lấy mẫu lại kiểu hệ thống (low-variance), K = 1000, đo cỡ mẫu hiệu dụng (ESS).
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 hat.py
"""
import numpy as np

RNG = np.random.default_rng(39)  # chọn lần chạy có lúc đám hạt tin nhầm vị trí soi gương (để kể chuyện); kết quả vẫn là chạy thật
K = 1000
RONG, DAI = 10.0, 8.0
MOC = np.array([[2.0, 4.0], [8.0, 4.0]])  # 2 mốc nằm trên đường y = 4: vị trí đối xứng qua đường này cho cùng khoảng cách
SIG_Z = 0.2
SIG_V, SIG_W = 0.05, np.radians(4)
DT = 0.5
SO_BUOC = 40


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def lenh(k):
    """Rẽ phải ngay từ đầu rồi rẽ trái (luôn ở nửa dưới phòng, không cắt đường nối 2 mốc).
    Đi thẳng thì vị trí "soi gương" khớp hoàn toàn với số đo; phải rẽ mới phân biệt được."""
    return (0.45, -0.18) if k <= 14 else (0.45, 0.15)


def di(X, v, w, nhieu=True):
    n = len(X)
    vv = v + (RNG.normal(0, SIG_V, n) if nhieu else 0)
    ww = w + (RNG.normal(0, SIG_W, n) if nhieu else 0)
    th = X[:, 2] + ww * DT
    return np.column_stack([X[:, 0] + vv * DT * np.cos(th), X[:, 1] + vv * DT * np.sin(th), goc(th)])


def do(X):
    return np.stack([np.hypot(X[:, 0] - m[0], X[:, 1] - m[1]) for m in MOC], -1)


def lay_mau_lai(w):
    """Lấy mẫu lại kiểu hệ thống: K mốc cách đều 1/K, một số ngẫu nhiên duy nhất."""
    c = np.cumsum(w)
    u = (RNG.random() + np.arange(K)) / K
    return np.minimum(np.searchsorted(c, u), K - 1)


def chay():
    x = np.array([[1.0, 1.0, 0.6]])  # vị trí thật (robot không biết)
    # robot có la bàn (IMU) biết hướng ±5°, chỉ chưa biết vị trí: hạt rải đều khắp phòng
    P = np.column_stack([RNG.uniform(0, RONG, K), RNG.uniform(0, DAI, K), x[0, 2] + RNG.normal(0, np.radians(5), K)])
    W = np.full(K, 1 / K)
    log = [{"k": 0, "x": x[0].copy(), "P": P.copy(), "w": W.copy(), "ess": float(K), "buoc": "đầu"}]
    for k in range(1, SO_BUOC + 1):
        v, w = lenh(k)
        x = di(x, v, w, nhieu=False)
        z = do(x)[0] + RNG.normal(0, SIG_Z, 2)
        P = di(P, v, w)  # (1) dự đoán
        d = do(P) - z
        wt = W * np.exp(-0.5 * np.sum((d / SIG_Z) ** 2, axis=1))  # (2) trọng số = p(z | x) (nhân dồn nếu chưa lấy mẫu lại)
        wt = wt / wt.sum()
        ess = float(1 / np.sum(wt ** 2))
        log.append({"k": k, "x": x[0].copy(), "P": P.copy(), "w": wt.copy(), "ess": ess, "buoc": "trọng số"})
        # (3) lấy mẫu lại, chỉ khi ESS < K/2 (mở rộng: giữ được nhiều đỉnh lâu hơn, tránh cạn hạt)
        if ess < K / 2:
            P = P[lay_mau_lai(wt)]
            P[:, :2] += RNG.normal(0, 0.03, (K, 2))  # rung nhẹ tránh trùng hạt (mở rộng)
            W = np.full(K, 1 / K)
            lmd = True
        else:
            W = wt
            lmd = False
        log.append({"k": k, "x": x[0].copy(), "P": P.copy(), "w": W.copy(), "ess": float(1 / np.sum(W ** 2)), "buoc": "lấy mẫu lại", "lmd": lmd})
    return log


def thong_ke(r, ban_kinh=0.5):
    P, w, x = r["P"], r["w"], r["x"]
    gan = float(w[np.hypot(P[:, 0] - x[0], P[:, 1] - x[1]) < ban_kinh].sum())
    guong = np.array([x[0], 2 * MOC[0, 1] - x[1]])  # vị trí soi gương qua đường nối 2 mốc
    gan_guong = float(w[np.hypot(P[:, 0] - guong[0], P[:, 1] - guong[1]) < ban_kinh].sum())
    tb = (w[:, None] * P[:, :2]).sum(0)
    return gan, gan_guong, float(np.hypot(*(tb - x[:2])))


LOG = chay()

if __name__ == "__main__":
    print(f"K = {K} hạt · phòng {RONG} × {DAI} m · 2 mốc {MOC.tolist()} · đo khoảng cách σ = {SIG_Z} m")
    for r in LOG:
        if r["buoc"] == "lấy mẫu lại" and r["k"] not in (1, 2, 3, 5, 8, 10, 12, 15, 20, 30, 40):
            continue
        gan, guong, loi = thong_ke(r)
        print(f"bước {r['k']:2d} {r['buoc']:12s} | hạt quanh vị trí thật (±0,5 m) {gan * 100:5.1f}% | quanh vị trí soi gương {guong * 100:5.1f}% "
              f"| tâm đám hạt lệch {loi:.2f} m | ESS {r['ess']:.0f}")
    w_esses = [r["ess"] for r in LOG if r["buoc"] == "trọng số"]
    print(f"ESS sau khi gán trọng số: bước 1 = {w_esses[0]:.0f}, nhỏ nhất = {min(w_esses):.0f}, trung bình = {np.mean(w_esses):.0f} (trên {K})")
