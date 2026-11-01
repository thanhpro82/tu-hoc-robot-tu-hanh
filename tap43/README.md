# Tập 4.3 · Quy hoạch động: nhìn trước mọi nước đi

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.3") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 17](https://porabook.com/book/decision-making/)

## Tóm tắt video

Có hơn một tỷ tỷ chuỗi lệnh robot có thể chọn, quy hoạch động chỉ cần 4.800 phép tính để tìm cách đi tốt nhất 🧠 Robot của bạn có dám liều? 👇

Tập 4.3 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Nguyên lý tối ưu: nếu cả chặng là tốt nhất thì đoạn còn lại cũng tốt nhất → tính ngược từ cuối. Phương trình Bellman: J*_t(x) = min_u E[ g_t + J*_{t+1}(x') ]. Trên kho lưới sàn trơn của tập trước: 40 ô × 4 lệnh × 30 bước = 4.800 phép tính, ô xuất phát J* = 16,24 (đường vòng tự nghĩ 16,48). Chạy thử 10.000 lần: tới đích 99,24%. Bất ngờ: khi chỉ còn 15 bước, robot chọn đường tắt vì đi vòng dễ trễ giờ. Giới hạn: phải biết trước xác suất trượt và số ô tăng theo lũy thừa → tập sau: học tăng cường. Số liệu từ mô phỏng Python.

## Chạy thử

```bash
cd tap43/sim
python -X utf8 qhd.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/qhd.py` | Tập 4.3 - Quy hoạch động: nhìn trước mọi nước đi (Chương 17, Principles of Robot Autonomy). |

## Giải thích trong code

**`sim/qhd.py`**

```text
Tập 4.3 - Quy hoạch động: nhìn trước mọi nước đi (Chương 17, Principles of Robot Autonomy).

Dùng lại kho lưới của tập 4.2 (tap42/sim/mdp.py): 9 × 5, cầu thang, kệ, sàn trơn ε = 0,2, T = 30, g_t = 1, g_T = 100·(1 − 1[x = G]).
Quy hoạch động lùi (Algorithm 2, §17.2.2):
    J*_T(x) = g_T(x)
    J*_t(x) = min_u E_w[ g_t(x, u, w) + J*_{t+1}(f(x, u, w)) ],   t = T−1, ..., 0      (Eq. 17.13)
    π*_t(x) = argmin_u E_w[ ... ]                                                   (Eq. 17.14)
```

---
[← Về danh sách tập](../README.md)
