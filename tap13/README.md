# Tập 1.3 · PID: thuật toán quan trọng nhất

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.3") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 3](https://porabook.com/book/closed-loop-control/)

## Tóm tắt video

PID: 3 chữ cái giúp robot tự sửa sai 🤖🎯 P lắc lư, PD còn lệch, PID bám đúng vạch. Comment "PID" để lấy code 👇

Tập 1.3 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Robot xuất phát lệch 30 cm, bánh yếu một bên. Chỉ P: lắc ±40 cm. Thêm D: hết lắc, còn lệch 10 cm. Thêm I: lệch 0 cm. Kp = 1,5 · Ki = 0,6 · Kd = 2,8, tất cả từ mô phỏng Python thật.

## Chạy thử

```bash
cd tap13/sim
python -X utf8 pid.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/pid.py` | Tập 1.3 - PID: robot tự sửa sai (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/pid.py`**

```text
Tập 1.3 - PID: robot tự sửa sai (series Tự Học Robot Tự Hành)

Chương 3, Principles of Robot Autonomy: closed-loop control.
Bài toán: robot chạy theo vạch thẳng y = 0, xuất phát lệch 0.3 m,
bánh xe yếu một bên (luôn bị kéo lệch). Bộ điều khiển chọn ω từ sai số
e = r - y (mục tiêu trừ giá trị đo, đúng ký hiệu Eq. 3.3 của giáo trình, ở đây r = 0):

    ω = Kp·e + Ki·∫e dt + Kd·de/dt

So sánh: vòng hở, chỉ P, PD, PID.
Chạy: python pid.py
```

---
[← Về danh sách tập](../README.md)
