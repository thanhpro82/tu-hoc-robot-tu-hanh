"""Tập 1.3 - PID: robot tự sửa sai (series Tự Học Robot Tự Hành)

Chương 3, Principles of Robot Autonomy: closed-loop control.
Bài toán: robot chạy theo vạch thẳng y = 0, xuất phát lệch 0.3 m,
bánh xe yếu một bên (luôn bị kéo lệch). Bộ điều khiển chọn ω từ sai số
e = r - y (mục tiêu trừ giá trị đo, đúng ký hiệu Eq. 3.3 của giáo trình, ở đây r = 0):

    ω = Kp·e + Ki·∫e dt + Kd·de/dt

So sánh: vòng hở, chỉ P, PD, PID.
Chạy: python pid.py
"""
import math
import random

dt = 0.01
V = 0.5  # tốc độ tiến, m/s
GIAY = 16.0
Y0 = 0.3  # xuất phát lệch 30 cm

# Robot "thật": quay chỉ được 96% lệnh, bánh yếu kéo lệch 0.15 rad/s, có nhiễu
W_TY_LE = 0.96
W_LECH = -0.15
NHIEU = 0.03


def step(x, y, theta, v, omega):
    """Xe 2 bánh, giữ nguyên từ tập 0.2."""
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.tich_phan = 0.0
        self.e_truoc = None

    def lenh(self, e):
        self.tich_phan += e * dt
        dao_ham = 0.0 if self.e_truoc is None else (e - self.e_truoc) / dt
        self.e_truoc = e
        return self.kp * e + self.ki * self.tich_phan + self.kd * dao_ham


def chay(pid=None, seed=1):
    """pid=None: vòng hở (lệnh ω = 0, cứ chạy thẳng)."""
    rng = random.Random(seed)
    x, y, th = 0.0, Y0, 0.0
    path = [(x, y, th)]
    for _ in range(round(GIAY / dt)):
        e = 0.0 - y  # sai số = mục tiêu (vạch y = 0) - vị trí đo được
        w_lenh = pid.lenh(e) if pid else 0.0
        w_lenh = max(-2.0, min(2.0, w_lenh))  # giới hạn tốc độ quay của động cơ
        w_thuc = w_lenh * W_TY_LE + W_LECH + rng.gauss(0, NHIEU)
        x, y, th = step(x, y, th, V, w_thuc)
        path.append((x, y, th))
    return path


KET_QUA = {
    "vong_ho": chay(None),
    "P": chay(PID(kp=1.5, ki=0.0, kd=0.0)),
    "PD": chay(PID(kp=1.5, ki=0.0, kd=2.8)),
    "PID": chay(PID(kp=1.5, ki=0.6, kd=2.8)),
}


def lech_cuoi(path, giay=3.0):
    """Sai số trung bình trong `giay` giây cuối (cm)."""
    n = round(giay / dt)
    return sum(p[1] for p in path[-n:]) / n * 100


if __name__ == "__main__":
    for ten, p in KET_QUA.items():
        ys = [q[1] for q in p]
        print(f"{ten:7s} -> lệch cuối {lech_cuoi(p):+6.1f} cm | y nhỏ nhất {min(ys) * 100:+6.1f} cm | x cuối {p[-1][0]:.1f} m")
