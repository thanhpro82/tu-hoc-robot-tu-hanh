"""Vẽ 3 robot cùng làm bài "sang ngang 60 cm": đa hướng, xe 2 bánh, ô tô (đỗ xe song song).

Chạy: python -X utf8 ve_do_thi.py            -> ô tô dùng step_car của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import math
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import khong_di_ngang as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402


def than_xe(ax, x, y, th, dai, rong, mau, alpha):
    c, s = math.cos(th), math.sin(th)
    goc_xe = [(-0.1 * dai, -rong / 2), (0.9 * dai, -rong / 2), (0.9 * dai, rong / 2), (-0.1 * dai, rong / 2)]
    ax.add_patch(Polygon([(x + c * a - s * b, y + s * a + c * b) for a, b in goc_xe], closed=True,
                         fc=mau, ec="white", lw=0.8, alpha=alpha))


def ve(ns, ra="ket_qua.png"):
    step_car = ns["step_car"] if isinstance(ns, dict) else getattr(ns, "step_car")
    o_to = goc.chay(step_car, [(goc.t_cung, (-goc.V, goc.PHI_MAX)), (goc.t_cung, (-goc.V, -goc.PHI_MAX))])
    bai = [("Đa hướng: trượt ngang luôn", goc.omni, V.MAU["luc"], 0.2),
           ("Xe 2 bánh: quay, chạy, quay lại", goc.unicycle, V.MAU["xanh"], 0.2),
           ("Ô tô: lùi 2 cung (đỗ xe song song)", o_to, V.MAU["cam"], 0.3)]
    fig, axes = V.tao(1, 3, rong=12.5, cao=3.6)
    for ax, (ten, p, mau, dai) in zip(axes, bai):
        n = len(p)
        for k in range(0, 6):
            q = p[min(n - 1, k * (n - 1) // 5)]
            than_xe(ax, q[0], q[1], q[2], dai, 0.14, mau, 0.15 + 0.15 * k)
        ax.plot([q[0] for q in p], [q[1] for q in p], color="white", lw=1.4, ls="--")
        ax.axhline(0.6, color=V.MAU["xam"], lw=1, ls=":")
        x, y, th = p[-1][:3]
        V.trang_tri(ax, ten, "x (m)", "y (m)" if ax is axes[0] else None)
        ax.text(0.03, 0.92, f"tới ({x:+.2f}, {y:+.2f}), vận tốc ngang tối đa {goc.van_toc_ngang(p):.2f} m/s",
                transform=ax.transAxes, color=V.CHU, fontsize=8.8)
        ax.set_xlim(-1.25, 0.55)
        ax.set_ylim(-0.25, 0.95)
        ax.set_aspect("equal")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import xe_cua_ban
        ve(xe_cua_ban)
