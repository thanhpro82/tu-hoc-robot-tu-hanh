"""Vẽ niềm tin của robot ở 4 thời điểm (bằng bộ lọc của bạn): sau lần thấy cửa đầu tiên (3 đỉnh), bước 3, bước 4, bước 12.
Vùng tô xám là các cánh cửa, vạch trắng là vị trí thật (robot không biết).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import bayes as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import DS_Z, X_THAT  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    f = ns["loc_bayes"] if isinstance(ns, dict) else getattr(ns, "loc_bayes")
    ds = f(DS_Z)
    fig, axes = V.tao(4, 1, rong=11, cao=7.4, sharex=True)
    for ax, k in zip(axes, [0, 3, 4, 12]):
        for a, b in goc.CUA:
            ax.axvspan(a, b, color="#334155", alpha=0.7, lw=0)
        ax.fill_between(goc.X, ds[k] * 100, color=V.MAU["cam"], alpha=0.35)
        ax.plot(goc.X, ds[k] * 100, color=V.MAU["cam"], lw=1.8)
        ax.axvline(X_THAT[k], color="white", lw=1.6)
        z = "thấy cửa" if DS_Z[k] else "không thấy"
        V.trang_tri(ax)
        ax.text(0.01, 0.78, f"bước {k} ({z}): {goc.so_dinh(ds[k])} đỉnh, ±25 cm quanh vị trí thật {goc.p_quanh(ds[k], X_THAT[k]) * 100:.1f}%",
                transform=ax.transAxes, color="white", fontsize=10, bbox=dict(fc=V.NEN, ec="none", alpha=0.85))
        ax.set_ylabel("%", color=V.CHU)
    axes[-1].set_xlabel("vị trí trong hành lang (m)", color=V.CHU)
    axes[0].set_title("Niềm tin bel(x) của robot (xám: cửa · vạch trắng: vị trí thật)", color="white", fontsize=12.5, loc="left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import bayes_cua_ban
        ve(bayes_cua_ban)
