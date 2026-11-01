"""Tập 2.2 - Camera là cái hộp có lỗ (series Tự Học Robot Tự Hành)

Theo Chương 6, Principles of Robot Autonomy:
  - Eq. 6.1: x = f·X/Z, y = f·Y/Z
  - Eq. 6.7 / 6.11: u = α·X/Z + u0, v = β·Y/Z + v0, K = [[α, γ, u0], [0, β, v0], [0, 0, 1]]
  - Eq. 6.17: p^h = K [R t] P_W^h  (11 bậc tự do: 5 nội + 3 quay + 3 tịnh tiến)
Thông số camera dưới đây là GIẢ ĐỊNH (camera 640×480 điển hình), con số in ra là kết quả tính thật.
Chạy: python pinhole.py
"""
import math

# Camera giả định: ảnh 640×480, α = β = 500 px, không xiên (γ = 0), tâm ảnh ở giữa
ALPHA = BETA = 500.0
GAMMA = 0.0
U0, V0 = 320.0, 240.0
K = [[ALPHA, GAMMA, U0], [0.0, BETA, V0], [0.0, 0.0, 1.0]]


def nhan(A, b):
    return [sum(A[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]


def chieu(P_W, R=None, t=(0.0, 0.0, 0.0)):
    """p^h = K [R t] P_W^h, rồi chia cho thành phần cuối (Eq. 6.9) -> pixel (u, v)."""
    R = R or [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    P_C = [a + b for a, b in zip(nhan(R, P_W), t)]  # Eq. 6.15: P_C = t + R·P_W
    ph = nhan(K, P_C)
    return ph[0] / ph[2], ph[1] / ph[2]


def chieu_cao_anh(H, Z):
    """Vật cao H mét, cách Z mét -> cao bao nhiêu pixel trên ảnh."""
    return BETA * H / Z


# Hộp 30 cm ở các khoảng cách khác nhau
KHOANG_CACH = [1.0, 2.0, 4.0]
HOP = 0.30

# Nhập nhằng tỉ lệ: hộp 30 cm cách 1 m và hộp 60 cm cách 2 m cho cùng một ảnh
NHAP_NHANG = [(0.30, 1.0), (0.60, 2.0), (1.20, 4.0)]

# Lỗ to hay nhỏ (mở rộng, quang hình đơn giản): vật ở xa -> vệt mờ trên ảnh ≈ đường kính lỗ, độ sáng ∝ diện tích lỗ
LO = [0.5, 2.0, 8.0]  # mm


def lap_phuong(canh=0.4):
    h = canh / 2
    return [(x, y, z) for x in (-h, h) for y in (-h, h) for z in (-h, h)]


def quay_y(goc):
    c, s = math.cos(goc), math.sin(goc)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


def phim_lap_phuong(so_khung=90):
    """Khối lập phương 40 cm vừa quay vừa tiến từ 3 m về 1.2 m trước camera."""
    khung = []
    for k in range(so_khung):
        p = k / (so_khung - 1)
        Z = 3.0 - 1.8 * p
        R = quay_y(0.6 + 1.6 * p)
        khung.append([chieu(v, R, (0.0, 0.0, Z)) for v in lap_phuong()])
    return khung


LAP_PHUONG = phim_lap_phuong()

if __name__ == "__main__":
    print(f"K = {K}  (5 tham số nội: α, β, γ, u0, v0)")
    for Z in KHOANG_CACH:
        print(f"Hộp {HOP * 100:.0f} cm cách {Z:.0f} m -> cao {chieu_cao_anh(HOP, Z):.1f} px")
    for H, Z in NHAP_NHANG:
        print(f"Hộp {H * 100:.0f} cm cách {Z:.0f} m -> cao {chieu_cao_anh(H, Z):.1f} px")
    for a in LO:
        print(f"Lỗ {a} mm -> vệt mờ ~{a} mm, sáng gấp {(a / LO[0]) ** 2:.0f} lần lỗ {LO[0]} mm")
    u, v = chieu((0.2, 0.1, 2.0))
    print(f"Điểm (0.2, 0.1, 2.0) m -> pixel ({u:.0f}, {v:.0f})")
    xs = [p[0] for p in LAP_PHUONG[0] + LAP_PHUONG[-1]]
    print(f"Lập phương: khung đầu rộng {max(p[0] for p in LAP_PHUONG[0]) - min(p[0] for p in LAP_PHUONG[0]):.0f} px, "
          f"khung cuối rộng {max(p[0] for p in LAP_PHUONG[-1]) - min(p[0] for p in LAP_PHUONG[-1]):.0f} px")
