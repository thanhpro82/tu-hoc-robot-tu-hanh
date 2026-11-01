"""Vẽ: (hàng trên) 8 ảnh vạch dẫn đường của 4 lớp kèm dự đoán của SimpleCNN bạn viết (học 4 vòng);
(hàng dưới) 8 bản đồ kích hoạt của lớp conv1 cho ảnh đầu tiên: mỗi bộ lọc "để ý" một kiểu nét khác nhau.

Chạy: python -X utf8 ve_do_thi.py            -> dùng SimpleCNN của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import torch

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parents[1])]
from chung import ve as V  # noqa: E402
from kiem_tra import DL, du_lieu, hoc_nhanh  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    Lop = ns["SimpleCNN"] if isinstance(ns, dict) else getattr(ns, "SimpleCNN")
    m, acc = hoc_nhanh(Lop)
    X, y = du_lieu(400, 5)
    chon = [int((y == c).nonzero()[k]) for c in range(4) for k in range(2)]
    with torch.no_grad():
        doan = m(X[chon]).argmax(1)
        a1 = torch.relu(m.conv1(X[chon[0]:chon[0] + 1]))[0]
    fig, ax = V.tao(2, 8, rong=15, cao=5.1)
    for k, i in enumerate(chon):
        ax[k].imshow(X[i, 0], cmap="gray", vmin=0, vmax=1)
        dung = int(doan[k]) == int(y[i])
        ax[k].set_title(f"{DL['LOP'][int(y[i])]}\nđoán: {DL['LOP'][int(doan[k])]}", fontsize=9,
                        color=V.MAU["luc"] if dung else V.MAU["do"])
        ax[8 + k].imshow(a1[k], cmap="magma")
        ax[8 + k].set_title(f"bộ lọc {k + 1}", fontsize=9, color=V.CHU)
    for a in ax:
        a.set_xticks([])
        a.set_yticks([])
        a.grid(False)
    fig.suptitle(f"SimpleCNN học 4 vòng: đúng {acc * 100:.1f}% ảnh thử · hàng dưới: 8 bản đồ kích hoạt conv1 của ảnh đầu tiên",
                 color="white", fontsize=12, x=0.01, ha="left")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import cnn_cua_ban
        ve(cnn_cua_ban)
