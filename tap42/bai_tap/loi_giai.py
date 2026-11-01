"""Lời giải bài tập tập 4.2. Tự làm mdp_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
import mdp as _m  # noqa: E402
from mdp import chuyen, danh_gia  # noqa: E402,F401  (Bài 1, 2 có sẵn trong code video)


def mo_phong(pi, eps, n=2000, seed=42):
    kq = _m.mo_phong(pi, eps, n=n, seed=seed)
    return {"toi": kq["toi"], "roi": kq["roi"]}
