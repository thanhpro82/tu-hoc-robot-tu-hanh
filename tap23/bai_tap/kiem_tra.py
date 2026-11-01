"""Tự chấm bài tập tập 2.3. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import hieu_chinh as goc  # noqa: E402  (mô phỏng trong video, chụp 10 ảnh bàn cờ lúc import)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

DS_UV = [a["uv"] for a in goc.ANH]


def zhang_voi(tim_H, v_ij):
    """Chạy bước Zhang của video nhưng dùng tim_H và v_ij của bạn (thay tạm trong module goc)."""
    cu = goc.tim_H, goc.v_ij
    goc.tim_H, goc.v_ij = tim_H, v_ij
    try:
        return goc.zhang(DS_UV)
    finally:
        goc.tim_H, goc.v_ij = cu


def bai_1(ns):
    f = ham(ns, "meo")
    c = goc.K_THAT[:2, 2]
    rng = np.random.default_rng(1)
    uv = rng.uniform([0, 0], [640, 480], (50, 2))
    assert gan(f(uv, goc.K_MEO, c), goc.meo(uv, goc.K_MEO, c)), "50 điểm ngẫu nhiên: méo chưa đúng công thức (1 + k·r²)·d + c"
    assert gan(f(c[None], goc.K_MEO, c), c[None]), "điểm ở đúng tâm méo thì không bị lệch"
    lech = float(np.linalg.norm(f(goc.GOC, goc.K_MEO, c) - goc.GOC))
    assert gan(lech, goc.LECH_GOC_ANH), f"góc ảnh (640, 480) phải bị kéo lệch {goc.LECH_GOC_ANH:.1f} px, bạn ra {lech:.1f}"
    return f"méo thùng k = {goc.K_MEO:.0e}: góc ảnh bị kéo lệch {lech:.1f} px như video"


def bai_2(ns):
    f = ham(ns, "tim_H")
    for i, uv in enumerate(DS_UV[:3]):
        H = f(goc.DIEM_CO, uv)
        H_dap = goc.tim_H(goc.DIEM_CO, uv)
        assert np.shape(H) == (3, 3), f"H phải là ma trận 3×3, bạn ra hình {np.shape(H)}"
        assert gan(H / H[2, 2], H_dap, 1e-6), f"ảnh {i}: H chưa khớp đáp án (nhớ chuẩn hoá, SVD lấy hàng cuối của Vt, bỏ chuẩn hoá, chia H[2,2])"
    # H biến bàn cờ thành ảnh: chiếu thử và đo sai lệch
    H = f(goc.DIEM_CO, DS_UV[0])
    ph = (H @ np.column_stack([goc.DIEM_CO, np.ones(len(goc.DIEM_CO))]).T).T
    sai = float(np.sqrt(((ph[:, :2] / ph[:, 2:] - DS_UV[0]) ** 2).sum(axis=1).mean()))
    return f"H của 3 ảnh thử khớp đáp án; H đưa 54 góc ô cờ lên ảnh lệch trung bình {sai:.2f} px (phần lệch là do méo + nhiễu)"


def bai_3(ns):
    f = ham(ns, "v_ij")
    rng = np.random.default_rng(2)
    for _ in range(10):
        H = rng.normal(size=(3, 3))
        for i, j in [(0, 1), (0, 0), (1, 1)]:
            assert gan(f(H, i, j), goc.v_ij(H, i, j)), f"v_ij(H, {i}, {j}) chưa đúng 6 thành phần"
    K, _, V_shape = zhang_voi(goc.tim_H, f)
    K0 = goc.LICH_SU[0]["K"]
    assert gan(K, K0, 1e-6), "dùng v_ij của bạn, Zhang chưa ra đúng K như video"
    return (f"V có kích thước {V_shape}; Zhang ra α={K[0, 0]:.1f} β={K[1, 1]:.1f} u0={K[0, 2]:.1f} v0={K[1, 2]:.1f} như video "
            f"(thật 512/508/331/236; bước tinh chỉnh có méo đưa về {goc.K_UOC[0, 0]:.1f}/{goc.K_UOC[1, 1]:.1f}/{goc.K_UOC[0, 2]:.1f}/{goc.K_UOC[1, 2]:.1f})")


BAI = [("Bài 1 · méo xuyên tâm", bai_1), ("Bài 2 · homography (DLT)", bai_2), ("Bài 3 · Zhang: véc-tơ v_ij", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "hieu_chinh_cua_ban", loi_giai)
