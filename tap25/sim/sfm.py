"""Tập 2.5 - Dựng 3D từ ảnh chụp (series Tự Học Robot Tự Hành)

Theo Chương 7, Principles of Robot Autonomy, §7.3 Structure From Motion:
  - Một camera di chuyển, K đã biết; p_jk^h = K[R_k t_k] P_j^h
  - §7.3.1 hai ảnh: ước lượng F (Eq. 7.5-7.6, 8 điểm), E = K^T F K, tách E ra 4 cặp (R, t),
    chọn cặp cho các điểm có độ sâu dương ở cả hai camera, tam giác hoá (Eq. 7.8). Tỉ lệ tuyệt đối không suy ra được từ ảnh.
  - §7.3.2 thêm từng ảnh: PnP định vị camera mới bằng các điểm 3D đã có, tam giác hoá điểm mới;
    bundle adjustment (Eq. 7.9) chỉnh mọi camera và mọi điểm cùng lúc để cực tiểu sai số chiếu lại.
Mở rộng (ngoài sách): chuẩn hoá điểm khi ước lượng F, công thức tách E bằng SVD, giải PnP bằng cv2.solvePnP,
gắn tỉ lệ bằng một cạnh đo thật, căn chỉnh Umeyama để đo sai số.
Ngôi nhà mô hình, quỹ đạo camera và nhiễu là GIẢ ĐỊNH; mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 sfm.py
"""
import cv2
import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix
from scipy.spatial.transform import Rotation

RNG = np.random.default_rng(25)
K = np.array([[500.0, 0, 320], [0, 500.0, 240], [0, 0, 1]])  # camera 640×480 của tập 2.2
W, H = 640, 480
NHIEU_PX = 0.7
SO_ANH = 12

# Ngôi nhà mô hình (m): rộng 2 (x), sâu 1,5 (z), tường cao 1,2, nóc cao 1,8 (trục y hướng lên)
RONG, SAU, TUONG, NOC = 2.0, 1.5, 1.2, 1.8


def mat_nha():
    """Các mặt của ngôi nhà: (hàm lấy mẫu điểm, pháp tuyến hướng ra ngoài)."""
    x0, x1, z0, z1 = -RONG / 2, RONG / 2, -SAU / 2, SAU / 2
    mats = []
    mats.append((lambda a, b: np.stack([x0 + a * RONG, b * TUONG, np.full_like(a, z1)], -1), [0, 0, 1]))   # mặt trước
    mats.append((lambda a, b: np.stack([x0 + a * RONG, b * TUONG, np.full_like(a, z0)], -1), [0, 0, -1]))  # mặt sau
    mats.append((lambda a, b: np.stack([np.full_like(a, x0), b * TUONG, z0 + a * SAU], -1), [-1, 0, 0]))   # trái
    mats.append((lambda a, b: np.stack([np.full_like(a, x1), b * TUONG, z0 + a * SAU], -1), [1, 0, 0]))    # phải
    # hai mái: từ mép tường (y = TUONG, z = ±SAU/2) lên nóc (y = NOC, z = 0)
    n_mai = np.array([0, SAU / 2, NOC - TUONG]); n_mai /= np.linalg.norm(n_mai)
    mats.append((lambda a, b: np.stack([x0 + a * RONG, TUONG + b * (NOC - TUONG), z1 * (1 - b)], -1), list(n_mai)))
    mats.append((lambda a, b: np.stack([x0 + a * RONG, TUONG + b * (NOC - TUONG), z0 * (1 - b)], -1), [0, n_mai[1], -n_mai[2]]))
    return mats


def tao_diem():
    diem, phap = [], []
    for ham, n in mat_nha():
        so = 40
        P = ham(RNG.uniform(0.04, 0.96, so), RNG.uniform(0.04, 0.96, so))
        diem.append(P)
        phap.append(np.tile(n, (so, 1)))
    # sân quanh nhà (mặt đất y = 0): camera nào cũng thấy, giúp nối các ảnh với nhau
    goc, r = RNG.uniform(0, 2 * np.pi, 160), RNG.uniform(1.6, 3.0, 160)
    diem.append(np.stack([r * np.cos(goc), np.zeros(160), r * np.sin(goc)], -1))
    phap.append(np.tile([0, 1.0, 0], (160, 1)))
    # hai điểm mốc ở chân hai góc mặt trước: khoảng cách thật = RONG (dùng để gắn tỉ lệ)
    diem.append(np.array([[-RONG / 2 + 0.01, 0.01, SAU / 2], [RONG / 2 - 0.01, 0.01, SAU / 2]]))
    phap.append(np.array([[0, 0, 1.0], [0, 0, 1.0]]))
    return np.vstack(diem), np.vstack(phap)


