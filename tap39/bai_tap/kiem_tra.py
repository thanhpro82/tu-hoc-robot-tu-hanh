"""Tự chấm bài tập tập 3.9. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Dữ liệu là lần chạy Nav2 THẬT trong ROS 2 (../ws/out/), đọc bằng ../sim/phan_tich.py; không cần cài ROS.
"""
import math
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import phan_tich as goc  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def sai_so_amcl(that_luc):
    return np.array([math.hypot(*(goc.AM[k, :2] - that_luc(goc.TR, goc.THAT, goc.TA[k])[:2])) for k in range(len(goc.TA))])


def bai_1(ns):
    f = ham(ns, "that_luc")
    TR = np.array([0.0, 1.0, 2.0]); TH = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]], dtype=float)
    assert gan(f(TR, TH, 0.4), [1, 0, 0]) and gan(f(TR, TH, 9.0), [2, 0, 0]) and gan(f(TR, TH, -3.0), [0, 0, 0]), \
        "ví dụ: TR = [0, 1, 2], t = 0.4 → hàng 1 (searchsorted), t = 9 → hàng cuối, t = −3 → hàng đầu"
    e = sai_so_amcl(f)
    assert gan(e, goc.E_AMCL), "sai số AMCL tính bằng hàm của bạn chưa khớp video"
    k = int(np.argmax(e < 0.10))
    return (f"AMCL: lúc đầu lệch {e[0] * 100:.1f} cm (do bấm ước lượng lệch 43 cm), dưới 10 cm sau {goc.TA[k]:.1f} s, "
            f"sau đó trung bình {e[k:].mean() * 100:.1f} cm như video")


def bai_2(ns):
    qc, dd = ham(ns, "qua_cua"), ham(ns, "do_dai")
    assert gan(dd(np.array([[0, 0], [3, 4], [3, 6]])), 7.0), "đường (0,0)→(3,4)→(3,6) dài 5 + 2 = 7"
    qua = [qc(np.array(p["xy"]), goc.CUA) for p in goc.PLAN]
    assert qua == goc.QUA_DUOI, "nhận biết đường có qua cửa dưới chưa khớp video"
    k = qua.index(False)
    return (f"đường đầu tiên dài {dd(np.array(goc.PLAN[0]['xy'])):.2f} m qua cửa dưới; t = {goc.TP[k]:.1f} s Nav2 phát hiện cửa đóng, "
            f"đổi sang đường {dd(np.array(goc.PLAN[k]['xy'])):.2f} m đi vòng (Nav2 báo {goc.DAI0:.2f} và {goc.DAI_MOI:.2f} m)")


def bai_3(ns):
    f = ham(ns, "do_toa")
    assert gan(f(np.array([[0, 0], [2, 0], [0, 0], [2, 0]])), 1.0), "4 hạt x = 0, 2, 0, 2: phương sai x = 1, y = 0 → độ toả 1"
    s = np.array([f(np.array(h["xy"])) for h in goc.HAT])
    assert gan(s, goc.SPREAD), "độ toả đám hạt chưa khớp video"
    return f"đám hạt AMCL: toả {s[0] * 100:.0f} cm lúc bấm ước lượng → {s[-1] * 100:.0f} cm khi tới bếp ({goc.HAT[0]['n']} → {goc.HAT[-1]['n']} hạt)"


BAI = [("Bài 1 · so AMCL với tư thế thật", bai_1), ("Bài 2 · đường đi và cửa đóng", bai_2), ("Bài 3 · độ toả đám hạt", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "nav_cua_ban", loi_giai)
