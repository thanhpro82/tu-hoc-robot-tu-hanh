"""Tự chấm bài tập tập 3.5. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 3 chạy lại cả lần định vị 100 bước của video (2 bộ lọc × 2000 hạt) bằng code của bạn, mất khoảng 30–60 giây.
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import mcl as goc  # noqa: E402  (mô phỏng trong video, chạy 100 bước lúc import ~30 giây)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def chay_lai(quet, trong_so, tha_hat):
    """Lặp lại đúng hàm chay() của video (cùng seed, cùng thứ tự số ngẫu nhiên) nhưng dùng 3 hàm của bạn."""
    goc.RNG = rng = np.random.default_rng(35)
    x = goc.X0.copy()
    lo_trinh, i = goc.DIEM_DEN, 0
    P = {"tha": goc.rai_hat(goc.K)}
    P["khong"] = P["tha"].copy()
    log = []
    for k in range(1, goc.SO_BUOC + 1):
        if k == goc.BAT_COC:
            x = goc.VI_TRI_BAT_COC.copy()
            lo_trinh, i = goc.DIEM_DEN_2, 0
        v, w, i = goc.dieu_khien(x, lo_trinh, i)
        x = goc.di(x[None], v, w, nhieu=False)[0]
        z = quet(x[None])[0] + rng.normal(0, goc.SIG_LIDAR, goc.SO_TIA)
        r = {"k": k, "x": x.copy(), "bat_coc": k == goc.BAT_COC}
        for ten in ("tha", "khong"):
            Pk = goc.di(P[ten], v, w)
            Pk = Pk[goc.lay_mau_lai(trong_so(Pk, z), goc.K)]
            if ten == "tha":
                n = int(goc.THA * goc.K)
                moi = goc.rai_hat(n)          # video viết Pk[RNG.choice(...)] = rai_hat(n): vế phải chạy trước
                Pk = tha_hat(Pk, rng.choice(goc.K, n, replace=False), moi)
            P[ten] = Pk
            tb = Pk[:, :2].mean(0)
            r[ten] = {"P": Pk.copy(), "tb": tb, "loi": float(np.hypot(*(tb - x[:2]))),
                      "gan": float(np.mean(np.hypot(Pk[:, 0] - x[0], Pk[:, 1] - x[1]) < 0.5))}
        log.append(r)
    return log


def lan_dau(log, ten, tu, nguong=0.8):
    return next((r["k"] for r in log if r["k"] >= tu and r[ten]["gan"] >= nguong), None)


def bai_1(ns):
    f = ham(ns, "quet")
    X = np.array([[1.2, 2.6, 0.0], [3.0, 3.0, 1.0], [9.0, 5.0, -2.0], [5.5, 6.5, 2.5]])
    ra = np.asarray(f(X))
    assert ra.shape == (4, 8), f"4 tư thế × 8 tia: phải ra mảng (4, 8), bạn ra {ra.shape}"
    assert gan(ra, goc.quet(X)), f"khoảng cách tia chưa khớp đáp án; tư thế đầu phải ra {np.round(goc.quet(X)[0], 2)}"
    return f"robot ở (1.2, 2.6) nhìn thấy tường ở {', '.join(f'{d:.2f}' for d in ra[0])} m"


def bai_2(ns):
    f = ham(ns, "trong_so")
    P = goc.LOG[0]["tha"]["P"][:300]
    z = goc.quet(goc.LOG[0]["x"][None])[0]
    w = np.asarray(f(P, z))
    assert gan(w.sum(), 1.0), "trọng số phải có tổng = 1"
    assert gan(w, goc.trong_so(P, z)), "trọng số chưa khớp đáp án (tích 8 tia, mô hình Gauss trộn đều, dùng log)"
    Pt = P.copy(); Pt[0, :2] = [6.05, 3.0]          # đặt một hạt vào giữa tường giữa
    assert np.asarray(f(Pt, z))[0] == 0, "hạt nằm trong tường phải có trọng số 0 (Eq. 13.2)"
    return "hạt trong tường bị loại; hạt có 8 tia dự đoán khớp số đo thì nặng"


def bai_3(ns):
    f = ham(ns, "tha_hat")
    P = np.zeros((5, 3)); moi = np.ones((2, 3))
    Q = np.asarray(f(P, np.array([1, 3]), moi))
    assert gan(Q[[1, 3]], moi) and gan(Q[[0, 2, 4]], np.zeros((3, 3))) and gan(P, np.zeros((5, 3))), "phải thay đúng hạt 1, 3 và không sửa mảng gốc"
    log = chay_lai(ham(ns, "quet"), ham(ns, "trong_so"), f)
    for a, b in zip(log, goc.LOG):
        assert gan(a["tha"]["tb"], b["tha"]["tb"]) and gan(a["khong"]["tb"], b["khong"]["tb"]), f"bước {b['k']}: đám hạt chưa khớp video"
    return (f"bị bắt cóc ở bước {goc.BAT_COC}: có thả 3% hạt ngẫu nhiên thì tìm lại ở bước {lan_dau(log, 'tha', goc.BAT_COC)}, "
            f"không thả thì {lan_dau(log, 'khong', goc.BAT_COC) or 'không bao giờ'} (lạc mãi), như video")


BAI = [("Bài 1 · dò tia LiDAR", bai_1), ("Bài 2 · trọng số theo bản đồ", bai_2), ("Bài 3 · thả hạt chống bắt cóc", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "mcl_cua_ban", loi_giai)
