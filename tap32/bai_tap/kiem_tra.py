"""Tự chấm bài tập tập 3.2. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import kalman as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

DS_U = [r["u"] for r in goc.LOG]            # gia tốc kế đo được ở từng bước trong video
DS_Z = [r["z"] for r in goc.LOG]            # cảm biến khoảng cách đo được
P = np.array([r["p"] for r in goc.LOG])     # vị trí thật
MU0, SIG0 = np.array([0.0, 0.0]), np.diag([1.0, 0.5])


def _rms(e):
    return float(np.sqrt(np.mean(np.asarray(e) ** 2)))


def bai_1(ns):
    f = ham(ns, "du_doan")
    mu_b, Sig_b = f(np.array([1.0, 2.0]), np.diag([0.04, 0.01]), 0.5)
    assert gan(mu_b, [1.0 + 0.2 + 0.0025, 2.05]), f"μ = (1, 2), u = 0.5: μ̄ phải = (1.2025, 2.05), bạn ra {mu_b}"
    A, Q = goc.A, goc.Q
    assert gan(Sig_b, A @ np.diag([0.04, 0.01]) @ A.T + Q), "Σ̄ = AΣAᵀ + Q chưa đúng"
    return "μ̄ = Aμ + Bu đẩy niềm tin tới; Σ̄ = AΣAᵀ + Q làm nó bè ra (thêm bất định của gia tốc kế)"


def bai_2(ns):
    du, f = ham(ns, "du_doan"), ham(ns, "cap_nhat")
    mu_b, Sig_b = du(MU0, SIG0, DS_U[0])
    mu, Sig, K = f(mu_b, Sig_b, DS_Z[0])
    assert gan(np.asarray(K)[0, 0], goc.LOG[0]["K"]), f"bước 1: K (vị trí) phải = {goc.LOG[0]['K']:.3f} như video, bạn ra {np.asarray(K).ravel()}"
    assert gan(mu[0], goc.LOG[0]["mu"]) and gan(np.sqrt(Sig[0, 0]), goc.LOG[0]["sig"]), "bước 1: μ hoặc Σ sau cập nhật chưa khớp video"
    assert gan(Sig, Sig.T), "Σ phải đối xứng"
    return f"bước 1: K = {np.asarray(K)[0, 0]:.3f} (chưa tin dự đoán nên tin gần hết số đo)"


def bai_3(ns):
    f = ham(ns, "loc_kalman")
    mus = f(DS_U, DS_Z, MU0, SIG0)
    p_hat = np.array([m[0] for m in mus])
    assert len(p_hat) == len(P), f"phải trả về {len(P)} μ, bạn trả về {len(p_hat)}"
    assert gan(p_hat, [r["mu"] for r in goc.LOG], 1e-8), "chuỗi μ chưa khớp video"
    z_rms, k_rms = _rms(np.array(DS_Z) - P), _rms(p_hat - P)
    return f"sai RMS: chỉ cảm biến {z_rms * 100:.1f} cm → Kalman {k_rms * 100:.1f} cm, tốt hơn {z_rms / k_rms:.1f} lần như video"


BAI = [("Bài 1 · dự đoán", bai_1), ("Bài 2 · cập nhật", bai_2), ("Bài 3 · cả bộ lọc Kalman", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "kalman_cua_ban", loi_giai)
