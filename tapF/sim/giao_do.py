"""Tập cuối F - Robot giao đồ trong nhà: ghép cả 4 mùa (series Tự Học Robot Tự Hành).

Nhiệm vụ: "lấy đồ ở bếp, giao tận tay người ở phòng ngủ / phòng làm việc". Mỗi bước 0,1 s, mọi khối là code của các tập trước:
  Mùa 4 · Bộ não (Ch. 16, tập 4.1): máy trạng thái M = (S, I, O, n, s0), s_{t+1} = n(s_t, i_t).
      CHỜ LỆNH → ĐỊNH VỊ → ĐI LẤY → NHẬN ĐỒ → ĐI GIAO → TÌM NGƯỜI → TIẾP CẬN → GIAO → XONG;
      DỪNG (có vật lạ phía trước) quay lại đúng trạng thái trước đó khi đường trống (nhớ trạng thái trước: mở rộng).
  Mùa 3 · Định vị (Ch. 13, tập 3.5): Monte Carlo Localization trên bản đồ căn hộ của tập 3.5; robot thức dậy KHÔNG biết
      mình ở đâu (định vị toàn cục), hạt trong tường có xác suất 0 (Eq. 13.2), trọng số = tích từng tia (Eq. 13.3),
      thả 3% hạt ngẫu nhiên mỗi lần (ghi chú lề §13.6).
  Mùa 1 · Tìm đường + điều khiển (Ch. 4 tập 1.5, Ch. 3 tập 1.3): A* trên lưới 10 cm đã nới vật cản 0,25 m;
      bám đường bằng PD trên góc hướng, e = r − y với r = hướng tới điểm nhìn trước 0,5 m, y = hướng ước lượng.
  Mùa 2 · Thị giác (Ch. 6 + Ch. 10, tập 2.2/2.8/2.9): camera lỗ kim f = 60 px, mạng YOLO đã học ở tập 2.8 (không học lại)
      tìm "người"; khoảng cách Z = f·H/h, hướng = atan((u − u0)/f).
Mở rộng / giả định: căn hộ 12 × 8 m của tập 3.5; robot tròn bán kính 0,15 m, v ≤ 0,5 m/s; bánh xe trượt (sai số tỉ lệ
v ~ N(0, 3%), ω ~ N(0, 5%), trôi góc ~ N(0, 0,01 rad/s) mỗi lượt + nhiễu từng bước); LiDAR 36 tia tầm 6 m nhiễu 3 cm
(bộ lọc hạt dùng 12 tia); một người đi qua lại trong bếp (0,5 m/s); người nhận đứng ở chỗ ngẫu nhiên trong phòng;
ảnh camera chỉ vẽ người (kiểu vẽ của tập 2.8/2.9), có kiểm tra bị tường che. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 giao_do.py [số lượt]
"""
import heapq
import math
import sys
from pathlib import Path

import numpy as np
import torch
from scipy.ndimage import distance_transform_edt

GOC = Path(__file__).resolve().parent

# ---------------- thế giới: căn hộ của tập 3.5 ----------------
O = 0.1
RONG, DAI = 12.0, 8.0
NX, NY = int(RONG / O), int(DAI / O)
DT = 0.1
T_MAX = 200.0
R_ROBOT, R_NGUOI = 0.15, 0.2
V_MAX, W_MAX = 0.5, 1.5
SO_TIA, TAM, SIG_LIDAR = 36, 6.0, 0.03
GOC_TIA = np.linspace(-np.pi, np.pi, SO_TIA, endpoint=False)
TIA_MCL = np.arange(0, SO_TIA, 2)          # 18 tia cho bộ lọc hạt
K = 1500
K0, SIG_TIA0 = 4000, 0.6                   # lúc định vị toàn cục: nhiều hạt hơn, mô hình đo mềm hơn (như tập 3.5)
THA = 0.03
SIG_TIA, P_DEU = 0.3, 0.1
F_CAM, N_ANH, H_CAM, H_NGUOI = 60.0, 128, 0.5, 1.7

TEN_PHONG = {"khach": "phòng khách", "bep": "bếp", "ngu": "phòng ngủ", "lamviec": "phòng làm việc"}
PHONG = {"khach": (0, 0, 6, 4), "bep": (6, 0, 12, 4), "ngu": (0, 4, 6, 8), "lamviec": (6, 4, 12, 8)}
DIEM_NHIN = {"ngu": [(3.0, 6.0), (1.4, 5.0)], "lamviec": [(9.0, 6.0), (10.6, 5.2)]}
DIEM_LAY = (10.2, 1.7)                     # trước tủ bếp
DUONG_NGUOI_DI = ((8.0, 0.8), (8.0, 3.5))  # người đi qua lại trong bếp


