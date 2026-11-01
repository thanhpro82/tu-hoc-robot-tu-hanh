"""Bài tập tập 3.8: kết hợp cảm biến và theo dõi nhiều người (Chương 15 của sách). Dùng numpy.

Một phát hiện là cặp (z, R): z = vị trí (x, y) đo được, R = ma trận hiệp phương sai 2×2 của nó.
Một track là trạng thái vận tốc không đổi x = [x, y, ẋ, ẏ] với hiệp phương sai P (4×4); chỉ đo được vị trí: H = [[1,0,0,0],[0,1,0,0]].
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/theo_doi.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

H = np.array([[1.0, 0, 0, 0], [0, 1, 0, 0]])


def ghep(ds):
    """Bài 1 (Mục 15.2.1, dạng thông tin): ghép nhiều phát hiện của cùng một người từ các cảm biến khác nhau.

        Y = Σ R_i⁻¹,   y = Σ R_i⁻¹·z_i,   Σ_ghép = Y⁻¹,   z_ghép = Σ_ghép·y
    ds là list các cặp (z, R). Trả về (z_ghep, S_ghep)."""
    raise NotImplementedError("TODO Bài 1: ghép theo dạng thông tin")


def m2(x, P, z, R):
    """Bài 2 (Mục 15.5.2): bình phương khoảng cách Mahalanobis giữa phát hiện (z, R) và track (x, P).

        S = H·P·Hᵀ + R,   z̃ = z − H·x,   m² = z̃ᵀ·S⁻¹·z̃
    Phát hiện chỉ được ghép với track nếu m² ≤ 9,21 (cổng χ² 2 bậc tự do, 99%). Trả về m² (số)."""
    raise NotImplementedError("TODO Bài 2: Mahalanobis")


def cap_nhat(x, P, z, R):
    """Bài 3: cập nhật Kalman một track bằng phát hiện đã ghép.

        S = H·P·Hᵀ + R,  K = P·Hᵀ·S⁻¹,  x_mới = x + K·(z − H·x),  P_mới = (I − K·H)·P
    Trả về (x_moi, P_moi)."""
    raise NotImplementedError("TODO Bài 3: cập nhật track")
