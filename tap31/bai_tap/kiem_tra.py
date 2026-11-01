"""Tự chấm bài tập tập 3.1. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import bayes as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

HC = [r for r in goc.LOG if r["loai"] == "hiệu chỉnh"]
DS_Z = [r["z"] for r in HC]                    # cảm biến báo gì ở từng bước trong video
X_THAT = [r["x"] for r in HC]


def bai_1(ns):
    f = ham(ns, "hieu_chinh")
    deu = np.full_like(goc.X, 1 / len(goc.X))
    bel, eta = f(deu, True)
    assert gan(bel, goc.LOG[1]["bel"]) and gan(eta, goc.LOG[1]["eta"]), "bước 0 'thấy cửa' từ niềm tin đều chưa khớp video"
    assert gan(bel.sum(), 1.0), "niềm tin sau hiệu chỉnh phải có tổng = 1"
    b2, _ = f(deu, False)
    assert gan(b2, goc.hieu_chinh(deu, False)[0]), "trường hợp 'không thấy' phải dùng 1 − p(thấy)"
    return f"thấy cửa lần đầu: niềm tin dồn vào 3 cửa (đỉnh {bel.max() * 100:.2f}%, η = {eta:.2f}) như video"


def bai_2(ns):
    f = ham(ns, "du_doan")
    for r_tr, r in zip(HC, [x for x in goc.LOG if x["loai"] == "dự đoán"]):
        assert gan(f(r_tr["bel"]), r["bel"]), f"dự đoán ở bước {r['buoc']} chưa khớp video"
    return "mỗi bước niềm tin dịch tới theo lệnh u = 0,5 m và nhoè đi vì nhiễu chuyển động; cả 12 bước dự đoán khớp video"


def bai_3(ns):
    f = ham(ns, "loc_bayes")
    ds = f(DS_Z)
    assert len(ds) == len(DS_Z), f"phải trả về {len(DS_Z)} niềm tin (mỗi bước một), bạn trả về {len(ds)}"
    for k, (b, r) in enumerate(zip(ds, HC)):
        assert gan(b, r["bel"]), f"bước {k}: niềm tin chưa khớp video"
    cuoi = ds[-1]
    tb = float((goc.X * cuoi).sum())
    return (f"số đỉnh: {goc.so_dinh(ds[0])} → {goc.so_dinh(ds[3])} (bước 3); cuối cùng ước lượng {tb:.2f} m (thật {X_THAT[-1]:.2f}), "
            f"{goc.p_quanh(cuoi, X_THAT[-1]) * 100:.1f}% niềm tin trong ±25 cm như video")


BAI = [("Bài 1 · hiệu chỉnh", bai_1), ("Bài 2 · dự đoán", bai_2), ("Bài 3 · cả bộ lọc Bayes", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "bayes_cua_ban", loi_giai)
