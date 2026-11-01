"""Lời giải bài tập tập 3.9 (tách từ ../sim/phan_tich.py). Tự làm nav_cua_ban.py trước rồi hãy mở!"""
import numpy as np


def that_luc(TR, THAT, t):
    return THAT[np.clip(np.searchsorted(TR, t), 0, len(TR) - 1)]


def qua_cua(xy, cua, ban_kinh=0.4):
    xy = np.asarray(xy)
    return bool(((np.abs(xy[:, 0] - cua[0]) < ban_kinh) & (xy[:, 1] < cua[1] + 1.1)).any())


def do_dai(xy):
    return float(np.hypot(*np.diff(np.asarray(xy), axis=0).T).sum())


def do_toa(xy):
    return float(np.sqrt(np.var(np.asarray(xy), axis=0).sum()))
