"""Vẽ: (trái) hình vuông vòng hở, lý tưởng vs robot có sai số chạy 3 vòng; (phải) đồ thị tốc độ hình thang.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import vong_ho as goc  # noqa: E402
from chung import ve as V  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    kh = lay("ke_hoach_vuong")(1.0, 0.5, 1.0)
    ly_tuong, _ = goc.chay(kh)
    thuc, lech = goc.chay(kh, so_vong=3, sai_so=goc.ROBOT_THAT, seed=3)
    fig, (a, b) = V.tao(1, 2, rong=11.5, cao=5.2, gridspec_kw={"width_ratios": [1, 1.15]})
    a.plot([p[0] for p in thuc], [p[1] for p in thuc], color=V.MAU["do"], lw=1.6, label="Robot có sai số, 3 vòng")
    a.plot([p[0] for p in ly_tuong], [p[1] for p in ly_tuong], color=V.MAU["xanh"], lw=2.6, ls="--", label="Lý tưởng")
    a.plot(0, 0, "o", color=V.MAU["luc"], ms=8, label="Xuất phát / đích")
    a.plot(thuc[-1][0], thuc[-1][1], "x", color="white", ms=9, mew=2)
    a.text(thuc[-1][0] + 0.05, thuc[-1][1], f"lệch {lech[-1] * 100:.0f} cm", color="white", fontsize=9.5, va="center",
           bbox=dict(fc=V.NEN, ec="none", alpha=0.8))
    V.trang_tri(a, "Vòng hở: hình vuông 1 m", "x (m)", "y (m)")
    a.set_aspect("equal", adjustable="datalim")
    V.chu_giai(a, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, fontsize=8.5)
    T = lay("thoi_gian_nhanh_nhat")(1.0, goc.V_MAX, goc.A_MAX)
    ts = [i * 0.01 for i in range(round(T / 0.01) + 1)]
    v = [lay("van_toc_luc")(t, 1.0, goc.V_MAX, goc.A_MAX) for t in ts]
    b.fill_between(ts, v, color=V.MAU["cam"], alpha=0.25)
    b.plot(ts, v, color=V.MAU["cam"], lw=2.6)
    b.axhline(goc.V_MAX, color=V.MAU["xam"], ls=":", lw=1)
    b.text(T / 2, 0.22, f"diện tích = {sum(v) * 0.01:.2f} m", color="white", ha="center", fontsize=10)
    b.text(0.1, goc.V_MAX + 0.02, "v_max", color=V.CHU, fontsize=9)
    V.trang_tri(b, f"Chạy 1 m nhanh nhất: {T:.1f} s (hình thang)", "thời gian (s)", "tốc độ v (m/s)")
    b.set_ylim(0, 0.65)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import vong_ho_cua_ban
        ve(vong_ho_cua_ban)
