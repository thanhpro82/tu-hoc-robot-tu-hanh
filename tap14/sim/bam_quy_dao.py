"""Tập 1.4 - Bám quỹ đạo: robot vẽ số 8 gần như hoàn hảo (series Tự Học Robot Tự Hành)

Theo đúng Ví dụ 3.1.2, Chương 3, Principles of Robot Autonomy:
  - Unicycle mở rộng (dynamic extension): trạng thái (x, y, v, θ), lệnh (a, ω).
  - x, y là "đầu ra phẳng" (differential flatness): v, θ, a, ω đều suy ra được từ x(t), y(t).
  - Điều khiển ảo (Eq. 3.7):  w1 = ẍ_d + kp·(x_d - x) + kd·(ẋ_d - ẋ)   (tương tự w2 cho y)
  - Đổi về lệnh thật:         [a, ω] = J⁻¹(θ, v)·[w1, w2],   J = [[cosθ, -v·sinθ], [sinθ, v·cosθ]]
Phần ẍ_d, ÿ_d là tính sẵn (feedforward), phần kp, kd là sửa sai (feedback).
Chạy: python bam_quy_dao.py
"""
import math
import random

dt = 0.01
A = 1.0  # nửa chiều rộng hình số 8, mét
T = 20.0  # thời gian vẽ trọn hình số 8, giây
W = 2 * math.pi / T
KP, KD = 4.0, 4.0  # kd = 2·√kp: tắt dần tới hạn


def tham_chieu(t):
    """Hình số 8 (lemniscate Gerono) của robot ảo: vị trí, vận tốc, gia tốc tại thời điểm t."""
    x, y = A * math.sin(W * t), A * math.sin(2 * W * t) / 2
    dx, dy = A * W * math.cos(W * t), A * W * math.cos(2 * W * t)
    ddx, ddy = -A * W**2 * math.sin(W * t), -2 * A * W**2 * math.sin(2 * W * t)
    return x, y, dx, dy, ddx, ddy


def tinh_san(dx, dy, ddx, ddy):
    """Phẳng vi phân: từ đạo hàm của x, y suy ra v, θ, a, ω (không cần giải phương trình vi phân)."""
    v = math.hypot(dx, dy)
    return v, math.atan2(dy, dx), (dx * ddx + dy * ddy) / v, (dx * ddy - dy * ddx) / v**2


def robot_that(a, omega, rng):
    """Robot "thật": bánh phải yếu (giống tập 0.2) + nhiễu."""
    return a + rng.gauss(0, 0.05), omega * 0.95 - 0.06 + rng.gauss(0, 0.1)


def chay(bam=True, seed=4):
    rng = random.Random(seed)
    x, y, dx, dy, _, _ = tham_chieu(0)
    v, th, _, _ = tinh_san(dx, dy, 0, 0)
    y -= 0.2  # xuất phát lệch 20 cm
    path, sai_so = [], []
    for i in range(round(T / dt) + 1):
        xd, yd, dxd, dyd, ddxd, ddyd = tham_chieu(i * dt)
        if bam:
            w1 = ddxd + KP * (xd - x) + KD * (dxd - v * math.cos(th))
            w2 = ddyd + KP * (yd - y) + KD * (dyd - v * math.sin(th))
            a = math.cos(th) * w1 + math.sin(th) * w2  # J⁻¹ hàng 1
            omega = (-math.sin(th) * w1 + math.cos(th) * w2) / v  # J⁻¹ hàng 2
        else:
            _, _, a, omega = tinh_san(dxd, dyd, ddxd, ddyd)  # chỉ phần tính sẵn
        path.append((x, y, th))
        sai_so.append(math.hypot(xd - x, yd - y))
        a, omega = robot_that(a, omega, rng)
        x, y = x + v * math.cos(th) * dt, y + v * math.sin(th) * dt
        th, v = th + omega * dt, max(0.05, v + a * dt)
    return path, sai_so


def _ref_pose(t):
    x, y, dx, dy, _, _ = tham_chieu(t)
    return x, y, math.atan2(dy, dx)


THAM_CHIEU = [_ref_pose(i * dt) for i in range(round(T / dt) + 1)]
TINH_SAN, SS_TINH_SAN = chay(bam=False)
BAM, SS_BAM = chay(bam=True)

if __name__ == "__main__":
    vs = [tinh_san(*tham_chieu(i * dt)[2:])[0] for i in range(round(T / dt))]
    print(f"Số 8 rộng {2 * A} m, {T:.0f} s, tốc độ robot ảo {min(vs):.2f}–{max(vs):.2f} m/s, kp = {KP}, kd = {KD}")
    for ten, ss in [("Chỉ tính sẵn", SS_TINH_SAN), ("Tính sẵn + sửa sai", SS_BAM)]:
        n5 = round(5 / dt)
        print(f"{ten:18s}: sai số đầu {ss[0] * 100:.0f} cm, lớn nhất {max(ss) * 100:.0f} cm, "
              f"trung bình 5 s cuối {sum(ss[-n5:]) / n5 * 100:.1f} cm")
