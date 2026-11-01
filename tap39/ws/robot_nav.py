"""Tập 3.9 - Tổng kết Mùa 3: robot giả lập cho Nav2 trong căn hộ của tập 3.7.

Nhận: /cmd_vel (geometry_msgs/Twist) từ Nav2, robot hai bánh v, ω (mô hình unicycle).
Phát: /scan (360 tia, 10 Hz), /odom + TF odom -> base_link (odometry trôi như tập 3.7), TF tĩnh base_link -> laser.
Thế giới hôm nay khác bản đồ: cửa giữa hai phòng dưới (x = 6 m, y 1,6–2,6 m) bị ĐÓNG (giả định, để Nav2 phải tìm đường khác).
Ghi: tư thế thật + odometry mỗi 0,1 s vào /ws/out/robot.jsonl (đồng hồ time.time() dùng chung với ra_lenh.py).
"""
import json
import math
import os
import time

import numpy as np
import rclpy
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster

O = 0.05
RONG, DAI = 12.0, 8.0
NX, NY = int(RONG / O), int(DAI / O)
SO_TIA, TAM, SIG_LIDAR = 360, 8.0, 0.01
LECH_TH = math.radians(0.5)  # quay hụt mỗi mét (như tập 3.7)
SIG_V, SIG_W = 0.02, math.radians(1.0)
BAN_KINH = 0.18
OUT = "/ws/out"
X0 = (1.2, 2.6, 0.0)  # chỗ xuất phát = gốc hệ map của slam_toolbox ở tập 3.7
CUA_DONG = os.environ.get("CUA_DONG", "duoi")


def tao_the_gioi():
    m = np.zeros((NY, NX), dtype=bool)
    m[:2, :] = m[-2:, :] = True
    m[:, :2] = m[:, -2:] = True

    def tuong(x0, y0, x1, y1):
        m[int(y0 / O):int(y1 / O) + 1, int(x0 / O):int(x1 / O) + 1] = True

    tuong(6.0, 0.0, 6.1, 8.0)
    tuong(0.0, 4.0, 12.0, 4.1)
    for x0, x1 in [(2.4, 3.4), (8.6, 9.6)]:
        m[int(4.0 / O):int(4.1 / O) + 1, int(x0 / O):int(x1 / O)] = False
    for y0, y1 in [(1.6, 2.6), (5.4, 6.4)]:
        m[int(y0 / O):int(y1 / O), int(6.0 / O):int(6.1 / O) + 1] = False
    tuong(1.0, 1.0, 2.0, 1.6)
    tuong(9.5, 0.6, 11.4, 1.2)
    tuong(10.6, 2.2, 11.4, 3.2)
    tuong(0.6, 6.8, 2.6, 7.4)
    tuong(4.0, 5.0, 4.6, 5.6)
    tuong(7.0, 6.6, 7.8, 7.4)
    tuong(4.9, 4.4, 5.3, 4.8)
    tuong(3.2, 7.5, 4.6, 7.8)
    tuong(4.8, 1.0, 5.6, 1.3)
    if CUA_DONG == "duoi":
        tuong(6.0, 1.55, 6.1, 2.65)       # cửa phòng dưới đóng
    elif CUA_DONG == "tren":
        tuong(6.0, 5.35, 6.1, 6.45)       # cửa phòng trên đóng
    return m


THE_GIOI = tao_the_gioi()
GOC_TIA = np.linspace(-math.pi, math.pi, SO_TIA, endpoint=False)
BUOC = np.arange(0.1, TAM, 0.02)
VONG = np.linspace(0, 2 * math.pi, 24, endpoint=False)


