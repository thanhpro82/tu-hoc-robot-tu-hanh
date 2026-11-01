# Tập 4.6 · Học bắt chước: robot học từ người lái

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.6") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 19](https://porabook.com/book/imitation-learning/)

## Tóm tắt video

Lái mẫu cho robot xem là chưa đủ: học từ 2 vòng mẫu, nó chỉ chạy hết vòng 55,6% 🏎️💥 Cách sửa: DAgger ✅ Bạn muốn robot bắt chước gì? 👇

Tập 4.6 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Người lái mẫu là bộ điều khiển bám đường (99,4% chạy hết vòng), robot chỉ có 9 tia LiDAR. Nhân bản hành vi (behavior cloning): ghi lại cảm biến + lệnh rẽ của chuyên gia rồi dạy mạng nơ-ron đoán lệnh, như học có giám sát. Kết quả: 2 vòng mẫu → 55,6%, 14 vòng mẫu → 87,0%. Vì sao? Chuyên gia chỉ lệch quá 20 cm 0,4% thời gian, nên robot chưa từng thấy cảnh sát mép: lệch chút là đoán sai, rồi lệch thêm (sai số lệnh rẽ 0,038 → 0,091 rad/s trên đường tự đi). DAgger: robot tự lái, chuyên gia nói lệnh đúng ở mọi chỗ robot đi qua, gộp dữ liệu rồi học lại → 2 vòng mẫu + 6 đợt tự lái đạt 97,0% với 2.513 mẫu, ít hơn 2.750 mẫu của 14 vòng. Số liệu: trung bình 4 lần học, thử trên 500 đường đua mới, mô phỏng Python + PyTorch.

## Chạy thử

`python -X utf8 sim/duongdua.py` (chuyên gia trên đường đua) · `python -X utf8 sim/thi_nghiem2.py <seed>` (BC vs DAgger, ra `tn2_<seed>.json`) · `python -X utf8 sim/do_lech.py` (lệch phân phối). Có sẵn các mạng đã học `dd_*.pt`.

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/batchuoc.py` | Tập 4.6 - Học bắt chước: robot học từ người lái (Chương 19, Principles of Robot Autonomy). |
| `sim/do_lech.py` | Đo phân bố độ lệch tâm của các trạng thái đã đi qua: chuyên gia vs BC 2 vòng vs DAgger (100 đường, 4 seed). |
| `sim/duongdua.py` | Tập 4.6 - Học bắt chước trên đường đua (Chương 19, Principles of Robot Autonomy). |
| `sim/thi_nghiem.py` | Thí nghiệm chính: chuyên gia, BC theo số lượt lái mẫu, DAgger 10 vòng × 20 lượt; 3 seed. Lưu thi_nghiem.json + mô hình. |
| `sim/thi_nghiem2.py` | Thí nghiệm chính trên đường đua: BC theo số vòng lái mẫu vs DAgger (2 vòng mẫu + 6 vòng × 2 lượt tự lái). Lưu tn2_<seed>.json + mô hình. |

## Giải thích trong code

**`sim/duongdua.py`**

```text
Tập 4.6 - Học bắt chước trên đường đua (Chương 19, Principles of Robot Autonomy).

Bối cảnh (giả định): mỗi lượt một đường đua khép kín ngẫu nhiên, rộng 0,8 m, robot unicycle v = 1 m/s, Δt = 0,1 s, ω liên tục |ω| ≤ 3 rad/s.
Quan sát của robot: 9 tia LiDAR (−90°..90°, tầm 3 m) tới hai mép đường — không biết bản đồ, không biết vị trí.
Chuyên gia π* ("người lái", giả định): pure pursuit bám đường tâm, nhìn trước 1,17 m — biết vị trí thật.
Người học π_θ: mạng 9-64-64-1, hồi quy ω, loss bình phương sai số (MSE, một loss sách liệt kê).
- Behavior cloning (§19.2, Algorithm 1): 𝒟 = {(x_i, u_i)} từ các vòng chuyên gia tự lái.
- DAgger (§19.2.1, Algorithm 3): π_θi tự lái, chuyên gia gán ω đúng cho mọi trạng thái robot đi qua, 𝒟 ← 𝒟 ∪ 𝒟_i, học lại.
```

---
[← Về danh sách tập](../README.md)
