"""Tập 2.3 - Hiệu chỉnh camera bằng bàn cờ (series Tự Học Robot Tự Hành)

Theo Chương 6, Principles of Robot Autonomy:
  - Eq. 6.4: méo xuyên tâm  [u_d, v_d] = (1 + k r²)[u - u_cd, v - v_cd] + [u_cd, v_cd]
  - §6.5.2 (Zhang): bàn cờ phẳng Z_W = 0 -> p^h = H P̃_W^h, H = K[r1 r2 t] (Eq. 6.26-6.27)
    r1 ⟂ r2 -> 2 phương trình mỗi ảnh theo B = K^-T K^-1 (Eq. 6.28-6.31), Vb = 0 (Eq. 6.32),
    b = vectơ kỳ dị nhỏ nhất (Eq. 6.33), lấy K dạng đóng (Eq. 6.34), R, t (Eq. 6.35-6.36).
  - Tinh chỉnh: cực tiểu tổng bình phương sai lệch ‖p_ij - p̂_ij‖² bằng Levenberg-Marquardt, giống Eq. 6.47.
Mở rộng (ngoài sách): chuẩn hoá điểm khi tìm H (Hartley), đưa k vào bước tinh chỉnh, tên gọi "sai số chiếu lại"
(RMS), đối chiếu với cv2.calibrateCamera.
Camera "thật", bàn cờ, các góc chụp và nhiễu là GIẢ ĐỊNH; mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 hieu_chinh.py
"""
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

RNG = np.random.default_rng(23)

# Camera "thật" (máy không biết): lệch nhẹ so với thông số danh nghĩa 500 / 320 / 240 của tập 2.2
W, H_ANH = 640, 480
K_THAT = np.array([[512.0, 0.0, 331.0], [0.0, 508.0, 236.0], [0.0, 0.0, 1.0]])
K_DANH_NGHIA = np.array([[500.0, 0.0, 320.0], [0.0, 500.0, 240.0], [0.0, 0.0, 1.0]])
K_MEO = -6e-7  # hệ số méo k (px^-2), âm = méo thùng
NHIEU_PX = 0.3  # nhiễu dò góc ô cờ (px)

# Bàn cờ 9×6 góc trong, ô 30 mm
CO_X, CO_Y, O = 9, 6, 0.03
DIEM_CO = np.array([[i * O, j * O] for j in range(CO_Y) for i in range(CO_X)])  # (X_W, Y_W), Z_W = 0
SO_ANH = 10


def meo(uv, k, c):
    """Eq. 6.4 (tâm méo = tâm ảnh)."""
    d = uv - c
    r2 = (d ** 2).sum(axis=1, keepdims=True)
    return (1 + k * r2) * d + c


def bo_meo(uv_d, k, c, lap=20):
    """Ngược Eq. 6.4 bằng lặp điểm bất động."""
    uv = uv_d.copy()
    for _ in range(lap):
        r2 = ((uv - c) ** 2).sum(axis=1, keepdims=True)
        uv = (uv_d - c) / (1 + k * r2) + c
    return uv