def tao_ban_do():
    """Giống hệt tap35/sim/mcl.py: căn hộ 4 phòng, cửa thông, vài món đồ."""
    m = np.zeros((NY, NX), dtype=bool)
    m[0, :] = m[-1, :] = True
    m[:, 0] = m[:, -1] = True

    def tuong(x0, y0, x1, y1):
        m[int(y0 / O):int(y1 / O) + 1, int(x0 / O):int(x1 / O) + 1] = True

    tuong(6.0, 0.0, 6.1, 8.0)
    tuong(0.0, 4.0, 12.0, 4.1)
    for x0, x1 in [(2.4, 3.4), (8.6, 9.6)]:
        m[int(4.0 / O):int(4.1 / O) + 1, int(x0 / O):int(x1 / O)] = False
    for y0, y1 in [(1.6, 2.6), (5.4, 6.4)]:
        m[int(y0 / O):int(y1 / O), int(6.0 / O):int(6.1 / O) + 1] = False
    tuong(1.0, 1.0, 2.0, 1.6)
    tuong(9.5, 0.6, 11.4, 1.2)
    tuong(10.6, 2.2, 11.4, 3.2)
    tuong(0.6, 6.8, 2.6, 7.4)
    tuong(4.0, 5.0, 4.6, 5.6)
    tuong(7.0, 6.6, 7.8, 7.4)
    return m


BAN_DO = tao_ban_do()


def no_vat_can(m, r):
    """Nới vật cản thêm r mét (để A* không đi sát tường)."""
    k = int(round(r / O))
    out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy <= k * k:
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


LUOI_AN_TOAN = no_vat_can(BAN_DO, 0.3)
KC_TUONG = no_vat_can(BAN_DO, 0.5)        # dùng để chọn chỗ đứng / chỗ xuất phát thoáng
KC_BAN_DO = distance_transform_edt(~BAN_DO) * O   # khoảng cách từ mỗi ô tới vật cản gần nhất trên bản đồ (m)


def o_cua(x, y):
    return np.clip((np.asarray(x) / O).astype(int), 0, NX - 1), np.clip((np.asarray(y) / O).astype(int), 0, NY - 1)


def chiem(x, y, m=BAN_DO):
    ix, iy = o_cua(x, y)
    ngoai = (np.asarray(x) < 0) | (np.asarray(x) >= RONG) | (np.asarray(y) < 0) | (np.asarray(y) >= DAI)
    return m[iy, ix] | ngoai


BUOC_TIA = np.arange(0.05, TAM + 1e-9, 0.05)


def quet_ban_do(X, goc):
    """Dò tia trên bản đồ tĩnh cho mảng tư thế X (n, 3), các góc goc -> (n, len(goc))."""
    th = X[:, 2:3] + goc[None, :]
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


def quet_that(x, nguoi, rng):
    """LiDAR thật: bản đồ + người (hình tròn), có nhiễu."""
    z = quet_ban_do(x[None], GOC_TIA)[0]
    th = x[2] + GOC_TIA
    dx, dy = np.cos(th), np.sin(th)
    for p in nguoi:
        wx, wy = p[0] - x[0], p[1] - x[1]
        b = wx * dx + wy * dy
        c = wx * wx + wy * wy - R_NGUOI ** 2
        D = b * b - c
        ok = (D >= 0) & (b > 0)
        t = np.where(ok, b - np.sqrt(np.maximum(D, 0)), TAM)
        z = np.minimum(z, np.where(t > 0, t, TAM))
    return np.clip(z + rng.normal(0, SIG_LIDAR, SO_TIA), 0.02, TAM)


def vat_la(uoc, z, da_biet=None):
    """Tia nào chạm vào thứ KHÔNG có trên bản đồ: điểm cuối tia (theo tư thế ước lượng) cách vật cản gần nhất > 0,3 m
    (và chưa được ghi vào lưới tạm)."""
    th = uoc[2] + GOC_TIA
    ix, iy = o_cua(uoc[0] + z * np.cos(th), uoc[1] + z * np.sin(th))
    la = (KC_BAN_DO[iy, ix] > 0.3) & (z < TAM - 0.1)
    return la if da_biet is None else la & ~da_biet[iy, ix]


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def nhin_thay(a, b):
    """Có đường nhìn thẳng từ a tới b (không bị tường che)?"""
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    s = np.linspace(0, 1, max(2, int(d / 0.05)))
    return not chiem(a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1]))[1:-1].any()


# ---------------- Mùa 1: A* (Ch. 4) ----------------
LANG_GIENG = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]


