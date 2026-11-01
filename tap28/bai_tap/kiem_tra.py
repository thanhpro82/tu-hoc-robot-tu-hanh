"""Tự chấm bài tập tập 2.8. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 1–2 chấm trên dữ liệu thử nhỏ. Bài 3 nạp mạng YOLO đã học của video (../sim/yolo.py, trong_so.pt) và tạo lại
đúng 500 ảnh thử (khoảng 20–60 giây lần đầu), rồi tính mAP bằng code của bạn.
"""
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

_GOC = {}


def goc():
    """Nạp ../sim/yolo.py một lần (mạng đã học + 500 ảnh thử + khung thô THO)."""
    if not _GOC:
        print("   (đang nạp YOLO của video và tạo lại 500 ảnh thử...)", flush=True)
        import yolo
        _GOC["m"] = yolo
    return _GOC["m"]


def _ngau_nhien(rng, n):
    return [(rng.randrange(3), round(rng.random(), 3), rng.uniform(0.2, 0.8), rng.uniform(0.2, 0.8),
             rng.uniform(0.05, 0.3), rng.uniform(0.05, 0.3)) for _ in range(n)]


def bai_1(ns):
    f = ham(ns, "iou")
    assert gan(f((0.5, 0.5, 0.2, 0.2), (0.5, 0.5, 0.2, 0.2)), 1.0), "hai khung trùng nhau phải có IoU = 1"
    assert gan(f((0.2, 0.2, 0.1, 0.1), (0.8, 0.8, 0.1, 0.1)), 0.0), "hai khung rời nhau phải có IoU = 0"
    assert gan(f((0.5, 0.5, 0.2, 0.2), (0.6, 0.5, 0.2, 0.2)), 0.02 / 0.06, 1e-6), "lệch nửa khung: giao 0.02, hợp 0.06 → IoU = 1/3"
    rng = random.Random(1)
    for _ in range(200):
        a, b = _ngau_nhien(rng, 2)
        assert gan(f(a[2:], b[2:]), _lg.iou(a[2:], b[2:]), 1e-6), f"IoU của {a[2:]} và {b[2:]} chưa đúng"
    return "IoU đúng: trùng = 1, rời = 0, lệch nửa khung = 1/3"


def bai_2(ns):
    f = ham(ns, "nms")
    ds = [(0, 0.9, 0.5, 0.5, 0.2, 0.2), (0, 0.8, 0.52, 0.5, 0.2, 0.2), (1, 0.7, 0.52, 0.5, 0.2, 0.2), (0, 0.6, 0.1, 0.1, 0.1, 0.1)]
    assert f(ds) == [ds[0], ds[2], ds[3]], f"ví dụ 4 khung: phải bỏ khung thứ 2 (cùng lớp, chồng khung điểm cao hơn), giữ khung khác lớp; bạn ra {f(ds)}"
    rng = random.Random(2)
    for _ in range(50):
        ds = _ngau_nhien(rng, 25)
        assert f(ds) == _lg.nms(ds), "NMS trên 25 khung ngẫu nhiên chưa khớp đáp án"
    return "giữ khung điểm cao nhất, bỏ khung cùng lớp chồng lên ≥ 50%, không đụng khung khác lớp"


def bai_3(ns):
    f, nms = ham(ns, "ap_lop"), ham(ns, "nms")
    du = [[(0, 0.9, 0.5, 0.5, 0.2, 0.2), (0, 0.5, 0.1, 0.1, 0.1, 0.1)], [(0, 0.8, 0.3, 0.3, 0.2, 0.2)]]
    that = [[(0, 0.5, 0.5, 0.2, 0.2)], [(0, 0.7, 0.7, 0.2, 0.2)]]
    ap, rec, pre = f(du, that, 0)
    assert gan(ap, 0.5) and gan(rec, [0.5, 0.5, 0.5]) and gan(pre, [1.0, 0.5, 1 / 3]), \
        f"ví dụ 2 ảnh: AP phải 0.5, recall [0.5, 0.5, 0.5], precision [1, 0.5, 0.333]; bạn ra {ap}, {list(rec)}, {list(pre)}"
    g = goc()
    tho = [[tuple(d) for d in dd] for dd in g.THO]
    sach = [nms(d) for d in tho]
    ap_c = [f(sach, g.V_THU, c)[0] for c in range(3)]
    map_ = sum(ap_c) / 3
    map_tho = sum(f(tho, g.V_THU, c)[0] for c in range(3)) / 3
    assert abs(map_ - g.MAP) < 1e-6, f"mAP sau NMS phải = {g.MAP * 100:.1f}% như video, bạn ra {map_ * 100:.1f}%"
    return (f"AP người {ap_c[0] * 100:.1f}% · hộp {ap_c[1] * 100:.1f}% · bóng {ap_c[2] * 100:.1f}% → mAP {map_ * 100:.1f}% "
            f"(không NMS: {map_tho * 100:.1f}%) như video; {sum(map(len, tho))} khung thô → {sum(map(len, sach))} sau NMS")


BAI = [("Bài 1 · IoU", bai_1), ("Bài 2 · NMS", bai_2), ("Bài 3 · AP và mAP", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "yolo_cua_ban", _lg)
