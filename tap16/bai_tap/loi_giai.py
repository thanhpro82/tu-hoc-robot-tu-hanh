"""Lời giải bài tập tập 1.6. Tự làm rrt_cua_ban.py trước rồi hãy mở!"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from rrt import ALPHA, BUOC, DIEM_DICH, H, Q_G, Q_S, W, khong_va_cham  # noqa: E402,F401


def gan_nhat(V, q):
    return min(range(len(V)), key=lambda i: math.dist(V[i], q))


def tien_ve(q_near, q_rand, buoc):
    d = math.dist(q_near, q_rand)
    s = min(1.0, buoc / d)
    return q_near[0] + (q_rand[0] - q_near[0]) * s, q_near[1] + (q_rand[1] - q_near[1]) * s


def rrt(seed=2, toi_da=3000):
    rng = random.Random(seed)
    V, cha = [Q_S], [-1]
    for k in range(toi_da):
        q_rand = Q_G if rng.random() < ALPHA else (rng.uniform(0, W), rng.uniform(0, H))
        i_near = gan_nhat(V, q_rand)
        if math.dist(V[i_near], q_rand) < 1e-9:
            continue
        q_new = tien_ve(V[i_near], q_rand, BUOC)
        if not (0 <= q_new[0] <= W and 0 <= q_new[1] <= H) or not khong_va_cham(V[i_near], q_new):
            continue
        V.append(q_new)
        cha.append(i_near)
        if math.dist(q_new, Q_G) < DIEM_DICH:
            duong, i = [], len(V) - 1
            while i >= 0:
                duong.append(V[i])
                i = cha[i]
            return {"V": V, "cha": cha, "duong": duong[::-1] + [Q_G], "vong_tim_thay": k + 1}
    return {"V": V, "cha": cha, "duong": [], "vong_tim_thay": None}
