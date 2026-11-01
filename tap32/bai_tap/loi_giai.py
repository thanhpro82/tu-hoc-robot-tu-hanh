"""Lời giải bài tập tập 3.2 (tách từ hàm chay() trong ../sim/kalman.py). Tự làm kalman_cua_ban.py trước rồi hãy mở!"""
import numpy as np

DT = 0.1
SIGMA_A, SIGMA_Z = 0.3, 0.3
A = np.array([[1, DT], [0, 1]])
B = np.array([DT ** 2 / 2, DT])
C = np.array([[1.0, 0.0]])
Q = np.outer(B, B) * SIGMA_A ** 2
R = np.array([[SIGMA_Z ** 2]])


def du_doan(mu, Sig, u):
    return A @ mu + B * u, A @ Sig @ A.T + Q


def cap_nhat(mu_b, Sig_b, z):
    S = C @ Sig_b @ C.T + R
    K = Sig_b @ C.T @ np.linalg.inv(S)
    mu = mu_b + (K @ (np.array([z]) - C @ mu_b)).ravel()
    IKC = np.eye(2) - K @ C
    return mu, IKC @ Sig_b @ IKC.T + K @ R @ K.T, K


def loc_kalman(ds_u, ds_z, mu0, Sig0):
    mu, Sig, ra = mu0, Sig0, []
    for u, z in zip(ds_u, ds_z):
        mu, Sig = du_doan(mu, Sig, u)
        mu, Sig, _ = cap_nhat(mu, Sig, z)
        ra.append(mu)
    return ra
