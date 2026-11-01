"""Bài tập tập 1.7: các mảnh Python thuần bên trong hệ thống ROS 2 "tự đi từ A đến B".

planner_node dùng A* (tập 1.5) rồi LÀM MƯỢT đường; controller_node GẮN THỜI GIAN cho đường (hình thang, tập 1.2)
rồi lấy ĐIỂM CẦN TỚI ở mỗi thời điểm để bám theo (tập 1.4). Ba bài dưới đây chính là ba mảnh đó, không cần cài ROS.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../ws/duong_di.py, ../ws/controller_node.py và loi_giai.py (tự làm trước đã).
"""
import bisect
import math


def lam_muot(pts, lan=3):
    """Bài 1: làm mượt đường gấp khúc bằng cách cắt góc Chaikin, lặp `lan` lần.

    Mỗi lần: giữ điểm đầu; với mỗi đoạn a → b, thêm 2 điểm ở 1/4 và 3/4 đoạn:
        0.75·a + 0.25·b   và   0.25·a + 0.75·b
    rồi giữ điểm cuối. pts là list (x, y); trả về list (x, y) mới."""
    raise NotImplementedError("TODO Bài 1: cắt góc Chaikin")


def s_tai(t, L, v_ref, a_ref):
    """Bài 2: quãng đường cần đi được tại thời điểm t, khi chạy hết đường dài L theo đồ thị tốc độ hình thang:
    tăng tốc a_ref tới v_ref, chạy đều, rồi giảm tốc a_ref, dừng đúng ở cuối đường.

    Tổng thời gian T = L/v_ref + v_ref/a_ref (giả sử đường đủ dài để chạm v_ref). Gọi t_tang = v_ref/a_ref:
        t < t_tang         : s = ½·a_ref·t²
        t > T − t_tang     : s = L − ½·a_ref·(T − t)²
        ở giữa             : s = ½·a_ref·t_tang² + v_ref·(t − t_tang)
    Kẹp t trong [0, T] trước khi tính. Trả về s (mét)."""
    raise NotImplementedError("TODO Bài 2: quãng đường theo thời gian")


def diem_tai(pts, s_cong_don, s):
    """Bài 3: điểm (x, y) nằm trên đường gấp khúc pts, cách điểm đầu một quãng s (đo dọc theo đường).

    s_cong_don[i] = độ dài đường từ pts[0] tới pts[i] (s_cong_don[0] = 0).
    Tìm đoạn i sao cho s_cong_don[i] ≤ s < s_cong_don[i+1] (gợi ý: bisect.bisect_right), rồi nội suy tuyến tính.
    Ngoài khoảng thì dùng đoạn đầu / đoạn cuối. Trả về tuple (x, y)."""
    raise NotImplementedError("TODO Bài 3: nội suy điểm theo quãng đường")
