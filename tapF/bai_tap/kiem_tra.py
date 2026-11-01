"""Tự chấm bài tập tập cuối F. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Bài 1, 2 dùng ảnh camera thật của mô phỏng và mạng YOLO đã học ở tập 2.8 (../../tap28/sim/trong_so.pt).
Một lượt giao đồ đầy đủ mất khoảng 1 phút trên CPU nên bộ chấm không chạy lại; số liệu 100 lượt nằm trong ../sim/ket_qua.txt.
"""
import itertools
import math
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import giao_do as goc  # noqa: E402  (robot giao đồ của video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

TRANG_THAI = ["CHỜ LỆNH", "ĐỊNH VỊ", "ĐI LẤY", "DỪNG", "NHẬN ĐỒ", "ĐI GIAO", "TÌM NGƯỜI", "TIẾP CẬN", "GIAO", "XONG"]
SU_KIEN = ["khong", "co_lenh", "da_dinh_vi", "mat_dau", "vat_la", "toi_noi", "duong_trong", "xong_viec", "thay_nguoi", "du_gan"]


def canh(n=40, seed=3):
    """Các cảnh thật: robot đứng trong phòng ngủ / phòng làm việc, người nhận đứng trước mặt (lệch ±25°, cách 1–3,5 m),
    tư thế ước lượng lệch chút ít như bộ lọc hạt (~5 cm). Trả về (x thật, ước lượng, người, ảnh camera, LiDAR)."""
    rng = np.random.default_rng(seed)
    ds = []
    while len(ds) < n:
        phong = ["ngu", "lamviec"][rng.integers(2)]
        p = np.array(goc.chon_diem(rng, phong))
        th = rng.uniform(-np.pi, np.pi)
        lui = rng.uniform(1.0, 3.5)
        a = th + rng.uniform(-0.45, 0.45)
        x = np.array([p[0] - lui * math.cos(a), p[1] - lui * math.sin(a), th])
        if goc.chiem(*x[:2], m=goc.LUOI_AN_TOAN) or not goc.nhin_thay(x, p):
            continue
        uoc = x + np.array([*rng.normal(0, 0.04, 2), rng.normal(0, 0.02)])
        ds.append((x, uoc, p, goc.ve_anh(x, [p], rng), goc.quet_that(x, [p], rng)))
    return ds


def bai_1(ns):
    f = ham(ns, "vi_tri_tu_khung")
    Z, h = f((0.9, 0.5, 0.5, 0.2, 0.5))
    assert gan(Z, 1.7 * 60 / 64) and gan(h, 0.0), "người cao nửa ảnh (64 px) ở giữa ảnh: Z = 1,7·60/64 ≈ 1,59 m, hướng 0"
    assert f((0.9, 0.8, 0.5, 0.2, 0.5))[1] > 0, "người lệch sang phải ảnh thì huong > 0"
    Y = goc.yolo()
    sai, n = [], 0
    for x, uoc, p, anh, z in canh():
        kq = goc.tim_nguoi(anh)
        if kq is None:
            continue
        Zb, hb = f(kq[2])
        assert gan(np.array([Zb, hb]), np.array(kq[:2]), 1e-6), "chưa khớp cách tính trong code video (tim_nguoi)"
        sai.append(abs(Zb - math.hypot(p[0] - x[0], p[1] - x[1])))
        n += 1
    return f"YOLO (tập 2.8) thấy người trong {n}/40 cảnh; chỉ dùng camera: đoán khoảng cách sai TB {np.mean(sai) * 100:.0f} cm"


def bai_2(ns):
    f, vt = ham(ns, "ghep"), ham(ns, "vi_tri_tu_khung")
    s_cam, s_ghep, dung_lidar = [], [], 0
    for x, uoc, p, anh, z in canh():
        kq = goc.tim_nguoi(anh)
        if kq is None:
            continue
        Zc, hc = vt(kq[2])
        (mx, my), d = f(uoc, z, Zc, hc)
        (gx, gy), gd = goc.ghep(uoc, z, Zc, hc)
        assert gan(np.array([mx, my, d]), np.array([gx, gy, gd]), 1e-6), "vị trí người sau khi ghép chưa khớp code video"
        dung_lidar += not gan(d, Zc)
        a = uoc[2] - hc
        s_cam.append(math.hypot(uoc[0] + Zc * math.cos(a) - p[0], uoc[1] + Zc * math.sin(a) - p[1]))
        s_ghep.append(math.hypot(mx - p[0], my - p[1]))
    # không có tia LiDAR nào chạm người -> phải dùng khoảng cách của camera
    x, uoc, p, anh, z = canh(1)[0]
    (mx, my), d = f(uoc, np.full(goc.SO_TIA, goc.TAM), 2.0, 0.0)
    assert gan(d, 2.0) and gan(np.array([mx, my]), uoc[:2] + 2.0 * np.array([math.cos(uoc[2]), math.sin(uoc[2])])), \
        "không tia LiDAR nào chạm vật lạ: phải dùng d = Z_cam, a = θ − huong"
    return (f"{len(s_ghep)} cảnh, {dung_lidar} cảnh LiDAR đo được người; vị trí người nhận sai TB: chỉ camera "
            f"{np.mean(s_cam) * 100:.0f} cm → ghép LiDAR {np.mean(s_ghep) * 100:.0f} cm")


def bai_3(ns):
    f = ham(ns, "chuyen")
    import loi_giai
    for s, e, td, dl in itertools.product(TRANG_THAI, SU_KIEN, ["ĐI LẤY", "ĐI GIAO"], [False, True]):
        a, b = f(s, e, td, dl), loi_giai.chuyen(s, e, td, dl)
        assert a == b, f"chuyen({s!r}, {e!r}, truoc_dung={td!r}, da_lay={dl}) phải là {b!r}, bạn trả về {a!r}"
    # lượt minh hoạ trong video (seed 11): thức dậy, định vị, đi lấy, dừng nhường người trong bếp, ... giao tận tay
    kich_ban = ["khong", "co_lenh", "da_dinh_vi", "vat_la", "duong_trong", "toi_noi", "xong_viec", "toi_noi", "thay_nguoi", "du_gan", "xong_viec"]
    s, truoc, da_lay, vet = "CHỜ LỆNH", None, False, ["CHỜ LỆNH"]
    for e in kich_ban:
        moi = f(s, e, truoc, da_lay)
        if moi == "DỪNG":
            truoc = s
        da_lay |= moi == "NHẬN ĐỒ"
        if moi != s:
            vet.append(moi)
        s = moi
    assert s == "XONG", f"kịch bản giao đồ phải kết thúc ở XONG, bạn dừng ở {s}"
    return f"đúng cả {len(TRANG_THAI) * len(SU_KIEN) * 4} trường hợp; lượt minh hoạ: " + " → ".join(vet)


BAI = [("Bài 1 · khoảng cách từ khung YOLO", bai_1), ("Bài 2 · ghép camera + LiDAR", bai_2), ("Bài 3 · máy trạng thái", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "giaodo_cua_ban", loi_giai)
