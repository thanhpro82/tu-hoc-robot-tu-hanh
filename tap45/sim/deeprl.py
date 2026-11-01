"""Tập 4.5 - Deep RL: luyện robot trong mô phỏng (Chương 18, Principles of Robot Autonomy).

Trạng thái liên tục (LiDAR + hướng đích) → không thể lập bảng Q như tập 4.4 → dùng mạng nơ-ron làm chính sách π_θ(u | x)
(xấp xỉ hàm, §18.5) và huấn luyện bằng gradient chính sách REINFORCE (§18.5.2, Eq. 18.31–18.32, Algorithm 6)
với biến thể "reward-to-go trừ baseline" của bài tập Cart-pole (§18.8, Problem 2):
    ∇_θ V(θ) ≈ (1/N) Σ_i Σ_t ∇_θ log π_θ(u_t^i | x_t^i) · (R_t^i − b),   R_t = Σ_{t'≥t} γ^{t'−t} r_{t'}
Môi trường (giả định): phòng 6 × 6 m, 4–7 vật cản tròn đặt ngẫu nhiên mỗi tập, robot unicycle v = 0,5 m/s,
3 lệnh ω ∈ {−1,5; 0; +1,5} rad/s, Δt = 0,2 s, tối đa 100 bước. Quan sát: 9 tia LiDAR (−90°..90°, tầm 3 m) + hướng và khoảng cách tới đích.
Thưởng (giả định, có "định hình" theo tiến độ — sách không bàn reward shaping): +10 tới đích, −10 va chạm, 2 × (khoảng cách giảm được) mỗi bước, −0,01 mỗi bước.
Sim-to-real (mở rộng, sách không nói): thử chính sách trong điều kiện "thật hơn" (LiDAR nhiễu σ 5 cm + mất 15% tia, bánh trượt ω × [0,6; 1,4],
động cơ trễ 1 nhịp 0,2 s),
so chính sách luyện trong mô phỏng sạch với chính sách luyện có ngẫu nhiên hoá miền (domain randomization).
"""
import math

import numpy as np
import torch
import torch.nn as nn

RONG = 6.0
V, DT, T_MAX = 0.5, 0.2, 100
OMEGA = np.array([-1.5, 0.0, 1.5])
N_TIA, TAM = 9, 3.0
GOC_TIA = np.linspace(-math.pi / 2, math.pi / 2, N_TIA)
R_ROBOT, R_DICH = 0.15, 0.3
N_OBS = 12


class MoiTruong:
    """B tập chạy song song (vector hoá bằng numpy)."""

    def __init__(self, B, rng, nhieu=False):
        self.B, self.rng, self.nhieu = B, rng, nhieu

    def reset(self, layout=None):
        B, rng = self.B, self.rng
        if layout is not None:
            self.obs_c, self.obs_r, self.x, self.goal = [np.repeat(a[None], B, 0).copy() for a in layout]
        else:
            k = rng.integers(4, 8, B)
            self.obs_c = rng.uniform(1.4, 4.6, (B, N_OBS, 2))
            self.obs_r = rng.uniform(0.25, 0.55, (B, N_OBS)) * (np.arange(N_OBS)[None] < k[:, None])
            self.x = np.stack([rng.uniform(0.4, 1.0, B), rng.uniform(0.6, 5.4, B), rng.uniform(-0.5, 0.5, B)], 1)
            self.goal = np.stack([rng.uniform(5.0, 5.6, B), rng.uniform(0.6, 5.4, B)], 1)
        self.done = np.zeros(self.B, bool)
        self.ket = np.zeros(self.B, int)        # 0 đang chạy/hết giờ, 1 tới đích, 2 va chạm
        self.t = 0
        self.d_cu = np.hypot(*(self.goal - self.x[:, :2]).T)
        self.ty_le_truot = self.rng.uniform(0.6, 1.4, self.B) if self.nhieu else np.ones(self.B)
        self.u_cu = np.ones(self.B, int)        # lệnh đang thực thi (trễ 1 nhịp khi 'nhiễu')
        return self.quan_sat()

    def layout(self, i):
        return self.obs_c[i].copy(), self.obs_r[i].copy(), self.x[i].copy(), self.goal[i].copy()

    def tia(self):
        """Khoảng cách 9 tia tới vật cản tròn / tường, (B, 9)."""
        a = self.x[:, 2:3] + GOC_TIA[None]                       # (B, 9)
        dx, dy = np.cos(a), np.sin(a)
        px, py = self.x[:, 0:1], self.x[:, 1:2]
        d = np.full(a.shape, TAM)
        # tường
        with np.errstate(divide="ignore", invalid="ignore"):
            for p, dd in ((px, dx), (py, dy)):
                for w in (0.0, RONG):
                    t = (w - p) / dd
                    d = np.where((t > 0) & (t < d), t, d)
        # vật cản tròn: |p + t·d − c|² = r²
        ox = self.obs_c[:, None, :, 0] - px[:, :, None]           # (B, 1, K)
        oy = self.obs_c[:, None, :, 1] - py[:, :, None]
        bproj = dx[:, :, None] * ox + dy[:, :, None] * oy        # (B, 9, K)
        c2 = ox ** 2 + oy ** 2 - self.obs_r[:, None, :] ** 2
        disc = bproj ** 2 - c2
        t = bproj - np.sqrt(np.maximum(disc, 0))
        hop = (disc > 0) & (t > 0) & (self.obs_r[:, None, :] > 0)
        t = np.where(hop, t, TAM)
        return np.minimum(d, t.min(axis=2))

    def quan_sat(self):
        r = self.tia()
        if self.nhieu:
            r = r + self.rng.normal(0, 0.05, r.shape)
            r = np.where(self.rng.random(r.shape) < 0.15, TAM, r)  # mất tia
            r = np.clip(r, 0, TAM)
        self.r_cuoi = r
        g = self.goal - self.x[:, :2]
        ga = np.arctan2(g[:, 1], g[:, 0]) - self.x[:, 2]
        return np.concatenate([r / TAM, np.cos(ga)[:, None], np.sin(ga)[:, None], (np.hypot(*g.T) / 6)[:, None]], 1).astype(np.float32)

    def buoc(self, u):
        if self.nhieu:                         # động cơ trễ 1 nhịp (0,2 s): thực thi lệnh của nhịp trước
            u, self.u_cu = self.u_cu, u
        w = OMEGA[u] * self.ty_le_truot
        th = self.x[:, 2] + w * DT
        nx = self.x[:, 0] + V * DT * np.cos(th)
        ny = self.x[:, 1] + V * DT * np.sin(th)
        song = ~self.done
        self.x[song] = np.stack([nx, ny, th], 1)[song]
        d = np.hypot(*(self.goal - self.x[:, :2]).T)
        dc = np.hypot(self.obs_c[..., 0] - self.x[:, 0:1], self.obs_c[..., 1] - self.x[:, 1:2]) - self.obs_r
        va = ((dc < R_ROBOT) & (self.obs_r > 0)).any(1) | (self.x[:, 0] < R_ROBOT) | (self.x[:, 0] > RONG - R_ROBOT) \
            | (self.x[:, 1] < R_ROBOT) | (self.x[:, 1] > RONG - R_ROBOT)
        toi = d < R_DICH
        r = 2.0 * (self.d_cu - d) - 0.01
        r = np.where(toi, r + 10, r)
        r = np.where(va & ~toi, r - 10, r)
        r = np.where(song, r, 0.0)
        moi_xong = song & (toi | va)
        self.ket[moi_xong & toi] = 1
        self.ket[moi_xong & va & ~toi] = 2
        self.done |= moi_xong
        self.t += 1
        if self.t >= T_MAX:
            self.done[:] = True
        self.d_cu = d
        return self.quan_sat(), r.astype(np.float32), song


