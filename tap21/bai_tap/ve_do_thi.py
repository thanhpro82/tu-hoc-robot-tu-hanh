"""Vẽ: (trái) 20 lần đo của 4 cảm biến quanh giá trị thật 1 m; (phải) gyro trôi 60 s, trước và sau khi trừ lệch bạn ước lượng.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import cam_bien as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import mau_gyro  # noqa: E402

TEN = {"chinh_xac_on_dinh": "Chính xác + ổn định", "on_dinh_sai": "Ổn định nhưng sai",
       "chinh_xac_nhieu": "Chính xác nhưng nhiễu", "sai_va_nhieu": "Sai và nhiễu"}


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    fig, (a, b) = V.tao(1, 2, rong=12, cao=4.8, gridspec_kw={"width_ratios": [1.1, 1]})
    mau = [V.MAU["luc"], V.MAU["vang"], V.MAU["xanh"], V.MAU["do"]]
    for i, (k, ds) in enumerate(goc.DO.items()):
        e, sd = lay("danh_gia")(ds, goc.THAT)
        a.scatter([(d - goc.THAT) * 100 for d in ds], [i] * len(ds), color=mau[i], s=26, alpha=0.75)
        a.text(19, i, f"e = {e * 100:+.1f} cm · ±{sd * 100:.1f} cm", color=V.CHU, va="center", fontsize=9.5)
    a.axvline(0, color="white", lw=1.4, ls="--")
    a.set_yticks(range(4))
    a.set_yticklabels([TEN[k] for k in goc.DO], color=V.CHU)
    a.set_xlim(-12, 39)
    V.trang_tri(a, "20 lần đo một vật cách đúng 1 m", "đo được − giá trị thật (cm)")
    mau_60 = mau_gyro(*goc.GYRO_RE, goc.GIAY)
    lech = lay("uoc_luong_lech")(mau_gyro(*goc.GYRO_RE, 10, seed=99))
    tp = lay("goc_tich_phan")
    t = [i for i in range(0, goc.GIAY + 1)]
    n = round(1 / goc.DT)
    tho = [tp(mau_60[: k * n], goc.DT) for k in t]
    hc = [tp(mau_60[: k * n], goc.DT, lech) for k in t]
    b.plot(t, tho, color=V.MAU["do"], lw=2.4, label=f"Không hiệu chỉnh: {tho[-1]:.1f}°")
    b.plot(t, hc, color=V.MAU["luc"], lw=2.4, label=f"Trừ lệch {lech:.2f} °/s: {hc[-1]:+.1f}°")
    b.axhline(0, color="white", lw=1, ls=":")
    V.trang_tri(b, "Robot đứng yên, gyro tưởng đã quay", "thời gian (s)", "góc cộng dồn (°)")
    V.chu_giai(b, loc="upper left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import cam_bien_cua_ban
        ve(cam_bien_cua_ban)
