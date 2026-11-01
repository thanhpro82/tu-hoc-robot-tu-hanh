"""Bài tập tập 2.3: hiệu chỉnh camera bằng bàn cờ (phương pháp Zhang, Mục 6.5.2 của sách). Dùng numpy.

Điểm ảnh là mảng numpy hình (N, 2): mỗi hàng là (u, v). Điểm bàn cờ là (X, Y) trên mặt bàn cờ (Z = 0).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/hieu_chinh.py (tự làm trước đã).
"""
import numpy as np


def meo(uv, k, c):
    """Bài 1: méo xuyên tâm (Eq. 6.4). uv: (N, 2), k: hệ số méo, c: tâm méo (u_c, v_c).

    Với mỗi điểm: d = uv − c,  r² = d_u² + d_v²,  điểm bị méo = (1 + k·r²)·d + c.
    k < 0: méo thùng (điểm xa tâm bị kéo vào trong). Trả về mảng (N, 2)."""
    raise NotImplementedError("TODO Bài 1: méo xuyên tâm")


def chuan_hoa(P):
    """Có sẵn: ma trận 3×3 dời tâm đám điểm về gốc và co giãn cho khoảng cách trung bình = √2 (giúp DLT ổn định)."""
    m = P.mean(axis=0)
    s = np.sqrt(2) / np.linalg.norm(P - m, axis=1).mean()
    return np.array([[s, 0, -s * m[0]], [0, s, -s * m[1]], [0, 0, 1]])


def tim_H(XY, uv):
    """Bài 2: homography H (3×3) đưa điểm bàn cờ (X, Y, 1) thành điểm ảnh (u, v, 1) theo kiểu DLT.

    1. Chuẩn hoá:  T1 = chuan_hoa(XY), T2 = chuan_hoa(uv); a = T1·[X, Y, 1]ᵀ, b = T2·[u, v, 1]ᵀ cho từng điểm.
    2. Mỗi cặp (a = (X, Y, 1), b = (u, v, 1)) cho 2 dòng của ma trận A (9 cột):
         [−X, −Y, −1,  0,  0,  0, u·X, u·Y, u]
         [ 0,  0,  0, −X, −Y, −1, v·X, v·Y, v]
    3. h = véc-tơ kỳ dị ứng với giá trị kỳ dị nhỏ nhất: np.linalg.svd(A)[2][-1]; H_n = h.reshape(3, 3).
    4. Bỏ chuẩn hoá: H = inv(T2) @ H_n @ T1, rồi chia cho H[2, 2]."""
    raise NotImplementedError("TODO Bài 2: DLT tìm H")


def v_ij(H, i, j):
    """Bài 3: véc-tơ 6 số dùng để lập phương trình cho B = K⁻ᵀK⁻¹ (Eq. 6.28–6.31).

    Gọi h_i = cột thứ i của H (i = 0 hoặc 1), tức h_i = H[:, i]. Trả về np.array gồm 6 số:
        [h_i0·h_j0,  h_i0·h_j1 + h_i1·h_j0,  h_i1·h_j1,  h_i2·h_j0 + h_i0·h_j2,  h_i2·h_j1 + h_i1·h_j2,  h_i2·h_j2]
    Mỗi ảnh cho 2 phương trình: v_01·b = 0 và (v_00 − v_11)·b = 0 (vì r1 ⟂ r2 và |r1| = |r2|)."""
    raise NotImplementedError("TODO Bài 3: véc-tơ v_ij")
