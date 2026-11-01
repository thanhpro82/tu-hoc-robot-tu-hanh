# Tập 4.5 · Deep RL: luyện robot trong mô phỏng

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.5") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 18](https://porabook.com/book/reinforcement-learning/)

## Tóm tắt video

Robot chưa từng được dạy né vật cản, nó tự học trong mô phỏng qua 32.000 lượt thử 🤖💥➡️✅ Bạn sẽ luyện robot làm gì? 👇

Tập 4.5 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Trạng thái giờ là 9 tia LiDAR + hướng tới đích, toàn số thực: chia mỗi số 10 mức thì bảng Q cần 10¹² ô. Nên thay bảng bằng mạng nơ-ron 5.187 tham số, đầu ra là xác suất rẽ trái / đi thẳng / rẽ phải. Huấn luyện bằng REINFORCE: lượt nào điểm cao hơn trung bình thì tăng xác suất các lệnh đã chọn, lượt tệ thì giảm. Lúc đầu đâm vật cản 100%; sau 500 lần cập nhật (64 lượt mỗi lần) tới đích 85,7% trong mô phỏng. Nhưng gặp cảm biến nhiễu, bánh trượt, động cơ trễ: còn 70,5%. Đó là khoảng cách giữa mô phỏng và thực tế. Số liệu từ mô phỏng Python + PyTorch.

## Chạy thử

```bash
cd tap45/sim
python -X utf8 deeprl.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/deeprl.py` | Tập 4.5 - Deep RL: luyện robot trong mô phỏng (Chương 18, Principles of Robot Autonomy). |

## Giải thích trong code

**`sim/deeprl.py`**

```text
Tập 4.5 - Deep RL: luyện robot trong mô phỏng (Chương 18, Principles of Robot Autonomy).

Trạng thái liên tục (LiDAR + hướng đích) → không thể lập bảng Q như tập 4.4 → dùng mạng nơ-ron làm chính sách π_θ(u | x)
(xấp xỉ hàm, §18.5) và huấn luyện bằng gradient chính sách REINFORCE (§18.5.2, Eq. 18.31–18.32, Algorithm 6)
với biến thể "reward-to-go trừ baseline" của bài tập Cart-pole (§18.8, Problem 2):
    ∇_θ V(θ) ≈ (1/N) Σ_i Σ_t ∇_θ log π_θ(u_t^i | x_t^i) · (R_t^i − b),   R_t = Σ_{t'≥t} γ^{t'−t} r_{t'}
Môi trường (giả định): phòng 6 × 6 m, 4–7 vật cản tròn đặt ngẫu nhiên mỗi tập, robot unicycle v = 0,5 m/s,
3 lệnh ω ∈ {−1,5; 0; +1,5} rad/s, Δt = 0,2 s, tối đa 100 bước. Quan sát: 9 tia LiDAR (−90°..90°, tầm 3 m) + hướng và khoảng cách tới đích.
Thưởng (giả định, có "định hình" theo tiến độ — sách không bàn reward shaping): +10 tới đích, −10 va chạm, 2 × (khoảng cách giảm được) mỗi bước, −0,01 mỗi bước.
Sim-to-real (mở rộng, sách không nói): thử chính sách trong điều kiện "thật hơn" (LiDAR nhiễu σ 5 cm + mất 15% tia, bánh trượt ω × [0,6; 1,4],
động cơ trễ 1 nhịp 0,2 s),
so chính sách luyện trong mô phỏng sạch với chính sách luyện có ngẫu nhiên hoá miền (domain randomization).
```

---
[← Về danh sách tập](../README.md)
