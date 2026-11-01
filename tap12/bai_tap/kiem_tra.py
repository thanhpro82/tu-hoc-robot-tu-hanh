"""Tự chấm bài tập tập 1.2. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import math
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import vong_ho as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def bai_1(ns):
    f = ham(ns, "ke_hoach_vuong")
    kh = f(1.0, 0.5, 1.0)
    assert len(kh) == 8, f"hình vuông cần 8 lệnh (4 cạnh × thẳng + quay), bạn có {len(kh)}"
    assert gan(kh, goc.KE_HOACH), f"cạnh 1 m, v = 0.5, quay trong 1 s: phải giống kế hoạch trong video {goc.KE_HOACH[:2]}..., bạn ra {kh[:2]}..."
    _, lech = goc.chay(f(2.0, 0.4, 2.0))
    assert lech[0] < 0.005, f"hình vuông cạnh 2 m chạy lý tưởng phải về đúng chỗ cũ, bạn lệch {lech[0] * 100:.1f} cm"
    _, lech = goc.chay(kh, so_vong=3, sai_so=goc.ROBOT_THAT, seed=3)
    return "lý tưởng về đúng chỗ cũ; robot có sai số thì lệch " + ", ".join(f"{d * 100:.0f}" for d in lech) + " cm sau 3 vòng như video"


def bai_2(ns):
    f = ham(ns, "thoi_gian_nhanh_nhat")
    T = f(1.0, 0.5, 0.5)
    assert gan(T, goc.T_toi_uu), f"1 m, v_max = 0.5, a_max = 0.5: phải mất {goc.T_toi_uu:.1f} s như video, bạn ra {T}"
    assert gan(f(4.0, 1.0, 0.5), 6.0), f"4 m, v_max = 1, a_max = 0.5: tăng tốc 2 s (1 m) + đều 2 s (2 m) + phanh 2 s (1 m) = 6 s, bạn ra {f(4.0, 1.0, 0.5)}"
    T3 = f(0.2, 0.5, 0.5)
    assert gan(T3, 2 * math.sqrt(0.4)), f"0.2 m quá ngắn để tới v_max (hình tam giác): T phải = 2·√(0.2/0.5) = {2 * math.sqrt(0.4):.3f} s, bạn ra {T3}"
    return f"1 m mất {T:.1f} s như video; quãng ngắn 0.2 m thành hình tam giác, {T3:.2f} s"


def bai_3(ns):
    f = ham(ns, "van_toc_luc")
    for d, vm, am in [(1.0, 0.5, 0.5), (0.2, 0.5, 0.5), (4.0, 1.0, 0.5)]:
        T = ham(ns, "thoi_gian_nhanh_nhat")(d, vm, am)
        dt = 0.001
        v = [f(i * dt, d, vm, am) for i in range(round(T / dt) + 1)]
        quang = sum(v) * dt
        gia_toc = max(abs(b - a) / dt for a, b in zip(v, v[1:]))
        assert abs(quang - d) < 0.01, f"d = {d} m: cộng v·dt được {quang:.3f} m, phải = {d} m"
        assert max(v) <= vm + 1e-9 and gia_toc <= am * 1.01, f"d = {d} m: vượt giới hạn (v lớn nhất {max(v):.3f}, gia tốc lớn nhất {gia_toc:.3f})"
        assert v[0] < 1e-9 and v[-1] < 1e-3, f"d = {d} m: phải xuất phát và dừng hẳn (v = 0) ở hai đầu"
    v = [f(i * goc.dt, 1.0, 0.5, 0.5) for i in range(len(goc.van_toc_toi_uu))]
    assert gan(v, goc.van_toc_toi_uu), "đồ thị v cho 1 m chưa khớp hình thang trong video"
    return "đồ thị hình thang khớp video; cả 3 quãng đều đi đúng quãng, không vượt v_max, a_max"


BAI = [("Bài 1 · kế hoạch hình vuông", bai_1), ("Bài 2 · thời gian nhanh nhất", bai_2), ("Bài 3 · đồ thị hình thang", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "vong_ho_cua_ban", loi_giai)
