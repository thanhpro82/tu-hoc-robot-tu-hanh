"""Lời giải bài tập tập cuối F (tách từ ../sim/giao_do.py). Tự làm giaodo_cua_ban.py trước rồi hãy mở!"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from giao_do import F_CAM, GOC_TIA, H_NGUOI, N_ANH, R_NGUOI, SO_TIA, goc, vat_la  # noqa: E402


def vi_tri_tu_khung(khung):
    s, cx, cy, w, h = khung
    return H_NGUOI * F_CAM / (h * N_ANH), math.atan((cx - 0.5) * N_ANH / F_CAM)


def ghep(uoc, z, Z_cam, huong):
    j = int(np.argmin(np.abs(goc(GOC_TIA + huong))))
    la = vat_la(uoc, z)
    ung = [(z[i % SO_TIA], i % SO_TIA) for i in (j - 1, j, j + 1) if la[i % SO_TIA]]
    if ung:
        d, i = min(ung)
        a = uoc[2] + GOC_TIA[i]
        d += R_NGUOI
    else:
        d, a = Z_cam, uoc[2] - huong
    return (uoc[0] + d * math.cos(a), uoc[1] + d * math.sin(a)), d


BANG = {("CHỜ LỆNH", "co_lenh"): "ĐỊNH VỊ", ("ĐI LẤY", "toi_noi"): "NHẬN ĐỒ", ("ĐI GIAO", "toi_noi"): "TÌM NGƯỜI",
        ("NHẬN ĐỒ", "xong_viec"): "ĐI GIAO", ("TÌM NGƯỜI", "thay_nguoi"): "TIẾP CẬN", ("TIẾP CẬN", "du_gan"): "GIAO",
        ("GIAO", "xong_viec"): "XONG"}


def chuyen(s, su_kien, truoc_dung=None, da_lay=False):
    if s == "ĐỊNH VỊ" and su_kien == "da_dinh_vi":
        return "ĐI GIAO" if da_lay else "ĐI LẤY"
    if s in ("ĐI LẤY", "ĐI GIAO", "DỪNG") and su_kien == "mat_dau":
        return "ĐỊNH VỊ"
    if s in ("ĐI LẤY", "ĐI GIAO") and su_kien == "vat_la":
        return "DỪNG"
    if s == "DỪNG" and su_kien == "duong_trong":
        return truoc_dung
    return BANG.get((s, su_kien), s)
