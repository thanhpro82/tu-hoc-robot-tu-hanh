"""Bài tập tập 4.7: hai ý của Physical AI trên đường đua tập 4.6: lớp an toàn bọc mạng nơ-ron, và mô hình thế giới để "tưởng tượng" trước khi lái.

Robot thấy 9 tia LiDAR: obs mảng (B, 9), đã chia cho tầm xa TAM = 3 m (khoảng cách thật = obs · TAM). Góc tia GOC_TIA từ −90° (phải) tới +90° (trái).
Lệnh lái là ω (rad/s), mỗi robot một số. Một "người lái" là hàm lai(env, obs) → mảng ω (B,).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/an_toan.py, ../sim/the_gioi.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np
import torch

from the_gioi import H, W_THU, diem, R  # noqa: F401  (mô hình thế giới của video, trong ../sim; R là đường đua tập 4.6)

GOC_TIA, TAM = R.GOC_TIA, R.TAM


def khoang_ho(obs):
    """Bài 1 (khoảng hở hai bên): mép đường cách robot bao xa theo phương ngang?

    d = obs · TAM (mét). Tia i ở góc a_i chạm mép ở khoảng d_i → khoảng cách ngang tới mép là d_i·|sin a_i|.
    c_L = nhỏ nhất của d_i·sin(a_i) trên các tia TRÁI (a_i > 0.1),
    c_R = nhỏ nhất của d_i·(−sin a_i) trên các tia PHẢI (a_i < −0.1).
    Trả về (c_L, c_R), mỗi cái mảng (B,)."""
    raise NotImplementedError("TODO Bài 1: khoảng hở hai bên")


def boc_an_toan(lai, m=0.17, k=12.0):
    """Bài 2 (lớp an toàn): bọc người lái `lai` (ví dụ mạng nơ-ron) bằng một luật cổ điển. Trả về hàm f(env, obs).

    Trong f: ω = lai(env, obs) (đổi sang mảng float);  c_L, c_R = khoang_ho(obs)
      chỗ nào c_L < m (sát mép trái):  ω ← min(ω, −k·(m − c_L))   (bắt buộc rẽ phải ít nhất chừng đó)
      chỗ nào c_R < m (sát mép phải):  ω ← max(ω, +k·(m − c_R))   (bắt buộc rẽ trái)
    Còn lại giữ nguyên lệnh của mạng. (Gợi ý: np.where, np.minimum, np.maximum.)"""
    raise NotImplementedError("TODO Bài 2: lớp an toàn")


def chi_phi_tuong_tuong(f, obs):
    """Bài 3 (lái bằng tưởng tượng): với mỗi robot, thử 25 lệnh W_THU, "mơ" H = 8 bước bằng mô hình thế giới f, chấm điểm.

    B = số robot. Làm trong torch.no_grad():
      x = obs lặp cho 25 lệnh: tensor (B·25, 9), hàng b·25 + j là obs[b]      (unsqueeze(1).expand(B, 25, 9).reshape(-1, 9))
      w = W_THU lặp B lần: tensor float32 (B·25,), hàng b·25 + j là W_THU[j]  (torch.as_tensor(W_THU, dtype=torch.float32).repeat(B))
      chi_phi = 0;  lặp h = 0..H−1:  x = f(x, w).clamp(0, 1);  chi_phi += diem(x) · 0.9**h
    Trả về chi_phi dạng mảng numpy (B, 25). Lệnh được chọn là W_THU[chi_phi.argmin(1)]."""
    raise NotImplementedError("TODO Bài 3: tưởng tượng 8 bước")
