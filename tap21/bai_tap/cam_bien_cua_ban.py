"""Bài tập tập 2.1: giác quan của robot (Chương 5 của sách).

Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/cam_bien.py và loi_giai.py (tự làm trước đã).
"""
import math


def khoang_cach(t, c):
    """Bài 1 (thời gian bay): cảm biến phát sóng, sóng dội lại sau t giây. Sóng đi với tốc độ c (m/s).

    Sóng đi tới vật RỒI quay về, nên quãng đường sóng đi là 2d. Trả về khoảng cách d (mét)."""
    raise NotImplementedError("TODO Bài 1: trả về d")


def danh_gia(cac_lan_do, gia_tri_that):
    """Bài 2: đánh giá một cảm biến từ nhiều lần đo cùng một vật.

    - Sai số hệ thống e = (trung bình các lần đo) − giá trị thật   (đo độ CHÍNH XÁC, accuracy)
    - Độ dao động = độ lệch chuẩn mẫu của các lần đo             (đo độ ỔN ĐỊNH, precision)
      độ lệch chuẩn mẫu = √( Σ(xᵢ − trung bình)² / (n − 1) )
    Trả về tuple (e, do_dao_dong), đơn vị mét."""
    raise NotImplementedError("TODO Bài 2: trả về (e, độ dao động)")


def uoc_luong_lech(mau_dung_yen):
    """Bài 3a (hiệu chỉnh gyro): robot đứng yên nên tốc độ quay thật = 0, mọi số gyro đọc được đều là lệch + nhiễu.

    Lấy TRUNG BÌNH các mẫu để nhiễu triệt tiêu, còn lại phần lệch. Trả về độ lệch (°/s)."""
    raise NotImplementedError("TODO Bài 3a: trung bình các mẫu")


def goc_tich_phan(cac_mau, dt, lech=0.0):
    """Bài 3b: cộng dồn tốc độ quay đo được (đã trừ lệch) để ra góc: góc += (mẫu − lech)·dt. Trả về góc cuối (độ)."""
    raise NotImplementedError("TODO Bài 3b: tích phân gyro")
