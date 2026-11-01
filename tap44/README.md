# Tập 4.4 · Học tăng cường: robot học từ thất bại

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.4") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 18](https://porabook.com/book/reinforcement-learning/)

## Tóm tắt video

Lần 1 robot rơi cầu thang sau 16 bước. Lần 2000 nó tự tìm ra đường an toàn, không ai chỉ 🤖📉➡️📈 Bạn muốn robot tự học gì? 👇

Tập 4.4 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Học tăng cường không cần biết trước xác suất trượt: robot chỉ đi thử và nhận điểm (mỗi bước −1, rơi cầu thang −100). Robot ghi nhớ bảng Q và sau mỗi bước cập nhật Q(x,u) ← Q(x,u) + α[r + γ·max Q(x',u') − Q(x,u)] với α = 0,2. Phải dám thử bừa 10% số bước (ε-greedy): không thử bừa thì chi phí TB 21,89, có thử bừa 17,43. 50 tập đầu rơi 52%; sau khoảng 500 tập chi phí đã dưới 20. Sau 2000 tập chính sách học được tốn 16,95, sát mức tối ưu 16,24 của quy hoạch động, thử 10.000 lần tới đích 98,89%. Số liệu từ mô phỏng Python.

## Chạy thử

```bash
cd tap44/sim
python -X utf8 qlearn.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/qlearn.py` | Tập 4.4 - Học tăng cường: robot học từ thất bại (Chương 18, Principles of Robot Autonomy). |

## Giải thích trong code

**`sim/qlearn.py`**

```text
Tập 4.4 - Học tăng cường: robot học từ thất bại (Chương 18, Principles of Robot Autonomy).

Q-learning (Eq. 18.18, Algorithm 5):  Q(x, u) ← Q(x, u) + α ( r + γ max_u' Q(x', u') − Q(x, u) )
Hành vi ε-greedy: xác suất 1 − ε chọn argmax_u Q(x, u), xác suất ε chọn ngẫu nhiên.
Chương 18 dùng PHẦN THƯỞNG (tối đa hoá), khác Chương 17 dùng chi phí.

Môi trường = kho lưới tập 4.2 (tap42/sim/mdp.py), robot KHÔNG biết xác suất trượt, chỉ tự đi thử:
    mỗi bước r = −1; tới G: kết thúc; rơi cầu thang: r = −100, kết thúc; quá T_TAP = 100 bước thì dừng tập (cắt, không phạt).
Sàn trơn 20% (xác suất đi hướng ngẫu nhiên, ở 4.2 gọi là ε; ở đây đổi tên TRUOT để khỏi trùng ε của ε-greedy).
Đánh giá: lấy chính sách tham lam π(x) = argmax_u Q(x, u), tính chi phí kỳ vọng J_π bằng mô hình thật (như 4.2)
để so với J* = 16,24 của quy hoạch động (tập 4.3).
```

---
[← Về danh sách tập](../README.md)
