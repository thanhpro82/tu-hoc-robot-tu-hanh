"""Vẽ: (trái) hình số 8 mẫu, robot chỉ tính sẵn, robot tính sẵn + sửa sai; (phải) sai số theo thời gian.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import bam_quy_dao as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import _tb5, chay  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    p_ts, ss_ts = chay(lay("tinh_san"))
    p_bam, ss_bam = chay(lay("tinh_san"), lay("dieu_khien_ao"), lay("doi_lenh"))
    fig, (a, b) = V.tao(1, 2, rong=12, cao=4.9, gridspec_kw={"width_ratios": [1.25, 1]})
    a.plot([p[0] for p in goc.THAM_CHIEU], [p[1] for p in goc.THAM_CHIEU], color="white", lw=1.6, ls="--", label="Hình số 8 mẫu")
    a.plot([p[0] for p in p_ts], [p[1] for p in p_ts], color=V.MAU["do"], lw=2, label="Chỉ tính sẵn")
    a.plot([p[0] for p in p_bam], [p[1] for p in p_bam], color=V.MAU["xanh"], lw=2.4, label="Tính sẵn + sửa sai")
    a.plot(p_bam[0][0], p_bam[0][1], "o", color=V.MAU["luc"], ms=7, label="Xuất phát (lệch 20 cm)")
    V.trang_tri(a, "Robot vẽ số 8 trong 20 giây", "x (m)", "y (m)")
    a.set_aspect("equal", adjustable="datalim")
    V.chu_giai(a, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=8.8)
    t = [i * goc.dt for i in range(len(ss_ts))]
    b.plot(t, [s * 100 for s in ss_ts], color=V.MAU["do"], lw=2, label=f"Chỉ tính sẵn: 5 s cuối {_tb5(ss_ts):.1f} cm")
    b.plot(t, [s * 100 for s in ss_bam], color=V.MAU["xanh"], lw=2.4, label=f"+ sửa sai: 5 s cuối {_tb5(ss_bam):.1f} cm")
    V.trang_tri(b, "Khoảng cách tới robot ảo", "thời gian (s)", "sai số (cm)")
    V.chu_giai(b, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=1, fontsize=8.8)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import bam_cua_ban
        ve(bam_cua_ban)
