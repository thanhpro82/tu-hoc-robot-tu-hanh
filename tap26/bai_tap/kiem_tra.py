"""Tự chấm bài tập tập 2.6. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import convolve, gaussian_filter

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import thi_giac as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def canh_voi(do_doc, anh, lam_min):
    """Như goc.canh nhưng dùng do_doc của bạn."""
    a = gaussian_filter(anh, goc.SIGMA) if lam_min else anh
    mag, sx, sy = do_doc(a)
    e = (mag > goc.NGUONG) & goc.chi_giu_dinh(mag, sx, sy)
    e[:3, :] = e[-3:, :] = False
    e[:, :3] = e[:, -3:] = False
    return e


def bai_1(ns):
    f = ham(ns, "tich_chap")
    rng = np.random.default_rng(3)
    anh = rng.uniform(0, 255, (12, 15))
    for k in [goc.SOBEL_X, goc.SOBEL_Y, rng.normal(size=(3, 3))]:
        assert gan(f(anh, k), convolve(anh, k, mode="nearest"), 1e-9), "tích chập chưa đúng (nhớ lật mặt nạ: anh[y − i, x − j], viền lấy pixel gần nhất)"
    return "khớp scipy.ndimage.convolve trên ảnh thử, cả với mặt nạ không đối xứng"


def bai_2(ns):
    f = ham(ns, "do_doc")
    a = gaussian_filter(goc.ANH, goc.SIGMA)
    mag, sx, sy = f(a)
    m0, sx0, sy0 = goc.do_doc(a)
    assert gan(sx, sx0, 1e-6) and gan(sy, sy0, 1e-6) and gan(mag, m0, 1e-6), "Sx, Sy hoặc |∇S| chưa khớp video"
    n0, g0 = goc.thong_ke(canh_voi(f, goc.ANH, False))
    n1, g1 = goc.thong_ke(canh_voi(f, goc.ANH, True))
    return f"không làm mịn: {n0} pixel cạnh, {g0 / n0 * 100:.0f}% giả; làm mịn Gauss trước: {n1} pixel cạnh, {g1} giả, như video"


def bai_3(ns):
    f = ham(ns, "hough")
    acc, alphas, r_max = f(goc.E_MIN)
    assert np.shape(acc) == goc.ACC.shape, f"lưới phải có hình {goc.ACC.shape}, bạn ra {np.shape(acc)}"
    assert (np.asarray(acc) == goc.ACC).all(), "số phiếu chưa khớp video (α từ −90° tới 89°, r làm tròn, cột r + r_max)"
    dinh = goc.tim_dinh(np.asarray(acc), alphas, r_max)
    a, r = np.mean([d[0] for d in dinh]), np.mean([d[1] for d in dinh])
    return (f"2 đỉnh: α = {dinh[0][0]:.0f}°, r = {dinh[0][1]:.0f} và {dinh[1][1]:.0f} px (hai mép vạch) → đường giữa α = {a:.1f}°, "
            f"r = {r:.1f} (thật 23.4°, 242.2) như video")


BAI = [("Bài 1 · tích chập", bai_1), ("Bài 2 · độ dốc Sobel", bai_2), ("Bài 3 · biến đổi Hough", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "thi_giac_cua_ban", loi_giai)
