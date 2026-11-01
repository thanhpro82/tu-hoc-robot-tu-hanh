"""Tập 3.8 - Kết hợp cảm biến & theo dõi nhiều người (series Tự Học Robot Tự Hành)

Theo Chương 15, Principles of Robot Autonomy:
  - Ví dụ 15.0.1: radar đo khoảng cách tốt, camera đo hướng tốt -> bổ sung cho nhau (complementary)
  - Ví dụ 15.2.1 / §15.2.1: ghép theo Bayes, phương sai sau ghép nhỏ hơn cả hai; dạng thông tin Y = Σ⁻¹ cộng dồn
  - §15.5.1: mô hình vận tốc không đổi (CV), x = [x, y, ẋ, ẏ], F(Δt), Q(q, Δt) gia tốc trắng
  - §15.5.2: cổng Mahalanobis m² = z̃ᵀ S⁻¹ z̃ ≤ χ²_{2;0,99} ≈ 9,21
  - §15.5.3 Thuật toán 2: GNN, ma trận chi phí C_ij = m²_ij, giải bằng thuật toán Hungary; không khớp -> tăng bất định
  - §15.5.4: khởi tạo M/N, giữ track khi bị che tối đa N_miss khung, xoá track hỏng
  - §15.5.7: MOTA = 1 − (FN + FP + IDSW) / GT
Mở rộng / giả định: 5 người với lộ trình định sẵn (2 người đi cắt qua nhau như Ví dụ 15.5.2), camera σ_r = 0,8 m σ_θ = 1°,
radar σ_r = 0,1 m σ_θ = 6°, mỗi cảm biến thấy mỗi người với xác suất 0,9, trung bình 1 báo động giả mỗi khung, coi như đã
biết phát hiện camera và radar nào cùng là một người; M/N = 2/3, N_miss = 5; ngưỡng so khớp khi chấm điểm 0,7 m;
cách so sánh "ghép theo điểm gần nhất, không dự đoán"; chi phí m² + ln|S|; không khởi tạo track từ phát hiện đã nằm trong cổng;
gộp track trùng khi cách nhau < 0,25 m. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 theo_doi.py
"""
import numpy as np
from scipy.optimize import linear_sum_assignment

RNG = np.random.default_rng(38)
DT, T = 0.1, 20.0
NF = int(T / DT)
CAM = (0.8, np.radians(1.0))   # σ khoảng cách, σ góc
RAD = (0.1, np.radians(6.0))
P_D, LAM_GIA = 0.9, 1.0
GATE = 9.21
Q_CV = 0.1
M_N = (3, 4)
N_MISS = 5
NGUONG_KHOP = 0.7


def nguoi():
    """5 lộ trình (x, y theo thời gian), robot ở gốc nhìn theo +y. None = chưa vào / đã ra khỏi tầm nhìn."""
    t = np.arange(NF) * DT
    P = []
    P.append(np.column_stack([-5 + 0.5 * t, 6.0 + 0.0 * t]))                 # A: trái -> phải
    P.append(np.column_stack([5 - 0.5 * t, 6.6 + 0.0 * t]))                  # B: phải -> trái, lướt qua A (cách 0,6 m) ở t = 10 s
    P.append(np.column_stack([-3 + 0.25 * t, 10 - 0.2 * t]))                 # C: chéo
    D = np.column_stack([3.5 + 0.0 * t, 3 + 0.35 * t]); D[t < 4] = np.nan   # D: xuất hiện ở giây 4
    P.append(D)
    E = np.column_stack([-4 + 0.4 * t, 3.5 + 0.1 * t]); E[t > 14] = np.nan  # E: rời đi ở giây 14
    P.append(E)
    return np.stack(P, 1)  # (NF, 5, 2)


GT = nguoi()


def cuc_sang_de_cac(r, b):
    return np.array([r * np.sin(b), r * np.cos(b)])  # góc b đo từ trục y (hướng nhìn), x sang phải


def do(p, s):
    r, b = np.hypot(*p), np.arctan2(p[0], p[1])
    rm, bm = r + RNG.normal(0, s[0]), b + RNG.normal(0, s[1])
    z = cuc_sang_de_cac(rm, bm)
    J = np.array([[np.sin(bm), rm * np.cos(bm)], [np.cos(bm), -rm * np.sin(bm)]])
    return z, J @ np.diag([s[0] ** 2, s[1] ** 2]) @ J.T


def ghep(ds):
    """Dạng thông tin (§15.2.1): Y = Σ R_i⁻¹, y = Σ R_i⁻¹ z_i."""
    Y = sum(np.linalg.inv(R) for _, R in ds)
    y = sum(np.linalg.inv(R) @ z for z, R in ds)
    S = np.linalg.inv(Y)
    return S @ y, S


