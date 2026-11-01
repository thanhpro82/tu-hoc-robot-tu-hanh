"""Thí nghiệm chính: chuyên gia, BC theo số lượt lái mẫu, DAgger 10 vòng × 20 lượt; 3 seed. Lưu thi_nghiem.json + mô hình."""
import json
import time
from pathlib import Path

import numpy as np
import torch

import batchuoc as B
import deeprl as D

GOC = Path(__file__).resolve().parent
SEEDS, N_VONG, N_LUOT = (0, 1, 2), 10, 20
t0 = time.time()
log = lambda *a: print(*a, round(time.time() - t0), flush=True)
kq = {"chuyen_gia": B.danh_gia(B.lai_chuyen_gia, seed=7), "seeds": []}
log("chuyên gia", kq["chuyen_gia"])
# tập kiểm tra cố định trên đường của chuyên gia (để đo "đoán sai" trên dữ liệu kiểu chuyên gia)
rk = B.chay(D.MoiTruong(100, np.random.default_rng(999)), B.lai_chuyen_gia, nhan=True)
for sd in SEEDS:
    pi_d, ls, (Xd, Ud) = B.dagger(N_VONG, N_LUOT, seed=sd, log=lambda x: log("dagger", sd, x))
    torch.save(pi_d.state_dict(), GOC / f"pi_dagger_{sd}.pt")
    r = B.chay(D.MoiTruong(240, np.random.default_rng(100 + sd)), B.lai_chuyen_gia, nhan=True)
    bc = []
    for n in range(N_LUOT, 241, N_LUOT):
        m = r["I"] < n
        pi = B.hoc(r["X"][m], r["U"][m], seed=sd)
        rr = B.chay(D.MoiTruong(200, np.random.default_rng(55 + sd)), B.lai_pi(pi), nhan=True)
        bc.append({"n_luot": n, "n_mau": int(m.sum()), "ket": B.danh_gia(B.lai_pi(pi), seed=7),
                   "sai_cg": B.ty_le_sai(pi, rk["X"], rk["U"]), "sai_tu_lai": rr["sai"]})
        log("bc", sd, bc[-1])
        if n == 200:
            torch.save(pi.state_dict(), GOC / f"pi_bc200_{sd}.pt")
    rd = B.chay(D.MoiTruong(200, np.random.default_rng(55 + sd)), B.lai_pi(pi_d), nhan=True)
    kq["seeds"].append({"dagger": [{"vong": v, "n_mau": n, "ket": k, "sai_vong": s} for v, n, k, s in ls],
                        "dagger_sai_cg": B.ty_le_sai(pi_d, rk["X"], rk["U"]), "dagger_sai_tu_lai": rd["sai"], "bc": bc})
    json.dump(kq, open(GOC / "thi_nghiem.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
log("xong")
