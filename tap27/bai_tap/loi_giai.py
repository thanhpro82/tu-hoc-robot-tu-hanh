"""Lời giải bài tập tập 2.7. Tự làm cnn_cua_ban.py trước rồi hãy mở!"""
import numpy as np
import torch
import torch.nn as nn


def lop_tich_chap(X, W, b):
    k = W.shape[0]
    h, w = X.shape[0] - k + 1, X.shape[1] - k + 1
    Y = np.full((h, w), float(b))
    for u in range(k):
        for v in range(k):
            Y += X[u:u + h, v:v + w] * W[u, v]
    return Y


def max_pool(A):
    H, W = A.shape
    return A.reshape(H // 2, 2, W // 2, 2).max(axis=(1, 3))


class SimpleCNN(nn.Module):   # giống hệt lớp SimpleCNN trong ../sim/cnn.py
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, 5, padding=2)
        self.conv2 = nn.Conv2d(8, 16, 5, padding=2)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 8 * 8, 32)
        self.fc2 = nn.Linear(32, 4)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        return self.fc2(torch.relu(self.fc1(x.flatten(1))))
