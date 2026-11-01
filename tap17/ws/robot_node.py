"""Tập 1.7 - Node robot: xe 2 bánh mô phỏng (tập 0.2/0.3), có bánh yếu và nhiễu như robot thật.

  nghe /cmd_vel (geometry_msgs/Twist) -> phát /pose (geometry_msgs/Pose2D), 100 lần/giây
"""
import math
import random

import rclpy
from geometry_msgs.msg import Pose2D, Twist
from rclpy.node import Node

import a_sao

dt = 0.01
O = a_sao.O_M


def step(x, y, theta, v, omega):
    """Giữ nguyên từ tập 0.2."""
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


class RobotNode(Node):
    def __init__(self):
        super().__init__("robot")
        r, c = a_sao.START
        self.x, self.y = (c + 0.5) * O, (a_sao.ROWS - 1 - r + 0.5) * O
        self.theta = math.pi / 2  # xuất phát quay mặt lên trên
        self.v = self.omega = 0.0
        self.rng = random.Random(7)
        self.create_subscription(Twist, "/cmd_vel", self.on_cmd, 10)
        self.pub = self.create_publisher(Pose2D, "/pose", 10)
        self.create_timer(dt, self.tick)
        self.get_logger().info(f"Robot ở ({self.x:.2f}, {self.y:.2f}), bánh phải yếu, đang nghe /cmd_vel")

    def on_cmd(self, msg: Twist):
        self.v, self.omega = msg.linear.x, msg.angular.z

    def tick(self):
        # robot "thật": quay chỉ được 95% lệnh, bánh yếu kéo lệch, có nhiễu (giống tập 1.4)
        v = self.v * (1 + self.rng.gauss(0, 0.05))
        w = self.omega * 0.95 - 0.06 * (self.v > 0.01) + self.rng.gauss(0, 0.1)
        self.x, self.y, self.theta = step(self.x, self.y, self.theta, v, w)
        self.pub.publish(Pose2D(x=self.x, y=self.y, theta=self.theta))


def main():
    rclpy.init()
    rclpy.spin(RobotNode())


if __name__ == "__main__":
    main()