P_THAT, PHAP = tao_diem()
MOC = [len(P_THAT) - 2, len(P_THAT) - 1]


def nhin_vao(tam, dich=np.array([0, 0.8, 0])):
    """R, t (thế giới -> camera) cho camera đặt ở `tam` nhìn về `dich`; trục camera: x phải, y xuống, z tới."""
    z = dich - tam; z /= np.linalg.norm(z)
    x = np.cross(z, [0, 1, 0]); x /= np.linalg.norm(x)
    y = np.cross(z, x)
    R = np.stack([x, y, z])
    return R, -R @ tam


# Camera đi nửa vòng quanh nhà, từ chếch trái phía trước sang chếch phải phía sau
GOC = np.radians(np.linspace(-60, 150, SO_ANH))
TAM_CAM = np.stack([5.0 * np.sin(GOC), np.full(SO_ANH, 1.6), 5.0 * np.cos(GOC)], -1)
CAM_THAT = [nhin_vao(c) for c in TAM_CAM]


def chieu(R, t, P):
    Pc = P @ R.T + t
    uv = Pc @ K.T
    return uv[:, :2] / uv[:, 2:], Pc[:, 2]


# Quan sát: điểm thấy được nếu mặt của nó quay về camera và nằm trong ảnh
QUAN_SAT = []  # mỗi ảnh: dict {chỉ số điểm: (u, v)}
for (R, t), c in zip(CAM_THAT, TAM_CAM):
    uv, z = chieu(R, t, P_THAT)
    thay = ((c - P_THAT) * PHAP).sum(1) > 0.05
    thay &= (z > 0) & (uv[:, 0] > 2) & (uv[:, 0] < W - 2) & (uv[:, 1] > 2) & (uv[:, 1] < H - 2)
    uv = uv + RNG.normal(0, NHIEU_PX, uv.shape)
    QUAN_SAT.append({j: uv[j] for j in np.where(thay)[0]})


def chuan_hoa(p):
    m = p.mean(0)
    s = np.sqrt(2) / np.linalg.norm(p - m, axis=1).mean()
    return np.array([[s, 0, -s * m[0]], [0, s, -s * m[1]], [0, 0, 1]])


def tim_F(p1, p2):
    """Eq. 7.5-7.6: p1^T F p2 = 0 (theo quy ước sách), 8 điểm có chuẩn hoá, ép hạng 2."""
    T1, T2 = chuan_hoa(p1), chuan_hoa(p2)
    a = (T1 @ np.column_stack([p1, np.ones(len(p1))]).T).T
    b = (T2 @ np.column_stack([p2, np.ones(len(p2))]).T).T
    Wm = np.stack([np.outer(x, y).ravel() for x, y in zip(a, b)])
    Fh = np.linalg.svd(Wm)[2][-1].reshape(3, 3)
    U, S, Vt = np.linalg.svd(Fh)
    Fh = U @ np.diag([S[0], S[1], 0]) @ Vt
    return T1.T @ Fh @ T2


def tam_giac(P1, P2, x1, x2):
    """Eq. 7.8: [(p1×)P1; (p2×)P2] P = 0, giải bằng SVD."""
    out = []
    for a, b in zip(x1, x2):
        A = np.vstack([a[0] * P1[2] - P1[0], a[1] * P1[2] - P1[1], b[0] * P2[2] - P2[0], b[1] * P2[2] - P2[1]])
        X = np.linalg.svd(A)[2][-1]
        out.append(X[:3] / X[3])
    return np.array(out)


