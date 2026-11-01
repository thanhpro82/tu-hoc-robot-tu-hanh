"""Bài tập tập 2.5: dựng 3D từ ảnh chụp (Structure from Motion, Mục 7.3 của sách). Dùng numpy.

Điểm ảnh là mảng (N, 2) pixel. Ma trận chiếu P = K·[R | t] có hình 3×4.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/sfm.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def chuan_hoa(p):
    """Có sẵn: ma trận 3×3 dời tâm đám điểm về gốc, co giãn cho khoảng cách trung bình = √2."""
    m = p.mean(0)
    s = np.sqrt(2) / np.linalg.norm(p - m, axis=1).mean()
    return np.array([[s, 0, -s * m[0]], [0, s, -s * m[1]], [0, 0, 1]])


def tim_F(p1, p2):
    """Bài 1 (Eq. 7.5–7.6, thuật toán 8 điểm): ma trận cơ bản F thoả  p1ᵀ·F·p2 = 0  cho mọi cặp điểm tương ứng.

    1. Chuẩn hoá: T1 = chuan_hoa(p1), T2 = chuan_hoa(p2); a = T1·[u, v, 1]ᵀ (ảnh 1), b = T2·[u, v, 1]ᵀ (ảnh 2).
    2. Mỗi cặp cho 1 dòng của ma trận W: np.outer(a, b).ravel()  (9 số).
    3. F_n = véc-tơ kỳ dị nhỏ nhất của W (np.linalg.svd(W)[2][-1]), reshape(3, 3).
    4. Ép hạng 2: U, S, Vt = svd(F_n); F_n = U @ diag(S[0], S[1], 0) @ Vt.
    5. Bỏ chuẩn hoá: F = T1ᵀ @ F_n @ T2."""
    raise NotImplementedError("TODO Bài 1: thuật toán 8 điểm")


def tam_giac(P1, P2, x1, x2):
    """Bài 2 (Eq. 7.8): tam giác hoá. Mỗi cặp pixel (a ở ảnh 1, b ở ảnh 2) cho 4 phương trình theo X = (X, Y, Z, 1):

        a_u·P1[2] − P1[0],   a_v·P1[2] − P1[1],   b_u·P2[2] − P2[0],   b_v·P2[2] − P2[1]      (mỗi dòng 4 số)
    Xếp thành A (4×4), X = véc-tơ kỳ dị nhỏ nhất của A, rồi chia cho X[3]. Trả về mảng (N, 3) các điểm 3D."""
    raise NotImplementedError("TODO Bài 2: tam giác hoá")


def dem_truoc_camera(R, t, X):
    """Bài 3: E tách ra được 4 nghiệm (R, t); chỉ nghiệm đúng cho điểm nằm TRƯỚC cả hai camera.

    Camera 1 ở gốc: độ sâu z1 = X[:, 2]. Camera 2: độ sâu z2 = (X·Rᵀ + t)[:, 2].
    Trả về số điểm có z1 > 0 VÀ z2 > 0 (kiểu int)."""
    raise NotImplementedError("TODO Bài 3: đếm điểm trước cả hai camera")
