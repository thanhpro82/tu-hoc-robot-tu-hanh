"""Tự chấm bài tập tập 3.3. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import ekf_ukf as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def _jac_so(fun, x, eps=1e-6):
    """Jacobi tính bằng sai phân số, để so với công thức của bạn."""
    y0 = fun(x)
    J = np.zeros((len(y0), len(x)))
    for i in range(len(x)):
        d = np.zeros(len(x)); d[i] = eps
        J[:, i] = (fun(x + d) - fun(x - d)) / (2 * eps)
    return J


def chay_lai_B(F_jac, H_jac, diem_sigma):
    """Chạy lại Phần B của video (cùng chuỗi số ngẫu nhiên) với các hàm của bạn thay vào EKF/UKF."""
    cu = goc.F_jac, goc.H_jac, goc.diem_sigma, goc.RNG
    goc.F_jac, goc.H_jac, goc.diem_sigma = F_jac, H_jac, diem_sigma
    goc.RNG = np.random.default_rng(33)
    goc.RNG.multivariate_normal(goc.MU_A, goc.SIG_A, 100_000)   # Phần A đã dùng các số ngẫu nhiên này trước
    goc.RNG.choice(100_000, 1500, replace=False)
    try:
        return goc.chay_B()
    finally:
        goc.F_jac, goc.H_jac, goc.diem_sigma, goc.RNG = cu


def rms(log, key):
    return float(np.sqrt(np.mean([np.sum((r[key][:2] - r["x"][:2]) ** 2) for r in log])))


def bai_1(ns):
    f = ham(ns, "F_jac")
    rng = np.random.default_rng(1)
    for _ in range(10):
        x, u = rng.normal(size=3), (rng.uniform(0, 1), rng.uniform(-1, 1))
        assert gan(f(x, u, 0.1), _jac_so(lambda s: np.array([s[0] + u[0] * 0.1 * np.cos(s[2]), s[1] + u[0] * 0.1 * np.sin(s[2]), s[2] + u[1] * 0.1]), x), 1e-6), \
            f"F tại x = {np.round(x, 2)} chưa khớp đạo hàm số"
    Fa = f(goc.MU_A, goc.U_A, goc.DT_A)
    cov = (Fa @ goc.SIG_A @ Fa.T)[:2, :2]
    return f"EKF tuyến tính hoá tại tâm: σx = {np.sqrt(cov[0, 0]) * 100:.1f} cm, σy = {np.sqrt(cov[1, 1]) * 100:.1f} cm (Monte Carlo: 44.4 và 102.5 cm)"


def bai_2(ns):
    f = ham(ns, "H_jac")
    rng = np.random.default_rng(2)
    for _ in range(10):
        x, l = rng.normal(size=3), rng.normal(size=2) * 4
        J = _jac_so(lambda s: np.array([np.hypot(l[0] - s[0], l[1] - s[1]), np.arctan2(l[1] - s[1], l[0] - s[0]) - s[2]]), x)
        assert gan(f(x, l), J, 1e-5), f"H tại x = {np.round(x, 2)}, mốc {np.round(l, 2)} chưa khớp đạo hàm số"
    return "H đúng: khoảng cách đổi theo vị trí, góc đổi theo cả vị trí lẫn hướng (−1 ở cột θ)"


def bai_3(ns):
    f = ham(ns, "diem_sigma")
    X, Wm, Wc = f(goc.MU_A, goc.SIG_A)
    X0, Wm0, Wc0 = goc.diem_sigma(goc.MU_A, goc.SIG_A)
    assert np.shape(X) == (7, 3), f"n = 3 thì có 7 điểm sigma (mảng 7×3), bạn ra {np.shape(X)}"
    assert gan(X, X0) and gan(Wm, Wm0) and gan(Wc, Wc0), "điểm sigma hoặc trọng số chưa khớp đáp án"
    Y = np.array([goc.f(x, goc.U_A, goc.DT_A) for x in X])
    mu = Wm @ Y[:, :2]
    log = chay_lai_B(ham(ns, "F_jac"), ham(ns, "H_jac"), f)
    return (f"Phần A: UKF ra tâm x = {mu[0]:.3f} m (Monte Carlo 1.661, EKF 2.000); "
            f"Phần B với 3 hàm của bạn: EKF RMS {rms(log, 'ekf') * 100:.1f} cm, UKF {rms(log, 'ukf') * 100:.1f} cm như video")


BAI = [("Bài 1 · Jacobi chuyển động (EKF)", bai_1), ("Bài 2 · Jacobi phép đo (EKF)", bai_2), ("Bài 3 · điểm sigma (UKF)", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "ekf_ukf_cua_ban", loi_giai)
