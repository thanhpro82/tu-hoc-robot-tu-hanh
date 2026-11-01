"""Tập 3.5 - Định vị trên bản đồ có sẵn (series Tự Học Robot Tự Hành)

Theo Chương 13, Principles of Robot Autonomy:
  - Ba bài toán (§13.1): bám vị trí, định vị toàn cục, robot bị bắt cóc (bị dời đi mà không báo)
  - Niềm tin có điều kiện theo bản đồ m (§13.2); chuyển động có bản đồ (Eq. 13.2): tư thế nằm trong tường có xác suất 0
  - Mô hình đo tách thành tích từng thành phần (Eq. 13.3): p(z_t | x_t, m) = Π_i p(z_t^i | x_t, m)
  - Monte Carlo Localization (Thuật toán 4): đẩy hạt qua chuyển động -> trọng số p(z_t | x̄, m) -> lấy mẫu lại
  - Ghi chú lề §13.6: thả thêm hạt ngẫu nhiên mỗi bước giúp xử lý robot bị bắt cóc
Mở rộng / giả định: căn hộ 12 × 8 m (lưới 10 cm), LiDAR 8 tia tầm 6 m nhiễu 5 cm, mô hình mỗi tia = Gauss σ = 0,6 m
trộn 10% đều (sách không nêu mô hình tia cụ thể), K = 2000 hạt, thả 3% hạt ngẫu nhiên mỗi bước, lộ trình định sẵn.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 mcl.py
"""
import numpy as np

RNG = np.random.default_rng(35)
O = 0.1
RONG, DAI = 12.0, 8.0
NX, NY = int(RONG / O), int(DAI / O)
SO_TIA, TAM = 8, 6.0
SIG_LIDAR = 0.05
SIG_TIA, P_DEU = 0.6, 0.1
K = 2000
THA = 0.03  # tỉ lệ hạt ngẫu nhiên thả vào mỗi bước
DT = 0.5
SIG_V, SIG_W = 0.05, np.radians(5)


def tao_ban_do():
    """Lưới chiếm chỗ: 1 = tường/đồ đạc. Căn hộ 4 phòng, có cửa thông, vài món đồ để các phòng khác nhau."""
    m = np.zeros((NY, NX), dtype=bool)
    m[0, :] = m[-1, :] = True
    m[:, 0] = m[:, -1] = True

    def tuong(x0, y0, x1, y1):
        m[int(y0 / O):int(y1 / O) + 1, int(x0 / O):int(x1 / O) + 1] = True

    tuong(6.0, 0.0, 6.1, 8.0)       # tường giữa dọc
    tuong(0.0, 4.0, 12.0, 4.1)      # tường giữa ngang
    for x0, x1 in [(2.4, 3.4), (8.6, 9.6)]:   # cửa giữa phòng trên và dưới
        m[int(4.0 / O):int(4.1 / O) + 1, int(x0 / O):int(x1 / O)] = False
    for y0, y1 in [(1.6, 2.6), (5.4, 6.4)]:   # cửa giữa phòng trái và phải
        m[int(y0 / O):int(y1 / O), int(6.0 / O):int(6.1 / O) + 1] = False
    tuong(1.0, 1.0, 2.0, 1.6)       # bàn phòng dưới trái
    tuong(9.5, 0.6, 11.4, 1.2)      # tủ phòng dưới phải
    tuong(10.6, 2.2, 11.4, 3.2)
    tuong(0.6, 6.8, 2.6, 7.4)       # giường phòng trên trái
    tuong(4.0, 5.0, 4.6, 5.6)
    tuong(7.0, 6.6, 7.8, 7.4)       # kệ phòng trên phải
    return m


BAN_DO = tao_ban_do()
GOC_TIA = np.linspace(-np.pi, np.pi, SO_TIA, endpoint=False)
BUOC_TIA = np.arange(0.05, TAM + 1e-9, 0.05)


def chiem(x, y):
    ix = np.clip((x / O).astype(int), 0, NX - 1)
    iy = np.clip((y / O).astype(int), 0, NY - 1)
    ngoai = (x < 0) | (x >= RONG) | (y < 0) | (y >= DAI)
    return BAN_DO[iy, ix] | ngoai


def quet(X):
    """Dò tia LiDAR cho mảng tư thế X (n, 3) -> khoảng cách (n, SO_TIA)."""
    th = X[:, 2:3] + GOC_TIA[None, :]
    ra = np.full(th.shape, TAM)
    da = np.zeros(th.shape, dtype=bool)
    c, s = np.cos(th), np.sin(th)
    for d in BUOC_TIA:
        trung = chiem(X[:, 0:1] + d * c, X[:, 1:2] + d * s) & ~da
        ra[trung] = d
        da |= trung
        if da.all():
            break
    return ra


def rai_hat(n):
    """Rải n hạt ngẫu nhiên ở chỗ trống trên bản đồ."""
    out = np.empty((0, 3))
    while len(out) < n:
        c = np.column_stack([RNG.uniform(0, RONG, 2 * n), RNG.uniform(0, DAI, 2 * n), RNG.uniform(-np.pi, np.pi, 2 * n)])
        out = np.vstack([out, c[~chiem(c[:, 0], c[:, 1])]])
    return out[:n]


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def di(X, v, w, nhieu=True):
    n = len(X)
    vv = v + (RNG.normal(0, SIG_V, n) if nhieu else 0)
    ww = w + (RNG.normal(0, SIG_W, n) if nhieu else 0)
    th = goc(X[:, 2] + ww * DT)
    return np.column_stack([X[:, 0] + vv * DT * np.cos(th), X[:, 1] + vv * DT * np.sin(th), th])


