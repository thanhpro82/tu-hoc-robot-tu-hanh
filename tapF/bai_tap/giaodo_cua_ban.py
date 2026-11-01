"""Bài tập tập cuối F: robot giao đồ trong nhà, ghép cả 4 mùa. Bạn viết 3 mối nối giữa các khối.

Căn hộ 12 × 8 m của tập 3.5. Robot thức dậy không biết mình ở đâu, lấy đồ ở bếp, mang tới tận tay người nhận ở phòng ngủ hoặc phòng làm việc.
Các khối A*, bộ lọc hạt, YOLO đã có sẵn trong ../sim/giao_do.py (code của các tập trước). Bạn viết phần nối:
  Bài 1 (Mùa 2): khung YOLO → người ở cách bao xa, hướng nào.   Bài 2 (Mùa 2 + 3): ghép camera với LiDAR.   Bài 3 (Mùa 4): máy trạng thái.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/giao_do.py và loi_giai.py (tự làm trước đã).
"""
import math

import numpy as np

from giao_do import F_CAM, GOC_TIA, H_NGUOI, N_ANH, R_NGUOI, SO_TIA, goc, vat_la  # noqa: F401  (trong ../sim)


def vi_tri_tu_khung(khung):
    """Bài 1 (camera lỗ kim, tập 2.2): khung = (s, cx, cy, w, h) của YOLO, toạ độ đã chia cho cỡ ảnh N_ANH = 128 px.

    Chiều cao người trong ảnh là h·N_ANH pixel; người thật cao H_NGUOI = 1,7 m; tiêu cự F_CAM = 60 px.
      Z     = H_NGUOI · F_CAM / (h · N_ANH)               (người càng nhỏ trong ảnh càng xa)
      huong = atan((cx − 0.5) · N_ANH / F_CAM)             (> 0: người lệch sang PHẢI ảnh)
    Trả về (Z, huong)."""
    raise NotImplementedError("TODO Bài 1: khoảng cách và hướng từ khung YOLO")


def ghep(uoc, z, Z_cam, huong):
    """Bài 2 (kết hợp cảm biến, tập 3.8): camera biết ĐÓ LÀ NGƯỜI và ở hướng nào, LiDAR đo khoảng cách chuẩn hơn.

    uoc = tư thế ước lượng (x, y, θ); z = 36 tia LiDAR (góc GOC_TIA, từ −π, cách nhau 10°); Z_cam, huong từ Bài 1.
    1. j = tia gần hướng người nhất: argmin |goc(GOC_TIA + huong)|      (người bên phải ảnh = góc âm so với mũi robot)
    2. la = vat_la(uoc, z): tia nào chạm thứ KHÔNG có trên bản đồ.
       Xét 3 tia j−1, j, j+1 (lấy chỉ số mod SO_TIA), giữ các tia có la = True.
    3. Nếu có: chọn tia ngắn nhất i, d = z[i] + R_NGUOI (LiDAR chạm mặt người, tâm ở sau thêm 0,2 m), a = θ + GOC_TIA[i]
       Nếu không: d = Z_cam, a = θ − huong.
    Trả về ((uoc_x + d·cos a, uoc_y + d·sin a), d)."""
    raise NotImplementedError("TODO Bài 2: ghép camera + LiDAR")


def chuyen(s, su_kien, truoc_dung=None, da_lay=False):
    """Bài 3 (máy trạng thái, tập 4.1): hàm chuyển n(s, i) của bộ não robot. Trả về trạng thái tiếp theo.

    su_kien là một trong: "khong", "co_lenh", "da_dinh_vi", "mat_dau", "vat_la", "toi_noi", "duong_trong", "xong_viec",
    "thay_nguoi", "du_gan". Sự kiện không có trong bảng thì GIỮ NGUYÊN trạng thái.
      CHỜ LỆNH   + co_lenh     → ĐỊNH VỊ
      ĐỊNH VỊ    + da_dinh_vi  → ĐI GIAO nếu da_lay, ngược lại ĐI LẤY
      ĐI LẤY, ĐI GIAO, DỪNG + mat_dau → ĐỊNH VỊ               (mất dấu: định vị lại)
      ĐI LẤY, ĐI GIAO + vat_la  → DỪNG
      ĐI LẤY     + toi_noi     → NHẬN ĐỒ
      ĐI GIAO    + toi_noi     → TÌM NGƯỜI
      DỪNG       + duong_trong → truoc_dung                    (quay lại đúng việc đang làm dở)
      NHẬN ĐỒ    + xong_viec   → ĐI GIAO
      TÌM NGƯỜI  + thay_nguoi  → TIẾP CẬN
      TIẾP CẬN   + du_gan      → GIAO
      GIAO       + xong_viec   → XONG"""
    raise NotImplementedError("TODO Bài 3: máy trạng thái")
