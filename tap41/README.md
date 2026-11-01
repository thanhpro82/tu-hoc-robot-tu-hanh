# Tập 4.1 · Bộ não hành vi: máy trạng thái

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.1") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 16](https://porabook.com/book/finite-state-machines/)

## Tóm tắt video

Robot thấy mèo thì đuổi, mất dấu thì đi tìm, pin yếu thì tự về sạc. Bộ não chỉ là một bảng 30 ô 🧠🐱 Bạn sẽ thêm trạng thái gì? 👇

Tập 4.1 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Máy trạng thái hữu hạn M = (S, I, O, n, s₀), kiểu Mealy: mỗi nhịp 0,1 s, s(t+1) = n(s(t), i(t)) và lệnh o(t) = o(s(t), i(t)). Bản chỉ có tuần tra ⇄ đuổi: mèo khuất sau tủ là bỏ, 27,3 s sau mới gặp lại. Thêm trạng thái TÌM: thời gian thấy mèo 36,0% → 71,6% (30 lần chạy). Không biết về sạc: 30/30 lần hết pin giữa nhà; thêm VỀ SẠC khi pin < 25%: 0/30. FSM phân cấp gom 3 trạng thái làm việc: 9 → 7 mũi tên. Nhưng ghép thêm cửa và đèn, bảng phình 30 → 1920 ô, và FSM không biết lựa chọn nào tốt hơn → tập sau: MDP. Số liệu từ mô phỏng Python.

## Chạy thử

```bash
cd tap41/sim
python -X utf8 fsm.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/fsm.py` | Tập 4.1 - Bộ não hành vi: máy trạng thái hữu hạn (Chương 16, Principles of Robot Autonomy). |

## Giải thích trong code

**`sim/fsm.py`**

```text
Tập 4.1 - Bộ não hành vi: máy trạng thái hữu hạn (Chương 16, Principles of Robot Autonomy).

FSM theo §16.1: M = (S, I, O, n, s0), kiểu Mealy (quy ước của sách):
    s_{t+1} = n(s_t, i_t),   o_t = o(s_t, i_t),   t = 0, 1, 2, ... (mỗi nhịp 0,1 s)
Robot tuần tra trong phòng 8 × 6 m, có con mèo chạy lung tung (trốn sau tủ, chạy khi robot tới gần).
Ba phiên bản bộ não:
    A: TUẦN TRA ⇄ ĐUỔI (mất dấu là quay lại tuần tra ngay)
    B: A + TÌM (tới chỗ thấy mèo lần cuối, xoay nhìn quanh; mất dấu quá 8 s mới bỏ)
    C: B + VỀ SẠC + SẠC (pin < 25% thì về đốc)
Đầu vào i_t do khối "sinh sự kiện" tạo từ cảm biến, mỗi nhịp đúng 1 đầu vào theo thứ tự ưu tiên (FSM tất định).
Mọi thứ khác (thế giới, mèo, camera, pin, A*) là giả định của mô phỏng, không có trong sách.
```

---
[← Về danh sách tập](../README.md)
