"""Tập 4.6 - Học bắt chước: robot học từ người lái (Chương 19, Principles of Robot Autonomy).

Dùng lại phòng vật cản của tập 4.5 (tap45/sim/deeprl.py): phòng 6 × 6 m, 4–7 vật cản tròn, unicycle v = 0,5 m/s,
3 lệnh ω ∈ {−1,5; 0; +1,5}, Δt = 0,2 s, quan sát 9 tia LiDAR + hướng/khoảng cách tới đích.
Chuyên gia π* (giả định, thay cho người lái): bộ lập kế hoạch nhìn trước biết bản đồ thật — thử 3^4 = 81 chuỗi lệnh
(mỗi lệnh giữ 2 nhịp = 1,6 s), bỏ chuỗi va chạm, chọn chuỗi kết thúc gần đích nhất, thực thi lệnh đầu.
Người học π_θ chỉ thấy LiDAR (mạng 12-64-64-3 như 4.5).
- Behavior cloning (§19.2, Algorithm 1): tập dữ liệu 𝒟 = {(x_i, u_i)} từ các lượt lái của chuyên gia, học bằng
  phân loại (loss entropy chéo, một dạng KL mà sách liệt kê).
- DAgger (§19.2.1, Algorithm 3): cho π_θi tự lái, chuyên gia gán nhãn lệnh đúng cho các trạng thái robot đã đi qua,
  gộp 𝒟 ← 𝒟 ∪ 𝒟_i, học lại π_θ(i+1).
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tap45/sim"))
import deeprl as D  # noqa: E402

SEQ = np.array(list(itertools.product(range(3), repeat=4)))   # (81, 4)
GIU = 2                                                         # mỗi lệnh giữ 2 nhịp
LE = 0.06                                                       # lề an toàn thêm khi lập kế hoạch (m)


O = 0.1                                                         # ô lưới của bản đồ khoảng cách (m)
NO = int(D.RONG / O)


def ban_do_kc(env):
    """Khoảng cách đi được (m) từ mỗi ô tới đích, tránh vật cản đã nở thêm bán kính robot — tính một lần mỗi lượt."""
    c = (np.arange(NO) + 0.5) * O
    gx, gy = np.meshgrid(c, c, indexing="ij")                                      # (NO, NO)
    dc = np.hypot(gx[None, :, :, None] - env.obs_c[:, None, None, :, 0], gy[None, :, :, None] - env.obs_c[:, None, None, :, 1]) - env.obs_r[:, None, None, :]
    dc = np.where(env.obs_r[:, None, None, :] > 0, dc, 9.0).min(-1)
    tuong = np.minimum.reduce([gx, gy, D.RONG - gx, D.RONG - gy])[None]
    chan = np.minimum(dc, tuong) < D.R_ROBOT + LE
    dd = np.hypot(gx[None] - env.goal[:, 0, None, None], gy[None] - env.goal[:, 1, None, None])
    kc = np.where(dd < D.R_DICH, 0.0, 1e3)
    kc[chan] = 1e3
    for _ in range(4 * NO):
        p = np.pad(kc, ((0, 0), (1, 1), (1, 1)), constant_values=1e3)
        m = np.minimum.reduce([p[:, 1:-1, :-2], p[:, 1:-1, 2:], p[:, :-2, 1:-1], p[:, 2:, 1:-1]]) + O
        m2 = np.minimum.reduce([p[:, :-2, :-2], p[:, :-2, 2:], p[:, 2:, :-2], p[:, 2:, 2:]]) + O * 1.414
        moi = np.where(chan, 1e3, np.minimum(kc, np.minimum(m, m2)))
        if np.array_equal(moi, kc):
            break
        kc = moi
    return kc


def chuyen_gia(env):
    """Lệnh của chuyên gia cho mọi môi trường đang chạy, (B,). Biết vị trí thật và bản đồ thật."""
    B = env.B
    if getattr(env, "_khoa", None) is not env.obs_c:
        env._kc, env._khoa = ban_do_kc(env), env.obs_c
    x = np.repeat(env.x[:, None, :], len(SEQ), 1)              # (B, 81, 3)
    hong = np.zeros((B, len(SEQ)), bool)
    toi = np.zeros((B, len(SEQ)), bool)
    kc_min = np.full((B, len(SEQ)), 9.0)
    song_duoc = np.zeros((B, len(SEQ)))                        # số nhịp đi được trước khi va
    for k in range(SEQ.shape[1]):
        w = D.OMEGA[SEQ[:, k]][None]
        for _ in range(GIU):
            th = x[..., 2] + w * D.DT
            x = np.stack([x[..., 0] + D.V * D.DT * np.cos(th), x[..., 1] + D.V * D.DT * np.sin(th), th], -1)
            dc = np.hypot(env.obs_c[:, None, :, 0] - x[..., 0:1], env.obs_c[:, None, :, 1] - x[..., 1:2]) - env.obs_r[:, None, :]
            dc = np.where(env.obs_r[:, None, :] > 0, dc, 9.0).min(-1)
            dt_ = np.minimum.reduce([x[..., 0], x[..., 1], D.RONG - x[..., 0], D.RONG - x[..., 1]])
            kc = np.minimum(dc, dt_)
            d = np.hypot(env.goal[:, None, 0] - x[..., 0], env.goal[:, None, 1] - x[..., 1])
            toi |= (d < D.R_DICH) & ~hong
            hong |= (kc < D.R_ROBOT + LE) & ~toi
            song_duoc += ~hong
            kc_min = np.minimum(kc_min, kc)
    fx = np.clip(x[..., 0] / O - 0.5, 0, NO - 1.001)              # nội suy song tuyến trên lưới
    fy = np.clip(x[..., 1] / O - 0.5, 0, NO - 1.001)
    i, j = fx.astype(int), fy.astype(int)
    a, b = fx - i, fy - j
    K, bi = np.minimum(env._kc, 50.0), np.arange(B)[:, None]
    d = (K[bi, i, j] * (1 - a) * (1 - b) + K[bi, i + 1, j] * a * (1 - b) + K[bi, i, j + 1] * (1 - a) * b + K[bi, i + 1, j + 1] * a * b)
    diem = -d + 0.3 * np.minimum(kc_min, 0.5) + 100 * toi - 1000 * hong + 10 * song_duoc * hong + 0.02 * (SEQ[:, 0] == 1)[None]
    return SEQ[diem.argmax(1), 0]


class NguoiHoc(nn.Module):
    def __init__(self, n_vao=D.N_TIA + 3, an=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_vao, an), nn.Tanh(), nn.Linear(an, an), nn.Tanh(), nn.Linear(an, 3))

    def forward(self, x):
        return self.net(x)


def chay(env, lai, layout=None, nhan=False, ghi=False):
    """Cho `lai` (hàm env, obs -> lệnh) lái; trả về các (obs, lệnh chuyên gia) đã đi qua nếu nhan=True."""
    obs = env.reset(layout)
    X, U, I, xs, sai, n = [], [], [], [env.x.copy()] if ghi else [], 0, 0
    while not env.done.all():
        song = ~env.done
        u = lai(env, obs)
        if nhan:
            ue = chuyen_gia(env)
            X.append(obs[song])
            U.append(ue[song])
            I.append(np.nonzero(song)[0])
            sai += int((ue[song] != u[song]).sum())
            n += int(song.sum())
        obs, _, _ = env.buoc(u)
        if ghi:
            xs.append(env.x.copy())
    out = {"ket": env.ket.copy(), "xs": xs}
    if nhan:
        out["X"], out["U"], out["I"], out["sai"] = np.concatenate(X), np.concatenate(U), np.concatenate(I), sai / max(n, 1)
    return out


def lai_chuyen_gia(env, obs):
    return chuyen_gia(env)


def lai_pi(pi):
    def f(env, obs):
        with torch.no_grad():
            return pi(torch.as_tensor(obs)).argmax(-1).numpy()
    return f


def hoc(X, U, seed=0, n_buoc=4000, lr=3e-3):
    """Học có giám sát trên 𝒟 (Algorithm 1): cực tiểu entropy chéo giữa π_θ(·|x) và lệnh chuyên gia, số bước cố định."""
    torch.manual_seed(seed)
    pi = NguoiHoc()
    opt = torch.optim.Adam(pi.parameters(), lr=lr)
    Xt, Ut = torch.as_tensor(X), torch.as_tensor(U, dtype=torch.long)
    g = torch.Generator().manual_seed(seed)
    for _ in range(n_buoc):
        j = torch.randint(len(Xt), (256,), generator=g)
        loss = nn.functional.cross_entropy(pi(Xt[j]), Ut[j])
        opt.zero_grad()
        loss.backward()
        opt.step()
    return pi


def ty_le_sai(pi, X, U):
    with torch.no_grad():
        return float((pi(torch.as_tensor(X)).argmax(-1).numpy() != U).mean())


def danh_gia(lai, n=1000, seed=123):
    env = D.MoiTruong(n, np.random.default_rng(seed))
    r = chay(env, lai)
    c = np.bincount(r["ket"], minlength=3) / n
    return {"toi": float(c[1]), "va": float(c[2]), "het_gio": float(c[0])}


def dagger(n_vong=10, n_luot=20, seed=0, log=print):
    """Algorithm 3: 𝒟 khởi đầu = n_luot lượt của chuyên gia; mỗi vòng π_θi tự lái n_luot lượt, chuyên gia gán nhãn, gộp, học lại."""
    rng = np.random.default_rng(seed)
    env = D.MoiTruong(n_luot, rng)
    r = chay(env, lai_chuyen_gia, nhan=True)
    X, U = r["X"], r["U"]
    pi = hoc(X, U, seed=seed)
    lich_su = [(0, len(X), danh_gia(lai_pi(pi), seed=7), None)]
    log(lich_su[-1])
    for i in range(1, n_vong + 1):
        r = chay(env, lai_pi(pi), nhan=True)                # robot tự lái, chuyên gia chỉ "nói" lệnh đúng
        X, U = np.concatenate([X, r["X"]]), np.concatenate([U, r["U"]])
        pi = hoc(X, U, seed=seed)
        lich_su.append((i, len(X), danh_gia(lai_pi(pi), seed=7), r["sai"]))
        log(lich_su[-1])
    return pi, lich_su, (X, U)


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("chuyên gia", danh_gia(lai_chuyen_gia, 500), round(time.time() - t0, 1), "s")
