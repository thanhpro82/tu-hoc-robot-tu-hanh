"""Tự chấm bài tập tập 3.8. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import theo_doi as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def chay_voi(m2, cap_nhat):
    """Chạy lại bộ theo dõi Kalman + cổng + Hungary của video trên đúng các khung phát hiện của video, với m2, cap_nhat của bạn."""
    cu = goc.Track.m2, goc.Track.cap_nhat

    def _m2(self, z, R):
        return m2(self.x, self.P, z, R)

    def _cn(self, z, R):
        self.x, self.P = cap_nhat(self.x, self.P, z, R)
    goc.Track.m2, goc.Track.cap_nhat = _m2, _cn
    try:
        return goc.chay_kalman_gnn()
    finally:
        goc.Track.m2, goc.Track.cap_nhat = cu


def _ngau_nhien_R(rng):
    A = rng.normal(size=(2, 2))
    return A @ A.T + 0.05 * np.eye(2)


def bai_1(ns):
    f = ham(ns, "ghep")
    z, S = f([(np.array([2.0, 0]), np.diag([0.8 ** 2, 1.0])), (np.array([2.3, 0]), np.diag([0.1 ** 2, 1.0]))])
    assert gan(np.sqrt(S[0, 0]), goc.S_GHEP, 1e-6), f"Ví dụ 15.2.1: σ 0,8 và 0,1 m ghép lại phải ra σ = {goc.S_GHEP:.3f} m, bạn ra {np.sqrt(S[0, 0]):.3f}"
    rng = np.random.default_rng(1)
    for _ in range(10):
        ds = [(rng.normal(size=2), _ngau_nhien_R(rng)) for _ in range(rng.integers(1, 4))]
        za, Sa = f(ds)
        zb, Sb = goc.ghep(ds)
        assert gan(za, zb) and gan(Sa, Sb), "ghép nhiều phát hiện chưa khớp đáp án"
    return f"σ camera 0.8 m + σ radar 0.1 m → σ ghép {np.sqrt(S[0, 0]):.3f} m (nhỏ hơn cả hai), như Ví dụ 15.2.1"


def bai_2(ns):
    f = ham(ns, "m2")
    rng = np.random.default_rng(2)
    for _ in range(20):
        x = rng.normal(size=4)
        A = rng.normal(size=(4, 4)); P = A @ A.T + 0.1 * np.eye(4)
        z, R = rng.normal(size=2), _ngau_nhien_R(rng)
        tr = goc.Track.__new__(goc.Track); tr.x, tr.P = x, P
        assert gan(f(x, P, z, R), tr.m2(z, R)), "m² chưa khớp đáp án"
    return "khoảng cách Mahalanobis tính cả độ bất định của track lẫn phát hiện; cổng 9,21 loại phát hiện ở quá xa"


def bai_3(ns):
    ra = chay_voi(ham(ns, "m2"), ham(ns, "cap_nhat"))
    d, d0, dnn = goc.cham_diem(ra), goc.DIEM_KF, goc.DIEM_NN
    assert gan(d["MOTA"], d0["MOTA"], 1e-9), f"MOTA chạy bằng code của bạn = {d['MOTA'] * 100:.1f}%, video {d0['MOTA'] * 100:.1f}%"
    return (f"Kalman + cổng + Hungary: IDSW {d['IDSW']}, FP {d['FP']}, FN {d['FN']} / {d['GT']} → MOTA {d['MOTA'] * 100:.1f}% "
            f"(cách gần nhất không dự đoán: {dnn['MOTA'] * 100:.1f}%), như video")


BAI = [("Bài 1 · ghép cảm biến", bai_1), ("Bài 2 · khoảng cách Mahalanobis", bai_2), ("Bài 3 · cập nhật track", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "theo_doi_cua_ban", loi_giai)
