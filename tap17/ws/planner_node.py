"""Tập 1.7 - Node lập kế hoạch: A* trên bản đồ lưới (tập 1.5), làm mượt góc, phát /path một lần.

  phát /path (nav_msgs/Path), QoS transient_local để node đến sau vẫn nhận được
"""
import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile

import a_sao
from duong_di import do_dai, lam_muot, o_sang_met


class PlannerNode(Node):
    def __init__(self):
        super().__init__("planner")
        duong, da_mo, _ = a_sao.A_SAO
        tho = [o_sang_met(o) for o in duong]
        muot = lam_muot(tho)
        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.pub = self.create_publisher(Path, "/path", qos)
        msg = Path()
        msg.header.frame_id = "map"
        for x, y in muot:
            p = PoseStamped()
            p.pose.position.x, p.pose.position.y = x, y
            msg.poses.append(p)
        self.pub.publish(msg)
        self.get_logger().info(
            f"A*: mở {len(da_mo)} ô, đường {len(duong)} ô dài {do_dai(tho):.2f} m -> làm mượt {len(muot)} điểm, dài {do_dai(muot):.2f} m"
        )


def main():
    rclpy.init()
    rclpy.spin(PlannerNode())


if __name__ == "__main__":
    main()
