"""Vẽ: (trái) khối lập phương 40 cm chiếu lên ảnh 640×480 bằng hàm chieu của bạn, khi ở xa và khi lại gần;
(phải) chiều cao trên ảnh của hộp 30 cm theo khoảng cách (h = β·H/Z).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import pinhole as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import _rong, phim  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

CANH = [(i, j) for i in range(8) for j in range(i + 1, 8) if bin(i ^ j).count("1") == 1]   # 12 cạnh của khối lập phương


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    K = lay("ma_tran_K")(goc.ALPHA, goc.BETA, goc.GAMMA, goc.U0, goc.V0)
    k = phim(lay("chieu"), K)
    fig, (a, b) = V.tao(1, 2, rong=12, cao=4.8, gridspec_kw={"width_ratios": [1.2, 1]})
    for khung, mau, ten in [(k[0], V.MAU["xam"], f"cách 3 m: rộng {_rong(k[0]):.0f} px"),
                            (k[45], V.MAU["xanh"], None), (k[-1], V.MAU["luc"], f"cách 1,2 m: rộng {_rong(k[-1]):.0f} px")]:
        for i, j in CANH:
            a.plot([khung[i][0], khung[j][0]], [khung[i][1], khung[j][1]], color=mau, lw=2)
        if ten:
            a.plot([], [], color=mau, lw=2, label=ten)
    a.add_patch(Rectangle((0, 0), 640, 480, fill=False, ec="white", lw=1.2))
    a.plot(goc.U0, goc.V0, "+", color=V.MAU["vang"], ms=12, mew=2)
    a.set_xlim(-10, 650)
    a.set_ylim(490, -10)
    a.set_aspect("equal")
    V.trang_tri(a, "Khối lập phương 40 cm trên ảnh 640×480", "u (px)", "v (px)")
    V.chu_giai(a, loc="lower right", fontsize=8.8)
    zs = [0.5 + 0.05 * i for i in range(91)]
    b.plot(zs, [goc.chieu_cao_anh(goc.HOP, z) for z in zs], color=V.MAU["cam"], lw=2.4)
    for z in goc.KHOANG_CACH:
        h = goc.chieu_cao_anh(goc.HOP, z)
        b.plot(z, h, "o", color="white", ms=7)
        b.text(z + 0.12, h + 6, f"{z:.0f} m → {h:.1f} px", color="white", fontsize=9.5)
    V.trang_tri(b, "Hộp 30 cm: xa gấp đôi thì nhỏ đi một nửa", "khoảng cách Z (m)", "chiều cao trên ảnh (px)")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import camera_cua_ban
        ve(camera_cua_ban)