def hai_anh(i=0, k=1):
    """§7.3.1: trả về (R, t) của ảnh k so với ảnh i (ảnh i là gốc), điểm 3D và số điểm trước camera của 4 nghiệm."""
    chung = sorted(set(QUAN_SAT[i]) & set(QUAN_SAT[k]))
    p1 = np.array([QUAN_SAT[i][j] for j in chung])
    p2 = np.array([QUAN_SAT[k][j] for j in chung])
    F = tim_F(p1, p2)  # p1^T F p2 = 0
    E = K.T @ F @ K    # x1^T E x2 = 0 với x = K^-1 p
    # Đổi về dạng x2^T E' x1 = 0 để tách (R, t) đưa điểm từ camera i sang camera k
    U, _, Vt = np.linalg.svd(E.T)
    if np.linalg.det(U) < 0: U = -U
    if np.linalg.det(Vt) < 0: Vt = -Vt
    Wz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    nghiem = [(U @ Wz @ Vt, U[:, 2]), (U @ Wz @ Vt, -U[:, 2]), (U @ Wz.T @ Vt, U[:, 2]), (U @ Wz.T @ Vt, -U[:, 2])]
    P1 = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
    dem, kq = [], []
    for R, t in nghiem:
        P2 = K @ np.hstack([R, t[:, None]])
        X = tam_giac(P1, P2, p1, p2)
        z1, z2 = X[:, 2], (X @ R.T + t)[:, 2]
        dem.append(int(((z1 > 0) & (z2 > 0)).sum()))
        kq.append((R, t, X))
    tot = int(np.argmax(dem))
    R, t, X = kq[tot]
    return R, t, dict(zip(chung, X)), dem, len(chung)


def ghep_tuan_tu():
    """§7.3.2: thêm từng ảnh bằng PnP, tam giác hoá điểm mới với ảnh liền trước. Chưa bundle adjustment."""
    R1, t1, diem, dem, n_chung = hai_anh(0, 1)
    cams = [(np.eye(3), np.zeros(3)), (R1, t1)]
    lich_su = [len(diem)]
    them_luc = {j: 1 for j in diem}  # điểm j được dựng ở ảnh thứ mấy
    for k in range(2, SO_ANH):
        co = [j for j in QUAN_SAT[k] if j in diem]
        obj = np.array([diem[j] for j in co])
        img = np.array([QUAN_SAT[k][j] for j in co])
        _, rv, tv = cv2.solvePnP(obj, img, K, None, flags=cv2.SOLVEPNP_ITERATIVE)
        R = cv2.Rodrigues(rv)[0]
        cams.append((R, tv.ravel()))
        # điểm mới: tam giác hoá với ảnh cũ thấy điểm đó mà đứng xa camera mới nhất (tia cắt nhau rõ hơn)
        tam = [-Ri.T @ ti for Ri, ti in cams]
        Pb = K @ np.hstack([R, tv])
        for j in QUAN_SAT[k]:
            if j in diem:
                continue
            cu = [i for i in range(k) if j in QUAN_SAT[i]]
            if not cu:
                continue
            i = max(cu, key=lambda i: np.linalg.norm(tam[i] - tam[k]))
            Pa = K @ np.hstack([cams[i][0], cams[i][1][:, None]])
            diem[j] = tam_giac(Pa, Pb, QUAN_SAT[i][j][None], QUAN_SAT[k][j][None])[0]
            them_luc[j] = k
        lich_su.append(len(diem))
    return cams, diem, dem, n_chung, lich_su, them_luc


def sai_chieu_lai(cams, diem):
    d = []
    for (R, t), qs in zip(cams, QUAN_SAT):
        for j, uv in qs.items():
            if j in diem:
                d.append(chieu(R, t, diem[j][None])[0][0] - uv)
    d = np.array(d)
    return float(np.sqrt((d ** 2).sum(1).mean()))


