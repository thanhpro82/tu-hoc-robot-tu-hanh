"""Bài tập tập 1.6: tự viết RRT, cây tìm đường bằng cách gieo điểm ngẫu nhiên.

Không gian 10 × 8,4 m có 4 bức tường. Điểm viết là tuple (x, y).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/rrt.py và loi_giai.py (tự làm trước đã).
"""
import math
import random

from rrt import ALPHA, BUOC, DIEM_DICH, H, Q_G, Q_S, W, khong_va_cham  # noqa: F401  (bản đồ + kiểm tra va chạm có sẵn, trong ../sim)


def gan_nhat(V, q):
    """Bài 1: chỉ số của đỉnh trong danh sách V gần điểm q nhất (khoảng cách Euclid)."""
    raise NotImplementedError("TODO Bài 1: trả về chỉ số i")


def tien_ve(q_near, q_rand, buoc):
    """Bài 2: từ q_near tiến về phía q_rand một đoạn dài `buoc` (nếu q_rand gần hơn `buoc` thì tới luôn q_rand).

    Gợi ý: d = khoảng cách, s = min(1, buoc/d), q_new = q_near + s·(q_rand − q_near). Trả về tuple (x, y)."""
    raise NotImplementedError("TODO Bài 2: trả về q_new")


def rrt(seed=2, toi_da=3000):
    """Bài 3: vòng lặp RRT (Mục 4.4.2 của sách). Dùng rng = random.Random(seed) và gọi rng ĐÚNG thứ tự này để ra giống video:

    Bắt đầu: V = [Q_S], cha = [-1]. Mỗi vòng k = 0, 1, 2, ...:
      1. Lấy mẫu: nếu rng.random() < ALPHA thì q_rand = Q_G (thiên về đích),
         ngược lại q_rand = (rng.uniform(0, W), rng.uniform(0, H)).
      2. i_near = gan_nhat(V, q_rand); nếu q_rand trùng hẳn V[i_near] (khoảng cách < 1e-9) thì bỏ qua vòng này.
      3. q_new = tien_ve(V[i_near], q_rand, BUOC). Nếu q_new ra ngoài không gian hoặc
         khong_va_cham(V[i_near], q_new) là False thì bỏ qua.
      4. Thêm q_new vào V, cha của nó là i_near.
      5. Nếu q_new cách Q_G dưới DIEM_DICH thì dừng: đã tìm thấy đường ở vòng k + 1.
    Trả về dict {"V": V, "cha": cha, "duong": [Q_S, ..., q_new, Q_G], "vong_tim_thay": k + 1}
    (duong lấy bằng cách lần theo cha từ q_new về Q_S rồi đảo ngược; không tìm thấy thì duong = [], vong_tim_thay = None)."""
    raise NotImplementedError("TODO Bài 3: vòng lặp RRT")
