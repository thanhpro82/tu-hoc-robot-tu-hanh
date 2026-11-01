"""Vẽ: (trái) bỏ đi một mùa thì robot giao đồ còn làm được không (100 lượt, số liệu video ../sim/ket_qua.txt);
(phải) lượt minh hoạ trong video (seed 11) trên bản đồ căn hộ, tô màu theo trạng thái của bộ não. Tham số `ns` không dùng.
Lượt minh hoạ đọc từ ../sim/luot_minh_hoa.json; chưa có thì chạy lại (khoảng 1 phút).

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png
"""
import json
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import giao_do as goc  # noqa: E402
from chung import ve as V  # noqa: E402

F_LUOT = _D.parent / "sim" / "luot_minh_hoa.json"
MAU_TT = {"ĐỊNH VỊ": V.MAU["vang"], "ĐI LẤY": V.MAU["xanh"], "DỪNG": V.MAU["do"], "NHẬN ĐỒ": V.MAU["tim"],
          "ĐI GIAO": V.MAU["luc"], "TÌM NGƯỜI": V.MAU["lam"], "TIẾP CẬN": V.MAU["hong"], "GIAO": "white"}


def luot_minh_hoa():
    if not F_LUOT.exists():
        print("chạy lại lượt minh hoạ seed 11 (khoảng 1 phút)…")
        L = goc.tao_luot(11)
        r = goc.chay_luot(L, "du", ghi=True)
        lg = r["log"]
        d = {"seed": 11, "ket": r["ket"], "t": r["t"], "x": lg["x"][::2], "uoc": lg["uoc"][::2], "s": lg["s"][::2],
             "nguoi_di": lg["nguoi_di"][::2], "nguoi_nhan": [round(float(v), 2) for v in L["nguoi_nhan"]]}
        F_LUOT.write_text(json.dumps(d, ensure_ascii=False), encoding="utf8")
    return json.loads(F_LUOT.read_text(encoding="utf8"))


def ve(ns=None, ra="ket_qua.png"):
    k = json.loads((_D.parent / "sim" / "ket_qua.txt").read_text(encoding="utf8"))["tk"]
    fig, (a, b) = V.tao(1, 2, rong=14, cao=5.4, gridspec_kw={"width_ratios": [1, 1.25]})
    ten = [("du", "đủ 4 mùa"), ("khong_m1", "bỏ A*\n(Mùa 1)"), ("khong_m2", "bỏ camera\n(Mùa 2)"),
           ("khong_m3", "bỏ định vị\n(Mùa 3)"), ("khong_m4", "bộ não tuần tự\n(Mùa 4)")]
    y = [k[t]["ok"] for t, _ in ten]
    a.bar(range(len(ten)), y, color=[V.MAU["do"]] + [V.MAU["xam"]] * 4)
    for i, (t, _) in enumerate(ten):
        ly = max(k[t]["ly_do"].items(), key=lambda kv: kv[1])
        a.text(i, y[i] + 2, f"{y[i]}%", color="white", ha="center", fontsize=10.5)
        if t != "du":
            a.text(i, y[i] + 9, f"{ly[0]}\n({ly[1]} lượt)", color=V.CHU, ha="center", fontsize=7.5)
    a.set_xticks(range(len(ten)), [n for _, n in ten], fontsize=8.5)
    a.set_ylim(0, 105)
    V.trang_tri(a, "Giao thành công (100 lượt)", None, "% lượt giao tận tay")
    m = luot_minh_hoa()
    b.imshow(goc.BAN_DO, origin="lower", extent=[0, goc.RONG, 0, goc.DAI], cmap="Greys", vmin=0, vmax=1.6, alpha=0.9)
    for p, ten_p in goc.TEN_PHONG.items():
        x0, y0, x1, y1 = goc.PHONG[p]
        b.text(x0 + 0.25, y1 - 0.45, ten_p, color="#1e293b", fontsize=9.5, weight="bold")
    x = np.array(m["x"])
    s = m["s"]
    for tt, mau in MAU_TT.items():
        on = np.array([v == tt for v in s])
        if on.any():
            b.scatter(x[on, 0], x[on, 1], s=9, color=mau, label=tt)
    b.plot(*goc.DIEM_LAY, "s", color=V.MAU["tim"], ms=9, mec="white")
    b.plot(*m["nguoi_nhan"], "o", color=V.MAU["cam"], ms=11, mec="white", label="người nhận")
    nd = np.array(m["nguoi_di"])
    b.plot(nd[:, 0], nd[:, 1], color=V.MAU["cam"], lw=3, alpha=0.35, label="người đi lại")
    b.plot(*x[0, :2], "*", color="white", ms=14, mec="#1e293b")
    b.text(x[0, 0] + 0.2, x[0, 1] + 0.2, "thức dậy", color="#1e293b", fontsize=9, weight="bold")
    b.set_xlim(0, goc.RONG)
    b.set_ylim(0, goc.DAI)
    b.set_aspect("equal")
    V.trang_tri(b, f"Lượt minh hoạ (seed {m['seed']}): giao xong sau {m['t']} s")
    b.grid(False)
    V.chu_giai(b, loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8)
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
