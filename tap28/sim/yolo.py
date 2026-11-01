"""Tập 2.8 - YOLO: robot nhận ra người và đồ vật (series Tự Học Robot Tự Hành)

Theo Chương 10, Principles of Robot Autonomy:
  - Định nghĩa 10.1: phát hiện = tập {(b_i, c_i, s_i)}: khung b = (x, y, w, h), lớp c, độ tin cậy s
  - §10.1.3 YOLO: lưới S×S, ô chứa tâm vật chịu trách nhiệm; mỗi ô B khung (x, y, w, h, confidence) + C xác suất lớp
    -> đầu ra S×S×(B·5 + C); hàm mất mát có λ_coord = 5, λ_noobj = 0,5, căn bậc hai của w, h;
    độ tin cậy lớp = P(lớp | vật) × P(vật) × IoU
  - IoU = phần giao / phần hợp; NMS: xếp theo điểm, bỏ khung chồng IoU cao lên khung điểm cao hơn; mAP
Mở rộng (ngoài sách): S = 8 (sách: 7), ảnh 128×128, ngưỡng NMS 0,5 (sách nêu ~0,7 cho RPN), cách tính AP
bằng diện tích dưới đường precision-recall, đo tốc độ trên máy này.
Cảnh, vật và nhãn là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả huấn luyện và đo thật.
Chạy: python -X utf8 yolo.py
"""
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(28)
RNG = np.random.default_rng(28)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
N = 128  # ảnh 128×128 RGB
S, B, C = 8, 2, 3  # lưới 8×8, 2 khung mỗi ô, 3 lớp
LOP = ["người", "hộp", "bóng"]
L_COORD, L_NOOBJ = 5.0, 0.5
NGUONG_TIN, NGUONG_NMS = 0.1, 0.5  # khung thô: điểm > 0,1


def ve_canh():
    """Cảnh robot nhìn: tường + sàn, đồ vật gây nhiễu (không có nhãn), 1-5 vật cần dò, có thể che nhau một phần.
    Trả về ảnh (3, N, N) và danh sách (lớp, cx, cy, w, h) theo tỉ lệ ảnh."""
    y, x = np.mgrid[0:N, 0:N] / N
    chan = RNG.uniform(0.4, 0.6)
    tuong = np.array(RNG.uniform(0.45, 0.85, 3))
    san = np.array(RNG.uniform(0.25, 0.55, 3))
    anh = np.where((y < chan)[..., None], tuong, san) + RNG.normal(0, 0.04, (N, N, 3))
    # đồ vật gây nhiễu: tranh trên tường, đồng hồ tròn trên tường, chậu cây, cọc tiêu
    for _ in range(RNG.integers(0, 4)):
        loai = RNG.integers(0, 4)
        cx, cy = RNG.uniform(0.05, 0.95), RNG.uniform(0.08, chan - 0.05) if loai < 2 else RNG.uniform(chan, 0.95)
        if loai == 0:
            w, h = RNG.uniform(0.08, 0.25, 2)
            anh[(np.abs(x - cx) < w / 2) & (np.abs(y - cy) < h / 2)] = RNG.uniform(0, 1, 3)
        elif loai == 1:
            r = RNG.uniform(0.04, 0.08)
            anh[(x - cx) ** 2 + (y - cy) ** 2 < r ** 2] = RNG.uniform(0.7, 1, 3)
        elif loai == 2:
            anh[((x - cx) / 0.06) ** 2 + ((y - cy) / 0.09) ** 2 < 1] = [0.15, RNG.uniform(0.4, 0.7), 0.15]
        else:
            hh = RNG.uniform(0.06, 0.12)
            anh[(y > cy - hh) & (y < cy) & (np.abs(x - cx) < (y - (cy - hh)) * 0.45)] = [0.95, 0.45, 0.1]
    # vật cần dò: sinh trước, vẽ từ xa tới gần (cy nhỏ vẽ trước) để vật gần che vật xa
    vat = []
    for _ in range(RNG.integers(1, 6)):
        c = int(RNG.integers(0, 3))
        if c == 0:  # người: đầu tròn + thân + chân, cao gầy
            h = RNG.uniform(0.28, 0.6); w = h * RNG.uniform(0.32, 0.42)
        elif c == 1:  # hộp: gần vuông
            w = RNG.uniform(0.1, 0.3); h = w * RNG.uniform(0.75, 1.15)
        else:  # bóng: tròn nhỏ
            w = RNG.uniform(0.07, 0.18); h = w
        cx, cy = RNG.uniform(w / 2, 1 - w / 2), RNG.uniform(max(h / 2, chan - h / 2), min(1 - h / 2, chan + 0.35))
        if any(abs(cx - v[1]) < (w + v[3]) / 2 * 0.45 and abs(cy - v[2]) < (h + v[4]) / 2 * 0.45 for v in vat):
            continue
        vat.append((c, cx, cy, w, h))
    for c, cx, cy, w, h in sorted(vat, key=lambda v: v[2] + v[4] / 2):
        x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
        mau = RNG.uniform(0, 1, 3)
        if c == 0:
            r = w * 0.32
            dau = (x - cx) ** 2 + (y - (y0 + r)) ** 2 < r ** 2
            than = (np.abs(x - cx) < w / 2) & (y > y0 + 2 * r) & (y < y0 + 0.62 * h)
            chan_ng = ((np.abs(x - (cx - w * 0.2)) < w * 0.14) | (np.abs(x - (cx + w * 0.2)) < w * 0.14)) & (y >= y0 + 0.62 * h) & (y < y1)
            anh[dau] = np.array([0.95, 0.8, 0.65]) * RNG.uniform(0.6, 1.0)
            anh[than | chan_ng] = mau
        elif c == 1:
            m = (x > x0) & (x < x1) & (y > y0) & (y < y1)
            vien = m & ~((x > x0 + 0.012) & (x < x1 - 0.012) & (y > y0 + 0.012) & (y < y1 - 0.012))
            anh[m] = np.array([0.6, 0.42, 0.22]) * RNG.uniform(0.7, 1.3)
            anh[vien] = [0.25, 0.16, 0.08]
            anh[m & (np.abs(x - cx) < 0.008)] = [0.85, 0.8, 0.6]  # băng dính giữa nắp
        else:
            r2 = ((x - cx) / (w / 2)) ** 2 + ((y - cy) / (h / 2)) ** 2
            anh[r2 < 1] = (mau * (1.1 - 0.5 * r2[..., None]))[r2 < 1]
    anh = np.clip(anh * RNG.uniform(0.7, 1.15) + RNG.normal(0, 0.05, anh.shape), 0, 1)  # độ sáng + nhiễu
    return anh.transpose(2, 0, 1).astype(np.float32), vat


