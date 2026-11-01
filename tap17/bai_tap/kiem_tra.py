"""Tự chấm bài tập tập 1.7. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "ws"), str(_D.parents[1])]
import a_sao  # noqa: E402  (A* của tập 1.5, chép vào ws/)
import duong_di as goc  # noqa: E402  (đổi ô sang mét + làm mượt, dùng trong planner_node)
import loi_giai as _lg  # noqa: E402
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

V_REF, A_REF = 0.3, 0.3          # như controller_node.py
DUONG_O = [goc.o_sang_met(o) for o in a_sao.A_SAO[0]]   # đường A* 26 ô, đổi sang mét


def bai_1(ns):
    f = ham(ns, "lam_muot")
    r = f([(0, 0), (4, 0), (4, 4)], 1)
    assert gan(r, [(0, 0), (1, 0), (3, 0), (4, 1), (4, 3), (4, 4)]), \
        f"làm mượt 1 lần đường (0,0)→(4,0)→(4,4) phải ra [(0,0),(1,0),(3,0),(4,1),(4,3),(4,4)], bạn ra {r}"
    muot = f(DUONG_O, 3)
    dap = goc.lam_muot(DUONG_O, 3)
    assert gan(muot, dap), "làm mượt 3 lần đường A* chưa khớp planner trong video"
    return f"đường A* {goc.do_dai(DUONG_O):.2f} m → làm mượt {len(muot)} điểm, dài {goc.do_dai(muot):.2f} m như log của planner"


def bai_2(ns):
    f = ham(ns, "s_tai")
    L = goc.do_dai(goc.lam_muot(DUONG_O, 3))
    T = L / V_REF + V_REF / A_REF
    assert gan(f(0, L, V_REF, A_REF), 0) and gan(f(T, L, V_REF, A_REF), L), "đầu đường s = 0, cuối đường (t = T) s = L"
    assert gan(f(0.5, L, V_REF, A_REF), 0.5 * 0.3 * 0.25), "t = 0.5 s đang tăng tốc: s = ½·0.3·0.5² = 0.0375 m"
    assert gan(f(T + 10, L, V_REF, A_REF), L), "sau thời gian T thì đứng yên ở cuối đường (kẹp t)"
    for t in [i * 0.37 for i in range(70)]:
        assert gan(f(t, L, V_REF, A_REF), _lg.s_tai(t, L, V_REF, A_REF)), f"t = {t:.2f} s: s phải = {_lg.s_tai(t, L, V_REF, A_REF):.4f}, bạn ra {f(t, L, V_REF, A_REF)}"
    return f"đường {L:.2f} m chạy hết trong {T:.1f} s như log của controller"


def bai_3(ns):
    f = ham(ns, "diem_tai")
    pts = [(0, 0), (1, 0), (1, 2)]
    sc = [0, 1, 3]
    for s, dap in [(0.5, (0.5, 0)), (1.0, (1, 0)), (2.0, (1, 1)), (3.0, (1, 2))]:
        assert gan(f(pts, sc, s), dap), f"đường (0,0)→(1,0)→(1,2): ở s = {s} phải là {dap}, bạn ra {f(pts, sc, s)}"
    rng = random.Random(5)
    muot = goc.lam_muot(DUONG_O, 3)
    sc = [0.0]
    for a, b in zip(muot, muot[1:]):
        sc.append(sc[-1] + math.dist(a, b))
    for _ in range(50):
        s = rng.uniform(0, sc[-1])
        assert gan(f(muot, sc, s), _lg.diem_tai(muot, sc, s)), f"trên đường làm mượt, điểm ở s = {s:.3f} chưa đúng"
    return "lấy đúng điểm cần tới theo quãng đường: ghép với Bài 2 là có robot ảo để controller bám theo"


BAI = [("Bài 1 · làm mượt đường", bai_1), ("Bài 2 · gắn thời gian (hình thang)", bai_2), ("Bài 3 · điểm theo quãng đường", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "duong_cua_ban", _lg)
