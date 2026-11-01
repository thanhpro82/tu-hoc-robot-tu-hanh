"""Tập 2.9 - Tổng kết Mùa 2: robot đi theo bạn (series Tự Học Robot Tự Hành)

Ghép các tập đã làm thành một vòng lặp chạy thật, mỗi bước 0,1 s:
  1. Camera lỗ kim (tập 2.2, Eq. 6.1): vẽ ảnh 128×128 robot nhìn thấy, u = f·X/Z + u0, chiều cao ảnh h = f·H/Z
  2. Bộ dò kiểu YOLO đã huấn luyện ở tập 2.8 (Ch. 10) tìm "người" và "bóng" trong ảnh (dùng lại trọng số, không học lại)
  3. Đo từ khung: khoảng cách Z ≈ f·H / h (người cao H = 1,7 m), hướng = atan((u − u0)/f)
  4. Điều khiển (Mùa 1): robot kiểu unicycle (tập 1.1), sai số e = r − y với r = 2 m (tập 1.3),
     v = Kp·e + Ki·∫e (PI), ω = Kθ·hướng; thấy bóng gần phía trước thì dừng (vật cản)
Mở rộng / giả định: người đi theo lộ trình định sẵn, quả bóng lăn ngang, các hệ số điều khiển, camera f = 60 px,
chiều cao camera 0,5 m; cách suy khoảng cách từ chiều cao khung khi biết chiều cao thật là áp dụng Eq. 6.1.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 di_theo.py
"""
import math
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tap28" / "sim"))
import yolo  # noqa: E402  (nạp trọng số đã học ở tập 2.8 từ ket_qua.pt)

RNG = np.random.default_rng(29)
N = yolo.N  # 128
F = 60.0  # tiêu cự (px)
H_CAM = 0.5  # camera cao 0,5 m
H_NGUOI = 1.7
D_BONG = 0.25
DT, T_MAX = 0.1, 32.0
R_KC = 2.0  # khoảng cách muốn giữ (m)
KP, KI, KTH = 0.8, 0.15, 1.6
V_MAX, W_MAX = 1.2, 1.5
TUONG = np.array([0.66, 0.7, 0.62])
SAN = np.array([0.42, 0.36, 0.32])
MAU_AO = np.array([0.15, 0.55, 0.85])
MAU_BONG = np.array([0.9, 0.2, 0.3])


def nguoi_tai(t):
    """Lộ trình người (m): đi thẳng, rẽ trái, đi tiếp, đứng lại."""
    v = 0.5
    if t < 3:
        return np.array([2.2, 0.0])
    s = min(t - 3, 24) * v  # quãng đường đã đi
    if s < 4:
        return np.array([2.2 + s, 0.0])
    a = min((s - 4) / 4.0, math.pi / 2)  # cung tròn bán kính 4 m, rẽ trái
    p = np.array([6.2 + 4 * math.sin(a), 4 - 4 * math.cos(a)])
    du = s - 4 - 4 * (math.pi / 2)
    if du > 0:
        p = np.array([10.2, 4.0 + du])
    return p


def chieu(dx, dy, th):
    """Đổi điểm thế giới (lệch dx, dy so với robot) sang hệ camera: X sang phải, Z ra trước."""
    Z = dx * math.cos(th) + dy * math.sin(th)
    X = dx * math.sin(th) - dy * math.cos(th)
    return X, Z


def ve_anh(robot, nguoi, bong):
    """Ảnh 128×128 theo đúng kiểu vẽ của tập 2.8; vật xa vẽ trước, vật gần vẽ sau."""
    y, x = np.mgrid[0:N, 0:N] / N
    anh = np.where((y < 0.5)[..., None], TUONG, SAN).copy()
    vat, that = [], []
    for loai, p in (("nguoi", nguoi), ("bong", bong)):
        if p is None:
            continue
        X, Z = chieu(p[0] - robot[0], p[1] - robot[1], robot[2])
        if Z < 0.4:
            continue
        fn = F / N
        if loai == "nguoi":
            h = fn * H_NGUOI / Z; w = h * 0.37
            cy = 0.5 + fn * H_CAM / Z - h / 2
        else:
            h = w = fn * D_BONG / Z
            cy = 0.5 + fn * (H_CAM - D_BONG / 2) / Z
        cx = 0.5 + fn * X / Z
        if cx + w / 2 < 0 or cx - w / 2 > 1:
            continue
        vat.append((Z, loai, cx, cy, w, h))
    for Z, loai, cx, cy, w, h in sorted(vat, reverse=True):
        x0, y0, y1 = cx - w / 2, cy - h / 2, cy + h / 2
        if loai == "nguoi":
            r = w * 0.32
            dau = (x - cx) ** 2 + (y - (y0 + r)) ** 2 < r ** 2
            than = (np.abs(x - cx) < w / 2) & (y > y0 + 2 * r) & (y < y0 + 0.62 * h)
            chan = ((np.abs(x - (cx - w * 0.2)) < w * 0.14) | (np.abs(x - (cx + w * 0.2)) < w * 0.14)) & (y >= y0 + 0.62 * h) & (y < y1)
            anh[dau] = [0.9, 0.75, 0.6]
            anh[than | chan] = MAU_AO
        else:
            r2 = ((x - cx) / (w / 2)) ** 2 + ((y - cy) / (h / 2)) ** 2
            anh[r2 < 1] = (MAU_BONG * (1.1 - 0.5 * r2[..., None]))[r2 < 1]
        that.append({"loai": loai, "Z": Z, "b": [cx, cy, w, h]})
    anh = np.clip(anh + RNG.normal(0, 0.05, anh.shape), 0, 1)
    return anh.transpose(2, 0, 1).astype(np.float32), that


