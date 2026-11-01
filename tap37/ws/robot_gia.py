"""Tập 3.7 - Robot vẽ bản đồ nhà tôi: node ROS 2 giả lập robot + LiDAR trong căn hộ 4 phòng.

Phát:  /scan (sensor_msgs/LaserScan, 360 tia, 10 Hz), /odom (nav_msgs/Odometry), TF odom -> base_link (từ odometry có trôi),
       TF tĩnh base_link -> laser.
Ghi:   tư thế thật, tư thế odometry, tư thế slam_toolbox (TF map -> base_link) mỗi 0,5 s và ảnh bản đồ /map mỗi 5 s
       vào /ws/out/ để vẽ video.
Căn hộ giống tập 3.5 (12 × 8 m). Odometry: nhiễu + quay hụt 0,5°/m (giả định) để thấy trôi.
"""
import json
import math
import os
import time

import numpy as np
import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from tf2_ros import Buffer, StaticTransformBroadcaster, TransformBroadcaster, TransformListener

O = 0.05
RONG, DAI = 12.0, 8.0
NX, NY = int(RONG / O), int(DAI / O)
SO_TIA, TAM, SIG_LIDAR = 360, 8.0, 0.01
V = 0.35
LECH_TH = math.radians(0.5)  # quay hụt mỗi mét
SIG_V, SIG_W = 0.02, math.radians(1.0)
OUT = "/ws/out"


def tao_ban_do():
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
    tuong(4.9, 4.4, 5.3, 4.8)       # cột phòng trên trái (để khác phòng dưới trái)
    tuong(3.2, 7.5, 4.6, 7.8)       # kệ sát tường trên
    tuong(4.8, 1.0, 5.6, 1.3)       # ghế dài phòng dưới trái
    return m


BAN_DO = tao_ban_do()
GOC_TIA = np.linspace(-math.pi, math.pi, SO_TIA, endpoint=False)
BUOC = np.arange(0.1, TAM, 0.02)
# Lộ trình đi qua cả 4 phòng rồi về chỗ xuất phát (khép vòng)
DIEM_DEN = [(3.0, 2.6), (5.0, 2.1), (7.2, 2.1), (9.0, 2.6), (9.1, 3.6), (9.1, 5.0), (8.0, 6.0), (6.6, 5.9),
            (5.2, 5.9), (3.4, 6.0), (1.6, 5.4), (2.9, 4.6), (2.9, 3.4), (2.0, 2.6), (1.2, 2.6)]
X0 = (1.2, 2.6, 0.0)


