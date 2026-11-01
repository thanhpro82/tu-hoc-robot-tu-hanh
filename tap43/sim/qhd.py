"""Tập 4.3 - Quy hoạch động: nhìn trước mọi nước đi (Chương 17, Principles of Robot Autonomy).

Dùng lại kho lưới của tập 4.2 (tap42/sim/mdp.py): 9 × 5, cầu thang, kệ, sàn trơn ε = 0,2, T = 30, g_t = 1, g_T = 100·(1 − 1[x = G]).
Quy hoạch động lùi (Algorithm 2, §17.2.2):
    J*_T(x) = g_T(x)
    J*_t(x) = min_u E_w[ g_t(x, u, w) + J*_{t+1}(f(x, u, w)) ],   t = T−1, ..., 0      (Eq. 17.13)
    π*_t(x) = argmin_u E_w[ ... ]                                                   (Eq. 17.14)
"""
import sys
from math import comb
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tap42" / "sim"))
import mdp as M  # noqa: E402

EPS = 0.2


def quy_hoach_dong(eps=EPS):
    """Trả về J[t][x] (t = 0..T) và PI[t][x] (t = 0..T−1), cùng số lần tính kỳ vọng."""
    J = [None] * (M.T + 1)
    PI = [None] * M.T
    J[M.T] = {x: M.gT(x) for x in M.O_TRONG}
    dem = 0
    for t in range(M.T - 1, -1, -1):
        Jt, Pt = {}, {}
        for x in M.O_TRONG:
            c = {}
            for u in M.U:
                c[u] = M.g(x) + sum(p * J[t + 1][n] for n, p in M.chuyen(x, u, eps).items())
                dem += 1
            u_best = min(M.U, key=lambda u: (round(c[u], 9), M.U.index(u)))
            Jt[x], Pt[x] = c[u_best], u_best
        J[t], PI[t] = Jt, Pt
    return J, PI, dem


def mo_phong(PI, eps=EPS, n=10000, seed=42):
    rng = np.random.default_rng(seed)
    dirs = list(M.HUONG.values())
    toi = roi = 0
    cp = []
    for _ in range(n):
        x, c = M.S, 0.0
        for t in range(M.T):
            c += M.g(x)
            x = M.buoc(x, dirs[rng.integers(4)] if rng.random() < eps else M.HUONG[PI[t][x]])
        c += M.gT(x)
        cp.append(c)
        toi += x == M.G
        roi += x in M.CAU_THANG
    return {"toi": toi / n, "roi": roi / n, "J_mc": float(np.mean(cp))}


if __name__ == "__main__":
    J, PI, dem = quy_hoach_dong()
    print("J*_0(S) = %.2f, số lần tính kỳ vọng = %d (= %d ô × %d lệnh × T %d)" % (J[0][M.S], dem, len(M.O_TRONG), len(M.U), M.T))
    print("so với chính sách vòng tay (4.2): %.2f" % M.danh_gia(M.pi_an_toan, EPS)[M.S])
    print("MC π*:", mo_phong(PI))
    print("π*_t(S) theo t:", [(t, PI[t][M.S]) for t in range(M.T)])
    for t in (0, 20, 24, 26, 28):
        print("t =", t)
        for y in range(M.H - 1, -1, -1):
            print("  " + " ".join(("##" if (x, y) in M.KE else PI[t][(x, y)][:2]) for x in range(M.W)))
    khac = [x for x in M.O_TRONG if x not in M.CAU_THANG and x != M.G and PI[0][x] != M.pi_an_toan(x)]
    print("ô π*_0 khác chính sách vòng:", khac)
    print("vét cạn vòng hở 4^T =", 4 ** M.T, "; số chính sách dừng 4^|X| =", 4 ** len(M.O_TRONG))
