"""Lời giải bài tập tập 3.6. Tự làm slam_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from slam import cong, goc, tru  # noqa: E402,F401  (Bài 1 có sẵn trong code video)


def can_chinh(P, Q):
    mp, mq = P.mean(0), Q.mean(0)
    U, _, Vt = np.linalg.svd((P - mp).T @ (Q - mq))
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[1] *= -1
        R = Vt.T @ U.T
    return float(np.arctan2(R[1, 0], R[0, 0])), mq - R @ mp


def sai_so_canh(xi, xj, z):
    e = tru(xi, xj) - z
    e[2] = goc(e[2])
    return e