def trong_so(P, z):
    """Eq. 13.3: tích theo từng tia; mỗi tia = Gauss quanh khoảng cách dự đoán trộn phần đều (mở rộng). Hạt trong tường: 0 (Eq. 13.2)."""
    du = quet(P)
    p = (1 - P_DEU) * np.exp(-0.5 * ((du - z) / SIG_TIA) ** 2) + P_DEU * 0.2
    logw = np.log(p).sum(1)
    logw[chiem(P[:, 0], P[:, 1])] = -np.inf
    w = np.exp(logw - logw.max())
    return w / w.sum()


def lay_mau_lai(w, n):
    c = np.cumsum(w)
    u = (RNG.random() + np.arange(n)) / n
    return np.minimum(np.searchsorted(c, u), len(w) - 1)


# Lộ trình: các điểm đi qua (robot đi theo, tốc độ 0,5 m/s); bị bắt cóc ở bước BAT_COC
DIEM_DEN = [(3.0, 2.8), (4.6, 2.2), (7.2, 2.1), (8.4, 2.8), (9.0, 3.6), (9.1, 5.2), (8.2, 6.0), (7.0, 5.8)]
DIEM_DEN_2 = [(2.2, 5.0), (3.4, 5.8), (2.0, 6.2), (1.0, 5.2), (2.8, 3.6), (3.0, 2.0)]
X0 = np.array([1.2, 2.6, 0.0])
BAT_COC = 52
VI_TRI_BAT_COC = np.array([1.4, 5.6, -0.6])  # bị nhấc sang phòng trên trái
SO_BUOC = 100


def dieu_khien(x, ds, i):
    if i >= len(ds):
        return 0.0, 0.0, i
    dx, dy = ds[i][0] - x[0], ds[i][1] - x[1]
    if np.hypot(dx, dy) < 0.35:
        return dieu_khien(x, ds, i + 1)
    e = goc(np.arctan2(dy, dx) - x[2])
    return 0.5 * max(0.2, np.cos(e)), float(np.clip(1.5 * e, -1.2, 1.2)), i


def chay():
    x = X0.copy()
    lo_trinh, i = DIEM_DEN, 0
    P = {"tha": rai_hat(K), "khong": None}
    P["khong"] = P["tha"].copy()
    log = []
    for k in range(1, SO_BUOC + 1):
        if k == BAT_COC:
            x = VI_TRI_BAT_COC.copy()  # bị bắt cóc: dời đi, không báo cho bộ lọc
            lo_trinh, i = DIEM_DEN_2, 0
        v, w, i = dieu_khien(x, lo_trinh, i)
        x = di(x[None], v, w, nhieu=False)[0]
        z = quet(x[None])[0] + RNG.normal(0, SIG_LIDAR, SO_TIA)
        r = {"k": k, "x": x.copy(), "z": z, "bat_coc": k == BAT_COC}
        for ten in ("tha", "khong"):
            Pk = di(P[ten], v, w)
            wt = trong_so(Pk, z)
            Pk = Pk[lay_mau_lai(wt, K)]
            if ten == "tha":  # thả hạt ngẫu nhiên (ghi chú lề §13.6)
                n = int(THA * K)
                Pk[RNG.choice(K, n, replace=False)] = rai_hat(n)
            P[ten] = Pk
            tb = Pk[:, :2].mean(0)
            gan = float(np.mean(np.hypot(Pk[:, 0] - x[0], Pk[:, 1] - x[1]) < 0.5))
            r[ten] = {"P": Pk.copy(), "tb": tb, "loi": float(np.hypot(*(tb - x[:2]))), "gan": gan}
        log.append(r)
    return log


LOG = chay()


def lan_dau(ten, tu, nguong=0.8):
    for r in LOG:
        if r["k"] >= tu and r[ten]["gan"] >= nguong:
            return r["k"]
    return None


if __name__ == "__main__":
    print(f"Bản đồ {RONG} × {DAI} m, ô {O * 100:.0f} cm · LiDAR {SO_TIA} tia tầm {TAM} m · K = {K} hạt · thả {THA * 100:.0f}% hạt ngẫu nhiên mỗi bước")
    for k in (1, 2, 3, 5, 8, 12, 20, 40, 51, 52, 53, 55, 60, 65, 70, 80, 100):
        r = LOG[k - 1]
        print(f"bước {k:3d}{' (BẮT CÓC)' if r['bat_coc'] else '          '} | có thả hạt: {r['tha']['gan'] * 100:5.1f}% gần đúng, lệch {r['tha']['loi']:.2f} m "
              f"| không thả: {r['khong']['gan'] * 100:5.1f}% gần đúng, lệch {r['khong']['loi']:.2f} m")
    print(f"Định vị toàn cục: ≥80% hạt quanh vị trí thật ở bước {lan_dau('tha', 1)} (có thả) / {lan_dau('khong', 1)} (không thả)")
    print(f"Sau bắt cóc (bước {BAT_COC}): tìm lại ở bước {lan_dau('tha', BAT_COC)} (có thả) / {lan_dau('khong', BAT_COC)} (không thả)")
    tr = [r["tha"]["loi"] for r in LOG if 20 <= r["k"] < BAT_COC]
    print(f"Lúc bám vị trí ổn định (bước 20-51): lệch trung bình {np.mean(tr) * 100:.1f} cm")
    print(f"Cuối cùng: có thả lệch {LOG[-1]['tha']['loi']:.2f} m · không thả lệch {LOG[-1]['khong']['loi']:.2f} m")
