"""Vẽ: ảnh thử #129 với khung thô của YOLO (trái) và sau NMS của bạn (giữa); đường precision-recall 3 lớp bằng ap_lop của bạn (phải).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png (nạp YOLO của video, ~20–60 giây)
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
from chung import ve as V  # noqa: E402
from kiem_tra import goc  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

MAU_LOP = [V.MAU["cam"], V.MAU["lam"], V.MAU["hong"]]
ANH_SO = 129


def _khung(ax, ds, ten):
    for c, s, cx, cy, w, h in ds:
        ax.add_patch(Rectangle(((cx - w / 2) * 128, (cy - h / 2) * 128), w * 128, h * 128, fill=False, ec=MAU_LOP[c], lw=1.8))
    ax.set_title(ten, color="white", fontsize=11.5, loc="left")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    g = goc()
    tho = [[tuple(d) for d in dd] for dd in g.THO]
    sach = [lay("nms")(d) for d in tho]
    fig, (a, b, c) = V.tao(1, 3, rong=14, cao=4.6)
    anh = g.X_THU[ANH_SO].permute(1, 2, 0).numpy()
    for ax, ds, ten in [(a, tho[ANH_SO], f"Khung thô: {len(tho[ANH_SO])}"), (b, sach[ANH_SO], f"Sau NMS: {len(sach[ANH_SO])} khung")]:
        ax.imshow(anh)
        _khung(ax, ds, ten)
    for k in range(3):
        ap, rec, pre = lay("ap_lop")(sach, g.V_THU, k)
        c.plot(rec, pre, color=MAU_LOP[k], lw=2.2, label=f"{g.LOP[k]}: AP {ap * 100:.1f}%")
    V.trang_tri(c, "Precision–recall (IoU ≥ 0,5)", "recall", "precision")
    c.set_xlim(0, 1.02)
    c.set_ylim(0, 1.02)
    V.chu_giai(c, loc="lower left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import yolo_cua_ban
        ve(yolo_cua_ban)
