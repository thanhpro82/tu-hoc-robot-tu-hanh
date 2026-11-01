# Tập 2.9 · Tổng kết Mùa 2: robot đi theo bạn

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.9") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 5–10](https://porabook.com/book/)

## Tóm tắt video

Ghép hết Mùa 2: robot nhìn bằng camera và đi theo bạn như thú cưng 🐶🤖 Mùa 2 bạn thích tập nào nhất? 👇

Tập 2.9 | 🏁 TỔNG KẾT MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Mỗi 0,1 giây: chụp ảnh (camera lỗ kim, tập 2.2) → bộ dò kiểu YOLO tìm người (tập 2.8, thấy ở 96% khung hình) → đo khoảng cách z = f·H/h (sai trung bình 26,3 cm) → bộ PI của Mùa 1 lái robot giữ cách 2 m. Quả bóng lăn ngang: robot dừng 3,9 giây, cách bóng 1,38 m. Mất dấu người 1 giây, quay tìm lại, đuổi kịp và dừng cách 1,85 m khi người đứng lại. (Mô phỏng Python, dùng lại mạng đã huấn luyện ở tập 2.8.)

## Chạy thử

```bash
cd tap29/sim
python -X utf8 di_theo.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/di_theo.py` | Tập 2.9 - Tổng kết Mùa 2: robot đi theo bạn (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/di_theo.py`**

```text
Tập 2.9 - Tổng kết Mùa 2: robot đi theo bạn (series Tự Học Robot Tự Hành)

Ghép các tập đã làm thành một vòng lặp chạy thật, mỗi bước 0,1 s:
  1. Camera lỗ kim (tập 2.2, Eq. 6.1): vẽ ảnh 128×128 robot nhìn thấy, u = f·X/Z + u0, chiều cao ảnh h = f·H/Z
  2. Bộ dò kiểu YOLO đã huấn luyện ở tập 2.8 (Ch. 10) tìm "người" và "bóng" trong ảnh (dùng lại trọng số, không học lại)
  3. Đo từ khung: khoảng cách Z ≈ f·H / h (người cao H = 1,7 m), hướng = atan((u − u0)/f)
  4. Điều khiển (Mùa 1): robot kiểu unicycle (tập 1.1), sai số e = r − y với r = 2 m (tập 1.3),
     v = Kp·e + Ki·∫e (PI), ω = Kθ·hướng; thấy bóng gần phía trước thì dừng (vật cản)
Mở rộng / giả định: người đi theo lộ trình định sẵn, quả bóng lăn ngang, các hệ số điều khiển, camera f = 60 px,
chiều cao camera 0,5 m; cách suy khoảng cách từ chiều cao khung khi biết chiều cao thật là áp dụng Eq. 6.1.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 di_theo.py
```

---
[← Về danh sách tập](../README.md)
