"""Tập 1.1 - Vì sao xe không đi ngang được? (series Tự Học Robot Tự Hành)

Bài toán: dời robot sang ngang 0.6 m, giữ nguyên hướng nhìn về phía trước.
So sánh 3 loại robot (Chương 1, Principles of Robot Autonomy):
  - Robot đa hướng (omni): đi ngang được ngay  -> holonomic
  - Xe 2 bánh (unicycle): quay 90°, chạy, quay lại
  - Ô tô (bicycle model, Eq. 1.29): góc lái φ bị giới hạn -> phải lùi theo 2 cung tròn (đỗ xe song song)
Chạy: python khong_di_ngang.py
"""
import math

dt = 0.01
SANG_NGANG = 0.6  # mét

# ── 3 mô hình ───────────────────────────────────────────────────────────────


def step_omni(x, y, theta, vx, vy, omega):
    """Robot đa hướng: chạy theo mọi phương, không bị ràng buộc."""
    return x + vx * dt, y + vy * dt, theta + omega * dt


def step_unicycle(x, y, theta, v, omega):
    """Xe 2 bánh (tập 0.2): chỉ tiến/lùi theo hướng đang nhìn."""
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


L = 0.30  # chiều dài cơ sở ô tô (trục trước - trục sau), mét
PHI_MAX = math.radians(30)  # góc lái tối đa
R_MIN = L / math.tan(PHI_MAX)  # bán kính quay nhỏ nhất (suy ra từ θ̇ = v·tanφ/L)


def step_car(x, y, theta, v, phi):
    """Ô tô (bicycle model), toạ độ đặt ở giữa trục sau, phi = góc lái bánh trước."""
    phi = max(-PHI_MAX, min(PHI_MAX, phi))
    return (
        x + v * math.cos(theta) * dt,
        y + v * math.sin(theta) * dt,
        theta + v * math.tan(phi) / L * dt,
    )


# ── 3 cách giải bài "sang ngang 0.6 m" ──────────────────────────────────────


def chay(step, lenh):
    """lenh: danh sách (số giây, tham số cho step). Trả về [(x, y, theta, tham_so...)]."""
    x, y, th = 0.0, 0.0, 0.0
    path = [(x, y, th, *lenh[0][1])]
    for giay, u in lenh:
        for _ in range(round(giay / dt)):
            x, y, th = step(x, y, th, *u)
            path.append((x, y, th, *u))
    return path


omni = chay(step_omni, [(2.0, (0.0, SANG_NGANG / 2.0, 0.0))])

unicycle = chay(
    step_unicycle,
    [
        (1.0, (0.0, math.pi / 2)),  # quay trái 90° tại chỗ
        (1.2, (SANG_NGANG / 1.2, 0.0)),  # chạy 0.6 m
        (1.0, (0.0, -math.pi / 2)),  # quay phải 90° về hướng cũ
    ],
)

# Đỗ xe song song: lùi 2 cung tròn ngược chiều, mỗi cung quay một góc goc_cung.
# Dời ngang = 2·R·(1 - cos goc_cung)  ->  goc_cung = acos(1 - d / 2R)
goc_cung = math.acos(1 - SANG_NGANG / (2 * R_MIN))
V = 0.25
t_cung = goc_cung * R_MIN / V
o_to = chay(
    step_car,
    [
        (t_cung, (-V, PHI_MAX)),  # lùi, đánh lái hết sang trái
        (t_cung, (-V, -PHI_MAX)),  # lùi, đánh lái hết sang phải
    ],
)


def van_toc_ngang(path):
    """Vận tốc theo phương ngang thân xe: ẋ·sinθ - ẏ·cosθ (bằng 0 nếu không trượt ngang)."""
    lon_nhat = 0.0
    for a, b in zip(path, path[1:]):
        vx, vy = (b[0] - a[0]) / dt, (b[1] - a[1]) / dt
        lon_nhat = max(lon_nhat, abs(vx * math.sin(a[2]) - vy * math.cos(a[2])))
    return lon_nhat


if __name__ == "__main__":
    print(f"Ô tô: L = {L} m, góc lái tối đa 30°, bán kính quay nhỏ nhất R = {R_MIN:.2f} m")
    print(f"Đỗ xe song song: 2 cung, mỗi cung {math.degrees(goc_cung):.0f}°\n")
    for ten, p in [("Đa hướng", omni), ("Xe 2 bánh", unicycle), ("Ô tô", o_to)]:
        x, y, th = p[-1][:3]
        print(
            f"{ten:9s} -> x={x:+.2f} m, y={y:+.2f} m, θ={math.degrees(th):+.0f}° | "
            f"vận tốc ngang lớn nhất = {van_toc_ngang(p):.2f} m/s"
        )