def goc(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def quet(x, y, th, rng):
    a = th + GOC_TIA
    px = x + np.outer(BUOC, np.cos(a))
    py = y + np.outer(BUOC, np.sin(a))
    ix = np.clip((px / O).astype(int), 0, NX - 1)
    iy = np.clip((py / O).astype(int), 0, NY - 1)
    trung = BAN_DO[iy, ix]
    co = trung.any(axis=0)
    dau = np.argmax(trung, axis=0)
    r = np.where(co, BUOC[dau], np.inf)
    return r + rng.normal(0, SIG_LIDAR, SO_TIA) * co


def quat(th):
    return 0.0, 0.0, math.sin(th / 2), math.cos(th / 2)


class RobotGia(Node):
    def __init__(self):
        super().__init__("robot_gia")
        self.rng = np.random.default_rng(37)
        self.that = list(X0)
        self.odo = list(X0)
        self.i = 0
        self.t0 = time.time()
        self.da_xong = False
        self.pub_scan = self.create_publisher(LaserScan, "/scan", 10)
        self.pub_odom = self.create_publisher(Odometry, "/odom", 10)
        self.tf = TransformBroadcaster(self)
        st = StaticTransformBroadcaster(self)
        m = TransformStamped()
        m.header.stamp = self.get_clock().now().to_msg()
        m.header.frame_id, m.child_frame_id = "base_link", "laser"
        m.transform.rotation.w = 1.0
        st.sendTransform(m)
        self.buf = Buffer()
        self.lis = TransformListener(self.buf, self)
        qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.create_subscription(OccupancyGrid, "/map", self.nhan_map, qos)
        self.map_cuoi = None
        os.makedirs(OUT, exist_ok=True)
        self.log = open(f"{OUT}/tu_the.jsonl", "w")
        self.dem_map = 0
        self.create_timer(0.1, self.buoc)
        self.create_timer(0.5, self.ghi)
        self.create_timer(5.0, self.luu_map)

    def dieu_khien(self):
        while self.i < len(DIEM_DEN):
            dx, dy = DIEM_DEN[self.i][0] - self.that[0], DIEM_DEN[self.i][1] - self.that[1]
            if math.hypot(dx, dy) > 0.25:
                e = goc(math.atan2(dy, dx) - self.that[2])
                return V * max(0.15, math.cos(e)), max(-1.0, min(1.0, 1.8 * e))
            self.i += 1
        # về tới nơi: quay về hướng ban đầu rồi dừng
        e = goc(X0[2] - self.that[2])
        if abs(e) > 0.05:
            return 0.0, max(-0.8, min(0.8, 1.5 * e))
        self.da_xong = True
        return 0.0, 0.0

    def buoc(self):
        dt = 0.1
        v, w = self.dieu_khien()
        x, y, th = self.that
        th = goc(th + w * dt)
        self.that = [x + v * dt * math.cos(th), y + v * dt * math.sin(th), th]
        # odometry: đo v, w có nhiễu + quay hụt theo quãng đường
        vo = v + self.rng.normal(0, SIG_V) * (v > 0)
        wo = w + (LECH_TH * v) + self.rng.normal(0, SIG_W) * (abs(v) + abs(w) > 0)
        xo, yo, tho = self.odo
        tho = goc(tho + wo * dt)
        self.odo = [xo + vo * dt * math.cos(tho), yo + vo * dt * math.sin(tho), tho]
        now = self.get_clock().now().to_msg()
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id, t.child_frame_id = "odom", "base_link"
        t.transform.translation.x, t.transform.translation.y = self.odo[0] - X0[0], self.odo[1] - X0[1]
        # hệ odom gốc ở điểm xuất phát (giống robot thật: odometry bắt đầu từ 0)
        c, s = math.cos(-X0[2]), math.sin(-X0[2])
        ox, oy = self.odo[0] - X0[0], self.odo[1] - X0[1]
        t.transform.translation.x, t.transform.translation.y = c * ox - s * oy, s * ox + c * oy
        qx, qy, qz, qw = quat(goc(self.odo[2] - X0[2]))
        t.transform.rotation.z, t.transform.rotation.w = qz, qw
        self.tf.sendTransform(t)
        od = Odometry()
        od.header.stamp = now
        od.header.frame_id, od.child_frame_id = "odom", "base_link"
        od.pose.pose.position.x, od.pose.pose.position.y = t.transform.translation.x, t.transform.translation.y
        od.pose.pose.orientation.z, od.pose.pose.orientation.w = qz, qw
        od.twist.twist.linear.x, od.twist.twist.angular.z = vo, wo
        self.pub_odom.publish(od)
        r = quet(*self.that, self.rng)
        sc = LaserScan()
        sc.header.stamp = now
        sc.header.frame_id = "laser"
        sc.angle_min, sc.angle_max = float(GOC_TIA[0]), float(GOC_TIA[-1])
        sc.angle_increment = float(GOC_TIA[1] - GOC_TIA[0])
        sc.scan_time, sc.range_min, sc.range_max = 0.1, 0.1, TAM
        sc.ranges = [float(v) for v in r]
        self.pub_scan.publish(sc)

    def ghi(self):
        slam = None
        try:
            tr = self.buf.lookup_transform("map", "base_link", rclpy.time.Time())
            q = tr.transform.rotation
            slam = [tr.transform.translation.x, tr.transform.translation.y, 2 * math.atan2(q.z, q.w)]
        except Exception:  # noqa: BLE001 (chưa có map -> base_link)
            pass
        self.log.write(json.dumps({"t": round(time.time() - self.t0, 2), "that": self.that, "odo": self.odo, "slam": slam,
                                   "xong": self.da_xong}) + "\n")
        self.log.flush()
        if self.da_xong and time.time() - getattr(self, "t_xong", time.time() + 1) > 8:
            self.luu_map()
            self.get_logger().info("XONG")
            raise SystemExit
        if self.da_xong and not hasattr(self, "t_xong"):
            self.t_xong = time.time()

    def nhan_map(self, msg):
        self.map_cuoi = msg

    def luu_map(self):
        m = self.map_cuoi
        if m is None:
            return
        a = np.array(m.data, dtype=np.int8).reshape(m.info.height, m.info.width)
        np.save(f"{OUT}/map_{self.dem_map:03d}.npy", a)
        with open(f"{OUT}/map_{self.dem_map:03d}.json", "w") as f:
            json.dump({"t": round(time.time() - self.t0, 2), "res": m.info.resolution, "ox": m.info.origin.position.x,
                       "oy": m.info.origin.position.y, "w": m.info.width, "h": m.info.height}, f)
        self.dem_map += 1


def main():
    rclpy.init()
    n = RobotGia()
    try:
        rclpy.spin(n)
    except SystemExit:
        pass
    n.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()
