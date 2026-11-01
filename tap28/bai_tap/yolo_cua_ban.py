"""Bài tập tập 2.8: YOLO nhận ra đồ vật, phần hậu xử lý và đánh giá (Chương 10 của sách). Python thuần + numpy.

Một khung (bounding box) viết dạng (cx, cy, w, h): tâm và kích thước, theo tỉ lệ ảnh (0..1).
Một dự đoán là tuple (lop, diem, cx, cy, w, h). Một vật thật là tuple (lop, cx, cy, w, h).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/yolo.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def iou(a, b):
    """Bài 1: IoU = diện tích phần giao / diện tích phần hợp của hai khung a, b dạng (cx, cy, w, h).

    Đổi về góc: x0 = cx − w/2, x1 = cx + w/2 (tương tự y). Giao = max(0, min(x1) − max(x0)) · max(0, min(y1) − max(y0)).
    Hợp = w_a·h_a + w_b·h_b − giao. Trả về giao / (hợp + 1e-9)."""
    raise NotImplementedError("TODO Bài 1: IoU")


def nms(du_doan, nguong=0.5):
    """Bài 2: non-maximum suppression. YOLO thường đoán vài khung chồng lên cùng một vật; chỉ giữ khung tốt nhất.

    1. Xếp các dự đoán theo điểm giảm dần.
    2. Duyệt lần lượt: giữ dự đoán d nếu với MỌI khung g đã giữ, hoặc khác lớp, hoặc iou(khung d, khung g) < nguong.
    Trả về list các dự đoán được giữ (theo thứ tự đã xếp)."""
    raise NotImplementedError("TODO Bài 2: NMS")


def ap_lop(du_doan, that, c, nguong_iou=0.5):
    """Bài 3: AP (average precision) của lớp c trên nhiều ảnh. du_doan[k], that[k] là list của ảnh thứ k.

    1. Gom mọi dự đoán lớp c của mọi ảnh, xếp theo điểm giảm dần. n_that = số vật thật lớp c.
    2. Duyệt từng dự đoán (ảnh k): tìm vật thật lớp c CHƯA được khớp trong ảnh k có IoU lớn nhất;
       nếu IoU ≥ nguong_iou thì là đúng (TP, đánh dấu vật đó đã khớp), ngược lại là sai (FP).
    3. Cộng dồn: recall = TP_dồn / n_that, precision = TP_dồn / (TP_dồn + FP_dồn).
    4. Làm precision không tăng từ phải sang trái: p_mono = np.maximum.accumulate(precision[::-1])[::-1].
    5. AP = Σ (recall_i − recall_{i−1}) · p_mono_i   (recall_{−1} = 0).
    Trả về (AP, mảng recall, mảng precision)."""
    raise NotImplementedError("TODO Bài 3: AP")
