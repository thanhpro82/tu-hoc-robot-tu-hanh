"""Đối chứng cho the_gioi.py: (1) lái ngẫu nhiên y như lúc thu dữ liệu, (2) cùng cách tưởng tượng nhưng mô hình thế giới
CHƯA học (trọng số ngẫu nhiên). Cho thấy điểm số tốt là nhờ mô hình đã học, không phải nhờ hàm chấm điểm."""
import json
from pathlib import Path

import numpy as np
import torch

import the_gioi as G
from the_gioi import R

GOC = Path(__file__).resolve().parent


def lai_ngau_nhien(seed=0):
    rng = np.random.default_rng(seed)
    w = [None]

    def f(env, obs):
        if w[0] is None:
            w[0] = rng.uniform(-R.W_MAX, R.W_MAX, env.B)
        w[0] = np.clip(0.8 * w[0] + rng.normal(0, 1.2, env.B), -R.W_MAX, R.W_MAX)
        return w[0]
    return f


if __name__ == "__main__":
    kq = {"ngau_nhien": R.danh_gia(lai_ngau_nhien())["xong"]}
    chua = []
    for s in (0, 1, 2, 3):
        torch.manual_seed(s)
        chua.append(R.danh_gia(G.lai_mo(G.TheGioi()))["xong"])
        print("chưa học", s, chua[-1], flush=True)
    kq["chua_hoc"] = chua
    print(json.dumps(kq))
    (GOC / "doi_chung.json").write_text(json.dumps(kq, indent=1), encoding="utf8")
