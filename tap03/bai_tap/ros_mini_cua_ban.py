"""Bài tập tập 0.3: tự viết một "ROS mini" bằng Python thuần để hiểu node, topic, message.

ROS 2 thật làm việc này qua mạng giữa nhiều chương trình. Ở đây ta làm trong 1 chương trình cho dễ thấy cơ chế:
  - topic = một cái tên, ví dụ "/cmd_vel";
  - node đăng ký nghe topic bằng một hàm gọi lại (callback);
  - node khác phát tin lên topic, mọi callback đang nghe topic đó được gọi.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên lớp, hàm và tham số. Lời giải: loi_giai.py (tự làm trước đã).
"""
import math

dt = 0.01  # 100 lần mỗi giây, như robot_node.py


def step(x, y, theta, v, omega):
    """Giữ nguyên từ tập 0.2."""
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


class BangTin:
    """Bài 1: "bảng tin" nối các node với nhau qua topic."""

    def __init__(self):
        self.nguoi_nghe = {}  # tên topic -> list các hàm callback

    def dang_ky(self, topic, callback):
        """Ghi nhận: mỗi khi có tin trên `topic` thì gọi callback(tin)."""
        raise NotImplementedError("TODO Bài 1: thêm callback vào danh sách của topic")

    def phat(self, topic, tin):
        """Gửi `tin` tới TẤT CẢ callback đã đăng ký topic này (topic chưa ai nghe thì thôi, không lỗi)."""
        raise NotImplementedError("TODO Bài 1: gọi từng callback")


class RobotNode:
    """Bài 2: node robot giống robot_node.py: nghe "/cmd_vel" (tin là tuple (v, ω)), phát "/pose" (tuple (x, y, θ))."""

    def __init__(self, bang_tin):
        self.bang_tin = bang_tin
        self.x = self.y = self.theta = 0.0
        self.v = self.omega = 0.0
        # TODO Bài 2: đăng ký nghe "/cmd_vel" bằng self.on_cmd

    def on_cmd(self, tin):
        """Nhận lệnh (v, ω), lưu lại để dùng ở các bước sau."""
        raise NotImplementedError("TODO Bài 2: lưu self.v, self.omega")

    def tick(self):
        """Gọi 100 lần mỗi giây: tiến 1 bước bằng step(), rồi phát vị trí mới lên "/pose"."""
        raise NotImplementedError("TODO Bài 2: step rồi phát /pose")


class DungNuaVong:
    """Bài 3: node điều khiển: nghe "/pose"; khi robot đã quay được nửa vòng (θ ≥ π) thì phát lệnh dừng (0, 0) lên "/cmd_vel".

    Chỉ phát lệnh dừng MỘT lần (dùng self.da_dung để nhớ)."""

    def __init__(self, bang_tin):
        self.bang_tin = bang_tin
        self.da_dung = False
        # TODO Bài 3: đăng ký nghe "/pose" bằng self.on_pose

    def on_pose(self, tin):
        raise NotImplementedError("TODO Bài 3: θ ≥ π và chưa dừng thì phát (0.0, 0.0) lên /cmd_vel")
