"""Tập 3.7 - phân tích lần chạy slam_toolbox thật (ROS 2 Jazzy trong Docker, xem tap37/ws/).

Đọc tap37/ws/out/: tu_the.jsonl (tư thế thật / odometry / slam_toolbox mỗi 0,5 s) và map_XXX.npy (bản đồ /map mỗi 5 s).
So sánh trong hệ gốc = điểm xuất phát của robot (giống hệ odom và map của slam_toolbox lúc đầu).
- Sai số tư thế: odometry vs slam_toolbox so với tư thế thật.
- Bản đồ "chỉ odometry": quét lại LiDAR tại tư thế thật (cùng mô hình cảm biến với robot_gia.py), ghép theo tư thế odometry,
  để so với bản đồ slam_toolbox tự dựng.
- Độ chính xác bản đồ: % ô bị chiếm (hoặc điểm quét) nằm trong 10 cm quanh tường thật.
Chạy: python -X utf8 phan_tich.py
"""
import json
import re
import sys
import types
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation

WS = Path(__file__).resolve().parents[1] / "ws"
OUTD = WS / "out"

# dùng lại bản đồ và mô hình LiDAR của robot_gia.py (giả các module ROS để import được trên Windows)
for name in ["rclpy", "rclpy.node", "rclpy.qos", "rclpy.time", "geometry_msgs", "geometry_msgs.msg", "nav_msgs", "nav_msgs.msg",
             "sensor_msgs", "sensor_msgs.msg", "tf2_ros"]:
    sys.modules.setdefault(name, types.ModuleType(name))
sys.modules["rclpy.node"].Node = object
for mod, names in {"rclpy.qos": ["DurabilityPolicy", "QoSProfile", "ReliabilityPolicy"], "geometry_msgs.msg": ["TransformStamped"],
                   "nav_msgs.msg": ["OccupancyGrid", "Odometry"], "sensor_msgs.msg": ["LaserScan"],
                   "tf2_ros": ["Buffer", "StaticTransformBroadcaster", "TransformBroadcaster", "TransformListener"]}.items():
    for n in names:
        setattr(sys.modules[mod], n, object)
sys.path.insert(0, str(WS))
import robot_gia as R  # noqa: E402

X0 = np.array(R.X0)
LOG = [json.loads(l) for l in (OUTD / "tu_the.jsonl").read_text().splitlines()]
LOG = [r for r in LOG if r["slam"] is not None]


def ve_goc(p):
    """Tư thế thế giới -> hệ gốc tại điểm xuất phát."""
    c, s = np.cos(-X0[2]), np.sin(-X0[2])
    dx, dy = p[0] - X0[0], p[1] - X0[1]
    return np.array([c * dx - s * dy, s * dx + c * dy, R.goc(p[2] - X0[2])])


THAT = np.array([ve_goc(r["that"]) for r in LOG])
ODO = np.array([ve_goc(r["odo"]) for r in LOG])
SLAM = np.array([r["slam"] for r in LOG])
T = np.array([r["t"] for r in LOG])
loi = lambda P: np.hypot(*(P[:, :2] - THAT[:, :2]).T)
E_ODO, E_SLAM = loi(ODO), loi(SLAM)

# tường thật trong hệ gốc, nới 10 cm
TUONG = binary_dilation(R.BAN_DO, iterations=2)


def tren_tuong(xy_goc):
    w = xy_goc + X0[:2]
    ix, iy = (w[:, 0] / R.O).astype(int), (w[:, 1] / R.O).astype(int)
    ok = (ix >= 0) & (ix < R.NX) & (iy >= 0) & (iy < R.NY)
    return TUONG[iy[ok], ix[ok]], ok


# bản đồ chỉ odometry: quét lại tại tư thế thật, ghép theo tư thế odometry (và theo tư thế slam để so cùng cách)
rng = np.random.default_rng(370)
def ghep(P):
    pts = []
    for p_that, p in zip(THAT, P):
        w = p_that + np.r_[X0[:2], 0]
        r = R.quet(*(np.array(R.X0[:2]) + p_that[:2]), p_that[2] + X0[2], rng)
        ok = np.isfinite(r)
        a = p[2] + R.GOC_TIA[ok]
        pts.append(np.column_stack([p[0] + r[ok] * np.cos(a), p[1] + r[ok] * np.sin(a)]))
    return np.vstack(pts)


DIEM_ODO = ghep(ODO)
DIEM_SLAM = ghep(SLAM)
NET_ODO = float(tren_tuong(DIEM_ODO)[0].mean())
NET_SLAM_DIEM = float(tren_tuong(DIEM_SLAM)[0].mean())

# bản đồ slam_toolbox tự dựng (ảnh cuối)
files = sorted(OUTD.glob("map_*.npy"))
MAPS = [(np.load(f), json.loads(f.with_suffix(".json").read_text())) for f in files]
M, INFO = MAPS[-1]
iy, ix = np.nonzero(M == 100)
xy = np.column_stack([INFO["ox"] + (ix + 0.5) * INFO["res"], INFO["oy"] + (iy + 0.5) * INFO["res"]])
o_tuong, ok = tren_tuong(xy)
NET_SLAM_MAP = float(o_tuong.mean())
DIEN_TICH = float((M == 0).sum() * INFO["res"] ** 2)
SO_TOI_UU = len(re.findall(r"preprocessor\.cc", (OUTD / "slam.log").read_text(errors="ignore")))
QUANG_DUONG = float(np.sum(np.hypot(*np.diff(THAT[:, :2], axis=0).T)))

if __name__ == "__main__":
    print(f"Thời gian {T[-1]:.1f} s · quãng đường thật {QUANG_DUONG:.1f} m · {len(MAPS)} ảnh bản đồ · số lần bộ giải Ceres chạy: {SO_TOI_UU}")
    print(f"Odometry: cuối lệch {E_ODO[-1]:.2f} m, lớn nhất {E_ODO.max():.2f} m, trung bình {E_ODO.mean():.2f} m")
    print(f"slam_toolbox: cuối lệch {E_SLAM[-1] * 100:.1f} cm, lớn nhất {E_SLAM.max() * 100:.1f} cm, trung bình {E_SLAM.mean() * 100:.1f} cm")
    print(f"Điểm quét rơi đúng tường (±10 cm): ghép theo odometry {NET_ODO * 100:.1f}% · theo slam_toolbox {NET_SLAM_DIEM * 100:.1f}%")
    print(f"Bản đồ slam_toolbox: {int(ok.sum())} ô tường, {NET_SLAM_MAP * 100:.1f}% nằm đúng tường thật · diện tích trống đã vẽ {DIEN_TICH:.1f} m² · ô {INFO['res'] * 100:.0f} cm")
    k = np.argmax(E_SLAM)
    print(f"Sai số slam lớn nhất ở t = {T[k]:.1f} s; odometry lúc đó lệch {E_ODO[k]:.2f} m")
