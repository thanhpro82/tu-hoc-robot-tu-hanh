"""Lời giải bài tập tập 4.6 (tách từ ../sim/duongdua.py). Tự làm batchuoc_cua_ban.py trước rồi hãy mở!"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from duongdua import chay, hoc, lai_pi  # noqa: E402


def omega_pure_pursuit(x, y, th, gx, gy, V, LD, W_MAX):
    al = math.atan2(gy - y, gx - x) - th
    al = (al + math.pi) % (2 * math.pi) - math.pi
    return float(np.clip(2 * V * math.sin(al) / LD, -W_MAX, W_MAX))


def hoc_bc(X, U, seed=0, n_buoc=3000, lr=3e-3):
    return hoc(X, U, seed=seed, n_buoc=n_buoc, lr=lr)


def vong_dagger(pi, env, X, U, hoc):
    r = chay(env, lai_pi(pi), nhan=True)
    X, U = np.concatenate([X, r["X"]]), np.concatenate([U, r["U"]])
    return hoc(X, U), X, U
