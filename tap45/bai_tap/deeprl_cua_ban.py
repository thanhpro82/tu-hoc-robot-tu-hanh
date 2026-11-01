"""Bài tập tập 4.5: deep RL, luyện robot trong mô phỏng bằng gradient chính sách REINFORCE (Mục 18.5.2 của sách). Dùng numpy + PyTorch.

Robot chạy cùng lúc B tập (B robot song song). Sau một lượt, có:
  rew  : mảng (T, B), thưởng ở từng bước của từng robot (robot đã xong thì thưởng 0);
  alive: mảng (T, B) True/False, robot còn chạy ở bước đó không;
  logp : list T tensor (B,), log π_θ(u_t | x_t) của lệnh đã chọn (có gradient).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/deeprl.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np
import torch

from deeprl import chay_tap  # noqa: F401  (chạy B tập song song, trong ../sim)


def reward_to_go(rew, gamma):
    """Bài 1: tổng thưởng từ bước t về sau, có chiết khấu:  R_t = Σ_{t' ≥ t} γ^{t'−t}·r_{t'}  (cho từng robot).

    Gợi ý: đi ngược từ bước cuối: acc = rew[t] + gamma·acc; R[t] = acc. Trả về mảng cùng hình rew (float32)."""
    raise NotImplementedError("TODO Bài 1: reward-to-go")


def loi_reinforce(logp, R, alive):
    """Bài 2 (Eq. 18.31–18.32, biến thể "trừ baseline" của bài Cart-pole): hàm mất mát để PyTorch lấy gradient.

    Chỉ tính các ô còn chạy (m = alive):
        b = trung bình R[m];   A = (R − b) / (độ lệch chuẩn R[m] + 1e-8)        (ưu thế: tốt hơn hay tệ hơn mức trung bình)
        loss = − Σ_{t, i} logp[t][i] · A[t, i] · m[t, i]  /  B                 (B = số robot)
    Giảm loss = tăng xác suất của lệnh dẫn tới kết quả tốt hơn trung bình. Trả về tensor số (có gradient)."""
    raise NotImplementedError("TODO Bài 2: hàm mất mát REINFORCE")


def mot_cap_nhat(pi, opt, env, gamma=0.99):
    """Bài 3: một lần cập nhật chính sách.

    1. logp, rew, alive, _ = chay_tap(pi, env)      (có sẵn, đã import ở đầu file)
    2. R = reward_to_go(rew, gamma);  loss = loi_reinforce(logp, R, alive)
    3. opt.zero_grad(); loss.backward(); opt.step()
    Trả về (rew, env.ket) để theo dõi (env.ket: 1 tới đích, 2 va chạm, 0 hết giờ)."""
    raise NotImplementedError("TODO Bài 3: một lần cập nhật")

