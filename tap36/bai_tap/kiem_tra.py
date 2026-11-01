"""Tự chấm bài tập tập 3.6. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import slam as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def dead_reckoning(cong):
    DR = [goc.THAT[0].copy()]
    for z in goc.ODO:
        DR.append(cong(DR[-1], z))
    return np.array(DR)


def toi_uu(sai_so_canh, DR):
    """Tối ưu đồ thị của video (57 cạnh odometry + 1 cạnh khép vòng) bằng sai_so_canh của bạn."""
    canh = goc.CANH + [goc.CANH_VONG]
    L = [np.linalg.cholesky(Om).T for *_, Om in canh]

    def phan_du(v):
        X = np.vstack([goc.THAT[0], v.reshape(-1, 3)])
        return np.concatenate([Lk @ np.asarray(sai_so_canh(X[i], X[j], z)) for (i, j, z, _), Lk in zip(canh, L)])
    kq = least_squares(phan_du, DR[1:].ravel(), method="lm")
    return np.vstack([goc.THAT[0], kq.x.reshape(-1, 3)])


def bai_1(ns):
    cong, tru = ham(ns, "cong"), ham(ns, "tru")
    rng = np.random.default_rng(1)
    for _ in range(20):
        a, b = rng.normal(size=3) * [3, 3, 2], rng.normal(size=3) * [3, 3, 2]
        assert gan(cong(a, b), goc.cong(a, b)), f"cong({np.round(a, 2)}, {np.round(b, 2)}) chưa đúng"
        assert gan(tru(a, b), goc.tru(a, b)), f"tru({np.round(a, 2)}, {np.round(b, 2)}) chưa đúng"
        assert gan(cong(a, tru(a, b))[:2], b[:2]), "a ⊕ (a⁻¹ ⊕ b) phải quay về b"
    e = goc.loi(dead_reckoning(cong))
    return f"cộng dồn odometry bằng hàm của bạn: về tới cuối lệch {e[-1]:.2f} m, lớn nhất {e.max():.2f} m như video"


def bai_2(ns):
    f = ham(ns, "can_chinh")
    rng = np.random.default_rng(2)
    P = rng.uniform(-3, 3, (60, 2))
    for dth, t in [(0.3, np.array([1.0, -0.5])), (-2.5, np.array([0.2, 3.0]))]:
        R = np.array([[np.cos(dth), -np.sin(dth)], [np.sin(dth), np.cos(dth)]])
        d, tt = f(P, P @ R.T + t)
        assert gan(d, dth, 1e-6) and gan(tt, t, 1e-6), f"quay {dth} rad, dời {t}: bạn tìm ra {d:.3f}, {np.round(tt, 3)}"
    return "từ các cặp điểm đã ghép, tìm đúng phép quay + dời (bước lõi lặp đi lặp lại trong ICP)"


def bai_3(ns):
    f = ham(ns, "sai_so_canh")
    xi, xj = np.array([1.0, 2.0, 3.1]), np.array([2.0, 2.5, -3.1])
    e = np.asarray(f(xi, xj, goc.tru(xi, xj)))
    assert gan(e, np.zeros(3), 1e-9), f"cạnh đúng hoàn toàn thì sai số = 0 (kể cả khi góc vắt qua ±π), bạn ra {e}"
    OPT = toi_uu(f, dead_reckoning(ham(ns, "cong")))
    assert gan(OPT, goc.OPT, 1e-5), "đồ thị tối ưu bằng sai số của bạn chưa khớp video"
    e = goc.loi(OPT)
    return (f"sau tối ưu đồ thị (có cạnh khép vòng): cuối lệch {e[-1]:.2f} m, trung bình {e.mean():.2f} m; "
            f"bản đồ nét {goc.do_net(goc.ve_ban_do(OPT)) * 100:.1f}% như video")


BAI = [("Bài 1 · ghép tư thế", bai_1), ("Bài 2 · căn chỉnh (ICP)", bai_2), ("Bài 3 · sai số cạnh của đồ thị", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "slam_cua_ban", loi_giai)
