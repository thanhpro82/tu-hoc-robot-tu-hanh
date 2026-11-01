"""Tập 2.4 - Hai mắt để đoán khoảng cách (series Tự Học Robot Tự Hành)

Theo Chương 7, Principles of Robot Autonomy:
  - §7.1.1: sau khi chỉnh ảnh (rectification), hai camera song song, đường epipolar là các hàng ngang
    -> tìm điểm tương ứng chỉ cần dò dọc 1 hàng
  - §7.2: disparity d = p_u - p'_u, độ sâu z = b·f / d (Eq. 7.7); so khớp bằng tương quan trên cửa sổ nhỏ;
    khó ở vùng trơn (không có vân), vùng bị che, vân lặp lại; độ phân giải độ sâu giảm theo bình phương khoảng cách.
Mở rộng (ngoài sách): hàm chi phí SSD, nội suy dưới pixel bằng parabol, kiểm tra trái-phải để loại vùng bị che,
ngưỡng độ vân. Cảnh 3D, camera (480×360, f = 375 px), baseline 12 cm và nhiễu ảnh là GIẢ ĐỊNH;
hai ảnh được kết xuất bằng dò tia từ cảnh giả định này, mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 stereo.py
"""
import numpy as np
from scipy.ndimage import uniform_filter, zoom

RNG = np.random.default_rng(24)
W, H = 480, 360
F = 375.0  # tiêu cự (px), cùng góc nhìn với camera 640×480, α = 500 px của tập 2.2
CX, CY = W / 2, H / 2
B = 0.12  # baseline (m): khoảng cách hai camera
NHIEU = 2.0  # nhiễu ảnh (mức xám 0-255)
D_MAX = 64
CUA_SO = 11  # cửa sổ so khớp 11×11 px

# Cảnh: tường z = 4 m (có tấm áp phích trơn), quả bóng ở 2,2 m, hộp ở 1,2 m (trục Y hướng xuống như ảnh)
TUONG_Z = 4.0
AP_PHICH = (0.55, 1.35, -1.05, -0.3)  # X0, X1, Y0, Y1 trên tường
HOP = {"z": 1.2, "X": (-0.6, -0.18), "Y": (-0.02, 0.4)}
BONG = {"c": np.array([0.3, 0.12, 2.2]), "r": 0.3}


def van(seed, o):
    """Vân ngẫu nhiên mịn, ô o mét, dùng chung cho cả hai camera (gắn vào vật, không gắn vào ảnh)."""
    g = np.random.default_rng(seed).uniform(0, 1, (400, 400))
    def mau(X, Y):
        x, y = X / o + 200, Y / o + 200
        x0, y0 = np.floor(x).astype(int) % 399, np.floor(y).astype(int) % 399
        fx, fy = x - np.floor(x), y - np.floor(y)
        return ((1 - fx) * (1 - fy) * g[y0, x0] + fx * (1 - fy) * g[y0, x0 + 1]
                + (1 - fx) * fy * g[y0 + 1, x0] + fx * fy * g[y0 + 1, x0 + 1])
    return mau


VAN_TUONG_TO, VAN_TUONG, VAN_HOP, VAN_BONG = van(1, 0.15), van(4, 0.04), van(2, 0.015), van(3, 0.02)


def ket_xuat(tam_x):
    """Dò tia cho camera đặt tại (tam_x, 0, 0), nhìn theo +z. Trả về ảnh xám và độ sâu thật."""
    u, v = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
    dx, dy = (u - CX) / F, (v - CY) / F
    z = np.full((H, W), TUONG_Z)
    X, Y = tam_x + dx * TUONG_Z, dy * TUONG_Z
    anh = 40 + 70 * VAN_TUONG_TO(X, Y) + 95 * VAN_TUONG(X, Y)
    trong = (X > AP_PHICH[0]) & (X < AP_PHICH[1]) & (Y > AP_PHICH[2]) & (Y < AP_PHICH[3])
    anh[trong] = 215.0
    loai = np.where(trong, 1, 0)  # 0 tường, 1 áp phích, 2 bóng, 3 hộp
    # quả cầu
    d = np.stack([dx, dy, np.ones_like(dx)], -1)
    oc = np.array([tam_x, 0, 0]) - BONG["c"]
    a, bq = (d ** 2).sum(-1), 2 * (d * oc).sum(-1)
    delta = bq ** 2 - 4 * a * ((oc ** 2).sum() - BONG["r"] ** 2)
    t = (-bq - np.sqrt(np.maximum(delta, 0))) / (2 * a)
    trung = (delta > 0) & (t < z)
    P = np.array([tam_x, 0, 0]) + d * t[..., None]
    n = (P - BONG["c"]) / BONG["r"]
    sang = np.clip(n @ np.array([-0.5, -0.6, -0.62]), 0.15, 1)
    anh[trung] = (40 + 190 * VAN_BONG(P[..., 0], P[..., 1]) * sang)[trung]
    z[trung], loai[trung] = t[trung], 2
    # hộp (mặt trước song song ảnh)
    Xh, Yh = tam_x + dx * HOP["z"], dy * HOP["z"]
    trung = (Xh > HOP["X"][0]) & (Xh < HOP["X"][1]) & (Yh > HOP["Y"][0]) & (Yh < HOP["Y"][1]) & (HOP["z"] < z)
    anh[trung] = (130 + 120 * VAN_HOP(Xh, Yh))[trung]
    z[trung], loai[trung] = HOP["z"], 3
    anh = anh + RNG.normal(0, NHIEU, anh.shape)
    return np.clip(anh, 0, 255), z, loai


