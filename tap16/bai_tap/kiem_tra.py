"""Tự chấm bài tập tập 1.6. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import rrt as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def _do_dai(duong):
    return sum(math.dist(a, b) for a, b in zip(duong, duong[1:]))


def bai_1(ns):
    f = ham(ns, "gan_nhat")
    V = [(0, 0), (3, 4), (1, 1), (5, 5)]
    assert f(V, (1.2, 0.9)) == 2, f"điểm (1.2, 0.9) gần (1, 1) nhất (chỉ số 2), bạn ra {f(V, (1.2, 0.9))}"
    assert f(V, (4, 4.5)) == 1, f"điểm (4, 4.5) gần (3, 4) nhất (chỉ số 1), bạn ra {f(V, (4, 4.5))}"
    rng = random.Random(3)
    V = [(rng.uniform(0, 10), rng.uniform(0, 8)) for _ in range(200)]
    for _ in range(50):
        q = (rng.uniform(0, 10), rng.uniform(0, 8))
        dap = min(range(len(V)), key=lambda i: math.dist(V[i], q))
        assert f(V, q) == dap, f"với 200 đỉnh ngẫu nhiên, đỉnh gần {q} nhất là số {dap}, bạn ra {f(V, q)}"
    return "tìm đúng đỉnh gần nhất (cách đơn giản: duyệt hết, mỗi lần O(n))"


def bai_2(ns):
    f = ham(ns, "tien_ve")
    assert gan(f((0, 0), (3, 4), 0.5), (0.3, 0.4)), f"từ (0,0) về phía (3,4) bước 0.5 phải tới (0.3, 0.4), bạn ra {f((0, 0), (3, 4), 0.5)}"
    assert gan(f((1, 1), (1.2, 1.0), 0.5), (1.2, 1.0)), "q_rand chỉ cách 0.2 < bước 0.5 thì phải tới luôn q_rand"
    return "tiến đúng một bước 0.5 m về phía điểm ngẫu nhiên, không vượt quá điểm đó"


def bai_3(ns):
    f = ham(ns, "rrt")
    kq = f(seed=2)
    duong = kq["duong"]
    assert duong and duong[0] == goc.Q_S and duong[-1] == goc.Q_G, "đường phải đi từ Q_S tới Q_G"
    for a, b in zip(duong[:-2], duong[1:-1]):
        assert goc.khong_va_cham(a, b) and math.dist(a, b) <= goc.BUOC + 1e-9, f"đoạn {a} → {b} xuyên tường hoặc dài quá 1 bước"
    giong = (kq["vong_tim_thay"], len(kq["V"]), round(_do_dai(duong), 2)) == (goc.RRT["vong_tim_thay"], len(goc.RRT["V"]), round(goc.RRT["dai"], 2))
    tim_thay = sum(1 for s in range(10) if f(seed=100 + s, toi_da=1000)["vong_tim_thay"])
    assert tim_thay >= 9, f"chạy 10 seed khác, mỗi lần 1000 vòng, chỉ tìm ra đường {tim_thay}/10 lần (video: 100% sau 1000 vòng)"
    cau = (f"giống hệt video: {kq['vong_tim_thay']} vòng, cây {len(kq['V'])} đỉnh, đường {_do_dai(duong):.2f} m" if giong else
           f"tìm ra đường hợp lệ sau {kq['vong_tim_thay']} vòng, dài {_do_dai(duong):.2f} m "
           f"(video: {goc.RRT['vong_tim_thay']} vòng, {goc.RRT['dai']:.2f} m; khác vì thứ tự gọi rng khác, vẫn đúng)")
    return cau + f"; 10 seed khác tìm ra {tim_thay}/10"


BAI = [("Bài 1 · đỉnh gần nhất", bai_1), ("Bài 2 · tiến một bước", bai_2), ("Bài 3 · vòng lặp RRT", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "rrt_cua_ban", loi_giai)
