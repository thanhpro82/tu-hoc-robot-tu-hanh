"""Vẽ đường đi của robot với 4 cách điều khiển: vòng hở, P, PD, PID.

Chạy: python -X utf8 ve_do_thi.py          -> dùng PID của bạn (pid_cua_ban.py), ra file ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai -> dùng lời giải gốc
Muốn thử hệ số khác: sửa bảng CACH bên dưới rồi chạy lại.
"""
import sys
from pathlib import Path

import matplotlib
if "ipykernel" not in sys.modules:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
import pid as goc  # noqa: E402

# (tên, Kp, Ki, Kd, màu); None = vòng hở
CACH = [("Vòng hở", None, None, None, "#64748b"),
        ("Chỉ P", 1.5, 0.0, 0.0, "#f59e0b"),
        ("PD", 1.5, 0.0, 2.8, "#a855f7"),
        ("PID", 1.5, 0.6, 2.8, "#3b82f6")]


def ve(PID, ra="ket_qua.png"):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=130)
    fig.patch.set_facecolor("#0b1220")
    ax.set_facecolor("#0b1220")
    ax.axhline(0, color="#22c55e", lw=2, ls="--", label="Vạch cần bám (y = 0)")
    for ten, kp, ki, kd, mau in CACH:
        path = goc.chay(None if kp is None else PID(kp, ki, kd))
        xs, ys = [p[0] for p in path], [p[1] * 100 for p in path]
        ax.plot(xs, ys, color=mau, lw=2.4, label=f"{ten}: lệch TB 3 s cuối {goc.lech_cuoi(path):+.1f} cm")
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-60, 40)
    ax.set_xlabel("Quãng đường đi tới, x (m)", color="#cbd5e1")
    ax.set_ylabel("Lệch khỏi vạch, y (cm)", color="#cbd5e1")
    ax.set_title("Robot xuất phát lệch 30 cm, bánh yếu một bên", color="white", fontsize=13, loc="left")
    ax.tick_params(colors="#94a3b8")
    for s in ax.spines.values():
        s.set_color("#334155")
    ax.grid(color="#1e293b")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, facecolor="#111827", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(ra, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("đã lưu", ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        ve(goc.PID, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        from pid_cua_ban import PID
        ve(PID)