def tao_phat_hien():
    """Mỗi khung: danh sách (z, R) đã ghép camera + radar cho người được thấy, cộng báo động giả."""
    khung, loi, gia = [], {"cam": [], "rad": [], "ghep": []}, []
    for k in range(NF):
        ds = []
        for i in range(GT.shape[1]):
            p = GT[k, i]
            if np.isnan(p[0]):
                continue
            c = do(p, CAM) if RNG.random() < P_D else None
            r = do(p, RAD) if RNG.random() < P_D else None
            if c:
                loi["cam"].append(np.hypot(*(c[0] - p)))
            if r:
                loi["rad"].append(np.hypot(*(r[0] - p)))
            co = [m for m in (c, r) if m]
            if co:
                z, R = ghep(co)
                if c and r:
                    loi["ghep"].append(np.hypot(*(z - p)))
                ds.append((z, R))
        n_that = len(ds)
        for _ in range(RNG.poisson(LAM_GIA)):  # báo động giả kiểu camera
            p = np.array([RNG.uniform(-6, 6), RNG.uniform(2, 12)])
            ds.append(do(p, CAM))
        khung.append(ds)
        gia.append(set(range(n_that, len(ds))))
    return khung, {k: float(np.sqrt(np.mean(np.square(v)))) for k, v in loi.items()}, gia


KHUNG, RMSE_CB, GIA = tao_phat_hien()

F = np.array([[1, 0, DT, 0], [0, 1, 0, DT], [0, 0, 1, 0], [0, 0, 0, 1]])
Q = Q_CV * np.array([[DT ** 3 / 3, 0, DT ** 2 / 2, 0], [0, DT ** 3 / 3, 0, DT ** 2 / 2], [DT ** 2 / 2, 0, DT, 0], [0, DT ** 2 / 2, 0, DT]])
H = np.array([[1.0, 0, 0, 0], [0, 1, 0, 0]])


class Track:
    dem = 0

    def __init__(self, z, R):
        Track.dem += 1
        self.id = Track.dem
        self.x = np.r_[z, 0, 0]
        self.P = np.diag([R[0, 0], R[1, 1], 0.25, 0.25])  # người đi bộ: vận tốc ban đầu σ 0,5 m/s
        self.lich_su = [1]
        self.mat = 0
        self.xac_nhan = False

    def du_doan(self):
        self.x = F @ self.x
        self.P = F @ self.P @ F.T + Q

    def m2(self, z, R):
        S = H @ self.P @ H.T + R
        e = z - H @ self.x
        return float(e @ np.linalg.solve(S, e))

    def chi_phi(self, z, R):
        """m² + ln|S| (âm log-likelihood, mở rộng): phát hiện mơ hồ (S lớn) bị phạt, không cướp chỗ phát hiện rõ."""
        S = H @ self.P @ H.T + R
        return self.m2(z, R) + float(np.log(np.linalg.det(S)))

    def cap_nhat(self, z, R):
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ (z - H @ self.x)
        self.P = (np.eye(4) - K @ H) @ self.P


def chay_kalman_gnn():
    Track.dem = 0
    tracks, ra = [], []
    for ds in KHUNG:
        for tr in tracks:
            tr.du_doan()
        if tracks and ds:
            C = np.full((len(tracks), len(ds)), 1e6)  # ngoài cổng: chi phí rất lớn
            for i, tr in enumerate(tracks):
                for j, (z, R) in enumerate(ds):
                    if tr.m2(z, R) <= GATE:
                        C[i, j] = tr.chi_phi(z, R)
            hang, cot = linear_sum_assignment(C)
            cap = [(i, j) for i, j in zip(hang, cot) if C[i, j] < 1e5]
        else:
            cap = []
        da_ghep_t = {i for i, _ in cap}
        da_ghep_d = {j for _, j in cap}
        for i, j in cap:
            tracks[i].cap_nhat(*ds[j])
            tracks[i].lich_su.append(1)
            tracks[i].mat = 0
        for i, tr in enumerate(tracks):
            if i not in da_ghep_t:
                tr.lich_su.append(0)
                tr.mat += 1
        for tr in tracks:
            if not tr.xac_nhan and sum(tr.lich_su[-M_N[1]:]) >= M_N[0]:
                tr.xac_nhan = True
        # dọn dẹp (§15.5.4, gộp track trùng): hai track đã xác nhận sát nhau < 0,25 m thì bỏ track mới hơn
        xn = sorted([tr for tr in tracks if tr.xac_nhan], key=lambda tr: tr.id)
        bo = set()
        for a in range(len(xn)):
            for b in range(a + 1, len(xn)):
                if xn[b].id not in bo and np.hypot(*(xn[a].x[:2] - xn[b].x[:2])) < 0.25:
                    bo.add(xn[b].id)
        tracks = [tr for tr in tracks if tr.id not in bo]
        tracks = [tr for tr in tracks if (tr.xac_nhan and tr.mat < N_MISS) or (not tr.xac_nhan and len(tr.lich_su) <= M_N[1] and sum(tr.lich_su[-M_N[1]:]) + (M_N[1] - len(tr.lich_su[-M_N[1]:])) >= M_N[0])]
        for j, (z, R) in enumerate(ds):
            # phát hiện thừa nằm trong cổng của track đã xác nhận thì không khởi tạo track mới (mở rộng)
            if j not in da_ghep_d and not any(tr.xac_nhan and tr.m2(z, R) <= GATE for tr in tracks):
                tracks.append(Track(z, R))
        ra.append([(tr.id, tr.x[:2].copy(), np.sqrt(np.trace(tr.P[:2, :2]))) for tr in tracks if tr.xac_nhan])
    return ra


