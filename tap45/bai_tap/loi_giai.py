"""Lời giải bài tập tập 4.5 (tách từ hàm huan_luyen() trong ../sim/deeprl.py). Tự làm deeprl_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from deeprl import chay_tap  # noqa: E402


def reward_to_go(rew, gamma):
    R = np.zeros_like(rew)
    acc = np.zeros(rew.shape[1], np.float32)
    for t in range(len(rew) - 1, -1, -1):
        acc = rew[t] + gamma * acc
        R[t] = acc
    return R


def loi_reinforce(logp, R, alive):
    m = alive.astype(bool)
    A = (R - R[m].mean()) / (R[m].std() + 1e-8)
    return -(torch.stack(logp) * torch.as_tensor(A) * torch.as_tensor(m.astype(np.float32))).sum() / R.shape[1]


def mot_cap_nhat(pi, opt, env, gamma=0.99):
    logp, rew, alive, _ = chay_tap(pi, env)
    loss = loi_reinforce(logp, reward_to_go(rew, gamma), alive)
    opt.zero_grad()
    loss.backward()
    opt.step()
    return rew, env.ket
