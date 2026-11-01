"""Tập 3.1 - "Tôi đang ở đâu?": robot nghĩ bằng xác suất (series Tự Học Robot Tự Hành)

Theo Chương 11, Principles of Robot Autonomy:
  - Niềm tin bel(x_t) = p(x_t | z_1:t, u_1:t) (Eq. 11.10), dự đoán bel̄(x_t) = p(x_t | z_1:t-1, u_1:t) (Eq. 11.11)
  - Mô hình chuyển động p(x_t | x_t-1, u_t) (Eq. 11.8), mô hình đo p(z_t | x_t) (Eq. 11.9)
  - Bộ lọc Bayes rời rạc (Thuật toán 2): dự đoán p̄_k = Σ_i p(x_k | x_i, u_t) p_i ; hiệu chỉnh p_k = η p(z_t | x_k) p̄_k
  - Ví dụ 11.3.1: robot trong hành lang 1 chiều, chuyển động Δx ~ N(u_t, 0,1²); cấu trúc lặp lại làm niềm tin nhiều đỉnh
Mở rộng / giả định: cảm biến "thấy cửa" (sách dùng cảm biến khoảng cách), vị trí 3 cửa, xác suất cảm biến
p(thấy cửa | ở cửa) = 0,8 và p(thấy cửa | không ở cửa) = 0,1, chuyển động u = 0,5 m mỗi bước.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 bayes.py
"""
import numpy as np

SEED = 36  # chọn lần chạy có bước đầu thấy cửa (để kể chuyện); kết quả vẫn là chạy thật
RNG = np.random.default_rng(SEED)
DAI, O = 10.0, 0.05  # hành lang 10 m, ô 5 cm
X = np.arange(0, DAI, O) + O / 2
CUA = [(1.0, 1.8), (2.6, 3.4), (6.2, 7.0)]  # 3 cánh cửa (từ, đến) mét: khoảng cách giữa các cửa khác nhau
O_CUA = np.zeros_like(X, dtype=bool)
for a, b in CUA:
    O_CUA |= (X >= a) & (X <= b)
P_THAY_O_CUA, P_THAY_KHONG_CUA = 0.8, 0.1
U, SIGMA = 0.5, 0.1  # Ví dụ 11.3.1: Δx ~ N(u, 0,1²)
SO_BUOC = 12
X0 = 1.3  # vị trí thật ban đầu (robot không biết)


def du_doan(bel):
    """p̄_k = Σ_i p(x_k | x_i, u) p_i với p(x_k | x_i, u) = N(x_k − x_i; u, σ²).
    Giả thuyết bị đẩy ra khỏi hành lang là không thể (robot chưa đụng tường) nên bỏ đi rồi chuẩn hoá lại."""
    d = X[:, None] - X[None, :]  # x_k − x_i
    K = np.exp(-0.5 * ((d - U) / SIGMA) ** 2) / (np.sqrt(2 * np.pi) * SIGMA / O)
    out = K @ bel
    return out / out.sum()


def hieu_chinh(bel_tr, thay_cua):
    """p_k = η p(z | x_k) p̄_k."""
    p_z = np.where(O_CUA, P_THAY_O_CUA, P_THAY_KHONG_CUA)
    if not thay_cua:
        p_z = 1 - p_z
    bel = p_z * bel_tr
    eta = 1 / bel.sum()
    return bel * eta, eta


def so_dinh(bel, nguong=0.25):
    """Đếm số đỉnh (cực đại cục bộ cao hơn 25% đỉnh lớn nhất)."""
    m = bel.max()
    return int(sum(1 for k in range(1, len(bel) - 1) if bel[k] >= bel[k - 1] and bel[k] > bel[k + 1] and bel[k] > nguong * m))


def p_quanh(bel, x, r=0.25):
    return float(bel[np.abs(X - x) <= r].sum())


def chay():
    bel = np.full_like(X, 1 / len(X))  # chưa biết gì: đều khắp hành lang
    x = X0
    log = [{"buoc": 0, "x": x, "loai": "đầu", "bel": bel.copy(), "z": None}]
    for k in range(SO_BUOC + 1):
        if k > 0:  # đi tới: vị trí thật trượt ngẫu nhiên
            x = x + RNG.normal(U, SIGMA)
            bel = du_doan(bel)
            log.append({"buoc": k, "x": x, "loai": "dự đoán", "bel": bel.copy(), "z": None})
        o_cua = any(a <= x <= b for a, b in CUA)
        z = bool(RNG.random() < (P_THAY_O_CUA if o_cua else P_THAY_KHONG_CUA))
        bel, eta = hieu_chinh(bel, z)
        log.append({"buoc": k, "x": x, "loai": "hiệu chỉnh", "bel": bel.copy(), "z": z, "eta": eta, "o_cua": o_cua})
    return log


LOG = chay()

if __name__ == "__main__":
    print(f"Hành lang {DAI} m chia {len(X)} ô {O * 100:.0f} cm · cửa ở {CUA} · p(thấy|cửa) = {P_THAY_O_CUA}, p(thấy|không) = {P_THAY_KHONG_CUA}")
    print(f"Chuyển động mỗi bước u = {U} m, nhiễu σ = {SIGMA} m")
    for r in LOG:
        b = r["bel"]
        uoc = float(X[np.argmax(b)])
        z = "" if r["z"] is None else ("thấy cửa" if r["z"] else "không thấy")
        print(f"bước {r['buoc']:2d} {r['loai']:10s} x thật {r['x']:.2f} m | {z:10s} | đỉnh lớn nhất {b.max() * 100:5.2f}% tại {uoc:.2f} m "
              f"| số đỉnh {so_dinh(b)} | P(±25 cm quanh vị trí thật) = {p_quanh(b, r['x']) * 100:.1f}%")
    cuoi = LOG[-1]
    print(f"Cuối: ước lượng (trung bình) {float((X * cuoi['bel']).sum()):.2f} m, thật {cuoi['x']:.2f} m")
