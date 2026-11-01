"""Tự chấm bài tập tập 4.2. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import mdp as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

EPS = 0.1


def bai_1(ns):
    f = ham(ns, "chuyen")
    for x in goc.O_TRONG:
        for u in goc.U:
            a, b = f(x, u, EPS), goc.chuyen(x, u, EPS)
            assert set(a) == set(b) and all(gan(a[k], b[k]) for k in b), f"ô {x}, lệnh {u}: phải ra {b}, bạn ra {a}"
    p = f((1, 1), "phai", EPS)
    return f"từ (1, 1) đi phải với ε = 0.1: tới (2, 1) {p[(2, 1)]:.3f}, rơi xuống (1, 0) {p.get((1, 0), 0):.3f}, ..."


def bai_2(ns):
    f = ham(ns, "danh_gia")
    dong = []
    for eps in (0.0, 0.1, 0.2):
        jt, ja = f(goc.pi_tat, eps)[goc.S], f(goc.pi_an_toan, eps)[goc.S]
        assert gan(jt, goc.danh_gia(goc.pi_tat, eps)[goc.S]) and gan(ja, goc.danh_gia(goc.pi_an_toan, eps)[goc.S]), \
            f"ε = {eps}: J chưa khớp video"
        dong.append(f"ε={eps}: tắt {jt:.2f} / vòng {ja:.2f}")
    return "J_π(S): " + " · ".join(dong) + " → sàn trơn thì đường vòng rẻ hơn, như video"


def bai_3(ns):
    f = ham(ns, "mo_phong")
    for pi, ten in [(goc.pi_tat, "tắt"), (goc.pi_an_toan, "vòng")]:
        a, b = f(pi, EPS, n=2000), goc.mo_phong(pi, EPS, n=2000)
        assert gan(a["toi"], b["toi"]) and gan(a["roi"], b["roi"]), f"đường {ten}: phải ra tới {b['toi']:.3f}, rơi {b['roi']:.3f}; bạn ra {a}"
    t, v = f(goc.pi_tat, EPS, n=2000), f(goc.pi_an_toan, EPS, n=2000)
    return f"2000 lần chạy, ε = 0.1: đường tắt rơi {t['roi'] * 100:.1f}%, đường vòng rơi {v['roi'] * 100:.1f}%"


BAI = [("Bài 1 · xác suất chuyển", bai_1), ("Bài 2 · đánh giá chính sách", bai_2), ("Bài 3 · mô phỏng Monte Carlo", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "mdp_cua_ban", loi_giai)
