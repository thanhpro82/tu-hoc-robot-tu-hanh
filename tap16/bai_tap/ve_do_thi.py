"""Vẽ cây RRT của bạn (trái) và cây RRT* trong video (phải, phần mở rộng).

Chạy: python -X utf8 ve_do_thi.py            -> dùng RRT của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import rrt as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import _do_dai  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def _ve_cay(ax, Vs, cha, duong, mau, tieu_de):
    for tx, ty, tw, th in goc.TUONG:
        ax.add_patch(Rectangle((tx, ty), tw, th, fc="#475569", ec="none"))
    for i, p in enumerate(cha):
        if p >= 0:
            ax.plot([Vs[p][0], Vs[i][0]], [Vs[p][1], Vs[i][1]], color=mau, lw=0.7, alpha=0.55)
    ax.plot([q[0] for q in duong], [q[1] for q in duong], color="white", lw=2.6)
    for q, chu in [(goc.Q_S, "S"), (goc.Q_G, "G")]:
        ax.text(q[0], q[1], chu, color=V.NEN, ha="center", va="center", fontsize=10, weight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc=V.MAU["luc"], ec="none"))
    ax.set_xlim(0, goc.W)
    ax.set_ylim(0, goc.H)
    ax.set_aspect("equal")
    V.trang_tri(ax, tieu_de)


def ve(ns, ra="ket_qua.png"):
    f = ns["rrt"] if isinstance(ns, dict) else getattr(ns, "rrt")
    kq = f(seed=2)
    fig, (a, b) = V.tao(1, 2, rong=12, cao=5.2)
    _ve_cay(a, kq["V"], kq["cha"], kq["duong"], V.MAU["xanh"],
            f"RRT: {kq['vong_tim_thay']} vòng, {len(kq['V'])} đỉnh, đường {_do_dai(kq['duong']):.2f} m")
    s = goc.RRT_SAO
    _ve_cay(b, s["V"], s["cha"], s["duong"], V.MAU["cam"], f"RRT* (mở rộng): 2500 vòng, đường {s['dai']:.2f} m")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import rrt_cua_ban
        ve(rrt_cua_ban)
