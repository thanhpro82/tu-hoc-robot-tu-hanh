"""Vẽ bản đồ ghép từ các lần quét LiDAR: (trái) theo odometry (cộng dồn bằng hàm cong của bạn), (phải) sau tối ưu đồ thị
có khép vòng (bằng sai_so_canh của bạn). Đường trắng: quỹ đạo thật; cam: quỹ đạo ước lượng.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import slam as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import dead_reckoning, toi_uu  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    DR = dead_reckoning(lay("cong"))
    OPT = toi_uu(lay("sai_so_canh"), DR)
    that = np.array(goc.THAT)
    fig, axes = V.tao(1, 2, rong=13, cao=4.9)
    for ax, (ten, P) in zip(axes, [("Chỉ odometry", DR), ("Sau tối ưu đồ thị (khép vòng)", OPT)]):
        g = goc.ve_ban_do(P)
        ax.imshow(np.minimum(g, 3), origin="lower", extent=[0, goc.RONG, 0, goc.DAI], cmap="magma")
        ax.plot(that[:, 0], that[:, 1], color="white", lw=1.2, ls="--")
        ax.plot(P[:, 0], P[:, 1], "o-", color=V.MAU["cam"], ms=2.5, lw=1.4)
        e = goc.loi(P)
        ax.set_title(f"{ten}: lệch cuối {e[-1]:.2f} m · bản đồ nét {goc.do_net(g) * 100:.0f}%", color="white", fontsize=11.5, loc="left")
        ax.set_xlim(-1.5, goc.RONG + 1)
        ax.set_ylim(-1.5, goc.DAI + 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import slam_cua_ban
        ve(slam_cua_ban)
