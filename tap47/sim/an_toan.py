"""Tập 4.7 - Lớp an toàn cổ điển bọc quanh chính sách học máy (phần Prospects: "Physical AI Safety").

Sách nêu: mô hình học từ dữ liệu có thể đoán sai khi ra ngoài phân phối huấn luyện; hướng đi là kết hợp học máy
với đảm bảo an toàn kiểu lý thuyết điều khiển (ví dụ control barrier function). Ở đây (mở rộng, giả định) là một
luật an toàn đơn giản chỉ dùng 9 tia LiDAR — KHÔNG phải CBF đầy đủ:
    khoảng hở bên trái  c_L = min_{tia trái}  d_i · sin(a_i),   bên phải c_R tương tự
    nếu c_L < m:  ω ← min(ω, −k (m − c_L))      (bị ép rẽ phải, tránh mép trái)
    nếu c_R < m:  ω ← max(ω, +k (m − c_R))      (bị ép rẽ trái)
Ngoài vùng sát mép, lệnh của mạng nơ-ron giữ nguyên.
Dùng lại đường đua + các mạng đã học ở tập 4.6 (tap46/sim/duongdua.py, dd_bc*_s.pt, dd_dagger_s.pt).
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

T46 = Path(__file__).resolve().parents[2] / "tap46/sim"
sys.path.insert(0, str(T46))
import duongdua as R  # noqa: E402

SIN = np.sin(R.GOC_TIA)
TRAI, PHAI = R.GOC_TIA > 0.1, R.GOC_TIA < -0.1
M, K = 0.17, 12.0                 # bề rộng vùng sát mép (m), độ gắt khi ép rẽ (rad/s mỗi m)


def khoang_ho(obs):
    d = obs * R.TAM
    return (d[:, TRAI] * SIN[TRAI]).min(1), (d[:, PHAI] * -SIN[PHAI]).min(1)


def boc_an_toan(lai, m=M, k=K, dem=None):
    def f(env, obs):
        w = np.asarray(lai(env, obs), dtype=float).copy()
        cl, cr = khoang_ho(obs)
        w0 = w.copy()
        w = np.where(cl < m, np.minimum(w, -k * (m - cl)), w)
        w = np.where(cr < m, np.maximum(w, k * (m - cr)), w)
        if dem is not None:
            song = ~env.done
            dem[0] += int((np.abs(w - w0)[song] > 1e-9).sum())
            dem[1] += int(song.sum())
        return w
    return f


def nap(ten):
    pi = R.NguoiHoc()
    pi.load_state_dict(torch.load(T46 / ten))
    return pi


def lai_thang(env, obs):
    return np.zeros(env.B)


def danh(lai):
    dem = [0, 0]
    r = R.danh_gia(boc_an_toan(lai, dem=dem)) if lai is not None else None
    return r, dem


if __name__ == "__main__":
    SEEDS = (0, 1, 2, 3)
    pct = lambda v: round(100 * float(np.mean(v)), 1)
    kq = {"m": M, "k": K}
    kq["thang"] = pct([R.danh_gia(lai_thang)["xong"]])
    dem = [0, 0]
    kq["thang_an_toan"] = pct([R.danh_gia(boc_an_toan(lai_thang, dem=dem))["xong"]])
    kq["chuyen_gia"] = pct([R.danh_gia(R.lai_chuyen_gia)["xong"]])
    kq["chuyen_gia_an_toan"] = pct([R.danh_gia(boc_an_toan(R.lai_chuyen_gia))["xong"]])
    for ten, mau in (("bc2", "dd_bc2_{}.pt"), ("bc14", "dd_bc14_{}.pt"), ("dagger", "dd_dagger_{}.pt")):
        tron, boc, can = [], [], []
        for s in SEEDS:
            pi = nap(mau.format(s))
            tron.append(R.danh_gia(R.lai_pi(pi))["xong"])
            dem = [0, 0]
            boc.append(R.danh_gia(boc_an_toan(R.lai_pi(pi), dem=dem))["xong"])
            can.append(dem[0] / max(dem[1], 1))
        kq[ten] = pct(tron)
        kq[ten + "_an_toan"] = pct(boc)
        kq[ten + "_ty_can_thiep"] = pct(can)
        kq[ten + "_tung_seed"] = [[round(100 * a, 1), round(100 * b, 1)] for a, b in zip(tron, boc)]
        print(ten, kq[ten], "→", kq[ten + "_an_toan"], "can thiệp", kq[ten + "_ty_can_thiep"], "%", flush=True)
    print(json.dumps(kq, ensure_ascii=False))
    (Path(__file__).parent / "an_toan.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf8")
