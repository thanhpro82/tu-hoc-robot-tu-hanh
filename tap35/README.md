# Tập 3.5 · Định vị trên bản đồ có sẵn

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.5") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 13](https://porabook.com/book/robot-localization/)

## Tóm tắt video

Bịt mắt robot, nhấc nó sang phòng khác mà không báo… nó có tự biết mình ở đâu không? 🤖🫳 Robot bạn đã bao giờ bị lạc chưa? 👇

Tập 3.5 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Định vị trên bản đồ có sẵn (Monte Carlo Localization): căn hộ 4 phòng, LiDAR 8 tia, 2000 hạt rải khắp chỗ trống (hạt trong tường bị loại). Mỗi hạt so số đo LiDAR dự đoán với số đo thật. Bước 1 chỉ 1,8% hạt gần đúng, bước 4 đã 96%, đi tiếp chỉ lệch 7,6 cm. Bị bắt cóc ở bước 52: cả đám hạt vẫn tin ở chỗ cũ, sai hơn 5 m. Thả thêm 3% hạt ngẫu nhiên mỗi bước → tìm lại sau 4 giây. Không thả thì kẹt mãi, cuối vẫn lệch 5,09 m. (Mô phỏng Python.)

## Chạy thử

```bash
cd tap35/sim
python -X utf8 mcl.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/mcl.py` | Tập 3.5 - Định vị trên bản đồ có sẵn (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/mcl.py`**

```text
Tập 3.5 - Định vị trên bản đồ có sẵn (series Tự Học Robot Tự Hành)

Theo Chương 13, Principles of Robot Autonomy:
  - Ba bài toán (§13.1): bám vị trí, định vị toàn cục, robot bị bắt cóc (bị dời đi mà không báo)
  - Niềm tin có điều kiện theo bản đồ m (§13.2); chuyển động có bản đồ (Eq. 13.2): tư thế nằm trong tường có xác suất 0
  - Mô hình đo tách thành tích từng thành phần (Eq. 13.3): p(z_t | x_t, m) = Π_i p(z_t^i | x_t, m)
  - Monte Carlo Localization (Thuật toán 4): đẩy hạt qua chuyển động -> trọng số p(z_t | x̄, m) -> lấy mẫu lại
  - Ghi chú lề §13.6: thả thêm hạt ngẫu nhiên mỗi bước giúp xử lý robot bị bắt cóc
Mở rộng / giả định: căn hộ 12 × 8 m (lưới 10 cm), LiDAR 8 tia tầm 6 m nhiễu 5 cm, mô hình mỗi tia = Gauss σ = 0,6 m
trộn 10% đều (sách không nêu mô hình tia cụ thể), K = 2000 hạt, thả 3% hạt ngẫu nhiên mỗi bước, lộ trình định sẵn.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 mcl.py
```

---
[← Về danh sách tập](../README.md)
