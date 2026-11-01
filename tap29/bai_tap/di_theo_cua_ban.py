"""Bài tập tập 2.9: tổng kết Mùa 2, robot đi theo bạn. Ghép camera (2.2) + YOLO (2.8) + PI (1.3).

Một khung YOLO là tuple (lop, diem, cx, cy, w, h), toạ độ theo tỉ lệ ảnh 128×128; lop 0 = người, 2 = bóng.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/di_theo.py và loi_giai.py (tự làm trước đã).
"""
import math

N, F = 128, 60.0            # ảnh 128 px, tiêu cự 60 px
H_NGUOI, D_BONG = 1.7, 0.25  # người cao 1,7 m, bóng đường kính 0,25 m
R_KC = 2.0                   # khoảng cách muốn giữ (m)
DT = 0.1
KP, KI, KTH = 0.8, 0.15, 1.6
V_MAX, W_MAX = 1.2, 1.5


def uoc_luong(d):
    """Bài 1: từ một khung, ước lượng khoảng cách Z (m) và hướng (rad, dương = vật lệch sang phải ảnh).

    - Hướng = atan((cx − 0.5)·N / F)          (cx = 0.5 là giữa ảnh)
    - Người (lop 0): biết chiều cao thật nên Z = H_NGUOI·F / (h·N)     (Eq. 6.1 đảo ngược, h·N là chiều cao khung theo pixel)
    - Bóng (lop khác 0): dùng bề rộng: Z = D_BONG·F / (w·N)
    Trả về (Z, huong)."""
    raise NotImplementedError("TODO Bài 1: (Z, hướng)")


def lenh(z_hat, huong, tich_phan):
    """Bài 2: bộ điều khiển đi theo người (PI cho tốc độ tới, P cho tốc độ quay).

    e = z_hat − R_KC (dương là đang xa hơn mong muốn)
    tich_phan_moi = kẹp(tich_phan + e·DT, −1.5, 1.5)
    v = kẹp(KP·e + KI·tich_phan_moi, 0, V_MAX)        (không bao giờ lùi)
    w = kẹp(−KTH·huong, −W_MAX, W_MAX)                 (người lệch phải → quay phải, ω âm)
    Trả về (v, w, tich_phan_moi)."""
    raise NotImplementedError("TODO Bài 2: (v, w, tích phân mới)")


def quyet_dinh(dets):
    """Bài 3: chọn trạng thái từ danh sách khung YOLO của một khung hình.

    1. Có bóng (lop 2): lấy quả điểm cao nhất, uoc_luong; nếu Z < 1.6 m VÀ |hướng| < 30° thì "dừng".
    2. Không phải "dừng" mà có người (lop 0) thì "theo".
    3. Còn lại "tìm".
    Trả về một trong 3 chuỗi "dừng", "theo", "tìm"."""
    raise NotImplementedError("TODO Bài 3: trạng thái")
