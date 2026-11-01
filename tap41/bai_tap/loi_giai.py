"""Lời giải bài tập tập 4.1. Tự làm fsm_cua_ban.py trước rồi hãy mở!"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
from fsm import ghep_song_song  # noqa: E402,F401  (Bài 3 có sẵn trong code video)


def chuyen_B():
    return {("TUAN_TRA", "THAY"): "DUOI", ("DUOI", "KHONG_THAY"): "TIM", ("TIM", "THAY"): "DUOI", ("TIM", "HET_GIO"): "TUAN_TRA"}


def them_sac(chuyen):
    c = dict(chuyen)
    for s in ("TUAN_TRA", "DUOI", "TIM"):
        c[(s, "PIN_YEU")] = "VE_SAC"
    c.update({("VE_SAC", "TOI_DOC"): "SAC", ("SAC", "DAY_PIN"): "TUAN_TRA"})
    return c
