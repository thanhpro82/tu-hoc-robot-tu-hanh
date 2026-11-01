# Tập 2.6 · Thị giác máy tính cổ điển

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.6") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 8](https://porabook.com/book/classical-perception/)

## Tóm tắt video

Với robot, bức ảnh chỉ là 76.800 con số 🔢 Làm sao nó tìm ra vạch dẫn đường? 👇

Tập 2.6 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Thị giác máy tính cổ điển: lấy đạo hàm thẳng trên ảnh nhiễu ra 15.001 chấm cạnh, 93% là giả. Làm mịn bằng lọc Gauss → mặt nạ Sobel đo độ dốc → giữ cực đại vượt ngưỡng: còn 634 chấm (538 ở mép vạch, 96 ở vết bẩn). Biến đổi Hough: mỗi chấm bỏ phiếu cho mọi đường đi qua nó → hai mép vạch được 144 và 135 phiếu, vết bẩn chỉ 20. Vạch đo được 23,0°, thật 23,4°. (Ảnh tạo bằng Python, ứng dụng dò vạch là phần mở rộng.)

## Chạy thử

```bash
cd tap26/sim
python -X utf8 thi_giac.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/thi_giac.py` | Tập 2.6 - Thị giác máy tính cổ điển (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/thi_giac.py`**

```text
Tập 2.6 - Thị giác máy tính cổ điển (series Tự Học Robot Tự Hành)

Theo Chương 8, Principles of Robot Autonomy:
  - §8.1.1 lọc ảnh: tương quan / tích chập (Eq. 8.1-8.2), lọc Gauss G_σ, mặt nạ tách được, mặt nạ Sobel (Eq. 8.5)
  - §8.1.2 dò cạnh: làm mịn -> đạo hàm theo x, y -> |∇S| = sqrt(S_x² + S_y²) -> ngưỡng + chỉ giữ cực đại cục bộ (Ví dụ 8.1.3)
  - §8.2.1 biến đổi Hough dạng cực x cos α + y sin α = r: mỗi điểm cạnh bỏ phiếu trong lưới (α, r), đỉnh = đường thẳng
Mở rộng (ngoài sách): ứng dụng dò vạch dẫn đường cho robot và góc lái suy ra từ vạch (sách không có ví dụ bám vạch);
cách chọn ngưỡng theo phần trăm; tách hai mép vạch thành đường giữa.
Ảnh sàn nhà, vạch, vết bẩn và nhiễu là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 thi_giac.py
```

---
[← Về danh sách tập](../README.md)