def do_tim(anh):
    with torch.no_grad():
        box, lop = yolo.MANG(torch.tensor(anh)[None])
    return yolo.nms(yolo.giai_ma(box[0], lop[0], 0.3))


def uoc_luong(d):
    """Khoảng cách và hướng từ khung (Eq. 6.1 đảo ngược): Z = f·H/h, hướng = atan((u − u0)/f)."""
    c, s, cx, cy, w, h = d
    huong = math.atan((cx - 0.5) * N / F)
    if c == 0:
        return H_NGUOI * F / (h * N), huong
    return D_BONG * F / (w * N), huong


def chay():
    robot = np.array([0.0, 0.0, 0.0])  # x, y, θ
    tich_phan = 0.0
    huong_cuoi = 0.0
    bong0 = None
    log = []
    for k in range(int(T_MAX / DT)):
        t = k * DT
        nguoi = nguoi_tai(t)
        # quả bóng lăn ngang trước robot từ giây 15
        if t >= 15 and bong0 is None:
            th = robot[2]
            bong0 = robot[:2] + 1.9 * np.array([math.cos(th), math.sin(th)]) + 0.9 * np.array([-math.sin(th), math.cos(th)])
            v_bong = 0.35 * np.array([math.sin(th), -math.cos(th)])
        bong = bong0 + v_bong * (t - 15) if bong0 is not None and t < 21.5 else None
        anh, that = ve_anh(robot, nguoi, bong)
        dets = do_tim(anh)
        ng = [d for d in dets if d[0] == 0]
        bo = [d for d in dets if d[0] == 2]
        z_hat = huong = None
        trang_thai = "tìm"
        v = w = 0.0
        if bo:
            zb, hb = uoc_luong(max(bo, key=lambda d: d[1]))
            if zb < 1.6 and abs(hb) < math.radians(30):
                trang_thai = "dừng"
        if ng:
            z_hat, huong = uoc_luong(max(ng, key=lambda d: d[1]))
            huong_cuoi = huong
            if trang_thai != "dừng":
                e = z_hat - R_KC  # e = r − y viết theo khoảng cách: dương là đang xa hơn mong muốn
                tich_phan = float(np.clip(tich_phan + e * DT, -1.5, 1.5))
                v = float(np.clip(KP * e + KI * tich_phan, 0, V_MAX))
                w = float(np.clip(KTH * -huong, -W_MAX, W_MAX))  # người lệch phải (huong > 0) -> quay phải (ω < 0)
                trang_thai = "theo"
        elif trang_thai != "dừng":
            w = 0.6 * (-1 if huong_cuoi > 0 else 1)  # mất dấu: quay về phía thấy lần cuối
        kc_that = float(np.hypot(*(nguoi - robot[:2])))
        log.append({"t": round(t, 1), "robot": robot.tolist(), "nguoi": nguoi.tolist(), "bong": None if bong is None else bong.tolist(),
                    "kc_that": kc_that, "z_hat": z_hat, "trang_thai": trang_thai, "v": v, "w": w,
                    "dets": dets, "that": that, "anh": anh})
        robot = robot + DT * np.array([v * math.cos(robot[2]), v * math.sin(robot[2]), w])
    return log


LOG = chay()

if __name__ == "__main__":
    n = len(LOG)
    thay = [r for r in LOG if r["z_hat"] is not None]
    loi = [abs(r["z_hat"] - r["kc_that"]) for r in thay]
    print(f"{n} bước × {DT} s = {n * DT:.0f} s · thấy người ở {len(thay)}/{n} khung ({len(thay) / n * 100:.0f}%)")
    print(f"Sai số ước lượng khoảng cách: trung bình {np.mean(loi) * 100:.1f} cm, lớn nhất {np.max(loi) * 100:.1f} cm")
    di = [r for r in LOG if 8 <= r["t"] <= 15 or 23 <= r["t"] <= 27]
    print(f"Khoảng cách thật khi người đang đi: trung bình {np.mean([r['kc_that'] for r in di]):.2f} m (muốn {R_KC} m)")
    cuoi = [r for r in LOG if r["t"] >= 30]
    print(f"Khi người đứng lại (t ≥ 30 s): khoảng cách {np.mean([r['kc_that'] for r in cuoi]):.2f} m")
    dung = [r for r in LOG if r["trang_thai"] == "dừng"]
    if dung:
        print(f"Dừng vì bóng: {len(dung) * DT:.1f} s (từ {dung[0]['t']} s đến {dung[-1]['t']} s)")
        kc_bong = min(np.hypot(*(np.array(r['bong']) - np.array(r['robot'][:2]))) for r in LOG if r['bong'] is not None)
        print(f"Khoảng cách gần nhất tới bóng: {kc_bong:.2f} m")
    duong = sum(np.hypot(*(np.array(LOG[i + 1]['robot'][:2]) - np.array(LOG[i]['robot'][:2]))) for i in range(n - 1))
    print(f"Robot đã đi {duong:.1f} m · trạng thái: " + str({s: sum(r['trang_thai'] == s for r in LOG) for s in ('theo', 'dừng', 'tìm')}))
