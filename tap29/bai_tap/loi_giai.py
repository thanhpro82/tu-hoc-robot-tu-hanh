"""Lời giải bài tập tập 2.9 (tách từ hàm chay() trong ../sim/di_theo.py). Tự làm di_theo_cua_ban.py trước rồi hãy mở!"""
import math

N, F = 128, 60.0
H_NGUOI, D_BONG = 1.7, 0.25
R_KC = 2.0
DT = 0.1
KP, KI, KTH = 0.8, 0.15, 1.6
V_MAX, W_MAX = 1.2, 1.5


def _kep(x, a, b):
    return max(a, min(b, x))


def uoc_luong(d):
    c, s, cx, cy, w, h = d
    huong = math.atan((cx - 0.5) * N / F)
    if c == 0:
        return H_NGUOI * F / (h * N), huong
    return D_BONG * F / (w * N), huong


def lenh(z_hat, huong, tich_phan):
    e = z_hat - R_KC
    tich_phan = _kep(tich_phan + e * DT, -1.5, 1.5)
    return _kep(KP * e + KI * tich_phan, 0, V_MAX), _kep(KTH * -huong, -W_MAX, W_MAX), tich_phan


def quyet_dinh(dets):
    bo = [d for d in dets if d[0] == 2]
    if bo:
        zb, hb = uoc_luong(max(bo, key=lambda d: d[1]))
        if zb < 1.6 and abs(hb) < math.radians(30):
            return "dừng"
    return "theo" if any(d[0] == 0 for d in dets) else "tìm"
