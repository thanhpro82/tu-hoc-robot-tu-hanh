"""Bài tập tập 4.6: học bắt chước, robot học từ người lái: behavior cloning và DAgger (Chương 19 của sách). Dùng numpy + PyTorch.

Đường đua uốn lượn rộng 0,8 m; robot chạy 1 m/s, chỉ thấy 9 tia LiDAR. "Chuyên gia" là thuật toán pure pursuit (thay cho người lái).
Người học là mạng NguoiHoc: 9 tia → lệnh quay ω. Dữ liệu là cặp (X, U): X mảng (N, 9) quan sát, U mảng (N,) lệnh của chuyên gia.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/duongdua.py và loi_giai.py (tự làm trước đã).
"""
import math

import numpy as np
import torch

from duongdua import NguoiHoc, chay, lai_pi  # noqa: F401  (đường đua + mạng người học, trong ../sim)


def omega_pure_pursuit(x, y, th, gx, gy, V, LD, W_MAX):
    """Bài 1 (chuyên gia pure pursuit): robot ở (x, y), hướng th, nhắm điểm (gx, gy) trên đường tâm phía trước cách ~LD.

    α = góc từ hướng mũi xe tới điểm nhắm = atan2(gy − y, gx − x) − th, bọc về [−π, π)
    ω = 2·V·sin(α) / LD, kẹp trong [−W_MAX, W_MAX]. Trả về ω."""
    raise NotImplementedError("TODO Bài 1: pure pursuit")


def hoc_bc(X, U, seed=0, n_buoc=3000, lr=3e-3):
    """Bài 2 (behavior cloning, Thuật toán 1): học mạng bắt chước chuyên gia bằng hồi quy.

    torch.manual_seed(seed); pi = NguoiHoc(); opt = Adam(pi.parameters(), lr); g = torch.Generator().manual_seed(seed)
    Lặp n_buoc lần: j = torch.randint(len(X), (256,), generator=g)   (chọn ngẫu nhiên 256 mẫu)
                    loss = trung bình (pi(X[j]) − U[j])²;  opt.zero_grad(); loss.backward(); opt.step()
    (Đổi X, U sang tensor bằng torch.as_tensor trước vòng lặp.) Trả về pi."""
    raise NotImplementedError("TODO Bài 2: behavior cloning")


def vong_dagger(pi, env, X, U, hoc):
    """Bài 3 (DAgger, Thuật toán 3): một vòng.

    1. Cho NGƯỜI HỌC tự lái và chuyên gia gán nhãn:  r = chay(env, lai_pi(pi), nhan=True)   → r["X"], r["U"]
    2. Gộp dữ liệu: X = nối X với r["X"], U = nối U với r["U"]   (np.concatenate)
    3. Học lại từ đầu trên dữ liệu đã gộp: pi_moi = hoc(X, U)
    Trả về (pi_moi, X, U)."""
    raise NotImplementedError("TODO Bài 3: một vòng DAgger")
