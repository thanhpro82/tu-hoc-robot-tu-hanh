"""Vẽ: (trái) lưới đường thẳng bị méo thùng bằng hàm meo của bạn; (phải) sai số chiếu lại của 10 ảnh bàn cờ:
Zhang bỏ qua méo và sau khi tinh chỉnh có méo (Levenberg-Marquardt, trong code video).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import hieu_chinh as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import DS_UV  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    meo = ns["meo"] if isinstance(ns, dict) else getattr(ns, "meo")
    fig, (a, b) = V.tao(1, 2, rong=12, cao=4.9)
    c = goc.K_THAT[:2, 2]
    for d in goc.luoi_thang():
        a.plot(d[:, 0], d[:, 1], color=V.MAU["xam"], lw=0.9, ls=":")
        m = meo(d, goc.K_MEO, c)
        a.plot(m[:, 0], m[:, 1], color=V.MAU["cam"], lw=1.6)
    a.set_xlim(-40, 680)
    a.set_ylim(520, -40)
    a.set_aspect("equal")
    lech = float(np.linalg.norm(meo(goc.GOC, goc.K_MEO, c) - goc.GOC))
    V.trang_tri(a, f"Méo thùng: góc ảnh bị kéo vào {lech:.1f} px", "u (px)", "v (px)")
    for h, mau in [(goc.LICH_SU[0], V.MAU["do"]), (goc.LICH_SU[1], V.MAU["luc"])]:
        du = goc.du_doan(h["K"], h["ngoai"], h["k"])
        loi = np.sqrt(((np.vstack(du) - np.vstack(DS_UV)) ** 2).sum(axis=1))
        b.hist(loi, bins=np.linspace(0, 16, 41), color=mau, alpha=0.7, label=f"{h['buoc']}: RMS {h['rms']:.2f} px")
    V.trang_tri(b, "Sai số chiếu lại của 540 góc ô cờ", "sai số (px)", "số góc ô")
    V.chu_giai(b, loc="upper right")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import hieu_chinh_cua_ban
        ve(hieu_chinh_cua_ban)
