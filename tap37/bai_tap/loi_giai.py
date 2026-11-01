"""Lời giải bài tập tập 3.7. Tự làm phan_tich_cua_ban.py trước rồi hãy mở!"""
import math

import numpy as np


def goc_sang_quat(th):
    return 0.0, 0.0, math.sin(th / 2), math.cos(th / 2)


def quat_sang_goc(x, y, z, w):
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def ve_goc(p, X0):
    c, s = np.cos(-X0[2]), np.sin(-X0[2])
    dx, dy = p[0] - X0[0], p[1] - X0[1]
    return np.array([c * dx - s * dy, s * dx + c * dy, (p[2] - X0[2] + np.pi) % (2 * np.pi) - np.pi])


def ty_le_dung_tuong(M, ox, oy, res, tuong, o_tuong):
    iy, ix = np.nonzero(M == 100)
    x, y = ox + (ix + 0.5) * res, oy + (iy + 0.5) * res
    jx, jy = (x / o_tuong).astype(int), (y / o_tuong).astype(int)
    ok = (jx >= 0) & (jx < tuong.shape[1]) & (jy >= 0) & (jy < tuong.shape[0])
    return float(tuong[jy[ok], jx[ok]].mean())
