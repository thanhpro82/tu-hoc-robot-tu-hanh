"""Bài tập tập 4.1: máy trạng thái hữu hạn, bộ não hành vi của robot (Chương 16 của sách).

Robot tuần tra phòng và đuổi theo con mèo. FSM kiểu Mealy: mỗi nhịp 0,1 s nhận ĐÚNG MỘT đầu vào i và chuyển s_{t+1} = n(s_t, i_t).
Bảng chuyển viết dạng dict {(trạng_thái, đầu_vào): trạng_thái_mới}; cặp nào không có trong dict thì ở yên trạng thái cũ.
Trạng thái: "TUAN_TRA", "DUOI", "TIM", "VE_SAC", "SAC".  Đầu vào: "THAY", "KHONG_THAY", "HET_GIO", "PIN_YEU", "TOI_DOC", "DAY_PIN".
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/fsm.py và loi_giai.py (tự làm trước đã).
"""


def chuyen_B():
    """Bài 1: bảng chuyển của bản B (có trạng thái TÌM). Cần đúng 4 mũi tên:

        TUAN_TRA --THAY--> DUOI          (thấy mèo thì đuổi)
        DUOI --KHONG_THAY--> TIM         (mất dấu thì đi tìm, thay vì bỏ cuộc như bản A)
        TIM --THAY--> DUOI               (tìm thấy lại thì đuổi tiếp)
        TIM --HET_GIO--> TUAN_TRA        (tìm 8 giây không thấy mới bỏ)
    Trả về dict."""
    raise NotImplementedError("TODO Bài 1: bảng chuyển bản B")


def them_sac(chuyen):
    """Bài 2: từ bảng của bản B, tạo bảng của bản C (biết đi sạc). Trả về dict MỚI (đừng sửa dict truyền vào), gồm mọi mũi tên cũ cộng:

        TUAN_TRA, DUOI, TIM --PIN_YEU--> VE_SAC     (pin < 25% thì bỏ dở việc, về đốc)
        VE_SAC --TOI_DOC--> SAC
        SAC --DAY_PIN--> TUAN_TRA"""
    raise NotImplementedError("TODO Bài 2: thêm hành vi sạc")


def ghep_song_song(*may):
    """Bài 3 (Eq. 16.2): ghép song song nhiều FSM. Mỗi máy là tuple (S, I, O, n, o, s0, chuyen), trong đó n là dict đủ mọi cặp (s, i).

    Máy ghép có trạng thái là bộ (s1, s2, ...), đầu vào là bộ (i1, i2, ...) (mọi tổ hợp, dùng itertools.product),
    và n((s1, s2, ...), (i1, i2, ...)) = (n1(s1, i1), n2(s2, i2), ...).
    Duyệt (BFS/DFS) từ trạng thái đầu (s0 của từng máy) để tìm mọi trạng thái tới được.
    Trả về (số trạng thái tới được, số đầu vào, số ô trong bảng n = tích hai số trên)."""
    raise NotImplementedError("TODO Bài 3: ghép song song")
