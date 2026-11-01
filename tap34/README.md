# Tập 3.4 · Particle Filter: ngàn phỏng đoán

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.4") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 12](https://porabook.com/book/approximate-filters/)

## Tóm tắt video

Không đoán được một chỗ thì đoán 1000 chỗ cùng lúc 🟠🟠🟠 Xem đám hạt tìm ra robot! Bạn thích bộ lọc nào nhất? 👇

Tập 3.4 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Bộ lọc hạt: rải 1000 hạt khắp phòng 10 × 8 m, mỗi hạt là một phỏng đoán. Đo khoảng cách tới 2 mốc → gán trọng số, chỉ ~16 hạt còn có trọng lượng → lấy mẫu lại thành 2 cụm (41,0% và 45,7%), vì vị trí soi gương qua đường nối 2 mốc cũng khớp y hệt. Có lúc đám hạt tin nhầm 86,8%! Robot rẽ → cụm soi gương hết khớp → bước 12 có 99,4% hạt đúng chỗ, cuối cùng lệch 6 cm. Chạy thử 30 lần, cả 30 lần đều tìm đúng. (Mô phỏng Python, robot có la bàn biết hướng.)

## Chạy thử

```bash
cd tap34/sim
python -X utf8 hat.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/hat.py` | Tập 3.4 - Particle Filter: ngàn phỏng đoán (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/hat.py`**

```text
Tập 3.4 - Particle Filter: ngàn phỏng đoán (series Tự Học Robot Tự Hành)

Theo Chương 12 (§12.4.2), Principles of Robot Autonomy:
  - Niềm tin = tập K hạt P_t = {x_t^[1], ..., x_t^[K]} (Eq. 12.11), K ≈ 10³ thường đủ dùng
  - Thuật toán 5: (1) dự đoán: rút x̄_t^[k] ~ p(x_t | x_t-1^[k], u_t); (2) trọng số w_t^[k] = p(z_t | x̄_t^[k]);
    (3) lấy mẫu lại có hoàn lại theo trọng số -> P_t
  - Không lấy mẫu lại thì trọng số dồn vào vài hạt (suy biến); hợp với định vị toàn cục, niềm tin nhiều đỉnh
Mở rộng / giả định: robot có la bàn biết hướng (±5°), phòng 10 × 8 m, 2 mốc phát sóng, robot chỉ đo khoảng cách tới 2 mốc (σ = 0,2 m) nên lúc đầu
có 2 vị trí "soi gương" đều khớp; lấy mẫu lại kiểu hệ thống (low-variance), K = 1000, đo cỡ mẫu hiệu dụng (ESS).
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 hat.py
```

---
[← Về danh sách tập](../README.md)
