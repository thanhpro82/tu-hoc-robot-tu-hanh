# Tập 3.2 · Kalman Filter dễ hiểu nhất

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.2") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 11](https://porabook.com/book/localization-filtering/)

## Tóm tắt video

Một cảm biến nhiễu + một mô hình bị trôi = một thứ tốt hơn cả hai 🔔🔔 Đó là bộ lọc Kalman! Bạn dùng Kalman bao giờ chưa? 👇

Tập 3.2 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Robot chạy thẳng 20 giây: cảm biến khoảng cách sai trung bình 30,3 cm, còn cộng dồn gia tốc IMU thì trôi 8,95 m. Kalman coi niềm tin là đường cong chuông (μ, Σ): dự đoán đẩy chuông tới và bè ra vì nhiễu Q, cập nhật nhân với chuông cảm biến (nhiễu R) → chuông mới ± 10,9 cm, hẹp hơn cả hai. Hệ số K từ 0,918 giảm còn 0,132. Kết quả: sai 13,8 cm, tốt hơn cảm biến 2,2 lần. (Mô phỏng Python theo Ví dụ 12.2.1.)

## Chạy thử

```bash
cd tap32/sim
python -X utf8 kalman.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/kalman.py` | Tập 3.2 - Kalman Filter dễ hiểu nhất (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/kalman.py`**

```text
Tập 3.2 - Kalman Filter dễ hiểu nhất (series Tự Học Robot Tự Hành)

Theo Principles of Robot Autonomy (Ch. 11 giới thiệu, công thức ở §12.2):
  - Mô hình (Eq. 12.3-12.4): x_t = A x_t-1 + B u_t + ε, ε ~ N(0, Q); z_t = C x_t + δ, δ ~ N(0, R)
  - Ví dụ 12.2.1: x = [p, v], A = [[1, Δt], [0, 1]], B = [Δt²/2, Δt], C = [1, 0] (đo vị trí)
  - Thuật toán 1: dự đoán μ̄ = Aμ + Bu, Σ̄ = AΣAᵀ + Q; S = CΣ̄Cᵀ + R; K = Σ̄CᵀS⁻¹;
    μ = μ̄ + K(z − Cμ̄), Σ = (I − KC)Σ̄(I − KC)ᵀ + KRKᵀ (dạng Joseph)
Mở rộng / giả định: hồ sơ gia tốc, nhiễu gia tốc kế σ_a = 0,3 m/s² và lệch 0,02 m/s², cảm biến khoảng cách σ = 0,3 m,
Δt = 0,1 s, chạy 20 s. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 kalman.py
```

---
[← Về danh sách tập](../README.md)
