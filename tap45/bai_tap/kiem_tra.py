"""Tự chấm bài tập tập 4.5. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 3 luyện mạng bằng code của bạn 30 lần cập nhật (khoảng 15–30 giây trên CPU) và so với code video.
"""
import sys
from pathlib import Path

import numpy as np
import torch

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import deeprl as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

N_CN = 30


def huan_luyen(mot_cap_nhat, n_cap_nhat=N_CN, B=64, lr=3e-3, seed=0):
    """Giống goc.huan_luyen nhưng mỗi lần cập nhật gọi hàm của bạn. Trả về (pi, lịch sử % tới đích)."""
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    pi = goc.ChinhSach()
    opt = torch.optim.Adam(pi.parameters(), lr=lr)
    env = goc.MoiTruong(B, rng)
    ls = []
    for _ in range(n_cap_nhat):
        _, ket = mot_cap_nhat(pi, opt, env)
        ls.append(float(np.mean(ket == 1)))
    return pi, ls


def nap(ten):
    pi = goc.ChinhSach()
    pi.load_state_dict(torch.load(_D.parent / "sim" / ten, weights_only=False)["state"])
    return pi


def bai_1(ns):
    f = ham(ns, "reward_to_go")
    rew = np.array([[1.0, 0.0], [0.0, 2.0], [3.0, 1.0]], np.float32)
    R = np.asarray(f(rew, 0.5))
    assert gan(R, [[1 + 0 + 0.75, 0 + 1 + 0.25], [0 + 1.5, 2 + 0.5], [3, 1]]), f"γ = 0.5: phải ra [[1.75, 1.25], [1.5, 2.5], [3, 1]], bạn ra {R.tolist()}"
    return "R_t cộng dồn thưởng từ t về sau (càng xa càng nhân thêm γ)"


def bai_2(ns):
    f = ham(ns, "loi_reinforce")
    import loi_giai
    rng = np.random.default_rng(1)
    for _ in range(5):
        T, B = 7, 5
        lp = [torch.tensor(rng.normal(size=B), dtype=torch.float32, requires_grad=True) for _ in range(T)]
        R = rng.normal(size=(T, B)).astype(np.float32)
        al = rng.random((T, B)) < 0.8
        assert gan(float(f(lp, R, al)), float(loi_giai.loi_reinforce(lp, R, al)), 1e-5), "hàm mất mát chưa khớp đáp án"
    loss = f(lp, R, al)
    loss.backward()
    assert lp[0].grad is not None, "loss phải có gradient theo logp (dùng phép tính của torch)"
    return "loss = −Σ logπ·A: lệnh nào cho kết quả tốt hơn trung bình (A > 0) sẽ được tăng xác suất"


def bai_3(ns):
    f = ham(ns, "mot_cap_nhat")
    g = f.__globals__
    if "chay_tap" not in g:
        g["chay_tap"] = goc.chay_tap
    pi, ls = huan_luyen(f)
    _, ls0 = goc.huan_luyen(n_cap_nhat=N_CN, ghi_moi=1, log=lambda *a: None)
    assert gan(ls, [x[1] for x in ls0], 1e-6), "luyện bằng code của bạn chưa ra đúng như code video (cùng seed)"
    sach = goc.danh_gia(nap("pi_sach_0.pt"), 1000, seed=500)
    return (f"{N_CN} lần cập nhật bằng code của bạn: tới đích {ls[0] * 100:.0f}% → {ls[-1] * 100:.0f}% (khớp code video); "
            f"mạng luyện đủ 500 lần trong video tới đích {sach['toi'] * 100:.1f}%")


BAI = [("Bài 1 · reward-to-go", bai_1), ("Bài 2 · hàm mất mát REINFORCE", bai_2), ("Bài 3 · một lần cập nhật", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "deeprl_cua_ban", loi_giai)
