"""Tập 2.6 - Thị giác máy tính cổ điển (series Tự Học Robot Tự Hành)

Theo Chương 8, Principles of Robot Autonomy:
  - §8.1.1 lọc ảnh: tương quan / tích chập (Eq. 8.1-8.2), lọc Gauss G_σ, mặt nạ tách được, mặt nạ Sobel (Eq. 8.5)
  - §8.1.2 dò cạnh: làm mịn -> đạo hàm theo x, y -> |∇S| = sqrt(S_x² + S_y²) -> ngưỡng + chỉ giữ cực đại cục bộ (Ví dụ 8.1.3)
  - §8.2.1 biến đổi Hough dạng cực x cos α + y sin α = r: mỗi điểm cạnh bỏ phiếu trong lưới (α, r), đỉnh = đường thẳng
Mở rộng (ngoài sách): ứng dụng dò vạch dẫn đường cho robot và góc lái suy ra từ vạch (sách không có ví dụ bám vạch);
cách chọn ngưỡng theo phần trăm; tách hai mép vạch thành đường giữa.
Ảnh sàn nhà, vạch, vết bẩn và nhiễu là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 thi_giac.py
"""
import numpy as np
from scipy.ndimage import convolve, gaussian_filter, maximum_filter

RNG = np.random.default_rng(26)
W, H = 320, 240
NHIEU = 28.0  # nhiễu ảnh (mức xám)
SIGMA = 2.0  # độ rộng lọc Gauss
VACH_RONG = 14  # bề rộng vạch (px)
# Vạch dẫn đường thật: đường giữa x cos α + y sin α = r (gốc ở góc trên trái, y hướng xuống)
ALPHA_THAT = np.radians(23.4)
R_THAT = 160 * np.cos(ALPHA_THAT) + 240 * np.sin(ALPHA_THAT)  # đi qua điểm (160, 240) ở mép dưới giữa ảnh


def tao_anh():
    y, x = np.mgrid[0:H, 0:W].astype(float)
    san = 170 + 20 * gaussian_filter(RNG.normal(0, 1, (H, W)), 6) * 6  # sàn có vân mờ
    kc = x * np.cos(ALPHA_THAT) + y * np.sin(ALPHA_THAT) - R_THAT  # khoảng cách có dấu tới đường giữa
    anh = np.where(np.abs(kc) < VACH_RONG / 2, 55.0, san)
    # vài vết bẩn tròn (vật gây nhiễu)
    for cx, cy, rr in [(60, 60, 9), (250, 170, 7), (95, 185, 6), (275, 50, 10)]:
        anh[(x - cx) ** 2 + (y - cy) ** 2 < rr ** 2] = 60.0
    sach = anh.copy()
    anh = anh + RNG.normal(0, NHIEU, anh.shape)
    return np.clip(anh, 0, 255), np.clip(sach, 0, 255), kc


SOBEL_X = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=float)  # Eq. 8.5
SOBEL_Y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=float)


def do_doc(anh):
    sx, sy = convolve(anh, SOBEL_X, mode="nearest"), convolve(anh, SOBEL_Y, mode="nearest")
    return np.hypot(sx, sy), sx, sy


def chi_giu_dinh(mag, sx, sy):
    """Chỉ giữ pixel lớn hơn hai hàng xóm theo hướng gradient (cực đại cục bộ, làm mảnh cạnh)."""
    goc = (np.round(np.arctan2(sy, sx) / (np.pi / 4)) % 4).astype(int)
    lech = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (1, -1)}
    giu = np.zeros_like(mag, dtype=bool)
    for g, (dy, dx) in lech.items():
        a = np.roll(mag, (dy, dx), axis=(0, 1))
        b = np.roll(mag, (-dy, -dx), axis=(0, 1))
        giu |= (goc == g) & (mag >= a) & (mag >= b)
    return giu


NGUONG = 160.0  # ngưỡng độ dốc |∇S| (cùng cho cả hai trường hợp)


def canh(anh, lam_min):
    a = gaussian_filter(anh, SIGMA) if lam_min else anh
    mag, sx, sy = do_doc(a)
    e = (mag > NGUONG) & chi_giu_dinh(mag, sx, sy)
    e[:3, :] = e[-3:, :] = False
    e[:, :3] = e[:, -3:] = False
    return e, mag, a


