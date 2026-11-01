"""Tự chấm bài tập tập 1.5. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import a_sao as goc  # noqa: E402  (mô phỏng trong video)
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def ban_do_ngau_nhien(seed, n=20):
    rng = random.Random(seed)
    o = [["#" if rng.random() < 0.25 else "." for _ in range(n)] for _ in range(n)]
    o[0][0] = o[n - 1][n - 1] = "."
    return ["".join(d) for d in o]


def _hop_le(duong, bat_dau, dich, ban_do):
    assert duong[0] == bat_dau and duong[-1] == dich, f"đường phải đi từ {bat_dau} tới {dich}, của bạn từ {duong[0]} tới {duong[-1]}"
    for a, b in zip(duong, duong[1:]):
        assert b in [q for q, _ in _lg.ke(a, ban_do)], f"bước {a} → {b} không hợp lệ (xuyên tường hoặc nhảy cóc)"
    return sum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(duong, duong[1:]))


def bai_1(ns):
    f = ham(ns, "ke")
    for r in range(goc.ROWS):
        for c in range(goc.COLS):
            if goc.BAN_DO[r][c] == "#":
                continue
            cua_ban = sorted((tuple(q), round(cp, 9)) for q, cp in f((r, c), goc.BAN_DO))
            dap_an = sorted((q, round(cp, 9)) for q, cp in goc.ke((r, c)))
            assert cua_ban == dap_an, f"ô {(r, c)}: ô kề phải là {dap_an}, bạn ra {cua_ban}"
    return "đúng ô kề cho cả 237 ô trống: 8 hướng, chéo √2, không xuyên tường, không cắt góc"


def bai_2(ns):
    f = ham(ns, "h_euclid")
    assert gan(f((0, 0), (3, 4)), 5.0), f"từ (0,0) tới (3,4) phải = 5, bạn ra {f((0, 0), (3, 4))}"
    assert gan(f(goc.START, goc.GOAL), goc.h_euclid(goc.START)), "h từ S tới G chưa đúng"
    return f"h(S) = {f(goc.START, goc.GOAL):.2f} ô: không bao giờ dài hơn đường thật (đường thật {goc.A_SAO[2]:.2f} ô)"


def bai_3(ns):
    f, h = ham(ns, "tim_duong"), ham(ns, "h_euclid")
    d_dij, mo_dij, cp_dij = f(goc.START, goc.GOAL, goc.BAN_DO, lambda o: 0.0)
    d_a, mo_a, cp_a = f(goc.START, goc.GOAL, goc.BAN_DO, lambda o: h(o, goc.GOAL))
    for d, cp, ten in [(d_dij, cp_dij, "Dijkstra"), (d_a, cp_a, "A*")]:
        dai = _hop_le(d, goc.START, goc.GOAL, goc.BAN_DO)
        assert gan(cp, goc.A_SAO[2]) and gan(dai, cp), f"{ten}: đường dài {cp * goc.O_M:.2f} m, ngắn nhất phải là {goc.A_SAO[2] * goc.O_M:.2f} m"
    assert mo_a < mo_dij, f"A* phải mở ít ô hơn Dijkstra (bạn: A* {mo_a}, Dijkstra {mo_dij})"
    for seed in range(5):
        bd = ban_do_ngau_nhien(seed)
        try:
            dap = _lg.tim_duong((0, 0), (19, 19), bd, lambda o: _lg.h_euclid(o, (19, 19)))[2]
        except KeyError:
            continue                      # bản đồ không có đường, bỏ qua
        cb = f((0, 0), (19, 19), bd, lambda o: h(o, (19, 19)))
        assert gan(cb[2], dap), f"bản đồ ngẫu nhiên số {seed}: đường ngắn nhất dài {dap:.2f} ô, bạn ra {cb[2]:.2f}"
    ghi_chu = "" if (mo_a, mo_dij) == (len(goc.A_SAO[1]), len(goc.DIJKSTRA[1])) else " (số ô mở hơi khác video do cách xếp các ô hoà điểm, vẫn đúng)"
    return f"cùng đường {cp_a * goc.O_M:.2f} m; Dijkstra mở {mo_dij} ô, A* chỉ mở {mo_a} ô{ghi_chu}"


BAI = [("Bài 1 · ô kề", bai_1), ("Bài 2 · heuristic", bai_2), ("Bài 3 · A*", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "a_sao_cua_ban", _lg)
