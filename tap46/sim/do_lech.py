"""Đo phân bố độ lệch tâm của các trạng thái đã đi qua: chuyên gia vs BC 2 vòng vs DAgger (100 đường, 4 seed)."""
import numpy as np, torch
import duongdua as R

def lech(lai, seed):
    env = R.DuongDua(100, np.random.default_rng(seed))
    obs = env.reset(); L = []
    while not env.done.all():
        song = ~env.done
        obs, _ = env.buoc(lai(env, obs)); L.append(np.abs(env.lech[song]))
    return np.concatenate(L)

def nap(t):
    p = R.NguoiHoc(); p.load_state_dict(torch.load(t)); return p
kq = {"cg": lech(R.lai_chuyen_gia, 321)}
for ten, f in (("bc2", "dd_bc2_{}.pt"), ("dag", "dd_dagger_{}.pt")):
    kq[ten] = np.concatenate([lech(R.lai_pi(nap(f.format(s))), 321) for s in range(4)])
for k, v in kq.items():
    print(k, "n", len(v), "TB lệch cm", round(100 * v.mean(), 1), "%>15cm", round(100 * (v > 0.15).mean(), 1), "%>20cm", round(100 * (v > 0.2).mean(), 1))
