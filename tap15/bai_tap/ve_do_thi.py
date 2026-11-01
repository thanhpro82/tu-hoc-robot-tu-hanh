"""Vẽ các ô đã mở và đường đi của Dijkstra (trái) và A* (phải).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import a_sao as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def _mo_theo_thu_tu(ns, h):
    """Chạy lại A*/Dijkstra của bạn nhưng ghi lại thứ tự mở ô (bọc hàm ke để biết ô nào được mở)."""
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    ke_goc, thu_tu = lay("ke"), []

    def ke_ghi(o, ban_do):
        thu_tu.append(o)
        return ke_goc(o, ban_do)
    g = lay("tim_duong").__globals__
    g["ke"] = ke_ghi
    try:
        duong, so_mo, cp = lay("tim_duong")(goc.START, goc.GOAL, goc.BAN_DO, h)
    finally:
        g["ke"] = ke_goc
    return duong, list(dict.fromkeys(thu_tu)) + [goc.GOAL], so_mo, cp


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    h = lay("h_euclid")
    fig, axes = V.tao(1, 2, rong=11.5, cao=5.4)
    for ax, (ten, hh, mau) in zip(axes, [("Dijkstra", lambda o: 0.0, V.MAU["tim"]),
                                         ("A*", lambda o: h(o, goc.GOAL), V.MAU["cam"])]):
        duong, mo, so_mo, cp = _mo_theo_thu_tu(ns, hh)
        for r in range(goc.ROWS):
            for c in range(goc.COLS):
                if goc.BAN_DO[r][c] == "#":
                    ax.add_patch(Rectangle((c, r), 1, 1, fc="#475569", ec="none"))
        for k, (r, c) in enumerate(mo):
            ax.add_patch(Rectangle((c, r), 1, 1, fc=mau, ec="none", alpha=0.18 + 0.5 * k / len(mo)))
        ax.plot([c + 0.5 for r, c in duong], [r + 0.5 for r, c in duong], color="white", lw=2.6)
        for (r, c), chu in [(goc.START, "S"), (goc.GOAL, "G")]:
            ax.text(c + 0.5, r + 0.5, chu, color=V.NEN, ha="center", va="center", fontsize=10, weight="bold",
                    bbox=dict(boxstyle="circle,pad=0.2", fc=V.MAU["luc"], ec="none"))
        ax.set_xlim(0, goc.COLS)
        ax.set_ylim(goc.ROWS, 0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(f"{ten}: mở {so_mo} ô, đường {cp * goc.O_M:.2f} m", color="white", fontsize=12.5, loc="left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import a_sao_cua_ban
        ve(a_sao_cua_ban)
