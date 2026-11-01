"""Tập 3.9 - "Bấm" ước lượng vị trí ban đầu (lệch cố ý) rồi ra lệnh Nav2 đi tới bếp, ghi lại mọi thứ để vẽ video.

Ghi vào /ws/out/nav.json:
  amcl     : tư thế AMCL + phương sai theo thời gian (/amcl_pose)
  hat      : đám hạt AMCL mỗi ~0,5 s (/particle_cloud, lấy mẫu 300 hạt)
  plan     : mỗi đường đi toàn cục Nav2 lập (/plan), lấy mẫu
  costmap  : vài ảnh global costmap (/global_costmap/costmap) lưu .npy
  ket_qua  : thời điểm ra lệnh / tới nơi, kết quả, số lần phục hồi
Mọi tư thế trong hệ map (= hệ của bản đồ tập 3.7, gốc ở chỗ xuất phát).
"""
import json
import math
import time

import numpy as np
import rclpy
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.msg import ParticleCloud
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from nav_msgs.msg import OccupancyGrid, Path
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy, qos_profile_sensor_data

OUT = "/ws/out"
UOC_LUONG = (0.35, -0.25, math.radians(12))   # người dùng "bấm" vị trí ban đầu lệch 43 cm, 12° (giả định)
SIG_XY, SIG_TH = 0.3, math.radians(10)
BEP = (9.2, 3.4, math.radians(90))            # điểm đích: bếp (phòng trên bên phải)


def yaw(q):
    return 2 * math.atan2(q.z, q.w)


def tu_the(x, y, th, nav):
    p = PoseStamped()
    p.header.frame_id = "map"
    p.header.stamp = nav.get_clock().now().to_msg()
    p.pose.position.x, p.pose.position.y = x, y
    p.pose.orientation.z, p.pose.orientation.w = math.sin(th / 2), math.cos(th / 2)
    return p


def main():
    rclpy.init()
    nav = BasicNavigator()
    log = {"amcl": [], "hat": [], "plan": [], "costmap": [], "uoc_luong": UOC_LUONG, "bep": BEP}
    t_hat = [0.0]
    t_cm = [0.0]

    def nhan_amcl(m):
        p = m.pose.pose
        c = m.pose.covariance
        log["amcl"].append([round(time.time(), 3), round(p.position.x, 4), round(p.position.y, 4), round(yaw(p.orientation), 4),
                            round(c[0], 5), round(c[7], 5), round(c[35], 5)])

    def nhan_hat(m):
        if time.time() - t_hat[0] < 0.5:
            return
        t_hat[0] = time.time()
        ps = m.particles
        chon = np.linspace(0, len(ps) - 1, min(300, len(ps))).astype(int)
        log["hat"].append({"t": round(time.time(), 3), "n": len(ps),
                           "xy": [[round(ps[i].pose.position.x, 3), round(ps[i].pose.position.y, 3)] for i in chon]})

    def nhan_plan(m):
        xy = [[round(p.pose.position.x, 3), round(p.pose.position.y, 3)] for p in m.poses]
        dai = sum(math.dist(a, b) for a, b in zip(xy, xy[1:]))
        log["plan"].append({"t": round(time.time(), 3), "dai": round(dai, 3), "xy": xy[::4] + xy[-1:]})

    def nhan_cm(m):
        if time.time() - t_cm[0] < 2.0:
            return
        t_cm[0] = time.time()
        k = len(log["costmap"])
        a = np.array(m.data, dtype=np.int8).reshape(m.info.height, m.info.width)
        np.save(f"{OUT}/costmap_{k:03d}.npy", a)
        log["costmap"].append({"t": round(time.time(), 3), "k": k, "res": m.info.resolution,
                               "ox": m.info.origin.position.x, "oy": m.info.origin.position.y})

    latch = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.TRANSIENT_LOCAL)
    nav.create_subscription(PoseWithCovarianceStamped, "/amcl_pose", nhan_amcl, latch)
    nav.create_subscription(ParticleCloud, "/particle_cloud", nhan_hat, qos_profile_sensor_data)
    nav.create_subscription(Path, "/plan", nhan_plan, 10)
    nav.create_subscription(OccupancyGrid, "/global_costmap/costmap", nhan_cm, latch)
    pub = nav.create_publisher(PoseWithCovarianceStamped, "/initialpose", 10)

    # 1) "bấm" ước lượng vị trí ban đầu (như nút 2D Pose Estimate trong RViz), có độ bất định
    nav._waitForNodeToActivate("amcl")
    while not nav.initial_pose_received:
        m = PoseWithCovarianceStamped()
        m.header.frame_id = "map"
        m.header.stamp = nav.get_clock().now().to_msg()
        m.pose.pose = tu_the(*UOC_LUONG, nav).pose
        m.pose.covariance[0] = m.pose.covariance[7] = SIG_XY ** 2
        m.pose.covariance[35] = SIG_TH ** 2
        pub.publish(m)
        rclpy.spin_once(nav, timeout_sec=1.0)
    nav.waitUntilNav2Active(localizer="amcl")
    for _ in range(20):
        rclpy.spin_once(nav, timeout_sec=0.1)

    # 2) bấm điểm đích: bếp
    t0 = time.time()
    nav.goToPose(tu_the(*BEP, nav))
    hoi_phuc = 0
    while not nav.isTaskComplete():
        fb = nav.getFeedback()
        if fb:
            hoi_phuc = fb.number_of_recoveries
        if time.time() - t0 > 300:
            nav.cancelTask()
    kq = nav.getResult()
    t1 = time.time()
    for _ in range(30):
        rclpy.spin_once(nav, timeout_sec=0.1)
    log["ket_qua"] = {"t_lenh": round(t0, 3), "t_toi": round(t1, 3), "ket_qua": str(kq), "thanh_cong": kq == TaskResult.SUCCEEDED,
                      "hoi_phuc": hoi_phuc}
    with open(f"{OUT}/nav.json", "w") as f:
        json.dump(log, f)
    print("KET QUA", log["ket_qua"], "so plan", len(log["plan"]), "so amcl", len(log["amcl"]))
    nav.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main()
