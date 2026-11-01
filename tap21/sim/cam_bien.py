"""Tập 2.1 - Giác quan của robot (series Tự Học Robot Tự Hành)

Theo Chương 5, Principles of Robot Autonomy:
  - Thời gian bay (Mục 5.4.2): d = c·t/2
  - Sai số (Mục 5.2.2): e = m - v (đo được trừ giá trị thật); chính xác (accuracy) khác ổn định (precision)
  - Trôi (Mục 5.4.1): sai số nhỏ cộng dồn theo thời gian khi tích phân gyro
Các tham số cảm biến dưới đây là GIẢ ĐỊNH để minh hoạ (ghi rõ trong video), con số in ra là kết quả tính thật.
Chạy: python cam_bien.py
"""
import random
import statistics

# ── 1. Thời gian bay ────────────────────────────────────────────────────────
C_AM = 343.0  # tốc độ âm thanh trong không khí ~20°C, m/s (giá trị vật lý chuẩn, sách không nêu số)
C_SANG = 3.0e8  # tốc độ ánh sáng, m/s


def thoi_gian_bay(d, c):
    """Thời gian khứ hồi để đo khoảng cách d: t = 2d / c."""
    return 2 * d / c


# ── 2. Chính xác vs ổn định: 4 cảm biến đo cùng một vật cách đúng 1.00 m ─────
THAT = 1.00
CAM_BIEN = {  # tên: (lệch hệ thống, độ nhiễu ngẫu nhiên) theo mét
    "chinh_xac_on_dinh": (0.00, 0.005),
    "on_dinh_sai": (0.08, 0.005),
    "chinh_xac_nhieu": (0.00, 0.05),
    "sai_va_nhieu": (0.08, 0.05),
}
SO_LAN = 20


def do(lech, nhieu, seed):
    rng = random.Random(seed)
    return [THAT + lech + rng.gauss(0, nhieu) for _ in range(SO_LAN)]


DO = {ten: do(l, n, 10 + i) for i, (ten, (l, n)) in enumerate(CAM_BIEN.items())}

# ── 3. Trôi: robot đứng yên, tích phân gyro 60 giây ─────────────────────────
DT = 0.01
GIAY = 60
GYRO_RE = (0.3, 0.5)  # gyro rẻ chưa hiệu chỉnh: lệch 0.3 °/s, nhiễu 0.5 °/s (giả định)
GYRO_HC = (0.01, 0.5)  # sau khi hiệu chỉnh lệch: còn 0.01 °/s (giả định)


def troi(lech, nhieu, seed=3):
    rng = random.Random(seed)
    goc, lich_su = 0.0, [0.0]
    for _ in range(round(GIAY / DT)):
        goc += (0.0 + lech + rng.gauss(0, nhieu)) * DT  # robot đứng yên: tốc độ quay thật = 0
        lich_su.append(goc)
    return lich_su


TROI_RE = troi(*GYRO_RE)
TROI_HC = troi(*GYRO_HC)

if __name__ == "__main__":
    print(f"Siêu âm: vật cách 1 m -> tiếng vang về sau {thoi_gian_bay(1, C_AM) * 1000:.2f} ms")
    print(f"LiDAR  : vật cách 1 m -> tia sáng về sau {thoi_gian_bay(1, C_SANG) * 1e9:.2f} ns")
    for ten, ds in DO.items():
        tb, sd = statistics.mean(ds), statistics.stdev(ds)
        print(f"{ten:18s}: trung bình {tb:.3f} m (sai số e = {(tb - THAT) * 100:+.1f} cm), dao động ±{sd * 100:.1f} cm")
    print(f"Gyro rẻ, đứng yên {GIAY} s: tưởng đã quay {TROI_RE[-1]:.1f}°")
    print(f"Gyro đã hiệu chỉnh, {GIAY} s: tưởng đã quay {TROI_HC[-1]:.1f}°")
