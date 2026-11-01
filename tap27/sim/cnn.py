"""Tập 2.7 - Deep learning nhìn thế giới thế nào (series Tự Học Robot Tự Hành)

Theo Chương 9, Principles of Robot Autonomy:
  - §9.1.1 lớp tích chập Y_ij = Σ_u Σ_v X_(i+u, j+v) W_uv + b (Eq. 9.1), nhiều bộ lọc -> nhiều bản đồ kích hoạt, ReLU sau tích chập
  - §9.1.2 max pooling 2×2 bước 2, lớp nối đầy đủ; dùng chung tham số, tương tác thưa, bất biến tịnh tiến
  - Bài tập 1 của chương: SimpleCNN = 2 lớp tích chập (ReLU + max pooling) + 2 lớp nối đầy đủ
  - §9.2.2 ViT: cắt ảnh H×W thành mảnh P×P -> N = HW/P² token
Mở rộng (ngoài sách): bộ dữ liệu ảnh vạch dẫn đường tự tạo, hàm mất mát cross-entropy và tối ưu Adam
(sách không nêu), so sánh với mạng nối đầy đủ, phép thử dịch ảnh.
Ảnh và nhãn là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả huấn luyện thật.
Chạy: python -X utf8 cnn.py
"""
import numpy as np
import torch
import torch.nn as nn
from scipy.ndimage import gaussian_filter

torch.manual_seed(27)
RNG = np.random.default_rng(27)
S = 32  # ảnh 32×32 xám
LOP = ["đi thẳng", "rẽ trái", "rẽ phải", "dừng"]
LECH_HOC = 4  # khi học: vạch lệch ngang tối đa ±4 px
LECH_THU = 9  # phép thử dịch ảnh: lệch ±(5..9) px, ngoài khoảng đã học


def ve_anh(lop, lech_min, lech_max):
    y, x = np.mgrid[0:S, 0:S].astype(float)
    anh = RNG.uniform(0.55, 0.85) + 0.06 * gaussian_filter(RNG.normal(0, 1, (S, S)), 2) * 4  # độ sáng sàn thay đổi
    dau = RNG.choice([-1, 1]) * RNG.uniform(lech_min, lech_max)  # lệch ngang của vạch
    rong = RNG.uniform(1.8, 3.0)
    cx = S / 2 + dau
    t = (S - y) / S  # 0 ở đáy ảnh, 1 ở đỉnh
    if lop == 0:
        tam = cx + RNG.uniform(-4, 4) * t
        vach = np.abs(x - tam) < rong
    elif lop in (1, 2):
        cong = (-1 if lop == 1 else 1) * RNG.uniform(5, 14)
        tam = cx + cong * t ** 2
        vach = (np.abs(x - tam) < rong) & (t < 0.95)
    else:
        tam = cx + RNG.uniform(-2, 2) * t
        y_ngang = RNG.uniform(9, 15)
        vach = ((np.abs(x - tam) < rong) & (y > y_ngang)) | (np.abs(y - y_ngang) < rong + 0.5)
    anh[vach] = RNG.uniform(0.1, 0.3)
    for _ in range(RNG.integers(0, 4)):  # vết bẩn
        bx, by, br = RNG.uniform(0, S), RNG.uniform(0, S), RNG.uniform(1, 2.5)
        anh[(x - bx) ** 2 + (y - by) ** 2 < br ** 2] = RNG.uniform(0.1, 0.35)
    anh += RNG.normal(0, 0.14, anh.shape)
    return np.clip(anh, 0, 1).astype(np.float32)


def bo_du_lieu(n, lech_min=0.0, lech_max=LECH_HOC):
    nhan = RNG.integers(0, 4, n)
    X = np.stack([ve_anh(int(c), lech_min, lech_max) for c in nhan])[:, None]
    return torch.tensor(X), torch.tensor(nhan)


