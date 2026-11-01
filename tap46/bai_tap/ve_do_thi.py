"""Vẽ: (trái) tỉ lệ chạy xong 1 vòng theo số mẫu dữ liệu: BC (chỉ lái mẫu) và DAgger (số liệu video, ../sim/ket_qua.txt);
(phải) một đường đua thử: chuyên gia, BC 2 vòng mẫu, DAgger (mạng seed 1 của video). Tham số `ns` không dùng.

Chạy: python -X utf8 ve_do_thi.py   -> ra ket_qua.png
"""
import json
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import duongdua as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import nap  # noqa: E402


def ve(ns=None, ra="ket_qua.png"):
    k = json.loads((_D.parent / "sim" / "ket_qua.txt").read_text(encoding="utf8"))
    fig, (a, b) = V.tao(1, 2, rong=13, cao=5)
    a.plot(k["bc_mau"], k["bc_ty"], "o-", color=V.MAU["do"], lw=2.2, label="BC: chỉ học từ lái mẫu")
    a.plot(k["dag_mau"], k["dag_ty"], "o-", color=V.MAU["luc"], lw=2.2, label="DAgger: tự lái + chuyên gia sửa")
    a.axhline(k["chuyen_gia"], color="white", ls=":", lw=1.2)
    a.text(k["bc_mau"][-1], k["chuyen_gia"] + 1, "chuyên gia", color=V.CHU, ha="right", fontsize=9)
    V.trang_tri(a, "Chạy xong 1 vòng (500 đường thử, TB 4 seed)", "số mẫu dữ liệu", "% chạy xong")
    V.chu_giai(a, loc="lower right")
    env = goc.DuongDua(1, np.random.default_rng(321))
    duong = goc.tao_duong(np.random.default_rng(321), 1)
    env.reset(duong)
    for mep in (env.trai[0], env.phai[0]):
        b.plot(*np.vstack([mep, mep[:1]]).T, color=V.MAU["xam"], lw=1.4)
    for ten, lai, mau in [("chuyên gia", goc.lai_chuyen_gia, "white"), ("BC 2 vòng", goc.lai_pi(nap("dd_bc2_1.pt")), V.MAU["do"]),
                          ("DAgger", goc.lai_pi(nap("dd_dagger_1.pt")), V.MAU["luc"])]:
        r = goc.chay(env, lai, duong=duong, ghi=True)
        xs = np.array(r["xs"])[:, 0]
        b.plot(xs[:, 0], xs[:, 1], color=mau, lw=1.8, label=f"{ten}: {'xong vòng' if r['ket'][0] == 1 else 'ra khỏi đường ở ' + format(r['di'][0] * 100, '.0f') + '% vòng'}")
    b.set_aspect("equal")
    V.trang_tri(b, "Một đường đua thử (đường rộng 0,8 m)")
    V.chu_giai(b, loc="upper right", fontsize=8.5)
    V.luu(fig, ra)


if __name__ == "__main__":
    ve(None, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