def a_sao(bat_dau, dich, luoi=LUOI_AN_TOAN):
    """f(q) = C(q) + h(q), h = khoảng cách Euclid tới đích (không bao giờ đoán quá chi phí thật).
    Mở rộng: ô trong vùng nới (sát tường < 0,3 m) vẫn đi được nhưng chi phí ×30, ô cách tường < 0,6 m bị cộng thêm chút ít
    -> đường đi giữa cửa, và robot đang đứng sát tường vẫn tìm được lối ra."""
    s = tuple(int(v) for v in o_cua(*bat_dau))
    g = tuple(int(v) for v in o_cua(*dich))
    if BAN_DO[g[1], g[0]]:
        return None
    h = lambda q: math.hypot(q[0] - g[0], q[1] - g[1])
    mo = [(h(s), 0.0, s)]
    C, cha = {s: 0.0}, {s: None}
    while mo:
        _, c, q = heapq.heappop(mo)
        if q == g:
            duong = []
            while q is not None:
                duong.append(((q[0] + 0.5) * O, (q[1] + 0.5) * O))
                q = cha[q]
            return duong[::-1]
        if c > C[q]:
            continue
        for dx, dy, w in LANG_GIENG:
            n = (q[0] + dx, q[1] + dy)
            if not (0 <= n[0] < NX and 0 <= n[1] < NY) or BAN_DO[n[1], n[0]]:
                continue
            cn = c + w * (30.0 if luoi[n[1], n[0]] else 1.0 + 2.0 * max(0.0, 0.6 - KC_BAN_DO[n[1], n[0]]) / 0.6)
            if cn < C.get(n, 1e18):
                C[n], cha[n] = cn, q
                heapq.heappush(mo, (cn + h(n), cn, n))
    return None


# ---------------- Mùa 3: Monte Carlo Localization (Ch. 13) ----------------
def rai_hat(n, rng):
    out = np.empty((0, 3))
    while len(out) < n:
        c = np.column_stack([rng.uniform(0, RONG, 2 * n), rng.uniform(0, DAI, 2 * n), rng.uniform(-np.pi, np.pi, 2 * n)])
        out = np.vstack([out, c[~chiem(c[:, 0], c[:, 1])]])
    return out[:n]


def mcl_di(P, ds, dth, rng):
    """Đẩy hạt theo quãng đường ds và góc quay dth đo từ bánh xe (có nhiễu)."""
    n = len(P)
    dd = ds + rng.normal(0, 0.1 * abs(ds) + 0.005, n)
    tt = dth + rng.normal(0, 0.08 * abs(dth) + 0.01, n)
    th = goc(P[:, 2] + tt)
    return np.column_stack([P[:, 0] + dd * np.cos(th), P[:, 1] + dd * np.sin(th), th])


def mcl_cap_nhat(P, z, rng, sig=SIG_TIA):
    du = quet_ban_do(P, GOC_TIA[TIA_MCL])
    p = (1 - P_DEU) * np.exp(-0.5 * ((du - z[TIA_MCL]) / sig) ** 2) + P_DEU * 0.2
    logw = np.log(p).sum(1)
    logw[chiem(P[:, 0], P[:, 1])] = -np.inf
    w = np.exp(logw - logw.max())
    w /= w.sum()
    c = np.cumsum(w)
    idx = np.minimum(np.searchsorted(c, (rng.random() + np.arange(len(P))) / len(P)), len(P) - 1)
    P = P[idx]
    nt = int(THA * len(P))
    P[rng.choice(len(P), nt, replace=False)] = rai_hat(nt, rng)
    return P


def mcl_uoc_luong(P):
    """Trung bình đám hạt đông nhất: lấy trung bình, rồi trung bình lại các hạt trong 0,7 m. Trả về (tư thế, tỉ lệ hạt gần)."""
    m = np.median(P[:, :2], 0)
    for _ in range(3):
        gan = np.hypot(P[:, 0] - m[0], P[:, 1] - m[1]) < 0.7
        if not gan.any():
            break
        m = P[gan, :2].mean(0)
    gan = np.hypot(P[:, 0] - m[0], P[:, 1] - m[1]) < 0.3
    th = math.atan2(np.sin(P[gan, 2]).mean(), np.cos(P[gan, 2]).mean()) if gan.any() else 0.0
    return np.array([m[0], m[1], th]), float(gan.mean())


# ---------------- Mùa 2: camera + YOLO của tập 2.8 ----------------
_YOLO = None


def yolo():
    global _YOLO
    if _YOLO is None:
        import yolo_nap as Y        # trọng số đã học ở tập 2.8
        _YOLO = Y
    return _YOLO


def chieu(dx, dy, th):
    Z = dx * math.cos(th) + dy * math.sin(th)
    X = dx * math.sin(th) - dy * math.cos(th)
    return X, Z


