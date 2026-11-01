"""Vẽ: (trái) đường A* gấp khúc, đường làm mượt của bạn, và đường robot chạy thật trong ROS 2 (ws/log.csv);
(phải) sai số bám đường theo thời gian, lấy từ log.

Chạy: python -X utf8 ve_do_thi.py            -> làm mượt bằng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import csv
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "ws"), str(_D.parents[1])]
import a_sao  # noqa: E402
import duong_di as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import DUONG_O  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


def doc_log():
    with open(_D.parent / "ws" / "log.csv", encoding="utf8") as f:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]


def ve(ns, ra="ket_qua.png"):
    lam_muot = ns["lam_muot"] if isinstance(ns, dict) else getattr(ns, "lam_muot")
    muot = lam_muot(DUONG_O, 3)
    log = doc_log()
    fig, (a, b) = V.tao(1, 2, rong=12, cao=5, gridspec_kw={"width_ratios": [1.15, 1]})
    for r in range(a_sao.ROWS):
        for c in range(a_sao.COLS):
            if a_sao.BAN_DO[r][c] == "#":
                x, y = goc.o_sang_met((r, c))
                a.add_patch(Rectangle((x - goc.O / 2, y - goc.O / 2), goc.O, goc.O, fc="#475569", ec="none"))
    a.plot([p[0] for p in DUONG_O], [p[1] for p in DUONG_O], color=V.MAU["vang"], lw=1.4, ls="--", label=f"A* gấp khúc {goc.do_dai(DUONG_O):.2f} m")
    a.plot([p[0] for p in muot], [p[1] for p in muot], color=V.MAU["xanh"], lw=3, alpha=0.7, label=f"Làm mượt {goc.do_dai(muot):.2f} m")
    a.plot([r["x"] for r in log], [r["y"] for r in log], color="white", lw=1.3, label="Robot chạy trong ROS 2")
    a.set_xlim(0, a_sao.COLS * goc.O)
    a.set_ylim(0, a_sao.ROWS * goc.O)
    a.set_aspect("equal")
    V.trang_tri(a, "Từ A đến B: lập kế hoạch rồi bám theo", "x (m)", "y (m)")
    V.chu_giai(a, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=8.5)
    err = [r["err"] * 100 for r in log]
    b.plot([r["t"] for r in log], err, color=V.MAU["xanh"], lw=2)
    b.text(0.97, 0.62, f"lớn nhất {max(err):.1f} cm · trung bình {sum(err) / len(err):.1f} cm", transform=b.transAxes,
           color="white", ha="right", fontsize=10)
    V.trang_tri(b, f"Sai số bám đường ({log[-1]['t']:.1f} s, log ROS 2 thật)", "thời gian (s)", "sai số (cm)")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import duong_cua_ban
        ve(duong_cua_ban)
