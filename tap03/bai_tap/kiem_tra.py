"""Tự chấm bài tập tập 0.3. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parents[1])]
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

# Lần echo /pose đầu tiên trong demo-output.txt (ROS 2 Jazzy chạy thật, lệnh v = 0.5, ω = 1)
ECHO_THAT = (0.03577186167094566, 0.9988896763077438, 3.0799999999999783)


def bai_1(ns):
    bt = ham(ns, "BangTin")()
    nhan_a, nhan_b = [], []
    bt.dang_ky("/a", nhan_a.append)
    bt.dang_ky("/a", nhan_b.append)
    bt.dang_ky("/b", lambda t: nhan_b.append(("b", t)))
    bt.phat("/a", 1)
    bt.phat("/b", 2)
    bt.phat("/khong_ai_nghe", 3)
    assert nhan_a == [1], f"callback 1 của /a phải nhận [1], nhận {nhan_a}"
    assert nhan_b == [1, ("b", 2)], f"callback 2 của /a và callback của /b phải nhận [1, ('b', 2)], nhận {nhan_b}"
    return "tin tới đúng mọi người nghe của topic; topic chưa ai nghe thì bỏ qua"


def _chay(ns, so_buoc, lenh=(0.5, 1.0), dung=False):
    bt = ham(ns, "BangTin")()
    robot = ham(ns, "RobotNode")(bt)
    pose = []
    bt.dang_ky("/pose", pose.append)
    if dung:
        ham(ns, "DungNuaVong")(bt)
    bt.phat("/cmd_vel", lenh)
    for _ in range(so_buoc):
        robot.tick()
    return robot, pose


def bai_2(ns):
    robot, pose = _chay(ns, 308)
    assert len(pose) == 308, f"chạy 308 bước phải phát 308 tin /pose, bạn phát {len(pose)}"
    assert gan(pose[0], (0.005, 0.0, 0.01)), f"tin /pose đầu tiên phải là (0.005, 0, 0.01), bạn phát {pose[0]}"
    x, y, th = pose[-1]
    assert gan(th, ECHO_THAT[2]) and abs(y - ECHO_THAT[1]) < 0.005 and abs(x - ECHO_THAT[0]) < 0.01, \
        f"sau 308 bước phải gần lần echo trong ROS 2 thật {tuple(round(v, 3) for v in ECHO_THAT)}, bạn ra {(round(x, 3), round(y, 3), round(th, 3))}"
    return f"sau 308 bước robot ở ({x:.3f}, {y:.3f}, θ = {th:.2f}), khớp lần echo /pose trong ROS 2 thật ({ECHO_THAT[0]:.3f}, {ECHO_THAT[1]:.3f}, {ECHO_THAT[2]:.2f})"


def bai_3(ns):
    ham(ns, "DungNuaVong")(ham(ns, "BangTin")()).on_pose((0.0, 0.0, 0.0))   # chưa viết on_pose thì báo "chưa làm"
    robot, pose = _chay(ns, 600, dung=True)
    assert robot.v == 0 and robot.omega == 0, "robot phải nhận lệnh dừng (0, 0) qua /cmd_vel"
    x, y, th = pose[-1]
    assert abs(th - math.pi) < 0.02 and abs(x) < 0.02 and abs(y - 1.0) < 0.01, f"phải dừng ở nửa vòng (0, 1, θ ≈ π), bạn dừng ở {(round(x, 3), round(y, 3), round(th, 3))}"
    return f"node điều khiển nghe /pose, phát /cmd_vel: robot dừng ở ({x:.2f}, {y:.2f}), θ = {math.degrees(th):.0f}° (vòng kín đầu tiên qua topic)"


BAI = [("Bài 1 · bảng tin (topic)", bai_1), ("Bài 2 · node robot", bai_2), ("Bài 3 · node điều khiển", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "ros_mini_cua_ban", _lg)
