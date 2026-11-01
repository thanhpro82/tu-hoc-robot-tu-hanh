"""Lời giải bài tập tập 2.6. Tự làm thi_giac_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from thi_giac import SOBEL_X, SOBEL_Y, hough  # noqa: E402,F401  (Bài 3 có sẵn trong code video)


def tich_chap(anh, mat_na):
    p = np.pad(anh, 1, mode="edge")
    h, w = anh.shape
    ra = np.zeros((h, w))
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            ra += mat_na[1 + i, 1 + j] * p[1 - i:1 - i + h, 1 - j:1 - j + w]
    return ra


def do_doc(anh):
    sx, sy = tich_chap(anh, SOBEL_X), tich_chap(anh, SOBEL_Y)
    return np.hypot(sx, sy), sx, sy
