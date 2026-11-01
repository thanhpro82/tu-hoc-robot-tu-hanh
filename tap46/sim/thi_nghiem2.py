"""Thí nghiệm chính trên đường đua: BC theo số vòng lái mẫu vs DAgger (2 vòng mẫu + 6 vòng × 2 lượt tự lái). Lưu tn2_<seed>.json + mô hình."""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

import duongdua as R

GOC = Path(__file__).resolve().parent
N_LUOT, N_VONG = 2, 6
t0 = time.time()
log = lambda *a: print(*a, round(time.time() - t0), flush=True)
rk = R.chay(R.DuongDua(20, np.random.default_rng(999)), R.lai_chuyen_gia, nhan=True)   # dữ liệu kiểm tra kiểu chuyên gia
for sd in map(int, sys.argv[1:]):
    pi_d, ls, (Xd, Ud) = R.dagger(N_VONG, N_LUOT, seed=sd, log=lambda x: log("dagger", sd, x))
    torch.save(pi_d.state_dict(), GOC / f"dd_dagger_{sd}.pt")
    tu = lambda pi: R.chay(R.DuongDua(50, np.random.default_rng(55 + sd)), R.lai_pi(pi), nhan=True)["sai"]
    out = {"dagger": [{"vong": v, "n_mau": n, "ket": k, "sai_vong": s} for v, n, k, s in ls],
           "dagger_sai_cg": R.sai_so(pi_d, rk["X"], rk["U"]), "dagger_sai_tu_lai": tu(pi_d), "bc": []}
    r = R.chay(R.DuongDua(14, np.random.default_rng(100 + sd)), R.lai_chuyen_gia, nhan=True)
    for n in range(2, 15, 2):
        m = r["I"] < n
        pi = R.hoc(r["X"][m], r["U"][m], seed=sd)
        out["bc"].append({"n_luot": n, "n_mau": int(m.sum()), "ket": R.danh_gia(R.lai_pi(pi)),
                          "sai_cg": R.sai_so(pi, rk["X"], rk["U"]), "sai_tu_lai": tu(pi)})
        torch.save(pi.state_dict(), GOC / f"dd_bc{n}_{sd}.pt")
        log("bc", sd, out["bc"][-1])
    json.dump(out, open(GOC / f"tn2_{sd}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
log("xong")
