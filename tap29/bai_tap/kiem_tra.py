"""Tự chấm bài tập tập 2.9. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 1 chấm nhanh. Bài 2–3 nạp lần chạy của video (../sim/di_theo.py: YOLO tập 2.8 + 320 bước, khoảng 30–60 giây lần đầu)
rồi phát lại từng bước bằng code của bạn: nếu cả 320 bước ra đúng lệnh và trạng thái thì robot đi y hệt video.
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

_GOC = {}


def goc():
    if not _GOC:
        print("   (đang chạy lại mô phỏng của video: YOLO + 320 bước...)", flush=True)
        import di_theo
        _GOC["m"] = di_theo
    return _GOC["m"]


def bai_1(ns):
    f = ham(ns, "uoc_luong")
    z, h = f((0, 0.9, 0.5, 0.5, 0.1, 0.3))
    assert gan(z, 1.7 * 60 / (0.3 * 128)) and gan(h, 0.0), f"người giữa ảnh, khung cao 0.3·128 px: Z = 1.7·60/38.4 ≈ 2.66 m, hướng 0; bạn ra {z, h}"
    rng = random.Random(1)
    for _ in range(100):
        d = (rng.choice([0, 2]), rng.random(), rng.uniform(0.1, 0.9), rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.6))
        assert gan(f(d), _lg.uoc_luong(d)), f"khung {tuple(round(v, 3) for v in d)}: phải ra {_lg.uoc_luong(d)}, bạn ra {f(d)}"
    return f"người cao 38 px giữa ảnh → cách {z:.2f} m; bóng dùng bề rộng; lệch phải thì hướng dương"


def bai_2(ns):
    f = ham(ns, "lenh")
    v, w, tp = f(3.0, 0.2, 0.0)
    assert gan((v, w, tp), (min(1.2, 0.8 * 1 + 0.15 * 0.1), -0.32, 0.1)), f"Z = 3 m, hướng 0.2 rad: phải ra v = 0.815, ω = −0.32, tích phân 0.1; bạn ra {v, w, tp}"
    assert f(1.0, 0.0, 0.0)[0] == 0, "đang gần hơn 2 m thì v phải bị kẹp về 0 (không lùi)"
    g = goc()
    tp = 0.0
    so = 0
    for r in g.LOG:
        if r["trang_thai"] == "theo":
            v, w, tp = f(r["z_hat"], math.atan((max((d for d in r["dets"] if d[0] == 0), key=lambda d: d[1])[2] - 0.5) * 128 / 60), tp)
            assert gan((v, w), (r["v"], r["w"]), 1e-9), f"bước t = {r['t']} s: video ra v = {r['v']:.3f}, ω = {r['w']:.3f}; bạn ra {v:.3f}, {w:.3f}"
            so += 1
    return f"phát lại {so} bước 'theo' của video: lệnh v, ω của bạn khớp từng bước"


def bai_3(ns):
    f = ham(ns, "quyet_dinh")
    assert f([]) == "tìm", "không thấy gì thì 'tìm'"
    assert f([(0, 0.9, 0.5, 0.5, 0.1, 0.3)]) == "theo", "chỉ thấy người thì 'theo'"
    bong_gan = (2, 0.8, 0.5, 0.7, 0.1, 0.1)      # bóng rộng 12.8 px → cách 1.17 m, ngay phía trước
    assert f([(0, 0.9, 0.5, 0.5, 0.1, 0.3), bong_gan]) == "dừng", "bóng gần ngay phía trước thì 'dừng' dù vẫn thấy người"
    g = goc()
    sai = [r["t"] for r in g.LOG if f(r["dets"]) != r["trang_thai"]]
    assert not sai, f"{len(sai)} bước chọn trạng thái khác video, ví dụ t = {sai[:5]}"
    dem = {s: sum(r["trang_thai"] == s for r in g.LOG) for s in ("theo", "dừng", "tìm")}
    return f"cả {len(g.LOG)} bước khớp video: {dem} → robot dừng 3.9 s khi bóng lăn qua rồi đi theo tiếp"


BAI = [("Bài 1 · khoảng cách và hướng từ khung", bai_1), ("Bài 2 · lệnh đi theo (PI)", bai_2), ("Bài 3 · chọn trạng thái", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "di_theo_cua_ban", _lg)
