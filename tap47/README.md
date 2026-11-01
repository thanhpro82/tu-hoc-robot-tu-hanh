# Tập 4.7 · Tương lai: Physical AI & robot nền tảng

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.7") · 📚 Giáo trình: Principles of Robot Autonomy, [Prospects](https://porabook.com/book/prospects/)

## Tóm tắt video

Tương lai robot là gì? Mình cho robot "tưởng tượng trước" 25 cách rẽ và nó chạy hết vòng 93,7% 🤖🔮 Bạn mong robot làm gì cho mình? 👇

Tập 4.7 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Cả giáo trình là vòng lặp Thấy – Nghĩ – Làm, mỗi khâu một khối do kỹ sư thiết kế. Xu hướng mới: gộp lại thành mô hình nền tảng học từ dữ liệu khổng lồ, ví dụ mô hình VLA (RT-2, π0, OpenVLA) nhìn camera + nghe lệnh bằng lời rồi xuất thẳng lệnh cho tay máy.

Thử nghiệm 1, mô hình thế giới thu nhỏ: robot chỉ lái lung tung (không ai chỉ lệnh), mạng nơ-ron học đoán 9 tia LiDAR bước sau. Mỗi bước robot tưởng tượng 25 cách rẽ trong 0,8 s rồi chọn cách an toàn nhất: 175 bước dữ liệu → 60,5%, 457 → 88,1%, 1.882 → 93,7% chạy hết vòng (lái lung tung: 0%). Tưởng tượng càng xa càng sai: 6,8 cm sau 0,1 s, 49,2 cm sau 0,8 s.

Thử nghiệm 2, lớp an toàn cổ điển: luật "sát mép dưới 17 cm thì ép rẽ ra" bọc quanh mạng của tập 4.6: BC 2 vòng 55,6% → 82,6% (chỉ sửa lệnh 4% thời gian), DAgger 97,0% → 99,1%. Luật một mình chỉ được 6%.

Số liệu: trung bình 4 lần học, thử trên 500 đường đua mới, mô phỏng Python + PyTorch. Hai thử nghiệm là phần mở rộng của mình, không có trong sách.

## Chạy thử

`python -X utf8 sim/an_toan.py` (lớp an toàn) · `python -X utf8 sim/the_gioi.py 20 50 200` (mô hình thế giới) · `python -X utf8 sim/doi_chung.py`. Cần các mạng của tập 4.6 trong `tap46/sim/`.

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/an_toan.py` | Tập 4.7 - Lớp an toàn cổ điển bọc quanh chính sách học máy (phần Prospects: "Physical AI Safety"). |
| `sim/doi_chung.py` | Đối chứng cho the_gioi.py: (1) lái ngẫu nhiên y như lúc thu dữ liệu, (2) cùng cách tưởng tượng nhưng mô hình thế giới |
| `sim/the_gioi.py` | Tập 4.7 - Mô hình thế giới thu nhỏ: robot "tưởng tượng" trước khi lái (phần Prospects: "World models"). |

## Giải thích trong code

**`sim/the_gioi.py`**

```text
Tập 4.7 - Mô hình thế giới thu nhỏ: robot "tưởng tượng" trước khi lái (phần Prospects: "World models").

Sách nêu: mô hình thế giới học cách thế giới thay đổi theo thời gian từ dữ liệu cảm biến, để robot dự đoán /
tưởng tượng các tương lai rồi lập kế hoạch trên đó; dữ liệu tương tác của robot đắt, nên mô hình nên học từ dữ liệu rẻ.
Phiên bản thu nhỏ ở đây (mở rộng, giả định):
- Dữ liệu: robot lái NGẪU NHIÊN (không có chuyên gia, không có nhãn lệnh đúng) trên các đường đua của tập 4.6,
  ghi lại (9 tia LiDAR o_t, lệnh rẽ ω_t, 9 tia o_{t+1}).
- Mô hình thế giới f_ψ: mạng 10-128-128-9, học Δo = o_{t+1} − o_t (MSE).
- Lái bằng tưởng tượng: mỗi bước thử 25 lệnh ω (giữ nguyên 0,8 s), dùng f_ψ "mơ" ra 8 bước tia LiDAR tương lai,
  chấm điểm (xa mép, giữa đường), chọn lệnh tốt nhất, chỉ thực hiện bước đầu rồi lặp lại (kiểu MPC).
```

**`sim/an_toan.py`**

```text
Tập 4.7 - Lớp an toàn cổ điển bọc quanh chính sách học máy (phần Prospects: "Physical AI Safety").

Sách nêu: mô hình học từ dữ liệu có thể đoán sai khi ra ngoài phân phối huấn luyện; hướng đi là kết hợp học máy
với đảm bảo an toàn kiểu lý thuyết điều khiển (ví dụ control barrier function). Ở đây (mở rộng, giả định) là một
luật an toàn đơn giản chỉ dùng 9 tia LiDAR — KHÔNG phải CBF đầy đủ:
    khoảng hở bên trái  c_L = min_{tia trái}  d_i · sin(a_i),   bên phải c_R tương tự
    nếu c_L < m:  ω ← min(ω, −k (m − c_L))      (bị ép rẽ phải, tránh mép trái)
    nếu c_R < m:  ω ← max(ω, +k (m − c_R))      (bị ép rẽ trái)
Ngoài vùng sát mép, lệnh của mạng nơ-ron giữ nguyên.
Dùng lại đường đua + các mạng đã học ở tập 4.6 (tap46/sim/duongdua.py, dd_bc*_s.pt, dd_dagger_s.pt).
```

---
[← Về danh sách tập](../README.md)