def chay_gan_nhat(nguong=1.0):
    """So sánh (mở rộng): ghép mỗi phát hiện với track gần vị trí cũ nhất, không dự đoán chuyển động, không cổng thống kê."""
    dem = 0
    tracks, ra = [], []
    for ds in KHUNG:
        dung = set()
        for tr in tracks:
            if not ds:
                tr["mat"] += 1
                continue
            d = [np.hypot(*(z - tr["p"])) if j not in dung else 1e9 for j, (z, _) in enumerate(ds)]
            j = int(np.argmin(d))
            if d[j] < nguong:
                tr["p"] = ds[j][0]
                tr["mat"] = 0
                tr["hit"] += 1
                dung.add(j)
            else:
                tr["mat"] += 1
        tracks = [tr for tr in tracks if tr["mat"] < N_MISS]
        for j, (z, _) in enumerate(ds):
            if j not in dung:
                dem += 1
                tracks.append({"id": dem, "p": z.copy(), "mat": 0, "hit": 1})
        ra.append([(tr["id"], tr["p"].copy(), 0.0) for tr in tracks if tr["hit"] >= 2])
    return ra


def cham_diem(ra):
    """MOTA (§15.5.7) với so khớp Hungary theo khoảng cách ≤ NGUONG_KHOP."""
    fn = fp = idsw = gt_tong = 0
    truoc = {}
    loi = []
    for k in range(NF):
        g = [(i, GT[k, i]) for i in range(GT.shape[1]) if not np.isnan(GT[k, i, 0])]
        h = ra[k]
        gt_tong += len(g)
        if g and h:
            D = np.array([[np.hypot(*(p - q)) for _, q, _ in h] for _, p in g])
            r, c = linear_sum_assignment(D)
            cap = [(a, b) for a, b in zip(r, c) if D[a, b] <= NGUONG_KHOP]
        else:
            cap = []
        fn += len(g) - len(cap)
        fp += len(h) - len(cap)
        for a, b in cap:
            gi, tid = g[a][0], h[b][0]
            if gi in truoc and truoc[gi] != tid:
                idsw += 1
            truoc[gi] = tid
            loi.append(np.hypot(*(g[a][1] - h[b][1])))
    return {"FN": fn, "FP": fp, "IDSW": idsw, "GT": gt_tong, "MOTA": 1 - (fn + fp + idsw) / gt_tong, "loi": float(np.mean(loi))}


RA_KF = chay_kalman_gnn()
RA_NN = chay_gan_nhat()
DIEM_KF, DIEM_NN = cham_diem(RA_KF), cham_diem(RA_NN)

# Ví dụ 15.2.1 dạng vô hướng: hai phép đo cùng một khoảng cách
S1, S2 = CAM[0], RAD[0]
S_GHEP = float(np.sqrt(S1 ** 2 * S2 ** 2 / (S1 ** 2 + S2 ** 2)))

if __name__ == "__main__":
    so_pd = sum(len(d) for d in KHUNG)
    print(f"{NF} khung × {DT} s · 5 người · {so_pd} phát hiện (gồm báo động giả, trung bình {LAM_GIA}/khung)")
    print(f"Sai số vị trí từng phát hiện (RMSE): chỉ camera {RMSE_CB['cam']:.2f} m · chỉ radar {RMSE_CB['rad']:.2f} m · ghép cả hai {RMSE_CB['ghep']:.2f} m")
    print(f"Ví dụ 15.2.1 (khoảng cách): σ_camera {S1} m, σ_radar {S2} m -> σ_ghép {S_GHEP:.3f} m")
    for ten, d in (("Gần nhất, không dự đoán", DIEM_NN), ("Kalman + cổng + Hungary", DIEM_KF)):
        print(f"{ten:24s}: IDSW {d['IDSW']:3d} · FP {d['FP']:4d} · FN {d['FN']:4d} / GT {d['GT']} · MOTA {d['MOTA'] * 100:5.1f}% · lệch TB {d['loi'] * 100:.1f} cm")
    print(f"Số ID đã cấp: Kalman {max(t for k in RA_KF for t, *_ in k)} · gần nhất {max(t for k in RA_NN for t, *_ in k)}")
