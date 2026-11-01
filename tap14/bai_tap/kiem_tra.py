"""Tự chấm bài tập tập 1.4. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import bam_quy_dao as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def chay(tinh_san, dieu_khien_ao=None, doi_lenh=None, seed=4):
    """Giống goc.chay nhưng dùng hàm của bạn. Không có dieu_khien_ao thì chỉ chạy phần tính sẵn."""
    rng = random.Random(seed)
    x, y, dx, dy, _, _ = goc.tham_chieu(0)
    v, th, _, _ = tinh_san(dx, dy, 0, 0)
    y -= 0.2
    path, sai_so = [], []
    for i in range(round(goc.T / goc.dt) + 1):
        xd, yd, dxd, dyd, ddxd, ddyd = goc.tham_chieu(i * goc.dt)
        if dieu_khien_ao:
            w1, w2 = dieu_khien_ao(xd, yd, dxd, dyd, ddxd, ddyd, x, y, v, th, goc.KP, goc.KD)
            a, omega = doi_lenh(w1, w2, th, v)
        else:
            _, _, a, omega = tinh_san(dxd, dyd, ddxd, ddyd)
        path.append((x, y, th))
        sai_so.append(math.hypot(xd - x, yd - y))
        a, omega = goc.robot_that(a, omega, rng)
        x, y = x + v * math.cos(th) * goc.dt, y + v * math.sin(th) * goc.dt
        th, v = th + omega * goc.dt, max(0.05, v + a * goc.dt)
    return path, sai_so


def _tb5(ss):
    n = round(5 / goc.dt)
    return sum(ss[-n:]) / n * 100


def bai_1(ns):
    f = ham(ns, "tinh_san")
    rng = random.Random(1)
    for _ in range(20):
        a = [rng.uniform(-1, 1) for _ in range(4)]
        assert gan(f(*a), goc.tinh_san(*a)), f"tinh_san{tuple(round(v, 3) for v in a)} ra {f(*a)}, đáp án {goc.tinh_san(*a)}"
    _, ss = chay(f)
    assert abs(_tb5(ss) - _tb5(goc.SS_TINH_SAN)) < 0.1, f"chỉ tính sẵn: sai số 5 s cuối {_tb5(ss):.1f} cm, video {_tb5(goc.SS_TINH_SAN):.1f} cm"
    return f"chỉ tính sẵn (vòng hở): robot vẽ lệch, sai số 5 s cuối {_tb5(ss):.1f} cm như video"


def bai_2(ns):
    f = ham(ns, "dieu_khien_ao")
    r = f(1, 2, 0.5, 0.0, 0.1, 0.2, 0.9, 2.1, 0.5, 0.0, 4.0, 4.0)
    assert gan(r, (0.1 + 0.4, 0.2 - 0.4)), f"thử 1: w1 = 0.1 + 4·0.1 + 4·0 = 0.5, w2 = 0.2 + 4·(−0.1) + 4·0 = −0.2, bạn ra {r}"
    r = f(0, 0, 0, 0, 0, 0, 0, 0, 1.0, math.pi / 2, 1.0, 2.0)
    assert gan(r, (0.0, -2.0)), f"thử 2: robot chạy lên trên (θ = 90°) với v = 1 mà robot ảo đứng yên: phải ra (0, −2), bạn ra {r}"
    return "w1, w2 đúng: phần ẍ_d, ÿ_d tính sẵn + phần kp, kd sửa sai"


def bai_3(ns):
    f = ham(ns, "doi_lenh")
    rng = random.Random(2)
    for _ in range(20):
        a, w, th, v = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-3, 3), rng.uniform(0.1, 1)
        w1 = math.cos(th) * a - v * math.sin(th) * w      # J·[a, ω]
        w2 = math.sin(th) * a + v * math.cos(th) * w
        assert gan(f(w1, w2, th, v), (a, w)), f"doi_lenh phải giải ngược J: với θ = {th:.2f}, v = {v:.2f} cần ra ({a:.3f}, {w:.3f}), bạn ra {f(w1, w2, th, v)}"
    _, ss = chay(ham(ns, "tinh_san"), ham(ns, "dieu_khien_ao"), f)
    assert abs(_tb5(ss) - _tb5(goc.SS_BAM)) < 0.05, f"bám quỹ đạo: sai số 5 s cuối {_tb5(ss):.2f} cm, video {_tb5(goc.SS_BAM):.1f} cm"
    return f"tính sẵn + sửa sai: sai số giảm từ 20 cm còn {_tb5(ss):.1f} cm trong 5 s cuối như video"


BAI = [("Bài 1 · phẳng vi phân", bai_1), ("Bài 2 · điều khiển ảo", bai_2), ("Bài 3 · đổi về lệnh thật", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "bam_cua_ban", loi_giai)
