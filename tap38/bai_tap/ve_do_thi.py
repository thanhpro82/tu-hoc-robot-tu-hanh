"""Vẽ đường đi của các track nhìn từ trên xuống: (trái) ghép theo điểm gần nhất, không dự đoán; (phải) Kalman + cổng + Hungary
chạy bằng m2 và cap_nhat của bạn. Mỗi màu là một ID; đường xám đứt là 5 người thật. Càng ít đổi màu dọc một người càng tốt.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import theo_doi as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import chay_voi  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    ra_kf = chay_voi(lay("m2"), lay("cap_nhat"))
    fig, axes = V.tao(1, 2, rong=13, cao=5.2)
    bang_mau = plt.get_cmap("tab20")
    for ax, (ten, kq) in zip(axes, [("Gần nhất, không dự đoán", goc.RA_NN), ("Kalman + cổng + Hungary", ra_kf)]):
        for i in range(goc.GT.shape[1]):
            ax.plot(goc.GT[:, i, 0], goc.GT[:, i, 1], color=V.MAU["xam"], lw=1.2, ls="--")
        duong = {}
        for k in kq:
            for tid, p, _ in k:
                duong.setdefault(tid, []).append(p)
        for tid, ps in duong.items():
            ps = np.array(ps)
            if len(ps) >= 3:
                ax.plot(ps[:, 0], ps[:, 1], color=bang_mau(tid % 20), lw=1.8)
        d = goc.cham_diem(kq)
        V.trang_tri(ax, f"{ten}: MOTA {d['MOTA'] * 100:.1f}% · đổi ID {d['IDSW']} lần", "x (m)", "y (m)")
        ax.set_aspect("equal", adjustable="datalim")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import theo_doi_cua_ban
        ve(theo_doi_cua_ban)
