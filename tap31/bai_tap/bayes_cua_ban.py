"""Bài tập tập 3.1: "Tôi đang ở đâu?", bộ lọc Bayes rời rạc (Thuật toán 2, Chương 11 của sách). Dùng numpy.

Hành lang 10 m chia 200 ô 5 cm; X là toạ độ tâm các ô; niềm tin bel là mảng 200 xác suất, tổng = 1.
O_CUA[k] = True nếu ô k nằm trước một cánh cửa. Cảm biến chỉ báo "thấy cửa" hoặc "không thấy".
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/bayes.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np

DAI, O = 10.0, 0.05
X = np.arange(0, DAI, O) + O / 2
CUA = [(1.0, 1.8), (2.6, 3.4), (6.2, 7.0)]
O_CUA = np.zeros_like(X, dtype=bool)
for _a, _b in CUA:
    O_CUA |= (X >= _a) & (X <= _b)
P_THAY_O_CUA, P_THAY_KHONG_CUA = 0.8, 0.1
U, SIGMA = 0.5, 0.1        # mỗi bước đi u = 0,5 m, nhiễu chuyển động σ = 0,1 m


def hieu_chinh(bel_tr, thay_cua):
    """Bài 1 (bước hiệu chỉnh): p_k = η · p(z | x_k) · p̄_k.

    p(z | x_k): nếu ô k ở cửa thì p(thấy) = 0,8, không ở cửa thì p(thấy) = 0,1.
    Nếu z là "không thấy" (thay_cua = False) thì dùng 1 − p(thấy).
    η = 1 / Σ_k p(z | x_k)·p̄_k để tổng lại bằng 1. Trả về (bel_moi, eta)."""
    raise NotImplementedError("TODO Bài 1: hiệu chỉnh")


def du_doan(bel):
    """Bài 2 (bước dự đoán): p̄_k = Σ_i p(x_k | x_i, u)·p_i, với p(x_k | x_i, u) là mật độ chuẩn N(x_k − x_i; U, SIGMA²)·O.

    Gợi ý: d = X[:, None] − X[None, :] (ma trận x_k − x_i), K = exp(−½·((d − U)/SIGMA)²) / (√(2π)·SIGMA/O),
    p̄ = K @ bel. Phần xác suất "đi ra ngoài hành lang" bị mất, nên chia cho tổng để chuẩn hoá lại. Trả về p̄."""
    raise NotImplementedError("TODO Bài 2: dự đoán")


def loc_bayes(ds_z):
    """Bài 3: chạy cả bộ lọc. ds_z[k] là kết quả cảm biến (True/False) ở bước k = 0, 1, ..., n.

    Bắt đầu: bel đều = 1/200 cho mọi ô (chưa biết gì). Mỗi bước k: nếu k > 0 thì du_doan trước, rồi hieu_chinh với ds_z[k].
    Trả về list niềm tin SAU hiệu chỉnh của từng bước (n + 1 mảng)."""
    raise NotImplementedError("TODO Bài 3: vòng lặp bộ lọc Bayes")
