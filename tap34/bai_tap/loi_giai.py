"""Lời giải bài tập tập 3.4 (tách từ ../sim/hat.py). Tự làm hat_cua_ban.py trước rồi hãy mở!"""
import numpy as np

MOC = np.array([[2.0, 4.0], [8.0, 4.0]])
SIG_Z = 0.2


def trong_so(P, z, W):
    d = np.stack([np.hypot(P[:, 0] - m[0], P[:, 1] - m[1]) for m in MOC], -1) - z
    wt = W * np.exp(-0.5 * np.sum((d / SIG_Z) ** 2, axis=1))
    return wt / wt.sum()


def ess(w):
    return float(1 / np.sum(np.asarray(w) ** 2))


def lay_mau_lai(w, r):
    K = len(w)
    return np.minimum(np.searchsorted(np.cumsum(w), (r + np.arange(K)) / K), K - 1)
