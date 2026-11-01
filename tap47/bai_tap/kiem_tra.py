"""Tự chấm bài tập tập 4.7. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bộ chấm thử trên 100 đường (video dùng 500 đường × 4 seed, số liệu trong ../sim/ket_qua.txt).
"""
import sys
from pathlib import Path

import numpy as np
import torch

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import an_toan as A  # noqa: E402  (lớp an toàn của video)
import the_gioi as G  # noqa: E402  (mô hình thế giới của video)
from the_gioi import R  # noqa: E402  (đường đua tập 4.6)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

N_THU = 100


def nap_tg(ten="tg200_1.pt"):
    """Nạp mô hình thế giới đã học trong video (200 đường lái ngẫu nhiên, seed 1)."""
    f = G.TheGioi()
    f.load_state_dict(torch.load(_D.parent / "sim" / ten))
    return f


def obs_mau(n=64, seed=5):
    """Quan sát thật trên đường đua: chuyên gia lái có nhiễu nên có cả lúc sát mép."""
    env = R.DuongDua(n, np.random.default_rng(seed), nhieu_lai=0.6)
    o, ds = env.reset(), []
    for t in range(30):
        o, _ = env.buoc(R.chuyen_gia(env))
        if t % 5 == 4:
            ds.append(o.copy())
    return np.concatenate(ds)


def bai_1(ns):
    f = ham(ns, "khoang_ho")
    o = np.ones((1, R.N_TIA), np.float32)
    cl, cr = f(o)
    assert gan(cl, np.full(1, 3.0 * np.sin(np.pi / 8))) and gan(cr, cl), "không có mép trong tầm 3 m: tia trái thấp nhất (22,5°) cho c_L = 3·sin 22,5° ≈ 1,15 m, c_R cũng vậy"
    O = obs_mau()
    a, b = f(O), A.khoang_ho(O)
    assert gan(a[0], b[0], 1e-5) and gan(a[1], b[1], 1e-5), "c_L hoặc c_R chưa đúng (tia trái là góc > 0.1, tia phải góc < −0.1)"
    return f"trên {len(O)} quan sát thật: khoảng hở nhỏ nhất {min(a[0].min(), a[1].min()) * 100:.0f} cm, lớn nhất {max(a[0].max(), a[1].max()):.2f} m"


def bai_2(ns):
    f = ham(ns, "boc_an_toan")
    O = obs_mau()
    rng = np.random.default_rng(0)
    for _ in range(3):
        w = rng.uniform(-R.W_MAX, R.W_MAX, len(O))
        lai = lambda env, obs, w=w: w
        assert gan(f(lai)(None, O), A.boc_an_toan(lai)(None, O), 1e-6), "lệnh sau lớp an toàn chưa khớp (xem lại min/max và dấu)"
    sua = float(np.mean(np.abs(A.boc_an_toan(lai)(None, O) - w) > 1e-9))
    pi = A.nap("dd_bc2_3.pt")
    tron = R.danh_gia(R.lai_pi(pi), n=N_THU)["xong"]
    boc = R.danh_gia(f(R.lai_pi(pi)), n=N_THU)["xong"]
    assert gan(boc, R.danh_gia(A.boc_an_toan(R.lai_pi(pi)), n=N_THU)["xong"]), "kết quả lái thử chưa khớp lớp an toàn của video"
    return (f"lệnh ngẫu nhiên bị sửa {sua * 100:.0f}% số lần; mạng BC 2 vòng (seed 3, {N_THU} đường): "
            f"tự lái xong {tron * 100:.0f}% → bọc lớp an toàn xong {boc * 100:.0f}%")


def bai_3(ns):
    c_f = ham(ns, "chi_phi_tuong_tuong")
    f = nap_tg()
    O = obs_mau(16)
    c = c_f(f, O)
    assert np.shape(c) == (len(O), len(G.W_THU)), f"chi phí phải có dạng ({len(O)}, 25), bạn trả về {np.shape(c)}"
    assert gan(c, G.tuong_tuong(f, O)[1], 1e-4), "chi phí tưởng tượng chưa khớp (nhớ clamp(0, 1) mỗi bước và nhân 0.9**h)"
    lai = lambda env, obs: G.W_THU[c_f(f, obs).argmin(1)]
    r = R.danh_gia(lai, n=N_THU)
    return (f"chi phí khớp video; lái bằng tưởng tượng (mô hình học từ 200 đường lái ngẫu nhiên, seed 1): "
            f"xong {r['xong'] * 100:.0f}% trên {N_THU} đường")


BAI = [("Bài 1 · khoảng hở hai bên", bai_1), ("Bài 2 · lớp an toàn", bai_2), ("Bài 3 · lái bằng tưởng tượng", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "physai_cua_ban", loi_giai)
