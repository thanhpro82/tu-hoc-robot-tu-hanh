"""Bài tập tập 2.6: thị giác máy tính cổ điển, dò vạch dẫn đường (Chương 8 của sách). Dùng numpy.

Ảnh là mảng numpy (cao × rộng) mức xám. Pixel (hàng y, cột x); gốc ở góc trên trái.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/thi_giac.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

SOBEL_X = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=float)   # Eq. 8.5
SOBEL_Y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=float)


def tich_chap(anh, mat_na):
    """Bài 1 (Eq. 8.2): tích chập ảnh với mặt nạ 3×3.

        kết quả[y, x] = Σ_{i,j ∈ {−1,0,1}}  mat_na[1+i, 1+j] · anh[y − i, x − j]
    (để ý dấu TRỪ: tích chập lật mặt nạ, khác tương quan). Ở viền ảnh, pixel ngoài ảnh lấy bằng pixel viền gần nhất
    (gợi ý: np.pad(anh, 1, mode="edge")). Trả về mảng cùng kích thước với anh."""
    raise NotImplementedError("TODO Bài 1: tích chập 3×3")


def do_doc(anh):
    """Bài 2: độ dốc ảnh bằng Sobel. Sx = tich_chap(anh, SOBEL_X), Sy = tich_chap(anh, SOBEL_Y), |∇S| = √(Sx² + Sy²).

    Trả về tuple (do_lon, Sx, Sy)."""
    raise NotImplementedError("TODO Bài 2: |∇S|, Sx, Sy")


def hough(canh, n_alpha=180):
    """Bài 3 (Mục 8.2.1): biến đổi Hough cho đường thẳng  x·cos α + y·sin α = r.

    canh: mảng True/False, True là pixel cạnh. α chạy từ −90° tới 89° (bước 1°, n_alpha giá trị); r làm tròn tới số nguyên.
    r_max = ceil(√(rộng² + cao²)); lưới bỏ phiếu acc có hình (n_alpha, 2·r_max + 1), cột của r là r + r_max.
    Mỗi pixel cạnh (x, y), với MỌI α: tính r = round(x·cos α + y·sin α), cộng 1 phiếu vào acc[α, r + r_max].
    Trả về (acc, alphas_radian, r_max)."""
    raise NotImplementedError("TODO Bài 3: lưới bỏ phiếu Hough")
