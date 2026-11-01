"""Tập 4.7 - Mô hình thế giới thu nhỏ: robot "tưởng tượng" trước khi lái (phần Prospects: "World models").

Sách nêu: mô hình thế giới học cách thế giới thay đổi theo thời gian từ dữ liệu cảm biến, để robot dự đoán /
tưởng tượng các tương lai rồi lập kế hoạch trên đó; dữ liệu tương tác của robot đắt, nên mô hình nên học từ dữ liệu rẻ.
Phiên bản thu nhỏ ở đây (mở rộng, giả định):
- Dữ liệu: robot lái NGẪU NHIÊN (không có chuyên gia, không có nhãn lệnh đúng) trên các đường đua của tập 4.6,
  ghi lại (9 tia LiDAR o_t, lệnh rẽ ω_t, 9 tia o_{t+1}).
- Mô hình thế giới f_ψ: mạng 10-128-128-9, học Δo = o_{t+1} − o_t (MSE).
- Lái bằng tưởng tượng: mỗi bước thử 25 lệnh ω (giữ nguyên 0,8 s), dùng f_ψ "mơ" ra 8 bước tia LiDAR tương lai,
  chấm điểm (xa mép, giữa đường), chọn lệnh tốt nhất, chỉ thực hiện bước đầu rồi lặp lại (kiểu MPC).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

T46 = Path(__file__).resolve().parents[2] / "tap46/sim"
sys.path.insert(0, str(T46))
import duongdua as R  # noqa: E402

GOC = Path(__file__).resolve().parent
SIN = np.sin(R.GOC_TIA)
TRAI, PHAI = R.GOC_TIA > 0.1, R.GOC_TIA < -0.1
W_THU = np.linspace(-R.W_MAX, R.W_MAX, 25)
H = 8


class TheGioi(nn.Module):
    def __init__(self, an=128):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(R.N_TIA + 1, an), nn.Tanh(), nn.Linear(an, an), nn.Tanh(), nn.Linear(an, R.N_TIA))

    def forward(self, o, w):
        return o + 0.1 * self.net(torch.cat([o, w[..., None] / R.W_MAX], -1))


def thu_du_lieu(n_duong, seed):
    """Lái ngẫu nhiên: ω là nhiễu đỏ (đổi dần), mỗi đường chạy tới khi ra khỏi đường hoặc hết giờ."""
    rng = np.random.default_rng(seed)
    env = R.DuongDua(n_duong, rng)
    o = env.reset()
    w = rng.uniform(-R.W_MAX, R.W_MAX, n_duong)
    O, W, O2 = [], [], []
    while not env.done.all():
        song = ~env.done
        w = np.clip(0.8 * w + rng.normal(0, 1.2, n_duong), -R.W_MAX, R.W_MAX)
        o2, _ = env.buoc(w)
        O.append(o[song]), W.append(w[song]), O2.append(o2[song])
        o = o2
    return np.concatenate(O), np.concatenate(W).astype(np.float32), np.concatenate(O2)


def hoc(O, W, O2, seed=0, n_buoc=6000, lr=2e-3):
    torch.manual_seed(seed)
    f = TheGioi()
    opt = torch.optim.Adam(f.parameters(), lr=lr)
    Ot, Wt, O2t = map(torch.as_tensor, (O, W, O2))
    g = torch.Generator().manual_seed(seed)
    for i in range(n_buoc):
        j = torch.randint(len(Ot), (512,), generator=g)
        loss = ((f(Ot[j], Wt[j]) - O2t[j]) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return f


def khoang_ho_t(o):
    d = o * R.TAM
    s = torch.as_tensor(SIN, dtype=d.dtype)
    return (d[..., TRAI] * s[TRAI]).min(-1).values, (d[..., PHAI] * -s[PHAI]).min(-1).values


def diem(o):
    """Chi phí một trạng thái tưởng tượng: sát mép bị phạt nặng, lệch tâm bị phạt nhẹ."""
    cl, cr = khoang_ho_t(o)
    return (cl - cr) ** 2 + 20 * torch.relu(0.2 - torch.minimum(cl, cr)) + 0.3 * torch.relu(1.0 - o[..., 4] * R.TAM)


def tuong_tuong(f, o):
    """o (B,9) → tia tưởng tượng (B, 25, H, 9) và chi phí (B, 25)."""
    B = o.shape[0]
    with torch.no_grad():
        x = torch.as_tensor(o).unsqueeze(1).expand(B, len(W_THU), R.N_TIA).reshape(-1, R.N_TIA)
        w = torch.as_tensor(W_THU, dtype=torch.float32).repeat(B)
        seq, cost = [], 0
        for h in range(H):
            x = f(x, w).clamp(0, 1)
            seq.append(x)
            cost = cost + diem(x) * (0.9 ** h)
    return torch.stack(seq, 1).reshape(B, len(W_THU), H, R.N_TIA).numpy(), cost.reshape(B, len(W_THU)).numpy()


def lai_mo(f):
    def lai(env, obs):
        _, c = tuong_tuong(f, obs)
        return W_THU[c.argmin(1)]
    return lai


def sai_du_doan(f, seed=99, n=200):
    """So tia tưởng tượng với tia thật khi robot thật đi theo đúng chuỗi lệnh đó (lấy theo chuyên gia + nhiễu)."""
    rng = np.random.default_rng(seed)
    env = R.DuongDua(n, rng, nhieu_lai=0.3)
    o = env.reset()
    obs_hist, w_hist = [o], []
    for t in range(40):
        w = R.chuyen_gia(env)
        o, _ = env.buoc(w)
        obs_hist.append(o)
        w_hist.append(env.x[:, 2] * 0 + w)
    ok = ~env.done
    x = torch.as_tensor(obs_hist[20])
    out = []
    with torch.no_grad():
        for h in range(H):
            x = f(x, torch.as_tensor(w_hist[20 + h].astype(np.float32))).clamp(0, 1)
            out.append(float((np.abs(x.numpy() - obs_hist[21 + h]) * R.TAM)[ok].mean()))
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    kq = {}
    for n_duong in (int(a) for a in (sys.argv[1:] or ["200"])):
        res = []
        for s in (0, 1, 2, 3):
            O, W, O2 = thu_du_lieu(n_duong, 100 + s)
            f = hoc(O, W, O2, seed=s)
            torch.save(f.state_dict(), GOC / f"tg{n_duong}_{s}.pt")
            r = R.danh_gia(lai_mo(f))
            e = sai_du_doan(f)
            res.append({"n_mau": len(O), "xong": r["xong"], "di_tb": r["di_tb"], "sai": e})
            print(n_duong, s, len(O), r, [round(v, 3) for v in e], round(time.time() - t0), flush=True)
        kq[n_duong] = res
    (GOC / ("the_gioi_" + "_".join(sys.argv[1:] or ["200"]) + ".json")).write_text(json.dumps(kq, indent=1), encoding="utf8")
