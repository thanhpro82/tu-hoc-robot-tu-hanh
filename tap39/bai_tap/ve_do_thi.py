"""Vẽ lần chạy Nav2 thật: (trái) bản đồ slam_toolbox của tập 3.7, đường đầu tiên qua cửa dưới, đường mới khi cửa đóng, đường robot đã đi;
(phải) sai số AMCL (hàm that_luc của bạn) và độ toả đám hạt (hàm do_toa của bạn) theo thời gian.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import phan_tich as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import sai_so_amcl  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    anh = np.array(Image.open(_D.parent / "ws" / "map" / "nha.pgm"))
    ox, oy, res = -1.1346, -2.5567, 0.05
    h, w = anh.shape
    fig, (a, b) = V.tao(1, 2, rong=13, cao=4.8, gridspec_kw={"width_ratios": [1.35, 1]})
    a.imshow(anh, cmap="gray", extent=[ox, ox + w * res, oy, oy + h * res])
    k = [lay("qua_cua")(np.array(p["xy"]), goc.CUA) for p in goc.PLAN].index(False)
    p0, p1 = np.array(goc.PLAN[0]["xy"]), np.array(goc.PLAN[k]["xy"])
    a.plot(p0[:, 0], p0[:, 1], color=V.MAU["do"], lw=2, ls="--", label=f"đường đầu {lay('do_dai')(p0):.1f} m (qua cửa dưới)")
    a.plot(p1[:, 0], p1[:, 1], color=V.MAU["vang"], lw=2, ls="--", label=f"đường mới {lay('do_dai')(p1):.1f} m (cửa đóng)")
    th = goc.THAT[goc.CHAY]
    a.plot(th[:, 0], th[:, 1], color=V.MAU["luc"], lw=2.4, label="robot đã đi")
    a.plot(*goc.CUA, "X", color=V.MAU["do"], ms=12)
    a.plot(goc.BEP[0], goc.BEP[1], "*", color=V.MAU["vang"], ms=16)
    a.set_title(f"Nav2 tới bếp sau {goc.DT:.1f} s, lệch đích {goc.E_TOI * 100:.1f} cm", color="white", fontsize=11.5, loc="left")
    a.set_xticks([]); a.set_yticks([]); a.grid(False)
    V.chu_giai(a, loc="lower right", fontsize=8.3)
    e = sai_so_amcl(lay("that_luc"))
    s = np.array([lay("do_toa")(np.array(hh["xy"])) for hh in goc.HAT])
    b.plot(goc.TA, e * 100, color=V.MAU["xanh"], lw=2, label="sai số AMCL (cm)")
    b.plot(goc.TH, s * 100, color=V.MAU["cam"], lw=2, label="độ toả đám hạt (cm)")
    b.axvline(goc.T_DOI, color=V.MAU["xam"], ls=":", lw=1.2)
    b.text(goc.T_DOI + 0.5, max(e.max(), s.max()) * 85, "đổi đường", color=V.CHU, fontsize=9)
    V.trang_tri(b, "AMCL sửa vị trí bấm lệch 43 cm", "thời gian từ lúc ra lệnh (s)", "cm")
    V.chu_giai(b, loc="upper right")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import nav_cua_ban
        ve(nav_cua_ban)
