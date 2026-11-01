"""Lời giải bài tập tập 2.1. Tự làm cam_bien_cua_ban.py trước rồi hãy mở!"""
import statistics


def khoang_cach(t, c):
    return c * t / 2


def danh_gia(cac_lan_do, gia_tri_that):
    return statistics.mean(cac_lan_do) - gia_tri_that, statistics.stdev(cac_lan_do)


def uoc_luong_lech(mau_dung_yen):
    return sum(mau_dung_yen) / len(mau_dung_yen)


def goc_tich_phan(cac_mau, dt, lech=0.0):
    goc = 0.0
    for m in cac_mau:
        goc += (m - lech) * dt
    return goc
