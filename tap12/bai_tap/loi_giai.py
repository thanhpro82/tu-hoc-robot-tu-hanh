"""Lời giải bài tập tập 1.2. Tự làm vong_ho_cua_ban.py trước rồi hãy mở!"""
import math


def ke_hoach_vuong(canh, v, t_quay):
    return [(canh / v, v, 0.0), (t_quay, 0.0, math.pi / 2 / t_quay)] * 4


def thoi_gian_nhanh_nhat(d, v_max, a_max):
    if v_max ** 2 / a_max > d:          # không kịp tới v_max: hình tam giác
        return 2 * math.sqrt(d / a_max)
    return 2 * v_max / a_max + (d - v_max ** 2 / a_max) / v_max


def van_toc_luc(t, d, v_max, a_max):
    T = thoi_gian_nhanh_nhat(d, v_max, a_max)
    if t < 0 or t > T:
        return 0.0
    return min(a_max * t, v_max, a_max * (T - t))
