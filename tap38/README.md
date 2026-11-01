# Tập 3.8 · Kết hợp cảm biến & theo dõi vật thể

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.8") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 15](https://porabook.com/book/sensor-fusion/)

## Tóm tắt video

Hai người lướt qua nhau, robot có nhận nhầm ai là ai không? 👀🤖 Đoán thử trước khi xem nhé 👇

Tập 3.8 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Camera đoán hướng chuẩn nhưng đoán xa gần dở, radar thì ngược lại. Ghép hai cảm biến theo Bayes: sai số từ 0,83 m và 0,75 m còn 0,17 m. Theo dõi 5 người: mỗi người một track (Kalman, vận tốc không đổi), cổng Mahalanobis² < 9,21 loại báo động giả, thuật toán Hungary phân công ai ghép với ai. Ghép theo điểm gần nhất: tráo ID 3 lần khi hai người lướt qua nhau, MOTA 76,4%. Có dự đoán + phân công + luật xác nhận 3/4 khung: không tráo lần nào, MOTA 95,6%. Số liệu từ mô phỏng Python.

## Chạy thử

```bash
cd tap38/sim
python -X utf8 theo_doi.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/theo_doi.py` | Tập 3.8 - Kết hợp cảm biến & theo dõi nhiều người (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/theo_doi.py`**

```text
Tập 3.8 - Kết hợp cảm biến & theo dõi nhiều người (series Tự Học Robot Tự Hành)

Theo Chương 15, Principles of Robot Autonomy:
  - Ví dụ 15.0.1: radar đo khoảng cách tốt, camera đo hướng tốt -> bổ sung cho nhau (complementary)
  - Ví dụ 15.2.1 / §15.2.1: ghép theo Bayes, phương sai sau ghép nhỏ hơn cả hai; dạng thông tin Y = Σ⁻¹ cộng dồn
  - §15.5.1: mô hình vận tốc không đổi (CV), x = [x, y, ẋ, ẏ], F(Δt), Q(q, Δt) gia tốc trắng
  - §15.5.2: cổng Mahalanobis m² = z̃ᵀ S⁻¹ z̃ ≤ χ²_{2;0,99} ≈ 9,21
  - §15.5.3 Thuật toán 2: GNN, ma trận chi phí C_ij = m²_ij, giải bằng thuật toán Hungary; không khớp -> tăng bất định
  - §15.5.4: khởi tạo M/N, giữ track khi bị che tối đa N_miss khung, xoá track hỏng
  - §15.5.7: MOTA = 1 − (FN + FP + IDSW) / GT
Mở rộng / giả định: 5 người với lộ trình định sẵn (2 người đi cắt qua nhau như Ví dụ 15.5.2), camera σ_r = 0,8 m σ_θ = 1°,
radar σ_r = 0,1 m σ_θ = 6°, mỗi cảm biến thấy mỗi người với xác suất 0,9, trung bình 1 báo động giả mỗi khung, coi như đã
biết phát hiện camera và radar nào cùng là một người; M/N = 2/3, N_miss = 5; ngưỡng so khớp khi chấm điểm 0,7 m;
cách so sánh "ghép theo điểm gần nhất, không dự đoán"; chi phí m² + ln|S|; không khởi tạo track từ phát hiện đã nằm trong cổng;
gộp track trùng khi cách nhau < 0,25 m. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 theo_doi.py
```

---
[← Về danh sách tập](../README.md)
