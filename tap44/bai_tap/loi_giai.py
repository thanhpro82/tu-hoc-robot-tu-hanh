"""Lời giải bài tập tập 4.4 (tách từ hàm hoc() trong ../sim/qlearn.py). Tự làm qlearn_cua_ban.py trước rồi hãy mở!"""
import numpy as np


def chon_hanh_dong(Qi, eps, rng):
    return int(rng.integers(4)) if rng.random() < eps else int(rng.choice(np.flatnonzero(Qi == Qi.max())))


def cap_nhat_q(Q, i, a, r, i2, xong, alpha, gamma):
    muc_tieu = r if xong else r + gamma * Q[i2].max()
    Q[i, a] += alpha * (muc_tieu - Q[i, a])


def chinh_sach_tham_lam(Q, cac_o, IDX, U):
    return {x: U[int(np.argmax(Q[IDX[x]]))] for x in cac_o}
