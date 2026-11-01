"""Bộ chấm dùng chung cho bài tập của các tập (tapXX/bai_tap/kiem_tra.py gọi vào đây).

Mỗi bài là một hàm nhận `ns` (module bài làm, hoặc globals() của notebook), chạy các assert,
và trả về một câu nhận xét khi đạt.
"""
import math


def ham(ns, ten):
    """Lấy hàm/lớp tên `ten` trong bài làm (module hoặc dict globals() của notebook)."""
    return ns[ten] if isinstance(ns, dict) else getattr(ns, ten)


def gan(a, b, tol=1e-6):
    """So sánh số hoặc mảng, sai lệch tương đối/tuyệt đối tối đa `tol`."""
    try:
        import numpy as np
        a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        return a.shape == b.shape and bool(np.allclose(a, b, rtol=tol, atol=tol))
    except ImportError:
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def cham(ns, bai, cuoi="Thử phần Thử thách trong README nhé."):
    """Chấm danh sách `bai` = [(tên, hàm kiểm tra)], in ✅ / ❌ / ⏳ / 💥, trả về số bài đạt."""
    dat = 0
    for i, (ten, f) in enumerate(bai):
        try:
            print(f"✅ {ten}: {f(ns)}")
            dat += 1
        except NotImplementedError:
            print(f"⏳ {ten}: chưa làm")
        except AssertionError as loi:
            print(f"❌ {ten}: {loi}" + ("\n   (bài này dùng cả code các bài trước, hãy làm các bài trước cho đạt đã)" if dat < i else ""))
        except Exception as loi:  # lỗi cú pháp, sai tên biến, ...
            print(f"💥 {ten}: code bị lỗi {type(loi).__name__}: {loi}")
    print(f"\nĐạt {dat}/{len(bai)} bài." + (f"  🎉 Xong! {cuoi}" if dat == len(bai) else ""))
    return dat


def chay_tu_dong_lenh(bai, ten_file, loi_giai):
    """Dùng ở cuối kiem_tra.py: `python kiem_tra.py` chấm file bài làm, `--loi-giai` chấm lời giải gốc."""
    import importlib
    import sys
    if "--loi-giai" in sys.argv:
        return cham(loi_giai, bai)
    return cham(importlib.import_module(ten_file), bai)