class ChinhSach(nn.Module):
    def __init__(self, n_vao=N_TIA + 3, an=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_vao, an), nn.Tanh(), nn.Linear(an, an), nn.Tanh(), nn.Linear(an, 3))

    def forward(self, x):
        return torch.distributions.Categorical(logits=self.net(x))


def chay_tap(pi, env, layout=None, tham_lam=False, ghi=False):
    obs = env.reset(layout)
    logp, rew, alive, xs = [], [], [], [env.x.copy()] if ghi else []
    while not env.done.all():
        dist = pi(torch.as_tensor(obs))
        u = dist.probs.argmax(-1) if tham_lam else dist.sample()
        obs, r, song = env.buoc(u.numpy())
        logp.append(dist.log_prob(u))
        rew.append(r)
        alive.append(song)
        if ghi:
            xs.append(env.x.copy())
    return logp, np.array(rew), np.array(alive), xs


def huan_luyen(n_cap_nhat=300, B=64, gamma=0.99, lr=3e-3, seed=0, nhieu=False, ghi_moi=10, log=print):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    pi = ChinhSach()
    opt = torch.optim.Adam(pi.parameters(), lr=lr)
    env = MoiTruong(B, rng, nhieu=nhieu)
    lich_su = []
    for k in range(n_cap_nhat):
        logp, rew, alive, _ = chay_tap(pi, env)
        # reward-to-go R_t = Σ_{t'≥t} γ^{t'−t} r_t'
        R = np.zeros_like(rew)
        acc = np.zeros(B, np.float32)
        for t in range(len(rew) - 1, -1, -1):
            acc = rew[t] + gamma * acc
            R[t] = acc
        m = alive.astype(bool)
        b = R[m].mean()                                   # baseline = trung bình
        A = (R - b) / (R[m].std() + 1e-8)
        lp = torch.stack(logp)
        loss = -(lp * torch.as_tensor(A) * torch.as_tensor(m.astype(np.float32))).sum() / B
        opt.zero_grad()
        loss.backward()
        opt.step()
        if k % ghi_moi == 0 or k == n_cap_nhat - 1:
            ty_le = np.bincount(env.ket, minlength=3) / B
            lich_su.append((k, float(ty_le[1]), float(ty_le[2]), float(rew.sum(0).mean())))
            log(f"cập nhật {k:4d}: tới đích {ty_le[1]*100:5.1f}%  va chạm {ty_le[2]*100:5.1f}%  thưởng TB {rew.sum(0).mean():6.2f}")
    return pi, lich_su


def danh_gia(pi, n=1000, seed=123, nhieu=False, tham_lam=False):
    env = MoiTruong(n, np.random.default_rng(seed), nhieu=nhieu)
    torch.manual_seed(seed)
    with torch.no_grad():
        chay_tap(pi, env, tham_lam=tham_lam)
    c = np.bincount(env.ket, minlength=3) / n
    return {"toi": float(c[1]), "va": float(c[2]), "het_gio": float(c[0])}


def so_tham_so(pi):
    return sum(p.numel() for p in pi.parameters())


if __name__ == "__main__":
    import time
    t0 = time.time()
    pi, ls = huan_luyen(n_cap_nhat=60, ghi_moi=10)
    print("thời gian", round(time.time() - t0, 1), "s; tham số", so_tham_so(pi), danh_gia(pi, 500))