def bundle_adjustment(cams, diem):
    """Eq. 7.9: cực tiểu Σ_k Σ_j ‖p_jk − π(K, R_k, t_k, P_j)‖² theo mọi R_k, t_k, P_j (ảnh 0 giữ cố định)."""
    ids = sorted(diem)
    vi_tri = {j: i for i, j in enumerate(ids)}
    obs = [(k, vi_tri[j], uv) for k, qs in enumerate(cams and QUAN_SAT) for j, uv in qs.items() if j in vi_tri]
    nc = len(cams) - 1
    x0 = np.concatenate([np.concatenate([Rotation.from_matrix(R).as_rotvec(), t]) for R, t in cams[1:]] + [np.array([diem[j] for j in ids]).ravel()])

    def tach(x):
        cs = [(np.eye(3), np.zeros(3))] + [(Rotation.from_rotvec(x[6 * i:6 * i + 3]).as_matrix(), x[6 * i + 3:6 * i + 6]) for i in range(nc)]
        return cs, x[6 * nc:].reshape(-1, 3)

    def phan_du(x):
        cs, P = tach(x)
        r = np.empty((len(obs), 2))
        for n, (k, i, uv) in enumerate(obs):
            R, t = cs[k]
            Pc = R @ P[i] + t
            q = K @ Pc
            r[n] = q[:2] / q[2] - uv
        return r.ravel()

    A = lil_matrix((2 * len(obs), len(x0)), dtype=int)
    for n, (k, i, _) in enumerate(obs):
        if k > 0:
            A[2 * n:2 * n + 2, 6 * (k - 1):6 * k] = 1
        A[2 * n:2 * n + 2, 6 * nc + 3 * i:6 * nc + 3 * i + 3] = 1
    kq = least_squares(phan_du, x0, jac_sparsity=A, x_scale="jac", method="trf")
    cs, P = tach(kq.x)
    return cs, {j: P[vi_tri[j]] for j in ids}


def can_chinh(diem, cams):
    """Gắn tỉ lệ bằng cạnh đo thật (2 điểm mốc cách nhau RONG), rồi xoay + dời cho khớp (Umeyama, tỉ lệ cố định)."""
    s = RONG / np.linalg.norm(diem[MOC[0]] - diem[MOC[1]])
    ids = sorted(diem)
    A = np.array([diem[j] for j in ids]) * s
    B = P_THAT[ids]
    ma, mb = A.mean(0), B.mean(0)
    U, _, Vt = np.linalg.svd((B - mb).T @ (A - ma))
    D = np.diag([1, 1, np.sign(np.linalg.det(U @ Vt))])
    Rw = U @ D @ Vt
    A2 = (A - ma) @ Rw.T + mb
    loi = np.linalg.norm(A2 - B, axis=1)
    tam = []
    for R, t in cams:
        c = -R.T @ t * s  # tâm camera trong hệ dựng lại, đã nhân tỉ lệ
        tam.append(Rw @ (c - ma) + mb)
    return s, dict(zip(ids, A2)), loi, np.array(tam)


CAMS0, DIEM0, DEM_4, N_CHUNG, SO_DIEM, THEM_LUC = ghep_tuan_tu()
RMS_TRUOC = sai_chieu_lai(CAMS0, DIEM0)
CAMS1, DIEM1 = bundle_adjustment(CAMS0, DIEM0)
RMS_SAU = sai_chieu_lai(CAMS1, DIEM1)
S0, A0, LOI0, TAM0 = can_chinh(DIEM0, CAMS0)
S1, A1, LOI1, TAM1 = can_chinh(DIEM1, CAMS1)
TI_LE_GOC = float(np.linalg.norm(-CAMS1[1][0].T @ CAMS1[1][1]))  # khoảng cách ảnh 0 - ảnh 1 trong hệ dựng lại (=1)
BASELINE_THAT = float(np.linalg.norm(TAM_CAM[1] - TAM_CAM[0]))

if __name__ == "__main__":
    print(f"{len(P_THAT)} điểm trên nhà · {SO_ANH} ảnh · mỗi ảnh thấy {[len(q) for q in QUAN_SAT]} điểm")
    print(f"Hai ảnh đầu: {N_CHUNG} cặp điểm chung · 4 nghiệm (R, t) có số điểm nằm trước cả hai camera: {DEM_4}")
    print(f"Tỉ lệ: khoảng cách 2 camera đầu trong mô hình = {TI_LE_GOC:.2f} (đơn vị tuỳ ý), thật = {BASELINE_THAT:.2f} m")
    print(f"Số điểm 3D sau mỗi ảnh: {SO_DIEM}")
    print(f"Sai số chiếu lại: ghép tuần tự {RMS_TRUOC:.2f} px -> sau bundle adjustment {RMS_SAU:.2f} px")
    print(f"Sau khi gắn tỉ lệ bằng cạnh {RONG} m: sai số 3D trung bình {LOI0.mean() * 100:.1f} cm (trước BA) -> {LOI1.mean() * 100:.1f} cm (sau BA)")
    print(f"Tâm camera lệch trung bình: {np.linalg.norm(TAM0 - TAM_CAM, axis=1).mean() * 100:.1f} cm -> {np.linalg.norm(TAM1 - TAM_CAM, axis=1).mean() * 100:.1f} cm")
