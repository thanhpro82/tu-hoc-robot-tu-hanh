"""Tập 0.3 - Đưa robot của tập 0.2 vào ROS 2 (series Tự Học Robot Tự Hành).

Node này bọc đúng hàm step() của tập 0.2:
  - nghe   /cmd_vel  (geometry_msgs/Twist): linear.x = v, angular.z = ω
  - phát   /pose     (geometry_msgs/Pose2D): x, y, theta
  - chạy 100 lần mỗi giây (dt = 0.01)

Chạy (trong ROS 2 Jazzy):
  python3 robot_node.py
  ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 1.0}}"
  ros2 topic echo /pose
"""
import math

import rclpy
from geometry_msgs.msg import Pose2D, Twist
from rclpy.node import Node

dt = 0.01


def step(x, y, theta, v, omega):
    """Giữ nguyên từ tập 0.2."""
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt
    return x, y, theta


class RobotNode(Node):
    def __init__(self):
        super().__init__("robot")
        self.x = self.y = self.theta = 0.0
        self.v = self.omega = 0.0
        self.create_subscription(Twist, "/cmd_vel", self.on_cmd, 10)
        self.pub = self.create_publisher(Pose2D, "/pose", 10)
        self.create_timer(dt, self.tick)
        self.get_logger().info("Robot sẵn sàng, đang nghe /cmd_vel")

    def on_cmd(self, msg: Twist):
        self.v, self.omega = msg.linear.x, msg.angular.z

    def tick(self):
        self.x, self.y, self.theta = step(self.x, self.y, self.theta, self.v, self.omega)
        self.pub.publish(Pose2D(x=self.x, y=self.y, theta=self.theta))


def main():
    rclpy.init()
    rclpy.spin(RobotNode())


if __name__ == "__main__":
    main()
