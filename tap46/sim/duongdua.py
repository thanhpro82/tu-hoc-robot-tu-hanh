"""Tập 4.6 - Học bắt chước trên đường đua (Chương 19, Principles of Robot Autonomy).

Bối cảnh (giả định): mỗi lượt một đường đua khép kín ngẫu nhiên, rộng 0,8 m, robot unicycle v = 1 m/s, Δt = 0,1 s, ω liên tục |ω| ≤ 3 rad/s.
Quan sát của robot: 9 tia LiDAR (−90°..90°, tầm 3 m) tới hai mép đường — không biết bản đồ, không biết vị trí.
Chuyên gia π* ("người lái", giả định): pure pursuit bám đường tâm, nhìn trước 1,17 m — biết vị trí thật.
Người học π_θ: mạng 9-64-64-1, hồi quy ω, loss bình phương sai số (MSE, một loss sách liệt kê).
- Behavior cloning (§19.2, Algorithm 1): 𝒟 = {(x_i, u_i)} từ các vòng chuyên gia tự lái.
- DAgger (§19.2.1, Algorithm 3): π_θi tự lái, chuyên gia gán ω đúng cho mọi trạng thái robot đi qua, 𝒟 ← 𝒟 ∪ 𝒟_i, học lại.
"""
import math

import numpy as np
import torch
import torch.nn as nn

V, DT, W_MAX = 1.0, 0.1, 3.0
RONG = 0.8                       # bề rộng đường
R_ROBOT = 0.12
N_TIA, TAM = 9, 3.0
GOC_TIA = np.linspace(-math.pi / 2, math.pi / 2, N_TIA)
N_DIEM = 240                     # số điểm trên đường tâm
LD = 1.17                        # tầm nhìn trước của pure pursuit
T_MAX = 260                      # 26 s, đủ hơn 1 vòng


def tao_duong(rng, B):
    """Đường tâm khép kín r(θ) = R0 + Σ a_k cos(kθ + φ_k), (B, N, 2), cùng tiếp tuyến và pháp tuyến."""
    th = np.linspace(0, 2 * math.pi, N_DIEM, endpoint=False)
    r = np.full((B, N_DIEM), 3.0)
    for k, amp in ((2, 0.84), (3, 0.54), (4, 0.3), (5, 0.18)):
        r += rng.uniform(0, amp, (B, 1)) * np.cos(k * th[None] + rng.uniform(0, 2 * math.pi, (B, 1)))
    c = np.stack([r * np.cos(th), r * np.sin(th)], -1) + 4.5
    t = np.roll(c, -1, 1) - np.roll(c, 1, 1)
    t /= np.linalg.norm(t, axis=-1, keepdims=True)
    n = np.stack([-t[..., 1], t[..., 0]], -1)
    return c, t, n


