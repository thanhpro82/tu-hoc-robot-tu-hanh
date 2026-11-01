"""Lời giải bài tập tập 1.7 (rút từ ws/duong_di.py và ws/controller_node.py). Tự làm duong_cua_ban.py trước rồi hãy mở!"""
import bisect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ws"))
from duong_di import lam_muot  # noqa: E402,F401  (Bài 1 có sẵn trong planner của video)


def s_tai(t, L, v_ref, a_ref):
    t_tang = v_ref / a_ref
    T = L / v_ref + t_tang
    t = max(0.0, min(t, T))
    if t < t_tang:
        return 0.5 * a_ref * t * t
    if t > T - t_tang:
        return L - 0.5 * a_ref * (T - t) ** 2
    return 0.5 * a_ref * t_tang ** 2 + v_ref * (t - t_tang)


def diem_tai(pts, s_cong_don, s):
    i = min(len(pts) - 2, max(0, bisect.bisect_right(s_cong_don, s) - 1))
    k = (s - s_cong_don[i]) / max(1e-9, s_cong_don[i + 1] - s_cong_don[i])
    a, b = pts[i], pts[i + 1]
    return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
