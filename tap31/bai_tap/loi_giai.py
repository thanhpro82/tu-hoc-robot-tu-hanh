"""Lời giải bài tập tập 3.1. Tự làm bayes_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from bayes import O_CUA, X, du_doan, hieu_chinh  # noqa: E402,F401  (Bài 1, 2 có sẵn trong code video)


def loc_bayes(ds_z):
    bel = np.full_like(X, 1 / len(X))
    ra = []
    for k, z in enumerate(ds_z):
        if k > 0:
            bel = du_doan(bel)
        bel, _ = hieu_chinh(bel, z)
        ra.append(bel)
    return ra
