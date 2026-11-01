"""Bài tập tập 1.3: tự viết bộ điều khiển PID.

Làm lần lượt Bài 1 → Bài 2 → Bài 3 (các chỗ `raise NotImplementedError`). Xong mỗi bài thì chạy:

    python -X utf8 kiem_tra.py

Giữ nguyên tên lớp, tên hàm và tham số vì kiem_tra.py gọi đúng các tên này.
Lời giải (chính là code dùng trong video) nằm ở ../sim/pid.py. Hãy tự làm trước khi mở.
"""
dt = 0.01  # bước thời gian của mô phỏng (giây), giống ../sim/pid.py


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.tich_phan = 0.0  # ∫e dt cộng dồn từ đầu tới giờ
        self.e_truoc = None   # sai số ở bước trước (None = đây là bước đầu tiên)

    def lenh(self, e):
        """Nhận sai số e = r − y, trả về lệnh tốc độ quay ω = Kp·e + Ki·∫e dt + Kd·de/dt.

        Thành phần nào có hệ số bằng 0 thì bỏ qua, nên Bài 1 chạy được khi chưa làm Bài 2, 3."""
        w = self.thanh_phan_P(e)
        if self.kd:
            w += self.thanh_phan_D(e)
        if self.ki:
            w += self.thanh_phan_I(e)
        return w

    def thanh_phan_P(self, e):
        # Bài 1: lệch bao nhiêu thì bẻ lái bấy nhiêu, theo tỉ lệ Kp.
        raise NotImplementedError("TODO Bài 1: trả về Kp·e")

    def thanh_phan_D(self, e):
        # Bài 2: de/dt ≈ (e − e_trước) / dt. Bước đầu tiên chưa có e_trước thì coi de/dt = 0.
        # Nhớ lưu e vào self.e_truoc để bước sau dùng.
        raise NotImplementedError("TODO Bài 2: trả về Kd·de/dt")

    def thanh_phan_I(self, e):
        # Bài 3: cộng dồn e·dt vào self.tich_phan (cộng TRƯỚC rồi mới nhân), trả về Ki·∫e dt.
        raise NotImplementedError("TODO Bài 3: trả về Ki·∫e dt")