def hough(e, n_alpha=180):
    """§8.2.1: x cos α + y sin α = r, α ∈ [-90°, 90°), r ∈ [-r_max, r_max] bước 1 px."""
    ys, xs = np.nonzero(e)
    alphas = np.radians(np.arange(n_alpha) - 90)
    r_max = int(np.ceil(np.hypot(W, H)))
    acc = np.zeros((n_alpha, 2 * r_max + 1), dtype=int)
    r = np.round(np.outer(np.cos(alphas), xs) + np.outer(np.sin(alphas), ys)).astype(int) + r_max
    for i in range(n_alpha):
        np.add.at(acc[i], r[i], 1)
    return acc, alphas, r_max


def tim_dinh(acc, alphas, r_max, so=2):
    loc = (acc == maximum_filter(acc, size=(9, 9))) & (acc > 0)
    ids = np.argwhere(loc)
    ids = ids[np.argsort(-acc[loc])][:so]
    return [(float(np.degrees(alphas[i])), float(j - r_max), int(acc[i, j])) for i, j in ids]


ANH, SACH, KC = tao_anh()
MEP = (np.abs(np.abs(KC) - VACH_RONG / 2) < 2.5)  # pixel thuộc mép vạch thật (± 2,5 px)
VAT = np.zeros_like(MEP)
y_, x_ = np.mgrid[0:H, 0:W]
for cx, cy, rr in [(60, 60, 9), (250, 170, 7), (95, 185, 6), (275, 50, 10)]:
    VAT |= np.abs(np.hypot(x_ - cx, y_ - cy) - rr) < 2.5  # mép vết bẩn: cạnh thật nhưng không phải vạch

E_THO, MAG_THO, _ = canh(ANH, False)
E_MIN, MAG_MIN, ANH_MIN = canh(ANH, True)
ACC, ALPHAS, R_MAX = hough(E_MIN)
DINH = tim_dinh(ACC, ALPHAS, R_MAX)
# đường giữa vạch = trung bình hai mép
ALPHA_DO = np.mean([d[0] for d in DINH])
R_DO = np.mean([d[1] for d in DINH])


def thong_ke(e):
    n = int(e.sum())
    gia = int((e & ~MEP & ~VAT).sum())
    return n, gia


def lech_tai_day(alpha_deg, r):
    """Vị trí x của đường giữa ở mép dưới ảnh (y = H) -> robot lệch khỏi vạch bao nhiêu px."""
    a = np.radians(alpha_deg)
    return (r - H * np.sin(a)) / np.cos(a)


if __name__ == "__main__":
    print(f"Ảnh {W}×{H} = {W * H} con số · nhiễu σ = {NHIEU} · lọc Gauss σ = {SIGMA} · ngưỡng |∇S| > {NGUONG}")
    n0, g0 = thong_ke(E_THO)
    n1, g1 = thong_ke(E_MIN)
    print(f"Không làm mịn: {n0} pixel cạnh, {g0} cạnh giả ({g0 / max(n0, 1) * 100:.0f}%)")
    print(f"Làm mịn Gauss rồi Sobel: {n1} pixel cạnh, {g1} cạnh giả ({g1 / max(n1, 1) * 100:.0f}%)")
    print(f"Hough: lưới {ACC.shape[0]} góc × {ACC.shape[1]} giá trị r = {ACC.size} ô; mỗi điểm cạnh bỏ {ACC.shape[0]} phiếu")
    for a, r, v in DINH:
        print(f"  đỉnh: α = {a:.0f}°, r = {r:.0f} px, {v} phiếu")
    print(f"Vạch thật α = {np.degrees(ALPHA_THAT):.1f}°, r = {R_THAT:.1f} · đo được α = {ALPHA_DO:.1f}°, r = {R_DO:.1f} "
          f"-> lệch {abs(ALPHA_DO - np.degrees(ALPHA_THAT)):.1f}°")
    x_day = lech_tai_day(ALPHA_DO, R_DO)
    print(f"Mép dưới ảnh: vạch ở x = {x_day:.1f} px (thật {lech_tai_day(np.degrees(ALPHA_THAT), R_THAT):.1f}), "
          f"vạch nghiêng {ALPHA_DO:.1f}° so với phương thẳng đứng của ảnh")
    print(f"Đỉnh Hough thứ 3 (cực đại cục bộ): {tim_dinh(ACC, ALPHAS, R_MAX, 3)[2]}")
    print(f"Pixel cạnh trên vết bẩn (sau làm mịn): {int((E_MIN & VAT).sum())} · trên mép vạch: {int((E_MIN & MEP).sum())}")
