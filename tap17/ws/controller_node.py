"""Tập 1.7 - Node điều khiển: bám quỹ đạo theo Ví dụ 3.1.2 (tập 1.4) trên đường A* đã làm mượt.

  nghe /path (nav_msgs/Path) và /pose (geometry_msgs/Pose2D) -> phát /cmd_vel (Twist), 50 lần/giây
  1. Gắn thời gian cho đường: chạy theo độ dài cung, tốc độ tối đa V_REF, tăng/giảm tốc A_REF
  2. Phẳng vi phân + PD trên x, y: w = ẍ_d + kp(x_d - x) + kd(ẋ_d - ẋ), rồi [a, ω] = J⁻¹ w
  3. Ghi log CSV để làm video, in tổng kết khi tới đích
"""
import bisect
import csv
import math

import rclpy
from geometry_msgs.msg import Pose2D, Twist
from nav_msgs.msg import Path
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile

DT = 0.02
V_REF, A_REF = 0.3, 0.3
KP, KD = 4.0, 4.0
LOG = "/ws/log.csv"


class ControllerNode(Node):
    def __init__(self):
        super().__init__("controller")
        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.create_subscription(Path, "/path", self.on_path, qos)
        self.create_subscription(Pose2D, "/pose", self.on_pose, 10)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.pts = self.pose = None
        self.t = 0.0
        self.v = 0.0
        self.log = []
        self.create_timer(DT, self.tick)

    def on_path(self, msg):
        self.pts = [(p.pose.position.x, p.pose.position.y) for p in msg.poses]
        self.s = [0.0]
        for a, b in zip(self.pts, self.pts[1:]):
            self.s.append(self.s[-1] + math.dist(a, b))
        L = self.s[-1]
        t_tang = V_REF / A_REF
        self.T = L / V_REF + t_tang  # hình thang vận tốc (tập 1.2)
        self.get_logger().info(f"Nhận đường dài {L:.2f} m, dự kiến chạy {self.T:.1f} s")

    def on_pose(self, msg):
        self.pose = (msg.x, msg.y, msg.theta)

    def s_tai(self, t):
        """Quãng đường cần đi được tại thời điểm t (vận tốc hình thang)."""
        L, t_tang = self.s[-1], V_REF / A_REF
        t = max(0.0, min(t, self.T))
        if t < t_tang:
            return 0.5 * A_REF * t * t
        if t > self.T - t_tang:
            r = self.T - t
            return L - 0.5 * A_REF * r * r
        return 0.5 * A_REF * t_tang**2 + V_REF * (t - t_tang)

    def diem(self, s):
        i = min(len(self.pts) - 2, max(0, bisect.bisect_right(self.s, s) - 1))
        k = (s - self.s[i]) / max(1e-9, self.s[i + 1] - self.s[i])
        a, b = self.pts[i], self.pts[i + 1]
        return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k

    def ref(self, t, h=0.05):
        """Vị trí, vận tốc, gia tốc của robot ảo (sai phân trung tâm)."""
        p0, p1, p2 = self.diem(self.s_tai(t - h)), self.diem(self.s_tai(t)), self.diem(self.s_tai(t + h))
        v = ((p2[0] - p0[0]) / (2 * h), (p2[1] - p0[1]) / (2 * h))
        a = ((p2[0] - 2 * p1[0] + p0[0]) / h**2, (p2[1] - 2 * p1[1] + p0[1]) / h**2)
        return p1, v, a

    def tick(self):
        if self.pts is None or self.pose is None:
            return
        x, y, th = self.pose
        (xd, yd), (vxd, vyd), (axd, ayd) = self.ref(self.t)
        if self.v < 0.05:
            self.v = 0.05  # tránh chia cho 0 trong J⁻¹ lúc xuất phát
        w1 = axd + KP * (xd - x) + KD * (vxd - self.v * math.cos(th))
        w2 = ayd + KP * (yd - y) + KD * (vyd - self.v * math.sin(th))
        a = math.cos(th) * w1 + math.sin(th) * w2
        omega = max(-2.5, min(2.5, (-math.sin(th) * w1 + math.cos(th) * w2) / self.v))
        self.v = max(0.0, min(0.5, self.v + a * DT))
        cmd = Twist()
        cmd.linear.x, cmd.angular.z = self.v, omega
        err = math.hypot(xd - x, yd - y)
        self.log.append((round(self.t, 2), round(x, 4), round(y, 4), round(th, 4), round(xd, 4), round(yd, 4), round(err, 4)))
        gx, gy = self.pts[-1]
        if self.t > self.T and math.hypot(gx - x, gy - y) < 0.05 or self.t > self.T + 5:
            self.pub.publish(Twist())
            self.ket_thuc(math.hypot(gx - x, gy - y))
            return
        self.pub.publish(cmd)
        self.t += DT

    def ket_thuc(self, toi_dich):
        errs = [r[6] for r in self.log]
        with open(LOG, "w", newline="") as f:
            csv.writer(f).writerows([("t", "x", "y", "theta", "xd", "yd", "err")] + self.log)
        self.get_logger().info(
            f"TỚI ĐÍCH sau {self.t:.1f} s | sai số lớn nhất {max(errs) * 100:.1f} cm | "
            f"trung bình {sum(errs) / len(errs) * 100:.1f} cm | cách đích {toi_dich * 100:.1f} cm"
        )
        raise SystemExit


def main():
    rclpy.init()
    node = ControllerNode()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass


if __name__ == "__main__":
    main()
