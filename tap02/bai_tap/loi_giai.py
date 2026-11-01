"""Lời giải bài tập tập 0.2. Tự làm robot_cua_ban.py trước rồi hãy mở!"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from robot_dau_tien import dt, step  # noqa: E402,F401  (Bài 1 chính là hàm step trong video)


def omega_so_8(t):
    return 1.0 if t < 2 * math.pi else -1.0


def lenh_vong_tron(R, T):
    return 2 * math.pi * R / T, 2 * math.pi / T
