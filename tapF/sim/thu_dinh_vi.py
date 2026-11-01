"""Thử riêng giai đoạn ĐỊNH VỊ (định vị toàn cục) trên nhiều điểm xuất phát: sai số lúc chốt vị trí."""
import math
import sys
from multiprocessing import Pool

import numpy as np

import giao_do as G


def mot(seed):
    import torch
    torch.set_num_threads(1)
    G.T_MAX = 25.0
    L = G.tao_luot(seed)
    r = G.chay_luot(L, "du", ghi=True)
    lg = r["log"]
    for i, s in enumerate(lg["s"]):
        if s not in ("CHỜ LỆNH", "ĐỊNH VỊ"):
            x, u = lg["x"][i], lg["uoc"][i]
            return seed, round(i * G.DT, 1), round(math.hypot(x[0] - u[0], x[1] - u[1]), 2)
    return seed, None, None


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    with Pool(6) as p:
        kq = p.map(mot, range(n))
    sai = [k for k in kq if k[2] is None or k[2] > 0.5]
    print("chốt nhầm (>0,5 m) hoặc không chốt:", len(sai), "/", n, sai)
    print("thời gian chốt TB", np.mean([k[1] for k in kq if k[1] is not None]))
