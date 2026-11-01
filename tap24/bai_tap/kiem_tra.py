"""Tự chấm bài tập tập 2.4. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import stereo as goc  # noqa: E402  (mô phỏng trong video: dựng 2 ảnh và tính bản đồ disparity lúc import, mất vài giây)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def bai_1(ns):
    f = ham(ns, "do_sau")
    for t in goc.THONG_KE[:3]:
        assert gan(f(t["d_that"], goc.B, goc.F), t["z_that"]), f"{t['ten']}: d = {t['d_that']:.2f} px phải cho z = {t['z_that']:.2f} m"
    assert gan(f(np.array([45.0, 22.5]), goc.B, goc.F), [1.0, 2.0]), "phải chạy được với mảng numpy"
    sai = [f(goc.B * goc.F / z - 1, goc.B, goc.F) - z for z in (1.0, 2.0, 4.0)]
    return "lệch 1 px disparity làm sai " + ", ".join(f"{s * 100:.1f} cm ở {z:.0f} m" for s, z in zip(sai, (1, 2, 4))) + " như video (xa gấp đôi → sai gấp ~4)"


def bai_2(ns):
    f = ham(ns, "chi_phi_diem")
    c = np.asarray(f(goc.L, goc.R, goc.DIEM[0], goc.DIEM[1], goc.D_MAX, goc.CUA_SO))
    assert c.shape == (goc.D_MAX,), f"phải trả về {goc.D_MAX} chi phí (d = 0..{goc.D_MAX - 1}), bạn trả về hình {c.shape}"
    assert gan(c, goc.DUONG_CP, 1e-6), "chi phí chưa khớp video (nhớ dùng TRUNG BÌNH bình phương hiệu trên cửa sổ 11×11, ảnh phải dời sang trái d)"
    d = int(np.argmin(c))
    return f"điểm giữa hộp: chi phí nhỏ nhất ở d = {d} px (thật {goc.B * goc.F / goc.HOP['z']:.1f}) → z ≈ {goc.B * goc.F / d:.3f} m"


def bai_3(ns):
    f = ham(ns, "noi_suy_parabol")
    assert gan(f(4.0, 1.0, 4.0), 0.0), "parabol đối xứng (4, 1, 4) thì đỉnh đúng tại d, δ = 0"
    assert gan(f(3.0, 1.0, 2.0), 0.5 * (3 - 2) / (3 - 2 + 2)), "c = (3, 1, 2): δ = 0.5·1/3 ≈ 0.167"
    assert gan(f(1.0, 1.0, 1.0), 0.0), "đường phẳng (mẫu số = 0) thì δ = 0"
    c = goc.DUONG_CP
    d0 = int(np.argmin(c))
    d = d0 + f(c[d0 - 1], c[d0], c[d0 + 1])
    assert gan(d, goc.D[goc.DIEM], 1e-6), f"điểm giữa hộp: d dưới pixel phải = {goc.D[goc.DIEM]:.3f}, bạn ra {d:.3f}"
    return f"d = {d0} {d - d0:+.3f} = {d:.3f} px (thật 37.5) → z = {goc.B * goc.F / d:.3f} m, sát độ sâu thật 1.200 m"


BAI = [("Bài 1 · độ sâu từ disparity", bai_1), ("Bài 2 · so khớp trên một hàng", bai_2), ("Bài 3 · nội suy dưới pixel", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "stereo_cua_ban", loi_giai)