def ve_anh(x, nguoi, rng):
    """Ảnh 128×128 robot nhìn thấy, đúng kiểu vẽ của tập 2.8/2.9; người sau tường thì không vẽ."""
    N = N_ANH
    y, xx = np.mgrid[0:N, 0:N] / N
    anh = np.where((y < 0.5)[..., None], np.array([0.66, 0.7, 0.62]), np.array([0.42, 0.36, 0.32])).copy()
    vat = []
    for p in nguoi:
        X, Z = chieu(p[0] - x[0], p[1] - x[1], x[2])
        if Z < 0.4 or not nhin_thay(x, p):
            continue
        fn = F_CAM / N
        h = fn * H_NGUOI / Z
        w = h * 0.37
        cy = 0.5 + fn * H_CAM / Z - h / 2
        cx = 0.5 + fn * X / Z
        if cx + w / 2 < 0 or cx - w / 2 > 1:
            continue
        vat.append((Z, cx, cy, w, h))
    for Z, cx, cy, w, h in sorted(vat, reverse=True):
        y0, y1 = cy - h / 2, cy + h / 2
        r = w * 0.32
        dau = (xx - cx) ** 2 + (y - (y0 + r)) ** 2 < r ** 2
        than = (np.abs(xx - cx) < w / 2) & (y > y0 + 2 * r) & (y < y0 + 0.62 * h)
        chan = ((np.abs(xx - (cx - w * 0.2)) < w * 0.14) | (np.abs(xx - (cx + w * 0.2)) < w * 0.14)) & (y >= y0 + 0.62 * h) & (y < y1)
        anh[dau] = [0.9, 0.75, 0.6]
        anh[than | chan] = [0.15, 0.55, 0.85]
    anh = np.clip(anh + rng.normal(0, 0.05, anh.shape), 0, 1)
    return anh.transpose(2, 0, 1).astype(np.float32)


def tim_nguoi(anh):
    Y = yolo()
    with torch.no_grad():
        box, lop = Y.MANG(torch.tensor(anh)[None])
    ds = [d for d in Y.nms(Y.giai_ma(box[0], lop[0], 0.3)) if d[0] == 0 and d[1] >= 0.5]
    if not ds:
        return None
    c, s, cx, cy, w, h = max(ds, key=lambda d: d[1])
    return H_NGUOI * F_CAM / (h * N_ANH), math.atan((cx - 0.5) * N_ANH / F_CAM), (s, cx, cy, w, h)


def ghep(uoc, z, Z_cam, huong):
    """Kết hợp cảm biến (Mùa 3, tập 3.8): camera cho biết ĐÓ LÀ NGƯỜI và ở hướng nào; LiDAR đo khoảng cách chính xác:
    lấy tia gần hướng đó (±1 tia) chạm vào vật KHÔNG có trên bản đồ. Không có tia như vậy thì dùng Z = f·H/h của camera."""
    j = int(np.argmin(np.abs(goc(GOC_TIA + huong))))     # tia LiDAR gần hướng người nhất (huong > 0: người bên phải)
    la = vat_la(uoc, z)
    ung = [(z[i % SO_TIA], i % SO_TIA) for i in (j - 1, j, j + 1) if la[i % SO_TIA]]
    if ung:
        d, i = min(ung)
        a = uoc[2] + GOC_TIA[i]
        d += R_NGUOI                                      # LiDAR chạm mặt người, tâm người ở sau thêm một bán kính
    else:
        d, a = Z_cam, uoc[2] - huong
    return (uoc[0] + d * math.cos(a), uoc[1] + d * math.sin(a)), d


def trong_phong(p, phong):
    x0, y0, x1, y1 = PHONG[phong]
    return x0 < p[0] < x1 and y0 < p[1] < y1


# ---------------- một lượt giao đồ ----------------
def chon_diem(rng, phong, m=KC_TUONG):
    x0, y0, x1, y1 = PHONG[phong]
    while True:
        p = (rng.uniform(x0 + 0.3, x1 - 0.3), rng.uniform(y0 + 0.3, y1 - 0.3))
        if not chiem(*p, m=m):
            return p


def tao_luot(seed):
    rng = np.random.default_rng(seed)
    phong_dau = ["khach", "ngu", "lamviec"][rng.integers(3)]
    p = chon_diem(rng, phong_dau)
    dich = ["ngu", "lamviec"][rng.integers(2)]
    q = chon_diem(rng, dich)
    while math.hypot(q[0] - p[0], q[1] - p[1]) < 1.0:     # người nhận không đứng sát chỗ robot xuất phát
        q = chon_diem(rng, dich)
    return {"seed": seed, "x0": np.array([p[0], p[1], rng.uniform(-np.pi, np.pi)]), "phong_dau": phong_dau, "dich": dich,
            "nguoi_nhan": np.array(q), "pha_nguoi_di": rng.uniform(0, 15.0),
            "bv": rng.normal(0, 0.03), "bw": rng.normal(0, 0.05), "troi": rng.normal(0, 0.01)}


