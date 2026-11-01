"""Tập 0.2 - Robot đầu tiên trong mô phỏng (series Tự Học Robot Tự Hành).

Mô hình xe 2 bánh (unicycle) theo Chương 1, Principles of Robot Autonomy.
Chỉ cần Python thuần. Có matplotlib thì sẽ vẽ quỹ đạo.
Chạy: python robot_dau_tien.py
"""
import math

dt = 0.01  # mỗi bước 0.01 giây = 100 lần/giây


def step(x, y, theta, v, omega):
    """Trạng thái (x, y, θ), lệnh điều khiển (v, ω) -> trạng thái mới."""
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt
    return x, y, theta


def chay(v, omega_theo_t, giay):
    """Chạy robot trong `giay` giây, ω có thể thay đổi theo thời gian t."""
    x, y, theta = 0.0, 0.0, 0.0
    path = [(x, y, theta)]
    for i in range(round(giay / dt)):
        x, y, theta = step(x, y, theta, v, omega_theo_t(i * dt))
        path.append((x, y, theta))
    return path


# 3 bài thử: đi thẳng, đi vòng tròn, vẽ số 8
di_thang = chay(0.5, lambda t: 0.0, 6)
vong_tron = chay(0.5, lambda t: 1.0, 2 * math.pi)
so_tam = chay(0.5, lambda t: 1.0 if t < 2 * math.pi else -1.0, 4 * math.pi)

if __name__ == "__main__":
    for ten, p in [("Đi thẳng", di_thang), ("Vòng tròn", vong_tron), ("Số 8", so_tam)]:
        x, y, th = p[-1]
        print(f"{ten:10s} -> kết thúc tại x={x:+.2f} m, y={y:+.2f} m, θ={math.degrees(th):+.0f}°")
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        for ax, (ten, p) in zip(axes, [("Đi thẳng", di_thang), ("Vòng tròn", vong_tron), ("Số 8", so_tam)]):
            ax.plot([q[0] for q in p], [q[1] for q in p])
            ax.set_title(ten)
            ax.set_aspect("equal")
            ax.grid(True)
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("(Cài matplotlib để xem hình: pip install matplotlib)")
