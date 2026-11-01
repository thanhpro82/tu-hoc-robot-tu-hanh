"""Lời giải bài tập tập 1.1. Tự làm xe_cua_ban.py trước rồi hãy mở!"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from khong_di_ngang import L, PHI_MAX, dt, step_car, van_toc_ngang  # noqa: E402,F401  (Bài 1, 2 có sẵn trong code video)


def ke_hoach_do_xe(d, L, phi_max):
    R = L / math.tan(phi_max)
    return R, math.acos(1 - d / (2 * R))
