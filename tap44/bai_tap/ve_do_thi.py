"""Vẽ quá trình học (2000 tập, bằng 2 hàm của bạn): (trái) tỉ lệ rơi cầu thang trung bình 100 tập gần nhất;
(phải) chính sách tham lam học được (mũi tên) trên kho hàng.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[2] / "tap42" / "sim"), str(_D.parents[1])]
import qlearn as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import hoc  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

M = goc.M
MUI = {"len": (0, 0.32), "xuong": (0, -0.32), "trai": (-0.32, 0), "phai": (0.32, 0)}


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    Q, roi = hoc(lay("chon_hanh_dong"), lay("cap_nhat_q"))
    pi = lay("chinh_sach_tham_lam")(Q, M.O_TRONG, M.IDX, M.U)
    J = M.danh_gia(lambda x: pi[x], goc.TRUOT)[M.S]
    fig, (a, b) = V.tao(1, 2, rong=13, cao=4.4, gridspec_kw={"width_ratios": [1, 1.25]})
    tb = np.convolve(np.array(roi, float), np.ones(100) / 100, mode="valid") * 100
    a.plot(np.arange(100, len(roi) + 1), tb, color=V.MAU["do"], lw=2)
    V.trang_tri(a, "Tỉ lệ rơi cầu thang (TB 100 tập)", "số tập đã chơi", "% rơi")
    for x in range(M.W):
        for y in range(M.H):
            mau = "#7f1d1d" if (x, y) in M.CAU_THANG else "#475569" if (x, y) in M.KE else "#111827"
            b.add_patch(Rectangle((x, y), 1, 1, fc=mau, ec="#1e293b"))
            if (x, y) in pi and (x, y) not in M.CAU_THANG and (x, y) != M.G:
                dx, dy = MUI[pi[(x, y)]]
                b.annotate("", xy=(x + 0.5 + dx, y + 0.5 + dy), xytext=(x + 0.5 - dx, y + 0.5 - dy),
                           arrowprops=dict(arrowstyle="-|>", color=V.MAU["vang"], lw=1.6))
    for (x, y), chu in [(M.S, "S"), (M.G, "G")]:
        b.text(x + 0.85, y + 0.8, chu, color=V.MAU["luc"], fontsize=11, weight="bold", ha="center")
    b.set_xlim(0, M.W); b.set_ylim(0, M.H); b.set_aspect("equal"); b.axis("off")
    b.set_title(f"Chính sách tự học: J = {J:.2f} (J* biết mô hình = 16.24)", color="white", fontsize=12, loc="left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import qlearn_cua_ban
        ve(qlearn_cua_ban)
