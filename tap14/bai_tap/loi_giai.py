"""Lời giải bài tập tập 1.4. Tự làm bam_cua_ban.py trước rồi hãy mở!"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from bam_quy_dao import tinh_san  # noqa: E402,F401  (Bài 1 có sẵn trong code video)


def dieu_khien_ao(xd, yd, dxd, dyd, ddxd, ddyd, x, y, v, th, kp, kd):
    w1 = ddxd + kp * (xd - x) + kd * (dxd - v * math.cos(th))
    w2 = ddyd + kp * (yd - y) + kd * (dyd - v * math.sin(th))
    return w1, w2


def doi_lenh(w1, w2, th, v):
    return math.cos(th) * w1 + math.sin(th) * w2, (-math.sin(th) * w1 + math.cos(th) * w2) / v
