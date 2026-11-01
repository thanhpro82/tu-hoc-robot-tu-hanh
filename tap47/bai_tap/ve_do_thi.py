"""Vẽ số liệu video tập 4.7 (../sim/ket_qua.txt, 500 đường thử, TB 4 seed): (trái) chạy xong khi có / không có lớp an toàn;
(giữa) lái bằng mô hình thế giới theo lượng dữ liệu lái ngẫu nhiên; (phải) sai số tưởng tượng theo số bước. Tham số `ns` không dùng.

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png
"""
import json
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parents[1])]
from chung import ve as V  # noqa: E402


def ve(ns=None, ra="ket_qua.png"):
    k = json.loads((_D.parent / "sim" / "ket_qua.txt").read_text(encoding="utf8"))
    at = k["at"]
    fig, (a, b, c) = V.tao(1, 3, rong=15, cao=5)
    ten = ["lái thẳng", "BC 2 vòng", "BC 14 vòng", "DAgger"]
    kh = ["thang", "bc2", "bc14", "dagger"]
    x = np.arange(len(kh))
    for dx, duoi, mau, nhan in [(-0.2, "", V.MAU["xam"], "chỉ mạng nơ-ron"), (0.2, "_an_toan", V.MAU["do"], "+ lớp an toàn")]:
        y = [at[t + duoi] for t in kh]
        a.bar(x + dx, y, 0.38, color=mau, label=nhan)
        for xi, yi in zip(x, y):
            a.text(xi + dx, yi + 1.5, f"{yi:.0f}", color=V.CHU, ha="center", fontsize=9)
    a.set_xticks(x, ten)
    a.set_ylim(0, 112)
    V.trang_tri(a, "Lớp an toàn bọc ngoài mạng", None, "% chạy xong 1 vòng")
    V.chu_giai(a, loc="upper left")
    b.plot(k["tg_mau"], k["tg_ty"], "o-", color=V.MAU["do"], lw=2.2, label="lái bằng tưởng tượng")
    for n, m, y in zip(k["tg_duong"], k["tg_mau"], k["tg_ty"]):
        b.text(m, y - 13,f"{n} đường\n{y}%", color=V.CHU, ha="center", fontsize=8.5)
    b.axhline(k["chua_hoc"], color=V.MAU["vang"], ls="--", lw=1.2, label=f"mô hình chưa học: {k['chua_hoc']}%")
    b.axhline(k["ngau_nhien"], color=V.MAU["xam"], ls=":", lw=1.2, label=f"lái ngẫu nhiên: {k['ngau_nhien']:.0f}%")
    b.set_xscale("log")
    b.set_xlim(110, 3200)
    b.set_ylim(-5, 105)
    V.trang_tri(b, "Mô hình thế giới: càng nhiều dữ liệu rẻ", "số bước lái ngẫu nhiên đã ghi", "% chạy xong 1 vòng")
    V.chu_giai(b, loc="center right", fontsize=8.5)
    t = np.arange(1, len(k["tg_sai_cm"]) + 1) * k["dt"]
    c.plot(t, k["tg_sai_cm"], "o-", color=V.MAU["cam"], lw=2.2)
    e = k["tg_sai_cm"]
    c.text(t[0] + 0.04, e[0] - 1, f"{e[0]} cm", color=V.CHU, ha="left", va="top", fontsize=9)
    c.text(t[-1], e[-1] + 2.5, f"{e[-1]} cm", color=V.CHU, ha="center", fontsize=9)
    c.set_ylim(0, 60)
    V.trang_tri(c, "Tưởng tượng càng xa càng sai", "nhìn trước (giây)", "sai số tia LiDAR (cm)")
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
