"""Bài tập tập 4.4: học tăng cường, robot học từ thất bại bằng Q-learning (Chương 18 của sách, Thuật toán 5). Dùng numpy.

Robot ở kho hàng tập 4.2 nhưng KHÔNG biết sàn trơn bao nhiêu: chỉ tự đi thử. Mỗi bước thưởng r = −1; rơi cầu thang r = −100 (hết tập);
tới G là hết tập. Bảng Q có hình (số ô, 4): Q[i, a] là "tổng thưởng kỳ vọng" nếu ở ô i làm lệnh a rồi sau đó làm tốt nhất.
Lệnh đánh số 0..3 theo thứ tự U = ["len", "xuong", "trai", "phai"].
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/qlearn.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def chon_hanh_dong(Qi, eps, rng):
    """Bài 1 (ε-greedy): Qi là hàng Q của ô hiện tại (4 số). Gọi rng ĐÚNG thứ tự này:

        nếu rng.random() < eps:  a = int(rng.integers(4))                                  (khám phá: chọn bừa)
        ngược lại:               a = int(rng.choice(np.flatnonzero(Qi == Qi.max())))       (khai thác: chọn lệnh tốt nhất, hoà thì bốc thăm)
    Trả về a."""
    raise NotImplementedError("TODO Bài 1: ε-greedy")


def cap_nhat_q(Q, i, a, r, i2, xong, alpha, gamma):
    """Bài 2 (Eq. 18.18): cập nhật Q tại (i, a) sau khi làm lệnh a ở ô i, nhận thưởng r, tới ô i2.

        mục tiêu = r                         nếu xong (tập kết thúc: tới G hoặc rơi)
                 = r + gamma·max_a' Q[i2, a']  nếu chưa xong
        Q[i, a] ← Q[i, a] + alpha·(mục tiêu − Q[i, a])
    Sửa thẳng vào Q (không cần trả về)."""
    raise NotImplementedError("TODO Bài 2: cập nhật Q")


def chinh_sach_tham_lam(Q, cac_o, IDX, U):
    """Bài 3: chính sách học được π(x) = lệnh có Q lớn nhất (np.argmax, hoà thì lấy lệnh đứng trước).

    cac_o: list các ô; IDX: dict ô → chỉ số hàng trong Q; U: list tên lệnh. Trả về dict {ô: tên lệnh}."""
    raise NotImplementedError("TODO Bài 3: chính sách tham lam")
