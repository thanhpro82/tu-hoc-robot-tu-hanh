"""Tự chấm bài tập tập 1.1. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import khong_di_ngang as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def do_xe(R, alpha, L, phi_max, V=0.25):
    """Lùi 2 cung theo kế hoạch (R, alpha) với một chiếc xe dài L, lái tối đa phi_max; trả về đường đi."""
    def step(x, y, th, v, phi):
        return x + v * math.cos(th) * goc.dt, y + v * math.sin(th) * goc.dt, th + v * math.tan(phi) / L * goc.dt
    t = alpha * R / V
    return goc.chay(step, [(t, (-V, phi_max)), (t, (-V, -phi_max))])


def bai_1(ns):
    f = ham(ns, "step_car")
    rng = random.Random(7)
    for _ in range(20):
        a = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-3, 3), rng.uniform(-0.5, 0.5), rng.uniform(-0.4, 0.4))
        assert gan(f(*a), goc.step_car(*a)), f"step_car{tuple(round(v, 3) for v in a)} ra {f(*a)}, đáp án {goc.step_car(*a)}"
    a = (0.0, 0.0, 0.0, 0.5, math.radians(60))
    assert gan(f(*a), goc.step_car(*a)), "đánh lái 60° phải bị kẹp về 30° (PHI_MAX), bạn chưa kẹp góc lái"
    p = goc.chay(f, [(goc.t_cung, (-goc.V, goc.PHI_MAX)), (goc.t_cung, (-goc.V, -goc.PHI_MAX))])
    x, y, th = p[-1][:3]
    return f"đỗ xe song song bằng mô hình của bạn: dừng ở x = {x:+.2f} m, y = {y:+.2f} m, θ = {math.degrees(th):+.0f}° như video"


def bai_2(ns):
    f = ham(ns, "van_toc_ngang")
    ra = {ten: f(p) for ten, p in [("đa hướng", goc.omni), ("xe 2 bánh", goc.unicycle), ("ô tô", goc.o_to)]}
    assert gan(ra["đa hướng"], 0.30, 1e-6), f"robot đa hướng đi ngang 0.6 m trong 2 s, vận tốc ngang phải = 0.30 m/s, bạn ra {ra['đa hướng']}"
    assert ra["xe 2 bánh"] < 1e-6 and ra["ô tô"] < 1e-6, f"xe 2 bánh và ô tô không trượt ngang, phải ra 0, bạn ra {ra['xe 2 bánh']}, {ra['ô tô']}"
    assert gan(f([(0, 0, 0), (0.0, 0.002, 0)]), 0.2), "điểm (0,0,θ=0) tới (0,0.002) trong 0.01 s: vận tốc ngang phải = 0.2 m/s"
    return "đa hướng 0.30 m/s · xe 2 bánh 0.00 · ô tô 0.00: hai xe sau không bao giờ trượt ngang (ràng buộc nonholonomic)"


def bai_3(ns):
    f = ham(ns, "ke_hoach_do_xe")
    R, alpha = f(goc.SANG_NGANG, goc.L, goc.PHI_MAX)
    assert gan(R, goc.R_MIN), f"R phải = L/tan(30°) = {goc.R_MIN:.3f} m, bạn ra {R}"
    assert gan(alpha, goc.goc_cung), f"góc mỗi cung phải = {math.degrees(goc.goc_cung):.1f}°, bạn ra {math.degrees(alpha):.1f}°"
    R2, a2 = f(0.3, 0.5, math.radians(25))
    y = do_xe(R2, a2, 0.5, math.radians(25))[-1][1]
    assert abs(y - 0.3) < 0.01, f"xe dài 0.5 m, lái tối đa 25°, muốn dời 0.3 m: kế hoạch của bạn chỉ dời {y:.3f} m"
    return f"R = {R:.2f} m, mỗi cung {math.degrees(alpha):.0f}° như video; thử xe khác cũng dời đúng {y:.2f} m"


BAI = [("Bài 1 · mô hình ô tô", bai_1), ("Bài 2 · vận tốc ngang", bai_2), ("Bài 3 · kế hoạch đỗ xe", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "xe_cua_ban", loi_giai)
