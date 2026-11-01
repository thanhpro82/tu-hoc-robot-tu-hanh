"""Tự chấm bài tập tập 2.1. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import random
import statistics
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import cam_bien as goc  # noqa: E402  (mô phỏng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402


def mau_gyro(lech, nhieu, giay, seed=3):
    """Số gyro đọc được khi robot đứng yên (cùng cách sinh với goc.troi)."""
    rng = random.Random(seed)
    return [lech + rng.gauss(0, nhieu) for _ in range(round(giay / goc.DT))]


def bai_1(ns):
    f = ham(ns, "khoang_cach")
    t_am, t_sang = goc.thoi_gian_bay(1, goc.C_AM), goc.thoi_gian_bay(1, goc.C_SANG)
    assert gan(f(t_am, goc.C_AM), 1.0), f"siêu âm về sau {t_am * 1000:.2f} ms phải là vật cách 1 m, bạn ra {f(t_am, goc.C_AM)}"
    assert gan(f(t_sang, goc.C_SANG), 1.0), f"LiDAR về sau {t_sang * 1e9:.2f} ns phải là 1 m, bạn ra {f(t_sang, goc.C_SANG)}"
    assert gan(f(0.01, goc.C_AM), 1.715), "tiếng vang về sau 10 ms: d = 343·0.01/2 = 1.715 m"
    return f"siêu âm về sau {t_am * 1000:.2f} ms, LiDAR sau {t_sang * 1e9:.2f} ns, đều là vật cách 1 m như video"


def bai_2(ns):
    f = ham(ns, "danh_gia")
    dong = []
    for ten, ds in goc.DO.items():
        e, sd = f(ds, goc.THAT)
        assert gan(e, statistics.mean(ds) - goc.THAT) and gan(sd, statistics.stdev(ds)), \
            f"{ten}: phải ra e = {(statistics.mean(ds) - goc.THAT) * 100:+.1f} cm, dao động ±{statistics.stdev(ds) * 100:.1f} cm; bạn ra {e * 100:+.1f}, ±{sd * 100:.1f}"
        dong.append(f"{e * 100:+.1f}±{sd * 100:.1f}")
    return "4 cảm biến (cm): " + " · ".join(dong) + " như video"


def bai_3(ns):
    lech_f, tp = ham(ns, "uoc_luong_lech"), ham(ns, "goc_tich_phan")
    assert gan(lech_f([0.2, 0.4, 0.3]), 0.3), "trung bình của [0.2, 0.4, 0.3] phải = 0.3"
    assert gan(tp([1.0] * 100, 0.01), 1.0) and gan(tp([1.0] * 100, 0.01, lech=1.0), 0.0), "gyro báo 1 °/s trong 1 s → quay 1°; trừ lệch 1 thì 0°"
    mau = mau_gyro(*goc.GYRO_RE, goc.GIAY)
    assert gan(tp(mau, goc.DT), goc.TROI_RE[-1], 1e-6), f"gyro rẻ không hiệu chỉnh 60 s phải trôi {goc.TROI_RE[-1]:.1f}° như video, bạn ra {tp(mau, goc.DT):.1f}°"
    lech = lech_f(mau_gyro(*goc.GYRO_RE, 10, seed=99))   # 10 giây đứng yên lúc khởi động để đo lệch
    sau = tp(mau, goc.DT, lech)
    assert abs(lech - goc.GYRO_RE[0]) < 0.05 and abs(sau) < 3, f"ước lượng lệch {lech:.3f} °/s (thật 0.3); sau khi trừ lệch vẫn trôi {sau:.1f}°"
    return f"không hiệu chỉnh: trôi {goc.TROI_RE[-1]:.1f}° như video; đo lệch 10 s đứng yên được {lech:.3f} °/s, trừ đi thì 60 s chỉ trôi {sau:+.1f}°"


BAI = [("Bài 1 · thời gian bay", bai_1), ("Bài 2 · chính xác và ổn định", bai_2), ("Bài 3 · hiệu chỉnh gyro", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "cam_bien_cua_ban", loi_giai)