def chi_phi(L, R, huong=1):
    """SSD trên cửa sổ CUA_SO cho mọi d (huong=1: ảnh trái làm gốc, điểm khớp ở u - d trong ảnh phải)."""
    C = np.full((D_MAX, H, W), np.inf)
    for d in range(D_MAX):
        if huong == 1:
            diff = np.full((H, W), np.inf)
            diff[:, d:] = (L[:, d:] - R[:, :W - d]) ** 2
        else:
            diff = np.full((H, W), np.inf)
            diff[:, :W - d] = (R[:, :W - d] - L[:, d:]) ** 2
        ok = np.isfinite(diff)
        C[d] = np.where(uniform_filter(ok.astype(float), CUA_SO) > 0.999, uniform_filter(np.where(ok, diff, 0), CUA_SO), np.inf)
    return C


@np.errstate(invalid="ignore", divide="ignore")
def disparity(L, R):
    C = chi_phi(L, R)
    d0 = np.argmin(C, axis=0)
    # nội suy dưới pixel bằng parabol qua 3 điểm (mở rộng)
    i = np.clip(d0, 1, D_MAX - 2)
    hh, ww = np.indices(d0.shape)
    c0, c1, c2 = C[i - 1, hh, ww], C[i, hh, ww], C[i + 1, hh, ww]
    mau = c0 - 2 * c1 + c2
    dd = np.where(np.isfinite(mau) & (mau > 0), 0.5 * (c0 - c2) / np.where(mau > 0, mau, 1), 0)
    d = i + np.clip(dd, -0.5, 0.5)
    # vùng trơn: độ lệch chuẩn trong cửa sổ nhỏ hơn ngưỡng -> không có gì để so
    tb = uniform_filter(L, CUA_SO)
    std = np.sqrt(np.maximum(uniform_filter(L ** 2, CUA_SO) - tb ** 2, 0))
    tron = std < 4 * NHIEU
    # kiểm tra trái-phải: vùng chỉ một camera thấy (bị che) cho kết quả không khớp
    dR = np.argmin(chi_phi(L, R, -1), axis=0)
    u = np.clip((np.arange(W)[None, :] - d0).astype(int), 0, W - 1)
    che = np.abs(dR[hh, u] - d0) > 1
    vien = ~np.isfinite(c1)
    return d, tron, che & ~tron, vien, C


L, Z_THAT, LOAI = ket_xuat(0.0)
R, _, _ = ket_xuat(B)
D, TRON, CHE, VIEN, CHI_PHI = disparity(L, R)
HOP_DUNG = ~(TRON | CHE | VIEN)
Z_DO = np.where(HOP_DUNG & (D > 0.5), B * F / np.maximum(D, 1e-6), np.nan)  # Eq. 7.7

TEN = {0: "tường", 1: "áp phích", 2: "bóng", 3: "hộp"}


def thong_ke(loai):
    m = (LOAI == loai) & ~VIEN
    ok = m & HOP_DUNG
    z_that = float(np.median(Z_THAT[m]))
    return {"ten": TEN[loai], "z_that": z_that, "d_that": B * F / z_that, "d_do": float(np.median(D[ok])) if ok.any() else None,
            "z_do": float(np.nanmedian(Z_DO[ok])) if ok.any() else None, "loai_bo": float(1 - ok.sum() / m.sum())}


THONG_KE = [thong_ke(k) for k in (3, 2, 0, 1)]

# Một điểm giữa mặt hộp: đường chi phí theo d
DIEM = (int(CY + 0.2 * F / HOP["z"]), int(CX + (-0.39) * F / HOP["z"]))
DUONG_CP = CHI_PHI[:, DIEM[0], DIEM[1]]


def sai_1px(z):
    """Lệch 1 pixel disparity ở độ sâu z thì độ sâu tính ra (Eq. 7.7) sai bao nhiêu."""
    d = B * F / z
    return B * F / (d - 1) - z


if __name__ == "__main__":
    print(f"Camera {W}×{H}, f = {F:.0f} px, baseline b = {B * 100:.0f} cm -> b·f = {B * F:.1f} px·m")
    for t in THONG_KE:
        print(f"  {t['ten']:9s} z thật {t['z_that']:.2f} m · d thật {t['d_that']:.2f} px · d đo {t['d_do'] or 0:.2f} px · "
              f"z đo {t['z_do'] or 0:.3f} m · bị loại {t['loai_bo'] * 100:.0f}%")
    print(f"Điểm giữa hộp {DIEM}: d tốt nhất = {int(np.argmin(DUONG_CP))} px (thật {B * F / HOP['z']:.1f})")
    print(f"Pixel bị loại: vùng trơn {TRON.mean() * 100:.1f}% · bị che {CHE.mean() * 100:.1f}% · viền {VIEN.mean() * 100:.1f}%")
    for z in (1.0, 2.0, 4.0):
        print(f"  ở {z:.0f} m: d = {B * F / z:.2f} px, lệch 1 px -> sai {sai_1px(z) * 100:.1f} cm")
    m = HOP_DUNG & ~VIEN & np.isfinite(Z_DO)
    print(f"Sai số độ sâu trung vị trên pixel hợp lệ: {np.median(np.abs(Z_DO[m] - Z_THAT[m])) * 100:.1f} cm")