def ma_hoa(vat):
    """Nhãn dạng lưới: mỗi ô [obj, x_ô, y_ô, w, h, one-hot lớp] (ô chứa tâm chịu trách nhiệm)."""
    t = np.zeros((S, S, 5 + C), np.float32)
    for c, cx, cy, w, h in vat:
        i, j = min(int(cy * S), S - 1), min(int(cx * S), S - 1)
        t[i, j, :5] = [1, cx * S - j, cy * S - i, w, h]
        t[i, j, 5 + c] = 1
    return t


def bo_du_lieu(n):
    anh, nhan, vats = [], [], []
    for _ in range(n):
        a, v = ve_canh()
        anh.append(a); nhan.append(ma_hoa(v)); vats.append(v)
    return torch.tensor(np.stack(anh)), torch.tensor(np.stack(nhan)), vats


class TinyYolo(nn.Module):
    def __init__(self):
        super().__init__()
        k = lambda i, o: [nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.LeakyReLU(0.1)]
        self.f = nn.Sequential(*k(3, 16), nn.MaxPool2d(2), *k(16, 32), nn.MaxPool2d(2), *k(32, 64), nn.MaxPool2d(2),
                               *k(64, 128), nn.MaxPool2d(2), *k(128, 128), nn.Conv2d(128, B * 5 + C, 1))

    def forward(self, x):
        o = self.f(x).permute(0, 2, 3, 1)  # (n, S, S, B·5 + C)
        box = torch.sigmoid(o[..., :B * 5]).reshape(*o.shape[:3], B, 5)
        return box, o[..., B * 5:]


def iou_tam(a, b):
    """IoU của khung dạng (cx, cy, w, h) theo tỉ lệ ảnh (tensor, so từng cặp)."""
    ax0, ay0, ax1, ay1 = a[..., 0] - a[..., 2] / 2, a[..., 1] - a[..., 3] / 2, a[..., 0] + a[..., 2] / 2, a[..., 1] + a[..., 3] / 2
    bx0, by0, bx1, by1 = b[..., 0] - b[..., 2] / 2, b[..., 1] - b[..., 3] / 2, b[..., 0] + b[..., 2] / 2, b[..., 1] + b[..., 3] / 2
    giao = (torch.min(ax1, bx1) - torch.max(ax0, bx0)).clamp(0) * (torch.min(ay1, by1) - torch.max(ay0, by0)).clamp(0)
    return giao / (a[..., 2] * a[..., 3] + b[..., 2] * b[..., 3] - giao + 1e-9)


