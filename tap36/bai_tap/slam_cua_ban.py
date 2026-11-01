"""Bài tập tập 3.6: SLAM, con gà hay quả trứng? Graph SLAM với khép vòng (Chương 14 của sách). Dùng numpy.

Tư thế 2D là mảng [x, y, θ]. "a ⊕ b" ghép một chuyển động tương đối b (nhìn từ a) vào tư thế a; "a⁻¹ ⊕ b" là tư thế b nhìn từ a.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/slam.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def goc(a):
    """Có sẵn: bọc góc về [−π, π)."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def cong(a, b):
    """Bài 1a: a ⊕ b. Xoay b theo hướng a[2] rồi cộng vào a:
        [a_x + cos·b_x − sin·b_y,  a_y + sin·b_x + cos·b_y,  goc(a_θ + b_θ)]"""
    raise NotImplementedError("TODO Bài 1a: ghép tư thế")


def tru(a, b):
    """Bài 1b: a⁻¹ ⊕ b, tức tư thế b nhìn trong khung của a. Với dx = b_x − a_x, dy = b_y − a_y:
        [cos·dx + sin·dy,  −sin·dx + cos·dy,  goc(b_θ − a_θ)]       (cos, sin của a_θ)"""
    raise NotImplementedError("TODO Bài 1b: tư thế tương đối")


def can_chinh(P, Q):
    """Bài 2 (bước lõi của ICP): tìm phép quay R (2×2) và dời t sao cho R·p + t ≈ q với các cặp điểm đã ghép (P[i] ↔ Q[i]).

    1. Trừ tâm: mp = trung bình P, mq = trung bình Q.
    2. H = (P − mp)ᵀ·(Q − mq);  U, S, Vt = np.linalg.svd(H);  R = Vtᵀ·Uᵀ.
    3. Nếu det(R) < 0 (bị lật gương): đổi dấu hàng cuối của Vt rồi tính lại R.
    4. t = mq − R·mp.
    Trả về (dth, t) với dth = atan2(R[1,0], R[0,0])."""
    raise NotImplementedError("TODO Bài 2: căn chỉnh hai đám điểm")


def sai_so_canh(xi, xj, z):
    """Bài 3 (Mục 14.7): sai số của một cạnh trong đồ thị. Cạnh nói "từ nút i, nút j nằm ở z".

    r = (xi⁻¹ ⊕ xj) − z, nhớ bọc thành phần góc r[2] bằng goc(). Trả về mảng 3 số."""
    raise NotImplementedError("TODO Bài 3: sai số cạnh")
