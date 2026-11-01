"""Tự chấm bài tập tập 4.6. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bộ chấm học nhanh (300 bước thay vì 3000) để chạy trong vài chục giây; mạng đầy đủ của video có sẵn trong ../sim/dd_*.pt.
"""
import math
import sys
from pathlib import Path

import numpy as np
import torch

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import duongdua as goc  # noqa: E402  (đường đua của video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

N_NHANH = 300


def nap(ten):
    pi = goc.NguoiHoc()
    pi.load_state_dict(torch.load(_D.parent / "sim" / ten))
    return pi


def du_lieu_mau(seed=0, n_luot=2):
    env = goc.DuongDua(n_luot, np.random.default_rng(seed))
    r = goc.chay(env, goc.lai_chuyen_gia, nhan=True)
    return env, r["X"], r["U"]


def bai_1(ns):
    f = ham(ns, "omega_pure_pursuit")
    assert gan(f(0, 0, 0, 1.17, 0, 1.0, 1.17, 2.5), 0.0), "điểm nhắm ngay phía trước: ω = 0"
    assert gan(f(0, 0, 0, 0, 1.17, 1.0, 1.17, 2.5), 2 / 1.17), "điểm nhắm vuông góc bên trái (α = 90°): ω = 2·1·1/1.17"
    rng = np.random.default_rng(1)
    for _ in range(50):
        x, y, th, gx, gy = rng.uniform(-3, 3, 5)
        al = (math.atan2(gy - y, gx - x) - th + math.pi) % (2 * math.pi) - math.pi
        assert gan(f(x, y, th, gx, gy, 1.0, 1.17, 2.5), np.clip(2 * math.sin(al) / 1.17, -2.5, 2.5)), "pure pursuit chưa đúng (nhớ bọc góc và kẹp ω)"
    return "nhắm một điểm phía trước, quay càng gắt khi điểm càng lệch sang bên"


def bai_2(ns):
    f = ham(ns, "hoc_bc")
    _, X, U = du_lieu_mau()
    a, b = f(X, U, seed=0, n_buoc=N_NHANH), goc.hoc(X, U, seed=0, n_buoc=N_NHANH)
    for pa, pb in zip(a.parameters(), b.parameters()):
        assert gan(pa.detach().numpy(), pb.detach().numpy(), 1e-5), "mạng học bằng code của bạn chưa khớp code video (cùng seed, cùng cách chọn mẫu)"
    return f"học bắt chước trên {len(X)} mẫu của 2 vòng lái mẫu: mạng khớp code video"


def bai_3(ns):
    f, hoc_bc = ham(ns, "vong_dagger"), ham(ns, "hoc_bc")
    import loi_giai
    hoc = lambda X, U: goc.hoc(X, U, seed=0, n_buoc=N_NHANH)
    ket = []
    for vd in (f, loi_giai.vong_dagger):
        env, X, U = du_lieu_mau()
        pi = hoc(X, U)
        for _ in range(2):
            pi, X, U = vd(pi, env, X, U, hoc)
        ket.append((len(X), [p.detach().numpy().copy() for p in pi.parameters()]))
    assert ket[0][0] == ket[1][0], f"sau 2 vòng DAgger phải có {ket[1][0]} mẫu, bạn có {ket[0][0]}"
    assert all(gan(a, b, 1e-5) for a, b in zip(ket[0][1], ket[1][1])), "mạng sau 2 vòng DAgger chưa khớp đáp án"
    bc, dag = goc.danh_gia(goc.lai_pi(nap("dd_bc2_1.pt")), n=100), goc.danh_gia(goc.lai_pi(nap("dd_dagger_1.pt")), n=100)
    return (f"2 vòng DAgger: dữ liệu {ket[0][0]} mẫu, khớp đáp án; mạng của video (seed 1, 100 đường thử): "
            f"BC 2 vòng mẫu xong {bc['xong'] * 100:.0f}% · DAgger xong {dag['xong'] * 100:.0f}%")


BAI = [("Bài 1 · chuyên gia pure pursuit", bai_1), ("Bài 2 · behavior cloning", bai_2), ("Bài 3 · một vòng DAgger", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "batchuoc_cua_ban", loi_giai)
