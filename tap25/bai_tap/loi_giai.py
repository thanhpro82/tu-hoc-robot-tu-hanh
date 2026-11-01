"""Lời giải bài tập tập 2.5. Tự làm sfm_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from sfm import chuan_hoa, tam_giac, tim_F  # noqa: E402,F401  (Bài 1, 2 có sẵn trong code video)


def dem_truoc_camera(R, t, X):
    return int(((X[:, 2] > 0) & ((X @ R.T + t)[:, 2] > 0)).sum())
