"""Lời giải bài tập tập 4.3 (tách từ ../sim/qhd.py). Tự làm qhd_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
import qhd as _q  # noqa: E402
from mdp import O_TRONG, T, U, chuyen, g, gT  # noqa: E402  (qhd.py đã thêm tap42/sim vào đường dẫn)


def bellman(x, J_sau, eps):
    c = {u: g(x) + sum(p * J_sau[n] for n, p in chuyen(x, u, eps).items()) for u in U}
    u_best = min(U, key=lambda u: (round(c[u], 9), U.index(u)))
    return c[u_best], u_best


def quy_hoach_dong(eps):
    J, PI = [None] * (T + 1), [None] * T
    J[T] = {x: gT(x) for x in O_TRONG}
    for t in range(T - 1, -1, -1):
        kq = {x: bellman(x, J[t + 1], eps) for x in O_TRONG}
        J[t], PI[t] = {x: v[0] for x, v in kq.items()}, {x: v[1] for x, v in kq.items()}
    return J, PI


def mo_phong(PI, eps, n=2000, seed=42):
    kq = _q.mo_phong(PI, eps, n=n, seed=seed)
    return {"toi": kq["toi"], "roi": kq["roi"]}
