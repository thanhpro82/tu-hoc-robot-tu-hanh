"""Bài tập tập 2.4: hai mắt đoán khoảng cách (stereo, Chương 7 của sách). Dùng numpy.

Ảnh là mảng numpy (cao × rộng) mức xám; L là ảnh camera trái, R là ảnh camera phải (đã chỉnh song song).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/stereo.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def do_sau(d, b, f):
    """Bài 1 (Eq. 7.7): điểm lệch d pixel giữa hai ảnh, hai camera cách nhau b mét, tiêu cự f pixel → độ sâu z (mét).

        z = b·f / d       (d có thể là số hoặc mảng numpy)"""
    raise NotImplementedError("TODO Bài 1: z = b·f/d")


def chi_phi_diem(L, R, hang, cot, d_max, cua_so):
    """Bài 2: so khớp một pixel (hang, cot) của ảnh trái với các pixel cùng hàng của ảnh phải.

    Với mỗi d = 0, 1, ..., d_max − 1: lấy cửa sổ cua_so × cua_so quanh (hang, cot) trong L và quanh (hang, cot − d) trong R,
    tính TRUNG BÌNH bình phương hiệu (mean squared difference) của hai cửa sổ.
    Gợi ý: r = cua_so // 2; cửa sổ trái = L[hang−r : hang+r+1, cot−r : cot+r+1].
    Trả về mảng numpy độ dài d_max; d có chi phí nhỏ nhất là độ lệch (disparity) tìm được."""
    raise NotImplementedError("TODO Bài 2: chi phí theo d")


def noi_suy_parabol(c0, c1, c2):
    """Bài 3 (mở rộng): chi phí tại d−1, d, d+1 là c0, c1, c2 (c1 nhỏ nhất). Vẽ parabol qua 3 điểm, đỉnh parabol lệch khỏi d một đoạn

        δ = 0.5·(c0 − c2) / (c0 − 2·c1 + c2)
    Kẹp δ trong [−0.5, 0.5]; nếu mẫu số ≤ 0 thì trả về 0. Trả về δ (pixel) để có d + δ chính xác dưới 1 pixel."""
    raise NotImplementedError("TODO Bài 3: độ lệch dưới pixel")
