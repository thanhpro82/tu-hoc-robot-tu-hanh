"""Bài tập tập 2.7: deep learning nhìn thế giới thế nào (Chương 9 của sách). Bài 1–2 dùng numpy, Bài 3 dùng PyTorch.

Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm, lớp và tham số. Lời giải: ../sim/cnn.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np
import torch
import torch.nn as nn


def lop_tich_chap(X, W, b):
    """Bài 1 (Eq. 9.1): một bộ lọc trên ảnh một kênh, không đệm viền (kết quả nhỏ hơn ảnh).

        Y[i, j] = Σ_u Σ_v X[i + u, j + v] · W[u, v] + b        (u, v chạy hết kích thước bộ lọc)
    X: (H, W_anh), W: (k, k), b: số. Kết quả có hình (H − k + 1, W_anh − k + 1)."""
    raise NotImplementedError("TODO Bài 1: lớp tích chập")


def max_pool(A):
    """Bài 2 (Mục 9.1.2): max pooling 2×2 bước 2: chia A (H, W chẵn) thành các ô 2×2 không chồng nhau,
    mỗi ô giữ lại số LỚN NHẤT. Kết quả có hình (H/2, W/2). Gợi ý: A.reshape(H//2, 2, W//2, 2).max(axis=(1, 3))."""
    raise NotImplementedError("TODO Bài 2: max pooling")


class SimpleCNN(nn.Module):
    """Bài 3 (bài tập 1 của chương): mạng cho ảnh xám 32×32, 4 lớp (đi thẳng, rẽ trái, rẽ phải, dừng).

    conv1: Conv2d(1 → 8, bộ lọc 5×5, padding=2) → ReLU → MaxPool 2×2   (32×32 → 16×16)
    conv2: Conv2d(8 → 16, bộ lọc 5×5, padding=2) → ReLU → MaxPool 2×2  (16×16 → 8×8)
    fc1:   Linear(16·8·8 → 32) → ReLU
    fc2:   Linear(32 → 4)
    Dùng đúng tên thuộc tính self.conv1, self.conv2, self.pool, self.fc1, self.fc2."""

    def __init__(self):
        super().__init__()
        raise NotImplementedError("TODO Bài 3: khai báo các lớp")

    def forward(self, x):
        raise NotImplementedError("TODO Bài 3: x (N, 1, 32, 32) → điểm của 4 lớp (N, 4)")