def goc(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def chiem(px, py):
    ix = np.clip((np.asarray(px) / O).astype(int), 0, NX - 1)
    iy = np.clip((np.asarray(py) / O).astype(int), 0, NY - 1)
    return THE_GIOI[iy, ix]


def quet(x, y, th, rng):
    a = th + GOC_TIA
    trung = chiem(x + np.outer(BUOC, np.cos(a)), y + np.outer(BUOC, np.sin(a)))
    co = trung.any(axis=0)
    r = np.where(co, BUOC[np.argmax(trung, axis=0)], np.inf)
    return r + rng.normal(0, SIG_LIDAR, SO_TIA) * co


class RobotNav(Node):
    def __init__(self):
        super().__init__("robot_nav")
        self.rng = np.random.default_rng(39)
        self.that = list(X0)
        self.odo = list(X0)
        self.cmd = (0.0, 0.0)
        self.t_cmd = 0.0
        self.va_cham = 0
        self.pub_scan = self.create_publisher(LaserScan, "/scan", 10)
        self.pub_odom = self.create_publisher(Odometry, "/odom", 10)
        self.tf = TransformBroadcaster(self)
        st = StaticTransformBroadcaster(self)
        m = TransformStamped()
        m.header.stamp = self.get_clock().now().to_msg()
        m.header.frame_id, m.child_frame_id = "base_link", "laser"
        m.transform.rotation.w = 1.0
        st.sendTransform(m)
        self.create_subscription(Twist, "/cmd_vel", self.nhan_cmd, 10)
        os.makedirs(OUT, exist_ok=True)
        self.log = open(f"{OUT}/robot.jsonl", "w")
        self.create_timer(0.05, self.buoc)
        self.create_timer(0.1, self.phat_scan)

    def nhan_cmd(self, msg):
        self.cmd = (msg.linear.x, msg.angular.z)
        self.t_cmd = time.time()

    def buoc(self):
        dt = 0.05
        v, w = self.cmd if time.time() - self.t_cmd < 0.5 else (0.0, 0.0)
        x, y, th = self.that
        th2 = goc(th + w * dt)
        x2, y2 = x + v * dt * math.cos(th2), y + v * dt * math.sin(th2)
        if chiem(x2 + BAN_KINH * np.cos(VONG), y2 + BAN_KINH * np.sin(VONG)).any():
            x2, y2 = x, y           # đụng tường: đứng yên, đếm va chạm
            self.va_cham += 1
        self.that = [x2, y2, th2]
        di = math.hypot(x2 - x, y2 - y) / dt * (1 if v >= 0 else -1)
        vo = di + self.rng.normal(0, SIG_V) * (abs(di) > 1e-3)
        wo = w + LECH_TH * abs(di) + self.rng.normal(0, SIG_W) * (abs(di) + abs(w) > 1e-3)
        xo, yo, tho = self.odo
        tho = goc(tho + wo * dt)
        self.odo = [xo + vo * dt * math.cos(tho), yo + vo * dt * math.sin(tho), tho]
        now = self.get_clock().now().to_msg()
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id, t.child_frame_id = "odom", "base_link"
        t.transform.translation.x, t.transform.translation.y = self.odo[0] - X0[0], self.odo[1] - X0[1]
        qz, qw = math.sin(self.odo[2] / 2), math.cos(self.odo[2] / 2)
        t.transform.rotation.z, t.transform.rotation.w = qz, qw
        self.tf.sendTransform(t)
        od = Odometry()
        od.header.stamp = now
        od.header.frame_id, od.child_frame_id = "odom", "base_link"
        od.pose.pose.position.x, od.pose.pose.position.y = t.transform.translation.x, t.transform.translation.y
        od.pose.pose.orientation.z, od.pose.pose.orientation.w = qz, qw
        od.twist.twist.linear.x, od.twist.twist.angular.z = vo, wo
        self.pub_odom.publish(od)

    def phat_scan(self):
        r = quet(*self.that, self.rng)
        sc = LaserScan()
        sc.header.stamp = self.get_clock().now().to_msg()
        sc.header.frame_id = "laser"
        sc.angle_min, sc.angle_max = float(GOC_TIA[0]), float(GOC_TIA[-1])
        sc.angle_increment = float(GOC_TIA[1] - GOC_TIA[0])
        sc.scan_time, sc.range_min, sc.range_max = 0.1, 0.1, TAM
        sc.ranges = [float(v) for v in r]
        self.pub_scan.publish(sc)
        self.log.write(json.dumps({"t": round(time.time(), 3), "that": [round(v, 4) for v in self.that],
                                   "odo": [round(v, 4) for v in self.odo], "cmd": [round(c, 3) for c in self.cmd],
                                   "va_cham": self.va_cham}) + "\n")
        self.log.flush()


def main():
    rclpy.init()
    n = RobotNav()
    try:
        rclpy.spin(n)
    except (KeyboardInterrupt, SystemExit):
        pass
    n.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()
