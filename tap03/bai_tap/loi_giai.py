"""Lời giải bài tập tập 0.3. Tự làm ros_mini_cua_ban.py trước rồi hãy mở!"""
import math

dt = 0.01


def step(x, y, theta, v, omega):
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


class BangTin:
    def __init__(self):
        self.nguoi_nghe = {}

    def dang_ky(self, topic, callback):
        self.nguoi_nghe.setdefault(topic, []).append(callback)

    def phat(self, topic, tin):
        for cb in self.nguoi_nghe.get(topic, []):
            cb(tin)


class RobotNode:
    def __init__(self, bang_tin):
        self.bang_tin = bang_tin
        self.x = self.y = self.theta = 0.0
        self.v = self.omega = 0.0
        bang_tin.dang_ky("/cmd_vel", self.on_cmd)

    def on_cmd(self, tin):
        self.v, self.omega = tin

    def tick(self):
        self.x, self.y, self.theta = step(self.x, self.y, self.theta, self.v, self.omega)
        self.bang_tin.phat("/pose", (self.x, self.y, self.theta))


class DungNuaVong:
    def __init__(self, bang_tin):
        self.bang_tin = bang_tin
        self.da_dung = False
        bang_tin.dang_ky("/pose", self.on_pose)

    def on_pose(self, tin):
        if tin[2] >= math.pi and not self.da_dung:
            self.da_dung = True
            self.bang_tin.phat("/cmd_vel", (0.0, 0.0))
