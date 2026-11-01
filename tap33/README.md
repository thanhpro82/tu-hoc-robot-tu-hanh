# Tập 3.3 · EKF & UKF: Kalman cho thế giới cong

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.3") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 12](https://porabook.com/book/approximate-filters/)

## Tóm tắt video

Kalman chỉ giỏi khi mọi thứ thẳng tuột. Robot thì rẽ, quay, vòng 🍌↪️ EKF hay UKF, bạn chọn cái nào? 👇

Tập 3.3 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Hướng mơ hồ ±35°, đi thẳng 2 m: các khả năng cong như quả chuối. EKF kẻ thẳng bằng Jacobian → tâm lệch 33,9 cm và tưởng mình chắc hơn thực tế (dọc ±5 cm, thật ±44,4 cm). UKF thả 7 điểm sigma qua đúng đường cong → chỉ lệch 0,3 cm, không cần đạo hàm. Robot chạy 60 s: chỉ encoder + IMU trôi 2,93 m; thêm đo 2 mốc thì EKF 22,5 cm, UKF 21,5 cm, UKF nhỉnh hơn lúc đầu (32,6 so với 36,5 cm). (Mô phỏng Python, "sự thật" từ 100.000 mẫu.)

## Chạy thử

```bash
cd tap33/sim
python -X utf8 ekf_ukf.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/ekf_ukf.py` | Tập 3.3 - EKF & UKF: Kalman cho thế giới cong (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/ekf_ukf.py`**

```text
Tập 3.3 - EKF & UKF: Kalman cho thế giới cong (series Tự Học Robot Tự Hành)

Theo Chương 12 (§12.3), Principles of Robot Autonomy:
  - Mô hình phi tuyến (Eq. 12.5): x_t = f(x_t-1, u_t) + ε, ε ~ N(0, Q); z_t = h(x_t) + δ, δ ~ N(0, R)
  - EKF (Thuật toán 2): F_t = ∂f/∂x tại μ_t-1, H_t = ∂h/∂x tại μ̄_t; μ̄ = f(μ, u), Σ̄ = FΣFᵀ + Q; K = Σ̄Hᵀ(HΣ̄Hᵀ + R)⁻¹
  - UKF (Thuật toán 3): 2n + 1 điểm sigma, λ = α²(n + κ) − n, trọng số W_m, W_c; đưa điểm qua f, h thật, gộp lại
  - Ví dụ 12.3.1: tư thế [p_x, p_y, θ], đo khoảng cách và góc tới mốc ℓ: h = [√(Δx² + Δy²), atan2(Δy, Δx) − θ]
Phần A: biến đổi một phân bố Gauss qua chuyển động cong khi hướng còn mơ hồ; "sự thật" = 100.000 mẫu Monte Carlo.
Phần B: định vị robot unicycle: tốc độ từ encoder, tốc độ quay từ IMU, đo khoảng cách + góc tới 2 mốc mỗi 1 s.
Mở rộng / giả định: mọi tham số nhiễu, quỹ đạo, vị trí mốc, α = 1, β = 2, κ = 0. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 ekf_ukf.py
```

---
[← Về danh sách tập](../README.md)
