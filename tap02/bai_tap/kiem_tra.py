"""Tự chấm bài tập tập 0.2. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import robot_dau_tien as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def _chay(step, v, omega_theo_t, giay):
    """Giống goc.chay nhưng dùng hàm step của bạn."""
    x, y, th = 0.0, 0.0, 0.0
    path = [(x, y, th)]
    for i in range(round(giay / goc.dt)):
        x, y, th = step(x, y, th, v, omega_theo_t(i * goc.dt))
        path.append((x, y, th))
    return path


def bai_1(ns):
    step = ham(ns, "step")
    r = step(1.0, 2.0, 0.0, 0.5, 0.0)
    assert gan(r, (1.005, 2.0, 0.0)), f"mũi xe hướng θ = 0, v = 0.5: sau 0.01 s phải tới (1.005, 2, 0), bạn ra {r}"
    r = step(0.0, 0.0, math.pi / 2, 1.0, 2.0)
    assert gan(r, (0.0, 0.01, math.pi / 2 + 0.02)), f"θ = 90°, v = 1, ω = 2: phải ra (0, 0.01, θ + 0.02), bạn ra {r}"
    p = _chay(step, 0.5, lambda t: 0.0, 6)
    assert gan(p[-1], goc.di_thang[-1]), f"đi thẳng 6 s phải dừng ở x = 3.00 m như video, bạn ra {p[-1]}"
    p = _chay(step, 0.5, lambda t: 1.0, 2 * math.pi)
    x, y, th = p[-1]
    return f"đi thẳng 6 s tới x = 3.00 m; vòng tròn 2π giây quay về ({x:+.2f}, {y:+.2f}), θ = {math.degrees(th):.0f}° như video"


def bai_2(ns):
    w = ham(ns, "omega_so_8")
    assert gan(w(1.0), 1.0) and gan(w(7.0), -1.0), f"ω(1 s) phải = +1 (vòng đầu), ω(7 s) phải = −1 (vòng sau), bạn ra {w(1.0)}, {w(7.0)}"
    p = _chay(goc.step, 0.5, w, 4 * math.pi)
    assert gan(p[-1][:2], goc.so_tam[-1][:2], 1e-3), f"chạy 4π giây phải về gần điểm xuất phát như video, bạn dừng ở ({p[-1][0]:+.2f}, {p[-1][1]:+.2f})"
    lech_trai = max(q[1] for q in p)
    lech_phai = min(q[1] for q in p)
    assert lech_trai > 0.9 and lech_phai < -0.9, "hình số 8 phải có một vòng bên trái (y > 0) và một vòng bên phải (y < 0)"
    return f"số 8: hai vòng cao {lech_trai:.2f} m và {lech_phai:.2f} m, quay về ({p[-1][0]:+.2f}, {p[-1][1]:+.2f})"


def bai_3(ns):
    f = ham(ns, "lenh_vong_tron")
    for R, T in [(1.0, 10.0), (0.5, 4.0)]:
        v, w = f(R, T)
        p = _chay(goc.step, v, lambda t: w, T)
        tam = (0.0, R)  # xuất phát ở gốc, mũi xe hướng trục x, quay trái nên tâm nằm ở (0, R)
        r = [math.dist(q[:2], tam) for q in p]
        # sai số 1 cm: cách cập nhật từng bước (Euler) làm vòng tròn hơi lệch tâm cỡ v·dt/2
        assert math.dist(p[-1][:2], (0.0, 0.0)) < 0.01 and max(r) - min(r) < 0.01 and abs(sum(r) / len(r) - R) < 0.01, \
            f"R = {R} m, T = {T} s: lệnh (v, ω) = ({v:.3f}, {w:.3f}) chưa cho đúng 1 vòng bán kính {R} m"
    v, w = f(1.0, 10.0)
    return f"vòng R = 1 m trong 10 s cần v = {v:.3f} m/s, ω = {w:.3f} rad/s (để ý: v = ω·R)"


BAI = [("Bài 1 · hàm step", bai_1), ("Bài 2 · hình số 8", bai_2), ("Bài 3 · lệnh cho vòng tròn", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "robot_cua_ban", loi_giai)
