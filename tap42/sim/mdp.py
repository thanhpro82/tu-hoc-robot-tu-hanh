"""Tập 4.2 - Ra quyết định khi tương lai bất định: MDP (Chương 17, Principles of Robot Autonomy).

Ký hiệu theo sách (§17.2.1, dạng điều khiển tối ưu, tối thiểu hoá CHI PHÍ, chân trời hữu hạn T):
    x_{t+1} = f(x_t, u_t, w_t),   w_t ~ p(w | x_t, u_t)             (Eq. 17.7–17.8)
    J_π(x_0) = E_w[ g_T(x_T) + Σ_{t=0}^{T-1} g_t(x_t, π_t(x_t), w_t) ]   (Eq. 17.11)
Thế giới (giả định, kiểu bài Markovian Drone §17.5): lưới 9 × 5 trong kho, robot đi từ S tới G.
Hàng dưới cùng là CẦU THANG: rơi xuống thì kẹt luôn (trạng thái hút). Giữa kho có dãy KỆ chắn.
u ∈ {lên, xuống, trái, phải}. Sàn trơn: với xác suất ε robot đi theo hướng ngẫu nhiên (4 hướng đều nhau),
còn lại đi đúng lệnh. Đâm tường/kệ thì đứng yên.
Chi phí: g_t = 1 mỗi bước chưa tới G (tới G thì đứng yên, chi phí 0); g_T(x) = 100·(1 − 1[x = G]).
"""
import numpy as np

W, H, T = 9, 5, 30
S, G = (0, 1), (8, 1)
CAU_THANG = {(x, 0) for x in range(1, 8)}
KE = {(x, 2) for x in range(2, 7)}
HUONG = {"len": (0, 1), "xuong": (0, -1), "trai": (-1, 0), "phai": (1, 0)}
U = list(HUONG)
O_TRONG = [(x, y) for y in range(H) for x in range(W) if (x, y) not in KE]
IDX = {c: k for k, c in enumerate(O_TRONG)}


def buoc(x, d):
    if x == G or x in CAU_THANG:
        return x                                   # tới đích / đã rơi: đứng yên
    n = (x[0] + d[0], x[1] + d[1])
    if not (0 <= n[0] < W and 0 <= n[1] < H) or n in KE:
        return x
    return n


def chuyen(x, u, eps):
    """p(x_{t+1} | x_t, u_t): đúng lệnh với xác suất 1 − ε, mỗi hướng thêm ε/4."""
    p = {}
    for name, d in HUONG.items():
        q = (1 - eps) * (name == u) + eps / 4
        n = buoc(x, d)
        p[n] = p.get(n, 0.0) + q
    return p


def g(x):
    return 0.0 if x == G else 1.0


def gT(x):
    return 0.0 if x == G else 100.0


# ---------- hai chính sách vòng kín viết tay ----------
def pi_tat(x):
    """Đường tắt: về hàng y = 1 (sát mép cầu thang) rồi đi thẳng sang phải tới G."""
    if x[1] == 0:
        return "len"
    if x[1] > 1:
        return "xuong" if x[0] in (0, 1, 7, 8) else "phai"
    return "phai"


def pi_an_toan(x):
    """Đường vòng: lên hàng y = 3 (phía trên dãy kệ), đi sang phải, tới cột x = 8 thì đi xuống G."""
    if x[0] == 8:
        return "xuong" if x[1] > 1 else "len"
    if x[1] == 0:
        return "len"
    if x[1] in (1, 2):
        if x[0] in (0, 1):
            return "len"
        if x[0] == 7:
            return "phai"
        return "trai" if x[0] <= 4 else "phai"     # lỡ trượt xuống hàng sát cầu thang: về cột gần nhất
    return "phai" if x[1] == 3 else "xuong"


def danh_gia(pi, eps):
    """J_π(x) với π dừng (không đổi theo t), lùi từ t = T: J_T = g_T, J_t(x) = E[g_t + J_{t+1}(x_{t+1})]."""
    J = {x: gT(x) for x in O_TRONG}
    for _ in range(T):
        J = {x: g(x) + sum(p * J[n] for n, p in chuyen(x, pi(x), eps).items()) for x in O_TRONG}
    return J


def toi_uu(eps):
    """Chỉ để so sánh (tập 4.3 sẽ giải thích): quy hoạch động Eq. 17.13 cho J*_0 và π*_0."""
    J = {x: gT(x) for x in O_TRONG}
    pi = {}
    for _ in range(T):
        Jm = {}
        for x in O_TRONG:
            c = {u: sum(p * J[n] for n, p in chuyen(x, u, eps).items()) for u in U}
            u_best = min(c, key=c.get)
            Jm[x], pi[x] = g(x) + c[u_best], u_best
        J = Jm
    return J, pi


def mo_phong(pi, eps, n=10000, seed=42, vong_ho=None):
    """Monte Carlo: tỉ lệ tới G, tỉ lệ rơi, chi phí trung bình. vong_ho = chuỗi lệnh cố định tính trước (vòng hở, không nhìn x)."""
    rng = np.random.default_rng(seed)
    dirs = list(HUONG.values())
    toi = roi = 0
    chi_phi = []
    for _ in range(n):
        x, c = S, 0.0
        for t in range(T):
            u = (vong_ho[t] if t < len(vong_ho) else "phai") if vong_ho is not None else pi(x)
            c += g(x)
            x = buoc(x, dirs[rng.integers(4)] if rng.random() < eps else HUONG[u])
        c += gT(x)
        chi_phi.append(c)
        toi += x == G
        roi += x in CAU_THANG
    return {"toi": toi / n, "roi": roi / n, "J_mc": float(np.mean(chi_phi))}


def quy_dao(pi, eps, seed):
    rng = np.random.default_rng(seed)
    dirs = list(HUONG.values())
    x, out = S, [S]
    for _ in range(T):
        d = dirs[rng.integers(4)] if rng.random() < eps else HUONG[pi(x)]
        x = buoc(x, d)
        out.append(x)
        if x == G or x in CAU_THANG:
            break
    return out


VONG_HO_TAT = ["phai"] * 8


if __name__ == "__main__":
    for eps in (0.0, 0.1, 0.2, 0.3):
        Jt, Ja = danh_gia(pi_tat, eps)[S], danh_gia(pi_an_toan, eps)[S]
        Js = toi_uu(eps)[0][S]
        mt, ma = mo_phong(pi_tat, eps), mo_phong(pi_an_toan, eps)
        mo = mo_phong(None, eps, vong_ho=VONG_HO_TAT)
        print(f"ε={eps:.2f}  J_tắt={Jt:6.2f} (rơi {mt['roi']*100:5.1f}%, tới {mt['toi']*100:5.1f}%, MC {mt['J_mc']:.2f})"
              f"  J_vòng={Ja:6.2f} (rơi {ma['roi']*100:4.1f}%, tới {ma['toi']*100:5.1f}%)  J*={Js:6.2f}"
              f"  vòng hở: tới {mo['toi']*100:5.1f}% rơi {mo['roi']*100:4.1f}%")