def quay(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def chieu(K, R, t, XY):
    """p^h = K [r1 r2 t] [X, Y, 1]^T (Eq. 6.26-6.27)."""
    Hm = K @ np.column_stack([R[:, 0], R[:, 1], t])
    ph = (Hm @ np.column_stack([XY, np.ones(len(XY))]).T).T
    return ph[:, :2] / ph[:, 2:]


def chup_anh():
    """Chụp bàn cờ SO_ANH lần ở các góc khác nhau, ảnh có méo + nhiễu. Chỉ giữ ảnh thấy đủ cả bàn cờ."""
    anh = []
    tam = DIEM_CO.mean(axis=0)
    while len(anh) < SO_ANH:
        R = quay(*np.radians(RNG.uniform([-35, -35, -20], [35, 35, 20])))
        Z = RNG.uniform(0.3, 0.45)
        lech = RNG.uniform([-0.08, -0.06], [0.08, 0.06])
        t = np.array([lech[0], lech[1], Z]) - R @ np.array([tam[0], tam[1], 0.0])
        uv = meo(chieu(K_THAT, R, t, DIEM_CO), K_MEO, K_THAT[:2, 2])
        uv = uv + RNG.normal(0, NHIEU_PX, uv.shape)
        if (uv[:, 0] > 5).all() and (uv[:, 0] < W - 5).all() and (uv[:, 1] > 5).all() and (uv[:, 1] < H_ANH - 5).all():
            anh.append({"R": R, "t": t, "uv": uv})
    return anh


def chuan_hoa(P):
    m, s = P.mean(axis=0), np.sqrt(2) / np.linalg.norm(P - P.mean(axis=0), axis=1).mean()
    return np.array([[s, 0, -s * m[0]], [0, s, -s * m[1]], [0, 0, 1]])


def tim_H(XY, uv):
    """Homography bàn cờ -> ảnh bằng DLT (kiểu Eq. 6.20-6.23), có chuẩn hoá điểm."""
    T1, T2 = chuan_hoa(XY), chuan_hoa(uv)
    a = (T1 @ np.column_stack([XY, np.ones(len(XY))]).T).T
    b = (T2 @ np.column_stack([uv, np.ones(len(uv))]).T).T
    A = []
    for (X, Y, _), (u, v, _) in zip(a, b):
        A.append([-X, -Y, -1, 0, 0, 0, u * X, u * Y, u])
        A.append([0, 0, 0, -X, -Y, -1, v * X, v * Y, v])
    h = np.linalg.svd(np.array(A))[2][-1]
    Hm = np.linalg.inv(T2) @ h.reshape(3, 3) @ T1
    return Hm / Hm[2, 2]


def v_ij(Hm, i, j):
    c = Hm.T  # c[0] = c̃1, c[1] = c̃2
    hi, hj = c[i], c[j]
    return np.array([hi[0] * hj[0], hi[0] * hj[1] + hi[1] * hj[0], hi[1] * hj[1],
                     hi[2] * hj[0] + hi[0] * hj[2], hi[2] * hj[1] + hi[1] * hj[2], hi[2] * hj[2]])


def zhang(ds_uv):
    """§6.5.2: mỗi ảnh -> H -> 2 dòng của V; Vb = 0 -> B -> K -> R, t."""
    Hs = [tim_H(DIEM_CO, uv) for uv in ds_uv]
    V = np.vstack([np.vstack([v_ij(Hm, 0, 1), v_ij(Hm, 0, 0) - v_ij(Hm, 1, 1)]) for Hm in Hs])
    b = np.linalg.svd(V)[2][-1]
    B11, B12, B22, B13, B23, B33 = b
    v0 = (B12 * B13 - B11 * B23) / (B11 * B22 - B12 ** 2)
    lam = B33 - (B13 ** 2 + v0 * (B12 * B13 - B11 * B23)) / B11
    alpha = np.sqrt(lam / B11)
    beta = np.sqrt(lam * B11 / (B11 * B22 - B12 ** 2))
    gamma = -B12 * alpha ** 2 * beta / lam
    u0 = gamma * v0 / beta - B13 * alpha ** 2 / lam
    K = np.array([[alpha, gamma, u0], [0, beta, v0], [0, 0, 1]])
    Ki, ngoai = np.linalg.inv(K), []
    for Hm in Hs:
        s = 1 / np.linalg.norm(Ki @ Hm[:, 0])
        r1, r2, t = s * Ki @ Hm[:, 0], s * Ki @ Hm[:, 1], s * Ki @ Hm[:, 2]
        U, _, Vt = np.linalg.svd(np.column_stack([r1, r2, np.cross(r1, r2)]))  # Eq. 6.36
        ngoai.append((U @ Vt, t))
    return K, ngoai, V.shape


def du_doan(K, ngoai, k):
    return [meo(chieu(K, R, t, DIEM_CO), k, K[:2, 2]) for R, t in ngoai]


def rms(ds_a, ds_b):
    d = np.vstack(ds_a) - np.vstack(ds_b)
    return float(np.sqrt((d ** 2).sum(axis=1).mean()))


def goi(K, k, ngoai):
    x = [K[0, 0], K[1, 1], K[0, 1], K[0, 2], K[1, 2], k * 1e7]  # k nhân 1e7 cho cùng cỡ số
    for R, t in ngoai:
        x += list(Rotation.from_matrix(R).as_rotvec()) + list(t)
    return np.array(x)


def mo(x):
    a, b, g, u0, v0, k = x[:6]
    K = np.array([[a, g, u0], [0, b, v0], [0, 0, 1]])
    ngoai = [(Rotation.from_rotvec(x[6 + 6 * i:9 + 6 * i]).as_matrix(), x[9 + 6 * i:12 + 6 * i]) for i in range((len(x) - 6) // 6)]
    return K, k * 1e-7, ngoai


def hieu_chinh(anh):
    """B1: Zhang thuần (coi như không méo). B2: tinh chỉnh K, k, R, t cùng lúc (Levenberg-Marquardt)."""
    ds_uv = [a["uv"] for a in anh]
    K0, ngoai0, V_shape = zhang(ds_uv)
    x0 = goi(K0, 0.0, ngoai0)
    sai = lambda x: (np.vstack(du_doan(*mo(x)[:1], mo(x)[2], mo(x)[1])) - np.vstack(ds_uv)).ravel()
    kq = least_squares(sai, x0, method="lm")
    K, k, ngoai = mo(kq.x)
    lich_su = [{"buoc": "Zhang (bỏ qua méo)", "K": K0, "k": 0.0, "ngoai": ngoai0, "rms": rms(du_doan(K0, ngoai0, 0.0), ds_uv)},
               {"buoc": "Tinh chỉnh LM (có méo)", "K": K, "k": k, "ngoai": ngoai, "rms": rms(du_doan(K, ngoai, k), ds_uv)}]
    return K, k, ngoai, lich_su, V_shape


def do_cong(uv):
    """Độ cong của 1 hàng điểm: khoảng cách lớn nhất tới đường thẳng nối 2 đầu (px)."""
    a, b = uv[0], uv[-1]
    n = np.array([-(b - a)[1], (b - a)[0]]) / np.linalg.norm(b - a)
    return float(np.abs((uv - a) @ n).max())


def luoi_thang(n=9):
    """Các đường thẳng ngang/dọc phủ kín ảnh (để vẽ trước/sau khử méo)."""
    duong = []
    for y in np.linspace(20, H_ANH - 20, 7):
        duong.append(np.column_stack([np.linspace(0, W, 33), np.full(33, y)]))
    for x in np.linspace(20, W - 20, n):
        duong.append(np.column_stack([np.full(25, x), np.linspace(0, H_ANH, 25)]))
    return duong


ANH = chup_anh()
K_UOC, K_MEO_UOC, NGOAI, LICH_SU, V_SHAPE = hieu_chinh(ANH)
GOC = np.array([[W, H_ANH]], dtype=float)
LECH_GOC_ANH = float(np.linalg.norm(meo(GOC, K_MEO, K_THAT[:2, 2]) - GOC))

# Một điểm gần góc ảnh, cách camera 2 m: robot biết Z, dùng camera để đoán X, Y
DIEM_XA = np.array([0.55, 0.42, 2.0])
UV_DIEM_XA = meo((K_THAT @ DIEM_XA / DIEM_XA[2])[None, :2], K_MEO, K_THAT[:2, 2])[0]


def doan_diem(K, k):
    uv = bo_meo(UV_DIEM_XA[None], k, K[:2, 2])[0]
    return (np.linalg.inv(K) @ np.array([uv[0], uv[1], 1.0]))[:2] * DIEM_XA[2]


DOAN_TRUOC, DOAN_SAU = doan_diem(K_DANH_NGHIA, 0.0), doan_diem(K_UOC, K_MEO_UOC)
LECH_TRUOC = float(np.linalg.norm(DOAN_TRUOC - DIEM_XA[:2]))
LECH_SAU = float(np.linalg.norm(DOAN_SAU - DIEM_XA[:2]))

if __name__ == "__main__":
    print(f"Ảnh chụp: {len(ANH)} · mỗi ảnh {len(DIEM_CO)} góc ô · V có kích thước {V_SHAPE} (2N × 6)")
    print(f"Méo thật k = {K_MEO:.1e}: góc ảnh (640,480) bị kéo lệch {LECH_GOC_ANH:.1f} px")
    print(f"Điểm thật {DIEM_XA.tolist()} m -> pixel {UV_DIEM_XA.round(1)}; đoán lại vị trí khi biết Z = 2 m:")
    print(f"  dùng 500/320/240, bỏ méo: lệch {LECH_TRUOC * 100:.1f} cm · sau hiệu chỉnh: lệch {LECH_SAU * 1000:.1f} mm")
    for h in LICH_SU:
        Kh = h["K"]
        print(f"  {h['buoc']}: k = {h['k']:.2e}  α={Kh[0,0]:.1f} β={Kh[1,1]:.1f} γ={Kh[0,1]:.2f} "
              f"u0={Kh[0,2]:.1f} v0={Kh[1,2]:.1f}  RMS = {h['rms']:.2f} px")
    print(f"K thật: α=512 β=508 u0=331 v0=236 · k thật = {K_MEO:.1e} · ước lượng k = {K_MEO_UOC:.2e}")
    # Độ cong của hàng góc ô cờ ở mép ảnh (ảnh có góc nghiêng ít nhất) trước/sau khử méo
    hang = max(ANH, key=lambda a: np.abs(a["uv"][:CO_X, 1] - 240).mean())["uv"][:CO_X]
    print(f"Hàng góc ô cờ xa tâm nhất: cong {do_cong(hang):.2f} px trước, "
          f"{do_cong(bo_meo(hang, K_MEO_UOC, K_UOC[:2, 2])):.2f} px sau khử méo")
    duong = luoi_thang()
    cong = [do_cong(meo(d, K_MEO, K_THAT[:2, 2])) for d in duong]
    print(f"Lưới đường thẳng: cong tối đa {max(cong):.1f} px khi méo")

    # Đối chiếu OpenCV (mở rộng: OpenCV dùng mô hình méo k1, k2, p1, p2, k3 trên toạ độ chuẩn hoá)
    import cv2
    obj = [np.column_stack([DIEM_CO, np.zeros(len(DIEM_CO))]).astype(np.float32) for _ in ANH]
    img = [a["uv"].astype(np.float32).reshape(-1, 1, 2) for a in ANH]
    err, Kcv, dist, _, _ = cv2.calibrateCamera(obj, img, (W, H_ANH), None, None)
    print(f"OpenCV: fx={Kcv[0,0]:.1f} fy={Kcv[1,1]:.1f} cx={Kcv[0,2]:.1f} cy={Kcv[1,2]:.1f} RMS={err:.2f} px "
          f"(k1={dist.ravel()[0]:.3f})")
