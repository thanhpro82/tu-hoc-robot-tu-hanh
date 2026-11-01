"""Tự chấm bài tập tập 4.4. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[2] / "tap42" / "sim"), str(_D.parents[1])]
import qlearn as goc  # noqa: E402  (mô phỏng trong video; dùng kho của tập 4.2)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

M = goc.M


def hoc(chon_hanh_dong, cap_nhat_q, n_tap=2000, alpha=0.2, gamma=1.0, eps=0.1, seed=0, Q0=0.0):
    """Vòng học của video (goc.hoc) viết lại để gọi 2 hàm của bạn. Trả về (Q, tỉ lệ rơi theo từng tập)."""
    rng = np.random.default_rng(seed)
    Q = np.full((goc.NX, 4), Q0)
    roi = []
    for _ in range(n_tap):
        x, ket = M.S, "het_gio"
        for t in range(goc.T_TAP):
            i = M.IDX[x]
            a = chon_hanh_dong(Q[i], eps, rng)
            d = goc.DIRS[int(rng.integers(4))] if rng.random() < goc.TRUOT else goc.DIRS[a]
            x2 = M.buoc(x, d)
            if x2 == M.G:
                r, xong, ket = -1.0, True, "toi"
            elif x2 in M.CAU_THANG:
                r, xong, ket = -100.0, True, "roi"
            else:
                r, xong = -1.0, False
            cap_nhat_q(Q, i, a, r, M.IDX[x2], xong, alpha, gamma)
            x = x2
            if xong:
                break
        roi.append(ket == "roi")
    return Q, roi


def bai_1(ns):
    f = ham(ns, "chon_hanh_dong")
    Qi = np.array([-3.0, -1.0, -1.0, -5.0])
    rng = np.random.default_rng(1)
    chon = [f(Qi, 0.0, rng) for _ in range(200)]
    assert set(chon) == {1, 2}, f"ε = 0: chỉ được chọn lệnh tốt nhất (1 và 2 hoà nhau), bạn chọn {sorted(set(chon))}"
    rng_a, rng_b = np.random.default_rng(5), np.random.default_rng(5)
    for _ in range(300):
        dap = int(rng_b.integers(4)) if rng_b.random() < 0.3 else int(rng_b.choice(np.flatnonzero(Qi == Qi.max())))
        assert f(Qi, 0.3, rng_a) == dap, "ε = 0.3: chưa gọi rng đúng thứ tự trong docstring (random trước, rồi integers hoặc choice)"
    return "ε = 0 luôn khai thác (hoà thì bốc thăm), ε > 0 thỉnh thoảng thử bừa; gọi rng đúng thứ tự"


def bai_2(ns):
    f = ham(ns, "cap_nhat_q")
    Q = np.zeros((3, 4)); Q[2] = [-4, -2, -8, -3]
    f(Q, 0, 3, -1.0, 2, False, 0.5, 1.0)
    assert gan(Q[0, 3], 0.5 * (-1 + -2)), f"chưa xong: mục tiêu = −1 + max Q[2] = −3, Q mới = 0 + 0.5·(−3 − 0) = −1.5; bạn ra {Q[0, 3]}"
    f(Q, 1, 0, -100.0, 2, True, 0.5, 1.0)
    assert gan(Q[1, 0], -50.0), "rơi (xong): mục tiêu chỉ là r = −100, Q mới = −50"
    Q_ban, _ = hoc(ham(ns, "chon_hanh_dong"), f, n_tap=300)
    Q_goc = goc.hoc(n_tap=300, alpha=0.2, eps=0.1, seed=0, ghi_moi=10 ** 9)[0]
    assert gan(Q_ban, Q_goc), "học 300 tập bằng code của bạn chưa ra đúng bảng Q như code video"
    return "300 tập học bằng 2 hàm của bạn ra đúng bảng Q như code video"


def bai_3(ns):
    f = ham(ns, "chinh_sach_tham_lam")
    Q, roi = hoc(ham(ns, "chon_hanh_dong"), ham(ns, "cap_nhat_q"))
    pi = f(Q, M.O_TRONG, M.IDX, M.U)
    assert pi == goc.pi_tu_Q(Q), "chính sách tham lam chưa đúng (argmax từng hàng, hoà thì lệnh đứng trước)"
    J = M.danh_gia(lambda x: pi[x], goc.TRUOT)[M.S]
    J_opt = M.toi_uu(goc.TRUOT)[0][M.S]
    return (f"2000 tập: rơi {np.mean(roi[:100]) * 100:.0f}% ở 100 tập đầu → {np.mean(roi[-500:]) * 100:.1f}% ở 500 tập cuối; "
            f"chính sách học được J = {J:.2f} (tối ưu khi biết mô hình J* = {J_opt:.2f})")


BAI = [("Bài 1 · ε-greedy", bai_1), ("Bài 2 · cập nhật Q", bai_2), ("Bài 3 · chính sách học được", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "qlearn_cua_ban", loi_giai)
