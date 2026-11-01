# Tập 2.4 · Hai mắt để đoán khoảng cách

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.4") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 7](https://porabook.com/book/stereo-vision/)

## Tóm tắt video

Nhắm một mắt rồi chạm hai đầu ngón trỏ vào nhau 👀👉👈 Khó hơn hẳn đúng không? Bạn thử chưa? 👇

Tập 2.4 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Robot dùng 2 camera cách nhau 12 cm. Cùng một vật hiện lệch nhau d pixel (disparity): hộp ở gần lệch 37,5 px, tường ở xa chỉ 11,25 px. Độ sâu z = b·f/d. Trượt cửa sổ 11×11 dọc 1 hàng ngang để so khớp → bản đồ độ sâu: hộp 1,20 m, bóng 1,97 m, tường 4,00 m. Nhưng tấm áp phích trơn bị loại 76% điểm, và lệch 1 px thì ở 1 m sai 2,3 cm, ở 4 m sai 39 cm. (Cảnh và 2 ảnh là mô phỏng Python.)

## Chạy thử

```bash
cd tap24/sim
python -X utf8 stereo.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/stereo.py` | Tập 2.4 - Hai mắt để đoán khoảng cách (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/stereo.py`**

```text
Tập 2.4 - Hai mắt để đoán khoảng cách (series Tự Học Robot Tự Hành)

Theo Chương 7, Principles of Robot Autonomy:
  - §7.1.1: sau khi chỉnh ảnh (rectification), hai camera song song, đường epipolar là các hàng ngang
    -> tìm điểm tương ứng chỉ cần dò dọc 1 hàng
  - §7.2: disparity d = p_u - p'_u, độ sâu z = b·f / d (Eq. 7.7); so khớp bằng tương quan trên cửa sổ nhỏ;
    khó ở vùng trơn (không có vân), vùng bị che, vân lặp lại; độ phân giải độ sâu giảm theo bình phương khoảng cách.
Mở rộng (ngoài sách): hàm chi phí SSD, nội suy dưới pixel bằng parabol, kiểm tra trái-phải để loại vùng bị che,
ngưỡng độ vân. Cảnh 3D, camera (480×360, f = 375 px), baseline 12 cm và nhiễu ảnh là GIẢ ĐỊNH;
hai ảnh được kết xuất bằng dò tia từ cảnh giả định này, mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 stereo.py
```

---
[← Về danh sách tập](../README.md)
