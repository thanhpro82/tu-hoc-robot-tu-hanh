"""Tập 3.9 - Phân tích lần chạy Nav2 thật (tap39/ws/out): AMCL sửa vị trí bấm lệch, cửa đóng -> lập lại đường, tới bếp.

Hệ map = hệ bản đồ slam_toolbox tập 3.7 (gốc ở chỗ xuất phát X0 của thế giới). Tư thế thật đổi sang hệ map bằng cách trừ X0.
"""
import json
import math
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1] / "ws"
OUT = WS / "out"
NAV = json.loads((OUT / "nav.json").read_text())
R = [json.loads(l) for l in (OUT / "robot.jsonl").read_text().splitlines() if l.strip()]
X0 = np.array([1.2, 2.6, 0.0])
T0, T1 = NAV["ket_qua"]["t_lenh"], NAV["ket_qua"]["t_toi"]


def goc(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


TR = np.array([r["t"] for r in R]) - T0
THAT = np.array([r["that"] for r in R]) - X0           # hệ map
ODO = np.array([r["odo"] for r in R]) - X0
A = np.array(NAV["amcl"])
TA, AM = A[:, 0] - T0, A[:, 1:4]
SIG_A = np.sqrt(A[:, 4] + A[:, 5])


def that_luc(t):
    i = np.clip(np.searchsorted(TR, t), 0, len(TR) - 1)
    return THAT[i]


E_AMCL = np.array([math.hypot(*(AM[k, :2] - that_luc(TA[k])[:2])) for k in range(len(TA))])
E_AMCL_TH = np.array([abs(goc(AM[k, 2] - that_luc(TA[k])[2])) for k in range(len(TA))])
CHAY = (TR >= 0) & (TR <= T1 - T0)
E_ODO = np.hypot(*(ODO[:, :2] - THAT[:, :2]).T)
i_toi = np.searchsorted(TR, T1 - T0)
BEP = np.array(NAV["bep"])
TOI = THAT[min(i_toi, len(THAT) - 1)]
E_TOI = math.hypot(*(TOI[:2] - BEP[:2]))
QUANG_DUONG = float(np.hypot(*np.diff(THAT[CHAY, :2], axis=0).T).sum())
UOC = np.array(NAV["uoc_luong"])
E_UOC = math.hypot(*UOC[:2])
PLAN = NAV["plan"]
TP = np.array([p["t"] for p in PLAN]) - T0
# đường đầu tiên đi qua cửa dưới (x map ≈ 4,85, y map ≈ -0,5) hay không
QUA_DUOI = [bool(((np.abs(np.array(p["xy"])[:, 0] - 4.85) < 0.4) & (np.array(p["xy"])[:, 1] < 0.6)).any()) for p in PLAN]
k_doi = QUA_DUOI.index(False)
T_DOI = float(TP[k_doi])
VT_DOI = that_luc(T_DOI)
CUA = np.array([4.85, -0.5])
KC_CUA = math.hypot(*(VT_DOI[:2] - CUA))
DAI0 = PLAN[0]["dai"]
DAI_MOI = PLAN[k_doi]["dai"]
HAT = NAV["hat"]
TH = np.array([h["t"] for h in HAT]) - T0
SPREAD = np.array([np.sqrt(np.var(np.array(h["xy"]), axis=0).sum()) for h in HAT])
VA_CHAM = R[-1]["va_cham"]
# AMCL "hội tụ": lần đầu sai số < 10 cm
k_hoi = int(np.argmax(E_AMCL < 0.10))
DT = T1 - T0

if __name__ == "__main__":
    print(f"bấm ước lượng lệch {E_UOC*100:.0f} cm, {math.degrees(UOC[2]):.0f}°; hạt ban đầu σ ≈ {SPREAD[0]*100:.0f} cm, số hạt {HAT[0]['n']} -> {HAT[-1]['n']}")
    print(f"AMCL: sai số lần đầu {E_AMCL[0]*100:.1f} cm; < 10 cm lúc t = {TA[k_hoi]:.1f} s; trung bình khi chạy (t>{TA[k_hoi]:.0f}s) "
          f"{E_AMCL[k_hoi:].mean()*100:.1f} cm, max {E_AMCL[k_hoi:].max()*100:.1f} cm, góc TB {math.degrees(E_AMCL_TH[k_hoi:].mean()):.1f}°")
    print(f"đường đầu tiên {DAI0:.2f} m qua cửa dưới; t = {T_DOI:.1f} s đổi sang đường mới {DAI_MOI:.2f} m (robot cách cửa {KC_CUA:.2f} m); số lần lập đường {len(PLAN)}")
    print(f"tới bếp sau {DT:.1f} s, quãng đường {QUANG_DUONG:.2f} m, lệch đích {E_TOI*100:.1f} cm, va chạm {VA_CHAM}, phục hồi {NAV['ket_qua']['hoi_phuc']}")
    print(f"odometry lúc tới nơi lệch {E_ODO[min(i_toi, len(E_ODO)-1)]*100:.0f} cm (AMCL lúc đó {E_AMCL[-1]*100:.1f} cm)")
