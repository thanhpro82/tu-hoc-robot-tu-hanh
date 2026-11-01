# Tập 1.2 · Nhắm mắt mà chạy: điều khiển vòng hở

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.2") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 2](https://porabook.com/book/open-loop-control/)

## Tóm tắt video

Nhắm mắt đi một hình vuông, bạn có về đúng chỗ cũ không? 🙈🤖 Robot cũng vậy! Bạn từng thử chưa? 👇

Tập 1.2 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Điều khiển vòng hở: tính sẵn lệnh rồi chạy, không nhìn lại. Mô phỏng hoàn hảo lệch 0 cm, nhưng bánh nhỏ hơn 2% và quay hụt 3% là lệch 24 → 46 → 67 cm sau 3 vòng. Thêm: tối ưu quỹ đạo và lệnh tốc độ hình thang.

## Chạy thử

```bash
cd tap12/sim
python -X utf8 vong_ho.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/vong_ho.py` | Tập 1.2 - Nhắm mắt mà chạy: điều khiển vòng hở (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/vong_ho.py`**

```text
Tập 1.2 - Nhắm mắt mà chạy: điều khiển vòng hở (series Tự Học Robot Tự Hành)

Chương 2, Principles of Robot Autonomy: open-loop control & trajectory optimization.
  1. Tính sẵn chuỗi lệnh cho hình vuông 1 m, chạy mà không nhìn lại.
  2. Mô phỏng hoàn hảo -> về đúng chỗ cũ. Có sai số nhỏ -> lệch dần qua từng vòng.
  3. Tối ưu quỹ đạo: lệnh tốc độ nhanh nhất khi động cơ có giới hạn gia tốc = hình thang.
Chạy: python vong_ho.py
```

---
[← Về danh sách tập](../README.md)