LUOI = torch.stack(torch.meshgrid(torch.arange(S), torch.arange(S), indexing="ij"), -1).float()  # (S, S, 2): i, j


def ra_anh(box):
    """(x_ô, y_ô, w, h) -> (cx, cy, w, h) theo tỉ lệ ảnh."""
    g = LUOI.to(box.device)
    cx = (box[..., 0] + g[..., 1, None]) / S
    cy = (box[..., 1] + g[..., 0, None]) / S
    return torch.stack([cx, cy, box[..., 2], box[..., 3]], -1)


def mat_mat(box, lop, t):
    """Hàm mất mát YOLO (§10.1.3): khung chịu trách nhiệm = khung có IoU lớn nhất với vật thật."""
    obj = t[..., 0]
    that = ra_anh(t[..., None, 1:5].expand(*t.shape[:3], B, 4))
    du = ra_anh(box[..., :4])
    iou = iou_tam(du, that).detach()
    chon = nn.functional.one_hot(iou.argmax(-1), B).float() * obj[..., None]  # 1_ij^obj
    l_xy = (chon * ((box[..., 0] - t[..., None, 1]) ** 2 + (box[..., 1] - t[..., None, 2]) ** 2)).sum()
    l_wh = (chon * ((box[..., 2].sqrt() - t[..., None, 3].sqrt()) ** 2 + (box[..., 3].sqrt() - t[..., None, 4].sqrt()) ** 2)).sum()
    l_obj = (chon * (box[..., 4] - iou) ** 2).sum()
    l_noobj = ((1 - chon) * box[..., 4] ** 2).sum()
    l_cls = (obj[..., None] * (torch.softmax(lop, -1) - t[..., 5:]) ** 2).sum()
    return (L_COORD * (l_xy + l_wh) + l_obj + L_NOOBJ * l_noobj + l_cls) / len(t)


def giai_ma(box, lop, nguong=NGUONG_TIN):
    """Một ảnh -> danh sách (lớp, điểm, cx, cy, w, h); điểm = P(lớp|vật) × confidence."""
    p = torch.softmax(lop, -1)
    k = ra_anh(box[..., :4])
    diem = box[..., 4][..., None] * p[:, :, None, :]  # (S, S, B, C)
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


def ap_lop(du_doan, that, c, nguong_iou=0.5):
    """AP của lớp c: diện tích dưới đường precision-recall (mở rộng, kiểu VOC nội suy liên tục)."""
    ds = sorted([(s, k, box) for k, dd in enumerate(du_doan) for (cc, s, *box) in dd if cc == c], key=lambda z: -z[0])
    n_that = sum(1 for v in that for x in v if x[0] == c)
    da_khop = [set() for _ in that]
    tp = []
    for s, k, box in ds:
        best, bi = 0, -1
        for vi, v in enumerate(that[k]):
            if v[0] == c and vi not in da_khop[k]:
                u = float(iou_tam(torch.tensor(box), torch.tensor(v[1:])))
                if u > best:
                    best, bi = u, vi
        if best >= nguong_iou:
            da_khop[k].add(bi); tp.append(1)
        else:
            tp.append(0)
    tp = np.array(tp)
    tpc, fpc = np.cumsum(tp), np.cumsum(1 - tp)
    rec = tpc / max(n_that, 1)
    pre = tpc / np.maximum(tpc + fpc, 1)
    pre_mono = np.maximum.accumulate(pre[::-1])[::-1] if len(pre) else pre
    return float(np.sum(np.diff(np.concatenate([[0], rec])) * pre_mono)), rec, pre


CACHE = Path(__file__).with_name("ket_qua.pt")
SO_VONG = 30
MANG = TinyYolo().to(DEV)
t0 = time.perf_counter()
if CACHE.exists():  # đã huấn luyện: nạp lại để xuất dữ liệu không phải học lại
    ck = torch.load(CACHE, weights_only=False)
    MANG.load_state_dict(ck["mang"]); X_THU, V_THU, LS_LOSS = ck["x_thu"], ck["v_thu"], ck["loss"]
    N_HOC = ck["n_hoc"]
