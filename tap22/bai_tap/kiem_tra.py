"""Tự chấm bài tập tập 2.2. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import random
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import pinhole as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def phim(chieu, K, so_khung=90):
    """Như goc.phim_lap_phuong nhưng dùng hàm chieu của bạn."""
    khung = []
    for k in range(so_khung):
        p = k / (so_khung - 1)
        R = goc.quay_y(0.6 + 1.6 * p)
        khung.append([chieu(v, K, R, (0.0, 0.0, 3.0 - 1.8 * p)) for v in goc.lap_phuong()])
    return khung


def _rong(k):
    return max(p[0] for p in k) - min(p[0] for p in k)


def bai_1(ns):
    K = ham(ns, "ma_tran_K")(goc.ALPHA, goc.BETA, goc.GAMMA, goc.U0, goc.V0)
    assert gan(K, goc.K), f"camera trong video phải ra K = {goc.K}, bạn ra {K}"
    K2 = ham(ns, "ma_tran_K")(800, 790, 1.5, 640, 360)
    assert gan(K2, [[800, 1.5, 640], [0, 790, 360], [0, 0, 1]]), f"α = 800, β = 790, γ = 1.5, tâm (640, 360): bạn ra {K2}"
    return f"K = {K} (5 tham số nội)"


def bai_2(ns):
    f = ham(ns, "chieu")
    uv = f((0.2, 0.1, 2.0), goc.K, I3, (0, 0, 0))
    assert gan(uv, (370, 265)), f"điểm (0.2, 0.1, 2.0) m phải ra pixel (370, 265) như video, bạn ra {uv}"
    rng = random.Random(4)
    for _ in range(20):
        P = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.3, 0.3))
        R, t = goc.quay_y(rng.uniform(-2, 2)), (rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), rng.uniform(2, 4))
        assert gan(f(P, goc.K, R, t), goc.chieu(P, R, t)), f"điểm {tuple(round(v, 2) for v in P)} có quay + dời: bạn ra {f(P, goc.K, R, t)}, đáp án {goc.chieu(P, R, t)}"
    k = phim(f, goc.K)
    return f"(0.2, 0.1, 2.0) → pixel (370, 265); khối lập phương rộng {_rong(k[0]):.0f} px khi ở xa, {_rong(k[-1]):.0f} px khi lại gần như video"


def bai_3(ns):
    f = ham(ns, "khoang_cach_tu_anh")
    for H, Z in goc.NHAP_NHANG:
        h = goc.chieu_cao_anh(H, Z)
        assert gan(f(H, h, goc.BETA), Z), f"hộp {H * 100:.0f} cm cao {h:.0f} px phải cách {Z} m, bạn ra {f(H, h, goc.BETA)}"
    return "biết kích thước thật thì đo được khoảng cách; không biết thì 150 px có thể là hộp 30 cm cách 1 m, 60 cm cách 2 m hay 120 cm cách 4 m"


BAI = [("Bài 1 · ma trận K", bai_1), ("Bài 2 · chiếu điểm 3D", bai_2), ("Bài 3 · đo khoảng cách từ ảnh", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "camera_cua_ban", loi_giai)
