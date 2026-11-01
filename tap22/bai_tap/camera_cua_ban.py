"""Bài tập tập 2.2: camera lỗ kim, chiếu điểm 3D thành pixel (Chương 6 của sách).

Ma trận là list các hàng, ví dụ K = [[α, γ, u0], [0, β, v0], [0, 0, 1]]. Điểm 3D là tuple (X, Y, Z) tính bằng mét.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/pinhole.py và loi_giai.py (tự làm trước đã).
"""


def ma_tran_K(alpha, beta, gamma, u0, v0):
    """Bài 1: ma trận tham số nội K (5 tham số: tiêu cự theo pixel α, β; độ xiên γ; tâm ảnh u0, v0).

        K = [[α, γ, u0],
             [0, β, v0],
             [0, 0, 1 ]]"""
    raise NotImplementedError("TODO Bài 1: trả về K (list 3 hàng)")


def chieu(P_W, K, R, t):
    """Bài 2: chiếu điểm thế giới P_W thành pixel (u, v).

    1. Đổi sang toạ độ camera:   P_C = R·P_W + t        (R là ma trận quay 3×3, t là tuple 3 số)
    2. Nhân với K:               p = K·P_C              (p có 3 thành phần)
    3. Chia cho thành phần cuối:  u = p[0]/p[2],  v = p[1]/p[2]
    Trả về tuple (u, v)."""
    raise NotImplementedError("TODO Bài 2: trả về (u, v)")


def khoang_cach_tu_anh(H, h_px, beta):
    """Bài 3: biết vật thật cao H mét, trên ảnh cao h_px pixel, tiêu cự β pixel → vật cách camera bao xa?

    Từ công thức chiếu: h_px = β·H / Z. Trả về Z (mét)."""
    raise NotImplementedError("TODO Bài 3: trả về Z")
