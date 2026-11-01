"""Tự chấm bài tập tập 3.4. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import hat as goc  # noqa: E402  (mô phỏng trong video)
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def chay_lai(trong_so, ess, lay_mau_lai):
    """Chạy lại bộ lọc của video (cùng seed, cùng thứ tự dùng số ngẫu nhiên) với 3 hàm của bạn. Trả về log giống goc.LOG."""
    goc.RNG = rng = np.random.default_rng(39)
    K = goc.K
    x = np.array([[1.0, 1.0, 0.6]])
    P = np.column_stack([rng.uniform(0, goc.RONG, K), rng.uniform(0, goc.DAI, K), x[0, 2] + rng.normal(0, np.radians(5), K)])
    W = np.full(K, 1 / K)
    log = [{"k": 0, "x": x[0].copy(), "P": P.copy(), "w": W.copy(), "buoc": "đầu"}]
    for k in range(1, goc.SO_BUOC + 1):
        v, w = goc.lenh(k)
        x = goc.di(x, v, w, nhieu=False)
        z = goc.do(x)[0] + rng.normal(0, goc.SIG_Z, 2)
        P = goc.di(P, v, w)
        wt = trong_so(P, z, W)
        log.append({"k": k, "x": x[0].copy(), "P": P.copy(), "w": wt.copy(), "ess": ess(wt), "buoc": "trọng số"})
        if ess(wt) < K / 2:
            P = P[lay_mau_lai(wt, rng.random())]
            P[:, :2] += rng.normal(0, 0.03, (K, 2))
            W = np.full(K, 1 / K)
        else:
            W = wt
        log.append({"k": k, "x": x[0].copy(), "P": P.copy(), "w": W.copy(), "buoc": "lấy mẫu lại"})
    return log


def bai_1(ns):
    f = ham(ns, "trong_so")
    rng = np.random.default_rng(1)
    P = np.column_stack([rng.uniform(0, 10, 50), rng.uniform(0, 8, 50), np.zeros(50)])
    W = rng.dirichlet(np.ones(50))
    z = np.array([3.0, 4.5])
    w = np.asarray(f(P, z, W))
    assert gan(w.sum(), 1.0), "trọng số phải có tổng = 1"
    assert gan(w, _lg.trong_so(P, z, W)), "trọng số chưa đúng (nhớ nhân với W cũ và chuẩn hoá)"
    return "hạt nào cho khoảng cách tới 2 mốc gần số đo thì nặng hơn"


def bai_2(ns):
    f = ham(ns, "ess")
    assert gan(f(np.full(1000, 1e-3)), 1000), "1000 hạt nặng bằng nhau: ESS phải = 1000"
    w = np.zeros(1000); w[3] = 1
    assert gan(f(w), 1), "dồn hết vào 1 hạt: ESS phải = 1"
    e = [f(r["w"]) for r in goc.LOG if r["buoc"] == "trọng số"]
    assert gan(e[0], [r["ess"] for r in goc.LOG if r["buoc"] == "trọng số"][0]), "ESS bước 1 chưa khớp video"
    return f"bước 1: ESS = {e[0]:.0f}/1000 (chỉ ~16 hạt còn đáng kể), trung bình cả 40 bước {np.mean(e):.0f}"


def bai_3(ns):
    f = ham(ns, "lay_mau_lai")
    w = np.array([0.3, 0.0, 0.5, 0.2])
    chon = [int(i) for i in f(w, 0.5)]
    assert chon == [0, 2, 2, 3], f"w = [0.3, 0, 0.5, 0.2] (tổng dồn 0.3, 0.3, 0.8, 1), r = 0.5: mốc 0.125, 0.375, 0.625, 0.875 → [0, 2, 2, 3]; bạn ra {chon}"
    log = chay_lai(ham(ns, "trong_so"), ham(ns, "ess"), f)
    for a, b in zip(log, goc.LOG):
        assert gan(a["P"], b["P"]), f"bước {b['k']} ({b['buoc']}): đám hạt chưa khớp video"
    r12 = [r for r in log if r["k"] == 12 and r["buoc"] == "trọng số"][0]
    r9 = [r for r in log if r["k"] == 9 and r["buoc"] == "trọng số"][0]
    return (f"bước 9: {goc.thong_ke(r9)[1] * 100:.1f}% hạt tin nhầm vị trí soi gương; bước 12 (sau khi rẽ): "
            f"{goc.thong_ke(r12)[0] * 100:.1f}% quanh vị trí thật, như video")


BAI = [("Bài 1 · trọng số", bai_1), ("Bài 2 · cỡ mẫu hiệu dụng", bai_2), ("Bài 3 · lấy mẫu lại", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "hat_cua_ban", _lg)