def nguoi_di_tai(t, pha):
    """Đi 2,7 m mất 5,4 s, đứng 2 s, đi về, đứng 2 s (chu kỳ 14,8 s)."""
    (ax, ay), (bx, by) = DUONG_NGUOI_DI
    L = math.hypot(bx - ax, by - ay)
    T1 = L / 0.5
    u = (t + pha) % (2 * T1 + 4)
    if u < T1:
        k = u / T1
    elif u < T1 + 2:
        k = 1.0
    elif u < 2 * T1 + 2:
        k = 1 - (u - T1 - 2) / T1
    else:
        k = 0.0
    return np.array([ax + k * (bx - ax), ay + k * (by - ay)])


def chay_luot(L, bo="du", ghi=False):
    """bo: 'du' (đủ 4 mùa) | 'khong_m1' (không A*) | 'khong_m2' (không camera) | 'khong_m3' (không định vị, chỉ đếm bánh xe)
    | 'khong_m4' (bộ não tuần tự: không DỪNG chờ, không xoay tìm)."""
    rng = np.random.default_rng(1000 + L["seed"])
    rng_ghi = np.random.default_rng(0)
    x = L["x0"].copy()
    nhan = L["nguoi_nhan"]
    P = rai_hat(K0, rng)
    uoc = L["x0"].copy() if bo == "khong_m3" else np.array([RONG / 2, DAI / 2, 0.0])
    s = "CHỜ LỆNH"
    truoc_dung = None
    duong, i_duong, t_lap = None, 0, -99.0
    dich = None
    e_cu = 0.0
    hen = 0.0              # đồng hồ trong trạng thái (giây)
    luoi_tam, vat_tam, het_tam = LUOI_AN_TOAN.copy(), np.zeros_like(BAN_DO), -1.0
    vet, v_vet = None, np.zeros(2)            # vị trí + vận tốc ước lượng của vật lạ gần nhất
    tron_dinh_vi = 0
    lech_dem, so_mat, da_lay = 0, 0, False
    dau_tim, i_nhin, muc_tieu = 0.0, 0, None
    ds_acc = dth_acc = 0.0
    log = {"x": [], "uoc": [], "s": [], "nguoi_di": [], "hat": [], "duong": [], "anh": None, "loi_dinh_vi": []}
    ket, ly_do = "het_gio", ""
    so_dung, so_lap = 0, 0
    lan_dung_t = 0.0
    t = 0.0
    k = 0
    while t < T_MAX:
        nguoi_di = nguoi_di_tai(t, L["pha_nguoi_di"])
        z = quet_that(x, [nguoi_di, nhan], rng)
        # ---- Mùa 3: cập nhật định vị mỗi 0,2 s ----
        if bo != "khong_m3" and k % 2 == 0:
            P = mcl_di(P, ds_acc, dth_acc, rng)
            ds_acc = dth_acc = 0.0
            P = mcl_cap_nhat(P, z, rng, SIG_TIA0 if s in ("CHỜ LỆNH", "ĐỊNH VỊ") else SIG_TIA)
            uoc, gan = mcl_uoc_luong(P)
            # LiDAR có khớp bản đồ tại tư thế ước lượng không? (để phát hiện "mất dấu")
            khop = float(np.mean(np.abs(z - quet_ban_do(uoc[None], GOC_TIA)[0]) < 0.3))
            lech_dem = lech_dem + 1 if khop < 0.5 else 0
        # ---- sinh sự kiện (đầu vào i_t) ----
        truoc = np.abs(goc(GOC_TIA)) < math.radians(35)
        diem_la = vat_la(uoc, z, vat_tam if t < het_tam else None) & truoc & (z < 0.8)
        co_vat_la = s in ("ĐI LẤY", "ĐI GIAO", "DỪNG") and bo != "khong_m4" and bool(diem_la.any())
        # Mùa 3 (tập 3.8): theo dõi vật lạ đang di chuyển (người), ước lượng vận tốc, đoán 2 s tới có va vào đường robot không
        la_all = vat_la(uoc, z) & (z < 3.0)
        if la_all.any():
            th_a = uoc[2] + GOC_TIA[la_all]
            px, py = uoc[0] + z[la_all] * np.cos(th_a), uoc[1] + z[la_all] * np.sin(th_a)
            j0 = int(np.argmin(z[la_all]))
            cum = np.hypot(px - px[j0], py - py[j0]) < 0.5
            c = np.array([px[cum].mean(), py[cum].mean()])
            v_vet = 0.7 * v_vet + 0.3 * (c - vet) / DT if vet is not None and np.hypot(*(c - vet)) < 0.3 else np.zeros(2)
            vet = c
        else:
            vet, v_vet = None, np.zeros(2)
        nguy = False
        if vet is not None and s in ("ĐI LẤY", "ĐI GIAO", "DỪNG") and bo != "khong_m4" and np.hypot(*v_vet) > 0.15:
            huong_r = np.array([math.cos(uoc[2]), math.sin(uoc[2])])
            for tau in np.arange(0, 2.01, 0.2):
                if np.hypot(*(vet + v_vet * tau - uoc[:2] - V_MAX * tau * huong_r)) < 0.7:
                    nguy = True
                    break
        co_vat_la = co_vat_la or nguy
        v = w = 0.0

        def bam(dich_, nhin_truoc=0.4):
            """Mùa 1: A* (lập lại mỗi 3 s) + PD trên góc hướng."""
            nonlocal duong, i_duong, t_lap, e_cu, so_lap, luoi_tam
            if duong is None or t - t_lap > 3.0:
                if bo == "khong_m1":
                    duong = [tuple(dich_)]
                else:
                    duong = a_sao(uoc[:2], dich_, luoi_tam if t < het_tam else LUOI_AN_TOAN) or a_sao(uoc[:2], dich_) or [tuple(dich_)]
                i_duong, t_lap = 0, t
                so_lap += 1
                if ghi:
                    log["duong"].append({"t": round(t, 1), "d": [[round(a, 2), round(b, 2)] for a, b in duong[::3] + [duong[-1]]]})
            d = np.hypot(np.array([p[0] for p in duong]) - uoc[0], np.array([p[1] for p in duong]) - uoc[1])
            i_duong = max(i_duong, int(np.argmin(d[i_duong:])) + i_duong)
            j = i_duong
            while j < len(duong) - 1 and d[j] < nhin_truoc:
                j += 1
            r = math.atan2(duong[j][1] - uoc[1], duong[j][0] - uoc[0])
            e = float(goc(r - uoc[2]))                      # e = r − y
            w_ = float(np.clip(2.0 * e + 0.1 * (e - e_cu) / DT, -W_MAX, W_MAX))
            e_cu = e
            v_ = V_MAX * max(0.0, math.cos(e)) ** 2
            con = math.hypot(dich_[0] - uoc[0], dich_[1] - uoc[1])
            v_ = min(v_, 0.3 + con)
            if KC_BAN_DO[o_cua(*uoc[:2])[1], o_cua(*uoc[:2])[0]] < 0.6:   # sát tường / qua cửa: đi chậm
                v_ = min(v_, 0.25)
            return v_, w_, con

        # ---- Mùa 4: máy trạng thái ----
        s_moi = s
        if s == "CHỜ LỆNH":
            if t >= 1.0:
                s_moi = "ĐI LẤY" if bo == "khong_m3" else "ĐỊNH VỊ"
        elif s == "ĐỊNH VỊ":
            if hen < 8.0:
                w = 0.8
            else:  # đi về phía thoáng nhất phía trước để thấy thêm
                truoc90 = np.abs(goc(GOC_TIA)) <= math.radians(60)
                j = int(np.argmax(np.where(truoc90, z, -1)))
                w = float(np.clip(1.5 * goc(GOC_TIA[j]), -1.0, 1.0))
                v = 0.3 if z[truoc].min() > 0.5 else 0.0
            tron_dinh_vi = tron_dinh_vi + 1 if gan >= 0.9 else 0
            if tron_dinh_vi >= 15 and hen >= 12.0:   # xoay 8 s rồi đi thêm một đoạn: tránh chốt nhầm chỗ giống nhau
                s_moi = "ĐI GIAO" if da_lay else "ĐI LẤY"
                P = P[rng.choice(len(P), K, replace=False)]
            elif hen > 60:
                ket, ly_do = "that_bai", "không định vị được"
                break
        elif s in ("ĐI LẤY", "ĐI GIAO", "DỪNG") and lech_dem >= 10 and bo != "khong_m3":
            s_moi, P, tron_dinh_vi, duong = "ĐỊNH VỊ", rai_hat(K0, rng), 0, None   # mất dấu 2 s: định vị lại từ đầu
            so_mat += 1
        elif s in ("ĐI LẤY", "ĐI GIAO"):
            if co_vat_la:
                truoc_dung, s_moi = s, "DỪNG"
                so_dung += 1
            else:
                dich = DIEM_LAY if s == "ĐI LẤY" else DIEM_NHIN[L["dich"]][i_nhin]
                v, w, con = bam(dich)
                if con < 0.25:
                    s_moi = "NHẬN ĐỒ" if s == "ĐI LẤY" else ("TÌM NGƯỜI" if bo != "khong_m2" else "GIAO")
        elif s == "DỪNG":
            if vet is not None and np.hypot(*v_vet) > 0.15:     # người đang đi tới chỗ robot đứng: tiến hoặc lùi để tránh
                huong_r = np.array([math.cos(uoc[2]), math.sin(uoc[2])])
                ts = np.arange(0, 2.01, 0.2)
                gan_nhat = lambda vc: min(np.hypot(*(vet + v_vet * tau - uoc[:2] - vc * tau * huong_r)) for tau in ts)
                dung_yen = gan_nhat(0.0)
                if dung_yen < 0.6:
                    lua = [(gan_nhat(vc), vc) for vc, phia in ((0.25, 0.0), (-0.25, np.pi))
                           if z[np.abs(goc(GOC_TIA - phia)) < math.radians(30)].min() > 0.45]
                    if lua and max(lua)[0] > dung_yen:
                        v = max(lua)[1]
            if not co_vat_la and hen > 1.0:
                s_moi, duong = truoc_dung, None
            elif hen > 6.0:                         # chờ quá lâu: ghi vật lạ vào lưới tạm, lập đường vòng
                if t >= het_tam:
                    luoi_tam, vat_tam = LUOI_AN_TOAN.copy(), np.zeros_like(BAN_DO)
                th_t = uoc[2] + GOC_TIA[diem_la]
                for px, py in zip(uoc[0] + z[diem_la] * np.cos(th_t), uoc[1] + z[diem_la] * np.sin(th_t)):
                    ix, iy = o_cua(px, py)
                    yy, xx = np.ogrid[:NY, :NX]
                    luoi_tam |= (xx - ix) ** 2 + (yy - iy) ** 2 <= 5 ** 2
                    vat_tam |= (xx - ix) ** 2 + (yy - iy) ** 2 <= 4 ** 2
                het_tam = t + 20.0
                s_moi, duong = truoc_dung, None
        elif s == "NHẬN ĐỒ":
            da_lay = True
            if hen >= 2.0:
                s_moi = "ĐI GIAO"
        elif s == "TÌM NGƯỜI":
            if bo == "khong_m4" and hen > 0.3:     # không xoay tìm: chỉ nhìn một lần
                if muc_tieu is None:
                    ket, ly_do = "that_bai", "không thấy người nhận"
                    break
            else:
                w = 0.6
            if k % 3 == 0:
                anh = ve_anh(x, [nguoi_di, nhan], rng)
                kq = tim_nguoi(anh)
                if kq is not None:
                    Z, huong, box = kq
                    mt, Z = ghep(uoc, z, Z, huong)
                    kq = kq if trong_phong(mt, L["dich"]) else None   # người ở phòng khác (vd. thấy qua cửa): bỏ qua
                if kq is not None:
                    muc_tieu = mt
                    if ghi and log["anh"] is None:
                        log["anh"] = {"anh": anh, "box": [round(v_, 3) for v_ in box], "Z": round(Z, 2), "t": round(t, 1),
                                      "Z_that": round(float(math.hypot(nhan[0] - x[0], nhan[1] - x[1])), 2)}
                    s_moi, duong = "TIẾP CẬN", None
            if s_moi == "TÌM NGƯỜI" and hen > 2 * math.pi / 0.6 + 0.5 and bo != "khong_m4":
                if i_nhin + 1 < len(DIEM_NHIN[L["dich"]]):
                    i_nhin += 1
                    s_moi, duong = "ĐI GIAO", None
                else:
                    ket, ly_do = "that_bai", "không thấy người nhận"
                    break
        elif s == "TIẾP CẬN":
            if k % 3 == 0:                          # nhìn lại để cập nhật vị trí người nhận
                kq = tim_nguoi(ve_anh(x, [nguoi_di, nhan], rng))
                if kq is not None:
                    mt, _ = ghep(uoc, z, kq[0], kq[1])
                    if trong_phong(mt, L["dich"]):
                        muc_tieu = mt
            kc = math.hypot(muc_tieu[0] - uoc[0], muc_tieu[1] - uoc[1])
            if kc <= 0.65 or z[truoc].min() < 0.5:
                s_moi = "GIAO"
            else:
                g = muc_tieu
                if LUOI_AN_TOAN[o_cua(*g)[1], o_cua(*g)[0]]:   # người đứng gần đồ: nhắm điểm trống gần nhất trên đường tới
                    for a in np.linspace(0, 1, 30):
                        q = (g[0] + a * (uoc[0] - g[0]), g[1] + a * (uoc[1] - g[1]))
                        if not LUOI_AN_TOAN[o_cua(*q)[1], o_cua(*q)[0]]:
                            g = q
                            break
                v, w, _ = bam(g)
                v = min(v, 0.3)
        elif s == "GIAO":
            if muc_tieu is not None:
                e = float(goc(math.atan2(muc_tieu[1] - uoc[1], muc_tieu[0] - uoc[0]) - uoc[2]))
                w = float(np.clip(2.0 * e, -1.0, 1.0))
            if hen >= 2.0:
                d = float(math.hypot(nhan[0] - x[0], nhan[1] - x[1]))
                lech = abs(float(goc(math.atan2(nhan[1] - x[1], nhan[0] - x[0]) - x[2])))
                if d <= 1.0 and lech <= math.radians(30):
                    ket = "thanh_cong"
                else:
                    ket, ly_do = "that_bai", f"giao sai chỗ (cách người {d:.1f} m)"
                break
        if s_moi != s:
            s, hen = s_moi, 0.0
        # ---- chuyển động thật (bánh xe trượt) ----
        v_that = v * (1 + L["bv"]) + (rng.normal(0, 0.02) if v else 0.0)
        w_that = w * (1 + L["bw"]) + L["troi"] + rng.normal(0, 0.03)
        th = goc(x[2] + w_that * DT)
        x = np.array([x[0] + v_that * DT * math.cos(th), x[1] + v_that * DT * math.sin(th), th])
        ds_acc += v * DT
        dth_acc += w * DT
        if bo == "khong_m3":                        # chỉ đếm bánh xe
            th_u = goc(uoc[2] + w * DT)
            uoc = np.array([uoc[0] + v * DT * math.cos(th_u), uoc[1] + v * DT * math.sin(th_u), th_u])
        # ---- va chạm ----
        vong = x[2] + np.linspace(0, 2 * np.pi, 12, endpoint=False)
        if chiem(x[0] + R_ROBOT * np.cos(vong), x[1] + R_ROBOT * np.sin(vong)).any():
            ket, ly_do = "that_bai", "đâm tường / đồ đạc"
        elif min(np.hypot(*(nguoi_di - x[:2])), np.hypot(*(nhan - x[:2]))) < R_ROBOT + R_NGUOI:
            ket, ly_do = "that_bai", "đâm vào người"
        if ghi:
            log["x"].append([round(float(v_), 3) for v_ in x])
            log["uoc"].append([round(float(v_), 3) for v_ in uoc])
            log["s"].append(s)
            log["nguoi_di"].append([round(float(v_), 2) for v_ in nguoi_di])
            if k % 5 == 0 and bo != "khong_m3":
                sub = P[rng_ghi.choice(len(P), 150, replace=False)]   # rng riêng: ghi log không đổi kết quả
                log["hat"].append([[round(float(a), 2), round(float(b), 2)] for a, b, _ in sub])
        if bo != "khong_m3" and s not in ("CHỜ LỆNH", "ĐỊNH VỊ"):
            log["loi_dinh_vi"].append(float(math.hypot(uoc[0] - x[0], uoc[1] - x[1])))
        if ket == "that_bai":
            break
        t += DT
        hen += DT
        k += 1
    out = {"seed": L["seed"], "bo": bo, "ket": ket, "ly_do": ly_do, "t": round(t, 1), "so_dung": so_dung, "so_lap": so_lap, "so_mat": so_mat,
           "loi_dinh_vi_tb": float(np.mean(log["loi_dinh_vi"])) if log["loi_dinh_vi"] else None,
           "loi_dinh_vi_max": float(np.max(log["loi_dinh_vi"])) if log["loi_dinh_vi"] else None, "dich": L["dich"]}
    if ghi:
        out["log"] = log
    return out


def _chay(args):
    seed, bo = args
    torch.set_num_threads(1)
    return chay_luot(tao_luot(seed), bo)


if __name__ == "__main__":
    import json
    import time
    from multiprocessing import Pool

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    bos = sys.argv[2].split(",") if len(sys.argv) > 2 else ["du", "khong_m1", "khong_m2", "khong_m3", "khong_m4"]
    t0 = time.time()
    kq = {}
    with Pool(6) as pool:
        for bo in bos:
            r = pool.map(_chay, [(s, bo) for s in range(n)])
            kq[bo] = r
            ok = [x for x in r if x["ket"] == "thanh_cong"]
            ly = {}
            for x in r:
                if x["ket"] != "thanh_cong":
                    ly[x["ly_do"] or x["ket"]] = ly.get(x["ly_do"] or x["ket"], 0) + 1
            print(f"{bo}: thành công {len(ok)}/{n} · thời gian TB {np.mean([x['t'] for x in ok]) if ok else 0:.1f} s · lý do hỏng {ly} · {time.time() - t0:.0f} s", flush=True)
    (GOC / f"ket_qua_{n}.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf8")
