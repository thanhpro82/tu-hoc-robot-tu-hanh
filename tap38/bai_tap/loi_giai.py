"""Lời giải bài tập tập 3.8 (tách từ ../sim/theo_doi.py). Tự làm theo_doi_cua_ban.py trước rồi hãy mở!"""
import numpy as np

H = np.array([[1.0, 0, 0, 0], [0, 1, 0, 0]])


def ghep(ds):
    Y = sum(np.linalg.inv(R) for _, R in ds)
    y = sum(np.linalg.inv(R) @ z for z, R in ds)
    S = np.linalg.inv(Y)
    return S @ y, S


def m2(x, P, z, R):
    S = H @ P @ H.T + R
    e = z - H @ x
    return float(e @ np.linalg.solve(S, e))


def cap_nhat(x, P, z, R):
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    return x + K @ (z - H @ x), (np.eye(4) - K @ H) @ P
