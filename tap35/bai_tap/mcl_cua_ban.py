"""Bài tập tập 3.5: định vị trên bản đồ có sẵn, Monte Carlo Localization (Chương 13 của sách). Dùng numpy.

Bản đồ căn hộ 12 × 8 m là lưới ô 10 cm; chiem(x, y) cho biết điểm (mảng x, y) có nằm trong tường/đồ đạc không.
Tư thế là (x, y, θ); P là mảng (n, 3) các hạt. LiDAR có 8 tia đều quanh robot, tầm xa 6 m.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/mcl.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

from mcl import BUOC_TIA, GOC_TIA, K, P_DEU, SIG_TIA, TAM, chiem  # noqa: F401  (bản đồ và thông số có sẵn, trong ../sim)


def quet(X):
    """Bài 1: dò tia LiDAR cho mảng tư thế X (n, 3). Trả về mảng khoảng cách (n, 8).

    Tia thứ j của tư thế (x, y, θ) có hướng θ + GOC_TIA[j]. Đi dọc tia theo các bước d trong BUOC_TIA (5 cm, 10 cm, ..., 6 m):
    khoảng cách của tia là d ĐẦU TIÊN mà chiem(x + d·cos, y + d·sin) là True. Không chạm gì thì bằng TAM (6 m).
    Gợi ý: làm cho cả mảng cùng lúc; giữ một mảng "da" (đã chạm) để không ghi đè."""
    raise NotImplementedError("TODO Bài 1: dò tia")


def trong_so(P, z):
    """Bài 2 (Eq. 13.3): trọng số các hạt từ 8 tia đo được z.

    du = quet(P) (8 tia dự đoán cho mỗi hạt). Mỗi tia: p = (1 − P_DEU)·exp(−½((du − z)/SIG_TIA)²) + P_DEU·0.2
    Trọng số của hạt = tích của 8 p. Làm bằng log cho khỏi tràn số: logw = Σ log p; hạt nằm trong tường thì logw = −∞ (Eq. 13.2).
    w = exp(logw − max(logw)), rồi chuẩn hoá tổng = 1."""
    raise NotImplementedError("TODO Bài 2: trọng số")


def tha_hat(P, chon, hat_moi):
    """Bài 3 (ghi chú lề §13.6, chống bắt cóc): thay các hạt ở vị trí chon (mảng chỉ số) bằng hat_moi (rải ngẫu nhiên trên bản đồ).

    Trả về mảng hạt mới (đừng sửa thẳng vào P truyền vào: hãy copy trước)."""
    raise NotImplementedError("TODO Bài 3: thả hạt ngẫu nhiên")
