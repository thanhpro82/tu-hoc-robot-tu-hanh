"""Vẽ 3 đường đi của robot: đi thẳng, vòng tròn, số 8.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn (robot_cua_ban.py), ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import math
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
from chung import ve as V  # noqa: E402
from kiem_tra import _chay  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    step, w8 = lay("step"), lay("omega_so_8")
    bai = [("Đi thẳng: v = 0,5 · ω = 0", _chay(step, 0.5, lambda t: 0.0, 6), V.MAU["xam"]),
           ("Vòng tròn: ω = 1 rad/s", _chay(step, 0.5, lambda t: 1.0, 2 * math.pi), V.MAU["xanh"]),
           ("Số 8: ω = +1 rồi −1", _chay(step, 0.5, w8, 4 * math.pi), V.MAU["cam"])]
    fig, axes = V.tao(1, 3, rong=12, cao=4.2)
    for ax, (ten, p, mau) in zip(axes, bai):
        xs, ys = [q[0] for q in p], [q[1] for q in p]
        ax.plot(xs, ys, color=mau, lw=2.6)
        x, y, th = p[-1]
        ax.annotate("", xy=(x + 0.25 * math.cos(th), y + 0.25 * math.sin(th)), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=1.8))
        ax.plot(0, 0, "o", color=V.MAU["luc"], ms=7)
        V.trang_tri(ax, ten, "x (m)", "y (m)" if ax is axes[0] else None)
        ax.margins(0.12, 0.28)
        ax.set_aspect("equal", adjustable="datalim")
        ax.text(0.03, 0.92, f"dừng ở ({x:+.2f}, {y:+.2f})", transform=ax.transAxes, color=V.CHU, fontsize=9.5)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import robot_cua_ban
        ve(robot_cua_ban)
