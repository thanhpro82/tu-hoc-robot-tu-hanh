"""Bài tập tập 3.9: tổng kết Mùa 3, chấm lần chạy Nav2 THẬT (AMCL + lập lại đường khi cửa đóng). Dùng numpy.

Dữ liệu ở ../ws/out/: tư thế thật của robot theo thời gian (TR, THAT), ước lượng của AMCL, các đường Nav2 đã lập (mỗi đường là
mảng (n, 2) toạ độ x, y), và đám hạt của AMCL (mảng (n, 2)).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/phan_tich.py và loi_giai.py (tự làm trước đã).
"""
import numpy as np


def that_luc(TR, THAT, t):
    """Bài 1: tư thế thật tại thời điểm t, khi tư thế chỉ được ghi ở các thời điểm TR (tăng dần).

    Lấy chỉ số i = np.searchsorted(TR, t), kẹp trong [0, len(TR) − 1], trả về THAT[i].
    (Dùng để so mỗi ước lượng AMCL với tư thế thật cùng lúc.)"""
    raise NotImplementedError("TODO Bài 1: tư thế thật tại thời điểm t")


def qua_cua(xy, cua, ban_kinh=0.4):
    """Bài 2a: đường xy (mảng (n, 2)) có đi qua ô cửa không?

    Có, nếu có ít nhất một điểm với |x − cua_x| < ban_kinh VÀ y < cua_y + 1.1 (đi qua khe cửa ở phía dưới, như code video). Trả về True/False."""
    raise NotImplementedError("TODO Bài 2a")


def do_dai(xy):
    """Bài 2b: chiều dài đường gấp khúc xy = tổng khoảng cách giữa các điểm liên tiếp."""
    raise NotImplementedError("TODO Bài 2b")


def do_toa(xy):
    """Bài 3: độ toả của đám hạt AMCL = √(phương sai theo x + phương sai theo y) (np.var, mỗi cột một trục).

    Lúc mới bấm ước lượng, hạt toả rộng; khi AMCL đã chắc, hạt gom lại."""
    raise NotImplementedError("TODO Bài 3: độ toả đám hạt")
