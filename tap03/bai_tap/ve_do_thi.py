"""Vẽ: (trái) sơ đồ node và topic của Bài 3; (phải) đường robot chạy trong "ROS mini" của bạn, dừng ở nửa vòng.

Chạy: python -X utf8 ve_do_thi.py            -> dùng code của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parents[1])]
from chung import ve as V  # noqa: E402
from kiem_tra import ECHO_THAT, _chay  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402


def _hop(ax, x, y, chu, mau, tron=False, rong=2.2):
    ax.add_patch(FancyBboxPatch((x - rong / 2, y - 0.42), rong, 0.84, boxstyle="round,pad=0.05,rounding_size=0.4" if tron else "round,pad=0.05",
                                fc=mau, ec="white", lw=1.2, alpha=0.9))
    ax.text(x, y, chu, ha="center", va="center", color="white", fontsize=11, weight="bold")


def _mui_ten(ax, a, b, cong=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, color="white", lw=1.6,
                                 connectionstyle=f"arc3,rad={cong}"))


def ve(ns, ra="ket_qua.png"):
    robot, pose = _chay(ns, 600, dung=True)
    fig, (a, b) = V.tao(1, 2, rong=12, cao=4.8, gridspec_kw={"width_ratios": [1.1, 1]})
    a.set_xlim(0, 10)
    a.set_ylim(0, 5)
    a.axis("off")
    a.set_title("Node (hộp vuông) nói chuyện qua topic (hộp tròn)", color="white", fontsize=12.5, loc="left")
    _hop(a, 1.7, 2.5, "robot", V.MAU["xanh"])
    _hop(a, 8.3, 2.5, "dung_nua_vong", V.MAU["cam"], rong=3.0)
    _hop(a, 5.0, 4.0, "/pose", "#334155", tron=True)
    _hop(a, 5.0, 1.0, "/cmd_vel", "#334155", tron=True)
    _mui_ten(a, (2.4, 2.95), (3.9, 3.9), -0.2)
    _mui_ten(a, (6.1, 3.9), (7.3, 2.95), -0.2)
    _mui_ten(a, (7.3, 2.05), (6.1, 1.1), -0.2)
    _mui_ten(a, (3.9, 1.1), (2.4, 2.05), -0.2)
    a.text(2.4, 3.7, "phát", color=V.CHU, fontsize=9.5, ha="right")
    a.text(7.0, 3.75, "nghe", color=V.CHU, fontsize=9.5)
    a.text(7.0, 1.2, "phát", color=V.CHU, fontsize=9.5)
    a.text(2.4, 1.3, "nghe", color=V.CHU, fontsize=9.5, ha="right")
    xs, ys = [p[0] for p in pose], [p[1] for p in pose]
    b.plot(xs, ys, color=V.MAU["xanh"], lw=2.6, label="robot trong ROS mini")
    b.plot(ECHO_THAT[0], ECHO_THAT[1], "o", color=V.MAU["vang"], ms=8, label="echo /pose trong ROS 2 thật")
    b.plot(0, 0, "o", color=V.MAU["luc"], ms=7)
    b.text(xs[-1] - 0.06, ys[-1] - 0.1, "dừng (θ = π)", color="white", fontsize=9.5, ha="right")
    V.trang_tri(b, "v = 0,5 · ω = 1, dừng ở nửa vòng", "x (m)", "y (m)")
    b.set_aspect("equal", adjustable="datalim")
    b.margins(0.15)
    V.chu_giai(b, loc="upper right", fontsize=8.8)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import ros_mini_cua_ban
        ve(ros_mini_cua_ban)
