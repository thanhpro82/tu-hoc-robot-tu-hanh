# Tập 3.1 · "Tôi đang ở đâu?": robot nghĩ bằng xác suất

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.1") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 11](https://porabook.com/book/localization-filtering/)

## Tóm tắt video

Bịt mắt thả vào hành lang lạ, làm sao biết mình đang ở đâu? 🙈🚪 Robot nghĩ bằng xác suất! Bạn từng bị lạc chưa? 👇

Tập 3.1 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Bộ lọc Bayes: robot giữ niềm tin = xác suất ở từng ô (200 ô, lúc đầu mỗi ô 0,5%). Thấy cửa → hiệu chỉnh bel = η·p(z|x)·bel̄ → 3 đỉnh vì có 3 cửa. Đi tới 0,5 m → dự đoán, đỉnh dịch và bè ra. Thấy cửa thứ hai → 62,5% đúng chỗ. Đoạn không cửa → bè ra còn 28,8%. Tới cửa thứ ba → 84,5%, đoán 6,93 m, thật 6,91 m. (Mô phỏng Python.)

## Chạy thử

```bash
cd tap31/sim
python -X utf8 bayes.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/bayes.py` | Tập 3.1 - "Tôi đang ở đâu?": robot nghĩ bằng xác suất (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/bayes.py`**

```text
Tập 3.1 - "Tôi đang ở đâu?": robot nghĩ bằng xác suất (series Tự Học Robot Tự Hành)

Theo Chương 11, Principles of Robot Autonomy:
  - Niềm tin bel(x_t) = p(x_t | z_1:t, u_1:t) (Eq. 11.10), dự đoán bel̄(x_t) = p(x_t | z_1:t-1, u_1:t) (Eq. 11.11)
  - Mô hình chuyển động p(x_t | x_t-1, u_t) (Eq. 11.8), mô hình đo p(z_t | x_t) (Eq. 11.9)
  - Bộ lọc Bayes rời rạc (Thuật toán 2): dự đoán p̄_k = Σ_i p(x_k | x_i, u_t) p_i ; hiệu chỉnh p_k = η p(z_t | x_k) p̄_k
  - Ví dụ 11.3.1: robot trong hành lang 1 chiều, chuyển động Δx ~ N(u_t, 0,1²); cấu trúc lặp lại làm niềm tin nhiều đỉnh
Mở rộng / giả định: cảm biến "thấy cửa" (sách dùng cảm biến khoảng cách), vị trí 3 cửa, xác suất cảm biến
p(thấy cửa | ở cửa) = 0,8 và p(thấy cửa | không ở cửa) = 0,1, chuyển động u = 0,5 m mỗi bước.
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 bayes.py
```

---
[← Về danh sách tập](../README.md)
