# Tập 2.1 · Giác quan của robot

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.1") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 5](https://porabook.com/book/robot-sensors/)

## Tóm tắt video

Robot hiểu thế giới qua cảm biến, và cảm biến nào cũng "nói dối" một chút 🤖📡 Bạn từng dùng cảm biến nào? 👇

Tập 2.1 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Bên trong / bên ngoài, thụ động / chủ động. Siêu âm đo bằng tiếng vang d = c·t/2 (1 m ↔ 5,83 ms). Sai số e = m − v, và chính xác ≠ ổn định (ổn định ±0,5 cm mà vẫn lệch 8 cm). Gyro rẻ để đứng yên 1 phút "tưởng" đã quay 18,2°. Số liệu từ mô phỏng Python (tham số cảm biến là giả định).

## Chạy thử

```bash
cd tap21/sim
python -X utf8 cam_bien.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/cam_bien.py` | Tập 2.1 - Giác quan của robot (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/cam_bien.py`**

```text
Tập 2.1 - Giác quan của robot (series Tự Học Robot Tự Hành)

Theo Chương 5, Principles of Robot Autonomy:
  - Thời gian bay (Mục 5.4.2): d = c·t/2
  - Sai số (Mục 5.2.2): e = m - v (đo được trừ giá trị thật); chính xác (accuracy) khác ổn định (precision)
  - Trôi (Mục 5.4.1): sai số nhỏ cộng dồn theo thời gian khi tích phân gyro
Các tham số cảm biến dưới đây là GIẢ ĐỊNH để minh hoạ (ghi rõ trong video), con số in ra là kết quả tính thật.
Chạy: python cam_bien.py
```

---
[← Về danh sách tập](../README.md)
