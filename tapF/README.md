# Tập F · Robot tự hành hoàn chỉnh: nhiệm vụ giao đồ trong nhà

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập F") · 📚 Giáo trình: Principles of Robot Autonomy, Ch. 3–16

## Tóm tắt video

Tập cuối: ghép cả 4 mùa vào một robot giao đồ trong căn hộ. 100 lượt thử, giao tận tay 89 lượt 🤖📦 Bỏ đi một mùa thì sao? 👇

TẬP CUỐI | Series TỰ HỌC ROBOT TỰ HÀNH

Nhiệm vụ: "lấy đồ ở bếp, mang cho người ở phòng ngủ / phòng làm việc".

🧠 Mùa 4: máy trạng thái điều khiển cả nhiệm vụ: định vị → đi lấy → nhận đồ → đi giao → tìm người → tiếp cận → giao (có trạng thái DỪNG khi có người chắn, và định vị lại khi mất dấu).

📍 Mùa 3: robot thức dậy không biết mình ở đâu, bộ lọc hạt (4.000 hạt) tìm ra vị trí trên bản đồ căn hộ; theo dõi người đi lại, đoán trước họ đi đâu để dừng nhường.

🧭 Mùa 1: A* tìm đường đi giữa các cửa, PID (e = r − y) bám đường.

👀 Mùa 2: camera + YOLO đã học ở tập 2.8 nhận ra người nhận, LiDAR đo khoảng cách theo đúng hướng đó.

Kết quả 100 lượt ngẫu nhiên (chỗ xuất phát, phòng giao, chỗ người đứng, bánh xe trượt đều ngẫu nhiên): giao thành công 89/100, trung bình 84,6 s mỗi lượt. Bỏ một mùa: không A* 0%, không camera 4%, không định vị 7%, bộ não đơn giản 9%.

Mô phỏng Python + PyTorch, mọi con số là kết quả chạy thật. Cảm ơn bạn đã học cùng mình suốt 4 mùa! Series tiếp theo: AI Engineering hay AWS?

## Chạy thử

`python -X utf8 sim/giao_do.py 100` (100 lượt × 5 phiên bản, chạy song song, khá lâu) hoặc `python -X utf8 sim/giao_do.py 10 du` (10 lượt bản đủ 4 mùa). Cần `tap28/sim/trong_so.pt` (YOLO của tập 2.8).

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/giao_do.py` | Tập cuối F - Robot giao đồ trong nhà: ghép cả 4 mùa (series Tự Học Robot Tự Hành). |
| `sim/thu_dinh_vi.py` | Thử riêng giai đoạn ĐỊNH VỊ (định vị toàn cục) trên nhiều điểm xuất phát: sai số lúc chốt vị trí. |
| `sim/yolo_nap.py` | Nạp nhanh mạng YOLO đã học ở tập 2.8 (tap28/sim/ket_qua.pt hoặc trong_so.pt) để dùng lại, KHÔNG học lại và không chạy phần đánh giá. |

## Giải thích trong code

**`sim/giao_do.py`**

```text
Tập cuối F - Robot giao đồ trong nhà: ghép cả 4 mùa (series Tự Học Robot Tự Hành).

Nhiệm vụ: "lấy đồ ở bếp, giao tận tay người ở phòng ngủ / phòng làm việc". Mỗi bước 0,1 s, mọi khối là code của các tập trước:
  Mùa 4 · Bộ não (Ch. 16, tập 4.1): máy trạng thái M = (S, I, O, n, s0), s_{t+1} = n(s_t, i_t).
      CHỜ LỆNH → ĐỊNH VỊ → ĐI LẤY → NHẬN ĐỒ → ĐI GIAO → TÌM NGƯỜI → TIẾP CẬN → GIAO → XONG;
      DỪNG (có vật lạ phía trước) quay lại đúng trạng thái trước đó khi đường trống (nhớ trạng thái trước: mở rộng).
  Mùa 3 · Định vị (Ch. 13, tập 3.5): Monte Carlo Localization trên bản đồ căn hộ của tập 3.5; robot thức dậy KHÔNG biết
      mình ở đâu (định vị toàn cục), hạt trong tường có xác suất 0 (Eq. 13.2), trọng số = tích từng tia (Eq. 13.3),
      thả 3% hạt ngẫu nhiên mỗi lần (ghi chú lề §13.6).
  Mùa 1 · Tìm đường + điều khiển (Ch. 4 tập 1.5, Ch. 3 tập 1.3): A* trên lưới 10 cm đã nới vật cản 0,25 m;
      bám đường bằng PD trên góc hướng, e = r − y với r = hướng tới điểm nhìn trước 0,5 m, y = hướng ước lượng.
  Mùa 2 · Thị giác (Ch. 6 + Ch. 10, tập 2.2/2.8/2.9): camera lỗ kim f = 60 px, mạng YOLO đã học ở tập 2.8 (không học lại)
      tìm "người"; khoảng cách Z = f·H/h, hướng = atan((u − u0)/f).
Mở rộng / giả định: căn hộ 12 × 8 m của tập 3.5; robot tròn bán kính 0,15 m, v ≤ 0,5 m/s; bánh xe trượt (sai số tỉ lệ
v ~ N(0, 3%), ω ~ N(0, 5%), trôi góc ~ N(0, 0,01 rad/s) mỗi lượt + nhiễu từng bước); LiDAR 36 tia tầm 6 m nhiễu 3 cm
(bộ lọc hạt dùng 12 tia); một người đi qua lại trong bếp (0,5 m/s); người nhận đứng ở chỗ ngẫu nhiên trong phòng;
ảnh camera chỉ vẽ người (kiểu vẽ của tập 2.8/2.9), có kiểm tra bị tường che. Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 giao_do.py [số lượt]
```

---
[← Về danh sách tập](../README.md)