class SimpleCNN(nn.Module):
    """Theo bài tập 1 của chương: 2 × (tích chập + ReLU + max pooling 2×2) rồi 2 lớp nối đầy đủ."""

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, 5, padding=2)
        self.conv2 = nn.Conv2d(8, 16, 5, padding=2)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 8 * 8, 32)
        self.fc2 = nn.Linear(32, 4)

    def features(self, x):
        a1 = torch.relu(self.conv1(x))
        p1 = self.pool(a1)
        a2 = torch.relu(self.conv2(p1))
        p2 = self.pool(a2)
        return a1, p1, a2, p2

    def forward(self, x):
        p2 = self.features(x)[-1]
        return self.fc2(torch.relu(self.fc1(p2.flatten(1))))


class MangDay(nn.Module):
    """Mạng nối đầy đủ (mở rộng, để so sánh): mỗi pixel nối với mọi nơ-ron lớp sau."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(S * S, 256), nn.ReLU(), nn.Linear(256, 4))

    def forward(self, x):
        return self.net(x)


def so_tham_so(m):
    return sum(p.numel() for p in m.parameters())


def do_chinh_xac(m, X, y):
    with torch.no_grad():
        return float((m(X).argmax(1) == y).float().mean())


def huan_luyen(m, Xh, yh, Xt, yt, so_vong=12):
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    lich_su = [do_chinh_xac(m, Xt, yt)]
    for _ in range(so_vong):
        perm = torch.randperm(len(Xh))
        for i in range(0, len(Xh), 64):
            idx = perm[i:i + 64]
            opt.zero_grad()
            nn.functional.cross_entropy(m(Xh[idx]), yh[idx]).backward()
            opt.step()
        lich_su.append(do_chinh_xac(m, Xt, yt))
    return lich_su


X_HOC, Y_HOC = bo_du_lieu(1500)
X_THU, Y_THU = bo_du_lieu(1000)
X_DICH, Y_DICH = bo_du_lieu(1000, LECH_HOC + 1, LECH_THU)

CNN = SimpleCNN()
DAY = MangDay()
LS_CNN = huan_luyen(CNN, X_HOC, Y_HOC, X_THU, Y_THU)
LS_DAY = huan_luyen(DAY, X_HOC, Y_HOC, X_THU, Y_THU)
DICH_CNN = do_chinh_xac(CNN, X_DICH, Y_DICH)
DICH_DAY = do_chinh_xac(DAY, X_DICH, Y_DICH)

with torch.no_grad():
    NHAM = torch.zeros(4, 4, dtype=torch.int)
    for t_, p_ in zip(Y_THU, CNN(X_THU).argmax(1)):
        NHAM[t_, p_] += 1

P_VIT = 8
TOKEN = (S * S) // (P_VIT * P_VIT)  # §9.2.2: N = HW / P²

if __name__ == "__main__":
    print(f"Dữ liệu: {len(X_HOC)} ảnh học, {len(X_THU)} ảnh thử, ảnh {S}×{S} = {S * S} pixel, {len(LOP)} lớp {LOP}")
    print(f"SimpleCNN: {so_tham_so(CNN)} tham số · conv1 có {so_tham_so(CNN.conv1)} tham số (8 bộ lọc 5×5 + 8 bias)")
    print(f"Mạng nối đầy đủ: {so_tham_so(DAY)} tham số")
    print(f"Độ chính xác trên ảnh thử theo vòng học (CNN): {[round(a * 100, 1) for a in LS_CNN]}")
    print(f"Độ chính xác trên ảnh thử theo vòng học (mạng đầy đủ): {[round(a * 100, 1) for a in LS_DAY]}")
    print(f"Ảnh bị dịch ngang ±{LECH_HOC + 1}..{LECH_THU} px (chưa từng học): CNN {DICH_CNN * 100:.1f}% · mạng đầy đủ {DICH_DAY * 100:.1f}%")
    print("Ma trận nhầm lẫn CNN (hàng = thật, cột = đoán):")
    print(NHAM.numpy())
    print(f"ViT với mảnh {P_VIT}×{P_VIT}: ảnh {S}×{S} -> {TOKEN} token")
