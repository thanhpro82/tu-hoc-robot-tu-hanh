"""Lời giải bài tập tập 2.4. Tự làm stereo_cua_ban.py trước rồi hãy mở!"""
import numpy as np


def do_sau(d, b, f):
    return b * f / d


def chi_phi_diem(L, R, hang, cot, d_max, cua_so):
    r = cua_so // 2
    trai = L[hang - r:hang + r + 1, cot - r:cot + r + 1]
    return np.array([((trai - R[hang - r:hang + r + 1, cot - d - r:cot - d + r + 1]) ** 2).mean() for d in range(d_max)])


def noi_suy_parabol(c0, c1, c2):
    mau = c0 - 2 * c1 + c2
    if mau <= 0:
        return 0.0
    return float(np.clip(0.5 * (c0 - c2) / mau, -0.5, 0.5))
