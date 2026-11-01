"""Lời giải bài tập tập 4.7 (tách từ ../sim/an_toan.py và ../sim/the_gioi.py). Tự làm physai_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from the_gioi import H, W_THU, diem, R  # noqa: E402

SIN = np.sin(R.GOC_TIA)
TRAI, PHAI = R.GOC_TIA > 0.1, R.GOC_TIA < -0.1


def khoang_ho(obs):
    d = obs * R.TAM
    return (d[:, TRAI] * SIN[TRAI]).min(1), (d[:, PHAI] * -SIN[PHAI]).min(1)


def boc_an_toan(lai, m=0.17, k=12.0):
    def f(env, obs):
        w = np.asarray(lai(env, obs), dtype=float).copy()
        cl, cr = khoang_ho(obs)
        w = np.where(cl < m, np.minimum(w, -k * (m - cl)), w)
        return np.where(cr < m, np.maximum(w, k * (m - cr)), w)
    return f


def chi_phi_tuong_tuong(f, obs):
    B = obs.shape[0]
    with torch.no_grad():
        x = torch.as_tensor(obs).unsqueeze(1).expand(B, len(W_THU), R.N_TIA).reshape(-1, R.N_TIA)
        w = torch.as_tensor(W_THU, dtype=torch.float32).repeat(B)
        c = 0
        for h in range(H):
            x = f(x, w).clamp(0, 1)
            c = c + diem(x) * 0.9 ** h
    return c.reshape(B, len(W_THU)).numpy()
