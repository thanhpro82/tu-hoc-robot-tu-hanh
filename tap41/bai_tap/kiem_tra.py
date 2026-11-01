"""Tự chấm bài tập tập 4.1. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 1–2 cho robot chạy trong mô phỏng của video bằng bảng chuyển của bạn (vài lần chạy, khoảng 10–20 giây).
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import fsm as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

SEED = range(8)


def may_tu_bang(chuyen, S):
    """Dựng FSM đầy đủ (S, I, O, n, o, s0, chuyen) từ bảng chuyển, giống tao_fsm của video."""
    n = {(s, i): chuyen.get((s, i), s) for s in S for i in goc.I_ALL}
    o = {(s, i): goc.LENH[n[(s, i)]] for s in S for i in goc.I_ALL}
    return S, goc.I_ALL, sorted(set(o.values())), n, o, "TUAN_TRA", chuyen


def chay_voi(ban, may, **kw):
    """Chạy mô phỏng của video, thay bộ não bản `ban` bằng FSM `may` của bạn."""
    cu = goc.tao_fsm
    goc.tao_fsm = lambda b: may if b == ban else cu(b)
    try:
        return [goc.chay(ban, sd, **kw)[0] for sd in SEED]
    finally:
        goc.tao_fsm = cu


def bai_1(ns):
    c = ham(ns, "chuyen_B")()
    assert c == goc.tao_fsm("B")[6], f"bảng chuyển bản B phải có đúng 4 mũi tên, bạn có {len(c)}: {c}"
    ts = chay_voi("B", may_tu_bang(c, ["TUAN_TRA", "DUOI", "TIM"]), T=90, co_pin=False)
    ta = [goc.chay("A", sd, T=90, co_pin=False)[0] for sd in SEED]
    tb, aa = np.mean([x["ti_le_thay"] for x in ts]), np.mean([x["ti_le_thay"] for x in ta])
    return f"{len(SEED)} lần chạy: bản A thấy mèo {aa * 100:.1f}% thời gian, bản B của bạn {tb * 100:.1f}% (thêm trạng thái TÌM)"


def bai_2(ns):
    cB = goc.tao_fsm("B")[6]
    cu = dict(cB)
    c = ham(ns, "them_sac")(cB)
    assert cB == cu, "đừng sửa dict truyền vào, hãy tạo dict mới"
    assert c == goc.tao_fsm("C")[6], f"bảng chuyển bản C phải có 9 mũi tên, bạn có {len(c)}"
    ts = chay_voi("C", may_tu_bang(c, goc.S_ALL), T=150, co_pin=True)
    tb = [goc.chay("B", sd, T=150, co_pin=True)[0] for sd in SEED]
    het_B = sum(x["t_het_pin"] is not None for x in tb)
    het_C = sum(x["t_het_pin"] is not None for x in ts)
    return f"{len(SEED)} lần chạy 150 s: bản B hết pin giữa nhà {het_B}/{len(SEED)} lần, bản C của bạn {het_C}/{len(SEED)} lần"


def bai_3(ns):
    f = ham(ns, "ghep_song_song")
    R = goc.tao_fsm("C")
    assert tuple(f(goc.fsm_den())) == (2, 2, 4), "một máy đèn (2 trạng thái, 2 đầu vào): phải ra (2, 2, 4)"
    cua = tuple(f(R, goc.fsm_cua()))
    den = tuple(f(R, goc.fsm_cua(), goc.fsm_den()))
    assert cua == tuple(goc.ghep_song_song(R, goc.fsm_cua())), f"robot + cửa: phải ra {goc.ghep_song_song(R, goc.fsm_cua())}, bạn ra {cua}"
    assert den == tuple(goc.ghep_song_song(R, goc.fsm_cua(), goc.fsm_den())), "robot + cửa + đèn chưa khớp video"
    return f"robot 5×6 = 30 ô; ghép thêm cửa: {cua[2]} ô; thêm đèn: {den[2]} ô (bùng nổ tổ hợp), như video"


BAI = [("Bài 1 · bảng chuyển bản B", bai_1), ("Bài 2 · thêm hành vi sạc", bai_2), ("Bài 3 · ghép song song", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "fsm_cua_ban", loi_giai)
