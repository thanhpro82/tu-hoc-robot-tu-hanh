"""Lời giải bài tập tập 2.2. Tự làm camera_cua_ban.py trước rồi hãy mở!"""


def ma_tran_K(alpha, beta, gamma, u0, v0):
    return [[alpha, gamma, u0], [0.0, beta, v0], [0.0, 0.0, 1.0]]


def _nhan(A, b):
    return [sum(A[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]


def chieu(P_W, K, R, t):
    P_C = [a + b for a, b in zip(_nhan(R, P_W), t)]
    p = _nhan(K, P_C)
    return p[0] / p[2], p[1] / p[2]


def khoang_cach_tu_anh(H, h_px, beta):
    return beta * H / h_px
