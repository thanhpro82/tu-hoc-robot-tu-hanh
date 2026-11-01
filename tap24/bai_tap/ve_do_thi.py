"""Vẽ: (trái) ảnh camera trái; (giữa) bản đồ độ sâu (disparity của video đổi ra mét bằng hàm do_sau của bạn,
vùng xám là pixel bị loại: trơn, bị che, viền); (phải) đường chi phí so khớp tại điểm giữa hộp bằng hàm của bạn.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import stereo as goc  # noqa: E402
from chung import ve as V  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    fig, (a, b, c) = V.tao(1, 3, rong=14, cao=4.2, gridspec_kw={"width_ratios": [1, 1.15, 1]})
    a.imshow(goc.L, cmap="gray", vmin=0, vmax=255)
    a.plot(goc.DIEM[1], goc.DIEM[0], "+", color=V.MAU["cam"], ms=12, mew=2)
    a.set_title("Ảnh camera trái", color="white", fontsize=12, loc="left")
    with np.errstate(divide="ignore", invalid="ignore"):
        z = np.where(goc.HOP_DUNG & (goc.D > 0.5), lay("do_sau")(np.maximum(goc.D, 1e-6), goc.B, goc.F), np.nan)
    b.set_facecolor("#334155")
    im = b.imshow(z, cmap="turbo_r", vmin=1.0, vmax=4.5)
    cb = fig.colorbar(im, ax=b, fraction=0.04, pad=0.02)
    cb.ax.tick_params(colors="#94a3b8")
    cb.set_label("độ sâu (m)", color=V.CHU)
    b.set_title("Độ sâu z = b·f/d (xám: bị loại)", color="white", fontsize=12, loc="left")
    for ax in (a, b):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    cp = np.asarray(lay("chi_phi_diem")(goc.L, goc.R, goc.DIEM[0], goc.DIEM[1], goc.D_MAX, goc.CUA_SO))
    d0 = int(np.argmin(cp))
    c.plot(range(goc.D_MAX), cp, color=V.MAU["xanh"], lw=2.2)
    c.plot(d0, cp[d0], "o", color=V.MAU["cam"], ms=8)
    c.axvline(goc.B * goc.F / goc.HOP["z"], color="white", ls=":", lw=1.2)
    c.text(d0 + 2, cp.max() * 0.85, f"nhỏ nhất ở d = {d0} px\n(thật 37,5 px)", color="white", fontsize=9.5)
    V.trang_tri(c, "Chi phí so khớp tại điểm giữa hộp", "disparity d (px)", "trung bình bình phương hiệu")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import stereo_cua_ban
        ve(stereo_cua_ban)