elif CACHE.with_name("trong_so.pt").exists():  # bản trên GitHub: chỉ có trọng số đã học (1 MB thay vì 95 MB)
    ck = torch.load(CACHE.with_name("trong_so.pt"), weights_only=False)
    MANG.load_state_dict(ck["mang"]); LS_LOSS, N_HOC = ck["loss"], ck["n_hoc"]
    bo_du_lieu(5000)                  # sinh lại đúng thứ tự RNG như lúc huấn luyện -> bộ ảnh thử y hệt bản gốc
    X_THU, _, V_THU = bo_du_lieu(500)
else:
    X_HOC, T_HOC, _ = bo_du_lieu(5000)
    X_THU, _, V_THU = bo_du_lieu(500)
    N_HOC = len(X_HOC)
    print(f"[tạo dữ liệu {time.perf_counter() - t0:.0f} s]", flush=True)
    opt = torch.optim.Adam(MANG.parameters(), lr=2e-3)
    LS_LOSS = []
    for vong in range(SO_VONG):
        MANG.train()
        perm = torch.randperm(len(X_HOC))
        tong = 0.0
        for i in range(0, len(X_HOC), 64):
            idx = perm[i:i + 64]
            box, lop = MANG(X_HOC[idx].to(DEV))
            loss = mat_mat(box, lop, T_HOC[idx].to(DEV))
            opt.zero_grad(); loss.backward(); opt.step()
            tong += float(loss) * len(idx)
        LS_LOSS.append(tong / len(X_HOC))
        if vong == 20:
            for g in opt.param_groups:
                g["lr"] = 5e-4
    print(f"[huấn luyện xong {time.perf_counter() - t0:.0f} s]", flush=True)
    torch.save({"mang": MANG.state_dict(), "x_thu": X_THU, "v_thu": V_THU, "loss": LS_LOSS, "n_hoc": N_HOC}, CACHE)

MANG.eval()
with torch.no_grad():
    BOX, LOPRA = MANG(X_THU.to(DEV))
    BOX, LOPRA = BOX.cpu(), LOPRA.cpu()
THO = [giai_ma(BOX[k], LOPRA[k]) for k in range(len(X_THU))]
SACH = [nms(d) for d in THO]
AP = [ap_lop(SACH, V_THU, c)[0] for c in range(C)]
MAP = float(np.mean(AP))
AP_THO = float(np.mean([ap_lop(THO, V_THU, c)[0] for c in range(C)]))

# tốc độ: thời gian chạy 1 ảnh (không tính NMS), trên GPU và CPU của máy này
def do_fps(dev, lap=200):
    m = MANG.to(dev)
    x = X_THU[:1].to(dev)
    with torch.no_grad():
        for _ in range(20):
            m(x)
        if dev == "cuda":
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        for _ in range(lap):
            m(x)
        if dev == "cuda":
            torch.cuda.synchronize()
    return lap / (time.perf_counter() - t0)


print(f"[đánh giá xong {time.perf_counter() - t0:.0f} s]", flush=True)
FPS_CPU = do_fps("cpu")
FPS_GPU = do_fps("cuda") if DEV == "cuda" else None
MANG.to("cpu")
SO_THAM_SO = sum(p.numel() for p in MANG.parameters())

if __name__ == "__main__":
    print(f"Thiết bị: {DEV} · {N_HOC} ảnh học, {len(X_THU)} ảnh thử · ảnh {N}×{N} · {SO_THAM_SO} tham số")
    print(f"Đầu ra S×S×(B·5+C) = {S}×{S}×{B * 5 + C} = {S * S * (B * 5 + C)} con số mỗi ảnh")
    print(f"Mất mát theo vòng: {[round(v, 2) for v in LS_LOSS[::5]]} ... {LS_LOSS[-1]:.3f}")
    so_vat = sum(len(v) for v in V_THU)
    print(f"Ảnh thử có {so_vat} vật · khung trước NMS: {sum(map(len, THO))} · sau NMS: {sum(map(len, SACH))}")
    print(f"AP@0,5 từng lớp {dict(zip(LOP, [round(a * 100, 1) for a in AP]))} · mAP = {MAP * 100:.1f}% (không NMS: {AP_THO * 100:.1f}%)")
    print(f"Tốc độ 1 ảnh: CPU {FPS_CPU:.0f} khung/giây" + (f" · GPU {FPS_GPU:.0f} khung/giây" if FPS_GPU else ""))
    k = max(range(len(THO)), key=lambda k: len(THO[k]) - len(SACH[k]))
    print(f"Ảnh minh hoạ #{k}: {len(V_THU[k])} vật, {len(THO[k])} khung thô -> {len(SACH[k])} khung sau NMS")
