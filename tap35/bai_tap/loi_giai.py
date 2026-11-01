"""Lời giải bài tập tập 3.5. Tự làm mcl_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from mcl import quet, trong_so  # noqa: E402,F401  (Bài 1, 2 có sẵn trong code video)


def tha_hat(P, chon, hat_moi):
    P = P.copy()
    P[chon] = hat_moi
    return P
