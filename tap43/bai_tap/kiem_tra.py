"""Tự chấm bài tập tập 4.3. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[2] / "tap42" / "sim"), str(_D.parents[1])]
import qhd as goc  # noqa: E402  (mô phỏng trong video; dùng kho của tập 4.2)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

M = goc.M
EPS = goc.EPS
J0, PI0, DEM0 = goc.quy_hoach_dong()


def bai_1(ns):
    f = ham(ns, "bellman")
    for x in M.O_TRONG:
        c, u = f(x, J0[1], EPS)
        assert gan(c, J0[0][x]) and u == PI0[0][x], f"ô {x}: phải ra ({J0[0][x]:.3f}, {PI0[0][x]}), bạn ra ({c:.3f}, {u})"
    c, u = f(M.S, J0[1], EPS)
    return f"tại S, bước đầu: lệnh tốt nhất là '{u}', chi phí kỳ vọng {c:.2f}"


def bai_2(ns):
    J, PI = ham(ns, "quy_hoach_dong")(EPS)
    assert len(J) == M.T + 1 and len(PI) == M.T, f"J phải có {M.T + 1} bảng, PI có {M.T} bảng"
    for t in range(M.T):
        assert all(gan(J[t][x], J0[t][x]) for x in M.O_TRONG) and PI[t] == PI0[t], f"bước t = {t} chưa khớp video"
    tay = M.danh_gia(M.pi_an_toan, EPS)[M.S]
    return f"J*_0(S) = {J[0][M.S]:.2f} (chính sách vòng viết tay ở 4.2: {tay:.2f}); {len(M.O_TRONG)} ô × 4 lệnh × {M.T} bước = {DEM0} phép tính"


def bai_3(ns):
    f = ham(ns, "mo_phong")
    a, b = f(PI0, EPS, n=2000), goc.mo_phong(PI0, EPS, n=2000)
    assert gan(a["toi"], b["toi"]) and gan(a["roi"], b["roi"]), f"phải ra tới {b['toi']:.4f}, rơi {b['roi']:.4f}; bạn ra {a}"
    return f"2000 lần chạy π* với sàn trơn 20%: tới đích {a['toi'] * 100:.1f}%, rơi cầu thang {a['roi'] * 100:.1f}%"


BAI = [("Bài 1 · một bước Bellman", bai_1), ("Bài 2 · quy hoạch động lùi", bai_2), ("Bài 3 · chạy chính sách tối ưu", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "qhd_cua_ban", loi_giai)