class DuongDua:
    def __init__(self, B, rng, nhieu_lai=0.0):
        self.B, self.rng, self.nhieu_lai = B, rng, nhieu_lai

    def reset(self, duong=None):
        if duong is None:
            duong = tao_duong(self.rng, self.B)
        self.c, self.t, self.n = duong
        self.trai = self.c + self.n * RONG / 2
        self.phai = self.c - self.n * RONG / 2
        th0 = np.arctan2(self.t[:, 0, 1], self.t[:, 0, 0])
        self.x = np.stack([self.c[:, 0, 0], self.c[:, 0, 1], th0], 1)
        self.chi_so = np.zeros(self.B, int)          # điểm đường tâm gần nhất
        self.di_duoc = np.zeros(self.B, int)         # số điểm đã tiến (≥ N_DIEM = 1 vòng)
        self.done = np.zeros(self.B, bool)
        self.ket = np.zeros(self.B, int)             # 1 xong vòng, 2 ra khỏi đường
        self.lech = np.zeros(self.B)
        self.t_ = 0
        return self.quan_sat()

    def duong(self, i):
        return self.c[i:i + 1].copy(), self.t[i:i + 1].copy(), self.n[i:i + 1].copy()

    def gan_nhat(self):
        """Cập nhật điểm gần nhất (tìm quanh chỉ số cũ) và khoảng cách lệch tâm có dấu."""
        b = np.arange(self.B)
        k = (self.chi_so[:, None] + np.arange(-5, 15)[None]) % N_DIEM
        p = self.c[b[:, None], k]
        d = np.hypot(p[..., 0] - self.x[:, 0:1], p[..., 1] - self.x[:, 1:2])
        moi = k[b, d.argmin(1)]
        buoc = (moi - self.chi_so + N_DIEM // 2) % N_DIEM - N_DIEM // 2
        self.di_duoc += buoc
        self.chi_so = moi
        return ((self.x[:, :2] - self.c[b, moi]) * self.n[b, moi]).sum(-1)

    def tia(self):
        a = self.x[:, 2:3] + GOC_TIA[None]
        dx, dy = np.cos(a)[..., None], np.sin(a)[..., None]                 # (B, 9, 1)
        px, py = self.x[:, 0, None, None], self.x[:, 1, None, None]
        d = np.full((self.B, N_TIA), TAM)
        for bien in (self.trai, self.phai):
            q, q2 = bien, np.roll(bien, -1, 1)
            ex, ey = (q2 - q)[..., 0][:, None], (q2 - q)[..., 1][:, None]   # (B, 1, N)
            wx, wy = q[..., 0][:, None] - px, q[..., 1][:, None] - py
            den = dx * ey - dy * ex
            with np.errstate(divide="ignore", invalid="ignore"):
                s = (wx * ey - wy * ex) / den
                u = (wx * dy - wy * dx) / den
            ok = (np.abs(den) > 1e-9) & (s > 0) & (u >= 0) & (u <= 1)
            d = np.minimum(d, np.where(ok, s, TAM).min(-1))
        return d

    def quan_sat(self):
        return (self.tia() / TAM).astype(np.float32)

    def buoc(self, w):
        w = np.clip(w, -W_MAX, W_MAX)
        if self.nhieu_lai:
            w = w + self.rng.normal(0, self.nhieu_lai, self.B)
        song = ~self.done
        th = self.x[:, 2] + w * DT
        moi = np.stack([self.x[:, 0] + V * DT * np.cos(th), self.x[:, 1] + V * DT * np.sin(th), th], 1)
        self.x[song] = moi[song]
        lech = self.gan_nhat()
        ra = np.abs(lech) > RONG / 2 - R_ROBOT
        xong = self.di_duoc >= N_DIEM
        self.ket[song & ra] = 2
        self.ket[song & ~ra & xong] = 1
        self.done |= song & (ra | xong)
        self.t_ += 1
        if self.t_ >= T_MAX:
            self.done[:] = True
        self.lech = lech
        return self.quan_sat(), song


def chuyen_gia(env):
    """Pure pursuit: điểm đích trên đường tâm cách ~LD phía trước, ω = 2 v sin(α) / LD."""
    b = np.arange(env.B)
    k = (env.chi_so[:, None] + np.arange(0, 20)[None]) % N_DIEM
    p = env.c[b[:, None], k]
    d = np.hypot(p[..., 0] - env.x[:, 0:1], p[..., 1] - env.x[:, 1:2])
    j = np.where((d >= LD).any(1), (d >= LD).argmax(1), 19)
    g = p[b, j]
    al = np.arctan2(g[:, 1] - env.x[:, 1], g[:, 0] - env.x[:, 0]) - env.x[:, 2]
    al = (al + math.pi) % (2 * math.pi) - math.pi
    return np.clip(2 * V * np.sin(al) / LD, -W_MAX, W_MAX)


class NguoiHoc(nn.Module):
    def __init__(self, an=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(N_TIA, an), nn.Tanh(), nn.Linear(an, an), nn.Tanh(), nn.Linear(an, 1))

    def forward(self, x):
        return self.net(x)[..., 0] * W_MAX


def chay(env, lai, duong=None, nhan=False, ghi=False):
    obs = env.reset(duong)
    X, U, I, xs, sai, n = [], [], [], [env.x.copy()] if ghi else [], 0.0, 0
    while not env.done.all():
        song = ~env.done
        u = lai(env, obs)
        if nhan:
            ue = chuyen_gia(env)
            X.append(obs[song])
            U.append(ue[song])
            I.append(np.nonzero(song)[0])
            sai += float(np.abs(ue[song] - u[song]).sum())
            n += int(song.sum())
        obs, _ = env.buoc(u)
        if ghi:
            xs.append(env.x.copy())
    out = {"ket": env.ket.copy(), "xs": xs, "di": np.minimum(env.di_duoc, N_DIEM) / N_DIEM}
    if nhan:
        out.update(X=np.concatenate(X), U=np.concatenate(U).astype(np.float32), I=np.concatenate(I), sai=sai / max(n, 1))
    return out


def lai_chuyen_gia(env, obs):
    return chuyen_gia(env)


def lai_pi(pi):
    def f(env, obs):
        with torch.no_grad():
            return pi(torch.as_tensor(obs)).numpy()
    return f


def hoc(X, U, seed=0, n_buoc=3000, lr=3e-3):
    """Algorithm 1 bước 3–4: cực tiểu MSE giữa π_θ(x) và ω của chuyên gia trên 𝒟."""
    torch.manual_seed(seed)
    pi = NguoiHoc()
    opt = torch.optim.Adam(pi.parameters(), lr=lr)
    Xt, Ut = torch.as_tensor(X), torch.as_tensor(U)
    g = torch.Generator().manual_seed(seed)
    for _ in range(n_buoc):
        j = torch.randint(len(Xt), (256,), generator=g)
        loss = ((pi(Xt[j]) - Ut[j]) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return pi


def sai_so(pi, X, U):
    with torch.no_grad():
        return float(np.abs(pi(torch.as_tensor(X)).numpy() - U).mean())


def danh_gia(lai, n=500, seed=7, nhieu=0.0):
    env = DuongDua(n, np.random.default_rng(seed), nhieu)
    r = chay(env, lai)
    return {"xong": float((r["ket"] == 1).mean()), "ra": float((r["ket"] == 2).mean()), "di_tb": float(r["di"].mean())}


def dagger(n_vong=8, n_luot=10, seed=0, nhieu=0.0, log=print):
    """Algorithm 3: 𝒟 khởi đầu = n_luot vòng của chuyên gia; mỗi vòng π_θi tự lái, chuyên gia gán nhãn, gộp, học lại."""
    env = DuongDua(n_luot, np.random.default_rng(seed), nhieu)
    r = chay(env, lai_chuyen_gia, nhan=True)
    X, U = r["X"], r["U"]
    pi = hoc(X, U, seed=seed)
    ls = [(0, len(X), danh_gia(lai_pi(pi), nhieu=nhieu), None)]
    log(ls[-1])
    for i in range(1, n_vong + 1):
        r = chay(env, lai_pi(pi), nhan=True)
        X, U = np.concatenate([X, r["X"]]), np.concatenate([U, r["U"]])
        pi = hoc(X, U, seed=seed)
        ls.append((i, len(X), danh_gia(lai_pi(pi), nhieu=nhieu), r["sai"]))
        log(ls[-1])
    return pi, ls, (X, U)


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("chuyên gia", danh_gia(lai_chuyen_gia), round(time.time() - t0, 1))
    print("chuyên gia nhiễu 0.3", danh_gia(lai_chuyen_gia, nhieu=0.3), round(time.time() - t0, 1))
