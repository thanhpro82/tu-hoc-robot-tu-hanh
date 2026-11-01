"""Nạp nhanh mạng YOLO đã học ở tập 2.8 (tap28/sim/ket_qua.pt hoặc trong_so.pt) để dùng lại, KHÔNG học lại và không chạy phần đánh giá.
Các hàm dưới đây chép nguyên từ tap28/sim/yolo.py (TinyYolo, iou_tam, ra_anh, giai_ma, nms)."""
from pathlib import Path

import torch
import torch.nn as nn

N = 128
S, B, C = 8, 2, 3
LOP = ["người", "hộp", "bóng"]
NGUONG_TIN, NGUONG_NMS = 0.1, 0.5


class TinyYolo(nn.Module):
    def __init__(self):
        super().__init__()
        k = lambda i, o: [nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.LeakyReLU(0.1)]
        self.f = nn.Sequential(*k(3, 16), nn.MaxPool2d(2), *k(16, 32), nn.MaxPool2d(2), *k(32, 64), nn.MaxPool2d(2),
                               *k(64, 128), nn.MaxPool2d(2), *k(128, 128), nn.Conv2d(128, B * 5 + C, 1))

    def forward(self, x):
        o = self.f(x).permute(0, 2, 3, 1)
        box = torch.sigmoid(o[..., :B * 5]).reshape(*o.shape[:3], B, 5)
        return box, o[..., B * 5:]


def iou_tam(a, b):
    ax0, ay0, ax1, ay1 = a[..., 0] - a[..., 2] / 2, a[..., 1] - a[..., 3] / 2, a[..., 0] + a[..., 2] / 2, a[..., 1] + a[..., 3] / 2
    bx0, by0, bx1, by1 = b[..., 0] - b[..., 2] / 2, b[..., 1] - b[..., 3] / 2, b[..., 0] + b[..., 2] / 2, b[..., 1] + b[..., 3] / 2
    giao = (torch.min(ax1, bx1) - torch.max(ax0, bx0)).clamp(0) * (torch.min(ay1, by1) - torch.max(ay0, by0)).clamp(0)
    return giao / (a[..., 2] * a[..., 3] + b[..., 2] * b[..., 3] - giao + 1e-9)


LUOI = torch.stack(torch.meshgrid(torch.arange(S), torch.arange(S), indexing="ij"), -1).float()


def ra_anh(box):
    g = LUOI.to(box.device)
    cx = (box[..., 0] + g[..., 1, None]) / S
    cy = (box[..., 1] + g[..., 0, None]) / S
    return torch.stack([cx, cy, box[..., 2], box[..., 3]], -1)


def giai_ma(box, lop, nguong=NGUONG_TIN):
    p = torch.softmax(lop, -1)
    k = ra_anh(box[..., :4])
    diem = box[..., 4][..., None] * p[:, :, None, :]
    ra = []
    for i in range(S):
        for j in range(S):
            for b in range(B):
                c = int(diem[i, j, b].argmax())
                s = float(diem[i, j, b, c])
                if s > nguong:
                    ra.append((c, s, *[float(v) for v in k[i, j, b]]))
    return ra


def nms(ds, nguong=NGUONG_NMS):
    ds = sorted(ds, key=lambda d: -d[1])
    giu = []
    for d in ds:
        if all(d[0] != g[0] or float(iou_tam(torch.tensor(d[2:]), torch.tensor(g[2:]))) < nguong for g in giu):
            giu.append(d)
    return giu


MANG = TinyYolo()
_T28 = Path(__file__).resolve().parents[2] / "tap28/sim"
_F = _T28 / "ket_qua.pt" if (_T28 / "ket_qua.pt").exists() else _T28 / "trong_so.pt"   # bản GitHub chỉ có trong_so.pt
MANG.load_state_dict(torch.load(_F, weights_only=False, map_location="cpu")["mang"])
MANG.eval()
