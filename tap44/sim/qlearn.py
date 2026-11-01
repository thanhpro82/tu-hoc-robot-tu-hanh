"""Tập 4.4 - Học tăng cường: robot học từ thất bại (Chương 18, Principles of Robot Autonomy).

Q-learning (Eq. 18.18, Algorithm 5):  Q(x, u) ← Q(x, u) + α ( r + γ max_u' Q(x', u') − Q(x, u) )
Hành vi ε-greedy: xác suất 1 − ε chọn argmax_u Q(x, u), xác suất ε chọn ngẫu nhiên.
Chương 18 dùng PHẦN THƯỞNG (tối đa hoá), khác Chương 17 dùng chi phí.

Môi trường = kho lưới tập 4.2 (tap42/sim/mdp.py), robot KHÔNG biết xác suất trượt, chỉ tự đi thử:
    mỗi bước r = −1; tới G: kết thúc; rơi cầu thang: r = −100, kết thúc; quá T_TAP = 100 bước thì dừng tập (cắt, không phạt).
Sàn trơn 20% (xác suất đi hướng ngẫu nhiên, ở 4.2 gọi là ε; ở đây đổi tên TRUOT để khỏi trùng ε của ε-greedy).
Đánh giá: lấy chính sách tham lam π(x) = argmax_u Q(x, u), tính chi phí kỳ vọng J_π bằng mô hình thật (như 4.2)
để so với J* = 16,24 của quy hoạch động (tập 4.3).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tap42" / "sim"))
import mdp as M  # noqa: E402

TRUOT = 0.2
DIRS = [M.HUONG[u] for u in M.U]
NX = len(M.O_TRONG)


T_TAP = 100


def hoc(n_tap=3000, alpha=0.1, gamma=1.0, eps=0.1, seed=0, ghi_moi=50, ghi_qd=(), Q0=0.0):
    rng = np.random.default_rng(seed)
    Q = np.full((NX, 4), Q0)
    lich_su = []           # (tập, J_π của chính sách tham lam, % rơi trong 'ghi_moi' tập gần nhất, tổng thưởng TB)
    qd = {}
    roi_gan, thuong_gan = [], []
    for k in range(n_tap):
        x = M.S
        G_tap, duong, ket = 0.0, [x], "het_gio"
        for t in range(T_TAP):
            i = M.IDX[x]
            a = int(rng.integers(4)) if rng.random() < eps else int(rng.choice(np.flatnonzero(Q[i] == Q[i].max())))
            d = DIRS[int(rng.integers(4))] if rng.random() < TRUOT else DIRS[a]
            x2 = M.buoc(x, d)
            if x2 == M.G:
                r, xong, ket = -1.0, True, "toi"
            elif x2 in M.CAU_THANG:
                r, xong, ket = -100.0, True, "roi"
            else:
                r, xong = -1.0, False
            muc_tieu = r if xong else r + gamma * Q[M.IDX[x2]].max()
            Q[i, a] += alpha * (muc_tieu - Q[i, a])
            G_tap += r
            x = x2
            duong.append(x)
            if xong or t == T_TAP - 1:
                break
        roi_gan.append(ket == "roi")
        thuong_gan.append(G_tap)
        if k in ghi_qd:
            qd[k] = {"duong": duong, "ket": ket, "thuong": G_tap}
        if (k + 1) % ghi_moi == 0 or k == 0:
            lich_su.append((k + 1, J_cua(Q), float(np.mean(roi_gan[-ghi_moi:])), float(np.mean(thuong_gan[-ghi_moi:]))))
    return Q, lich_su, qd


def pi_tu_Q(Q):
    return {x: M.U[int(np.argmax(Q[M.IDX[x]]))] for x in M.O_TRONG}


def J_cua(Q):
    pi = pi_tu_Q(Q)
    return M.danh_gia(lambda x: pi[x], TRUOT)[M.S]


if __name__ == "__main__":
    J_opt = M.toi_uu(TRUOT)[0][M.S]
    print("J* (quy hoạch động, biết mô hình) = %.2f" % J_opt)
    for Q0 in (0.0, -50.0):
        for eps in (0.0, 0.1, 0.3):
            Js = [hoc(n_tap=2000, eps=eps, seed=sd, Q0=Q0, alpha=0.2, ghi_moi=500)[1][-1][1] for sd in range(10)]
            print(f"Q0 = {Q0:5.0f} ε = {eps:.2f}: J_π cuối TB {np.mean(Js):.2f}, trung vị {np.median(Js):.2f}, min {min(Js):.2f}, max {max(Js):.2f}", [round(j) for j in Js])
