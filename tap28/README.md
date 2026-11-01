# Tập 2.8 · YOLO: robot nhận ra người và đồ vật

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.8") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 10](https://porabook.com/book/object-detection/)

## Tóm tắt video

Robot phải biết đó là người, cái hộp hay quả bóng, và nó ở đâu 🧍📦⚽ Bạn muốn robot nhận ra thêm gì? 👇

Tập 2.8 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Phát hiện vật thể = mỗi vật một khung, một tên lớp, một độ tin cậy. Bộ dò kiểu YOLO tự huấn luyện: lưới 8×8, mỗi ô 2 khung × 5 số + 3 lớp → 8×8×13 = 832 con số trong một lần chạy. Ảnh mẫu có 14 khung thô cho 5 vật; NMS bỏ khung chồng IoU > 0,5 → còn 5. Trên 500 ảnh thử: mAP 92,1% (bỏ NMS: 84,4%). Bóng nhỏ khó nhất (86,7%). Tốc độ 322 ảnh/giây chỉ với CPU. (Cảnh tự tạo, huấn luyện thật bằng PyTorch.)

## Chạy thử

`python -X utf8 sim/yolo.py` (dùng `trong_so.pt` đã học sẵn và tạo lại đúng bộ 500 ảnh thử như trong video; xoá `trong_so.pt` nếu muốn tự huấn luyện lại từ đầu, mất vài phút với GPU).

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/yolo.py` | Tập 2.8 - YOLO: robot nhận ra người và đồ vật (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/yolo.py`**

```text
Tập 2.8 - YOLO: robot nhận ra người và đồ vật (series Tự Học Robot Tự Hành)

Theo Chương 10, Principles of Robot Autonomy:
  - Định nghĩa 10.1: phát hiện = tập {(b_i, c_i, s_i)}: khung b = (x, y, w, h), lớp c, độ tin cậy s
  - §10.1.3 YOLO: lưới S×S, ô chứa tâm vật chịu trách nhiệm; mỗi ô B khung (x, y, w, h, confidence) + C xác suất lớp
    -> đầu ra S×S×(B·5 + C); hàm mất mát có λ_coord = 5, λ_noobj = 0,5, căn bậc hai của w, h;
    độ tin cậy lớp = P(lớp | vật) × P(vật) × IoU
  - IoU = phần giao / phần hợp; NMS: xếp theo điểm, bỏ khung chồng IoU cao lên khung điểm cao hơn; mAP
Mở rộng (ngoài sách): S = 8 (sách: 7), ảnh 128×128, ngưỡng NMS 0,5 (sách nêu ~0,7 cho RPN), cách tính AP
bằng diện tích dưới đường precision-recall, đo tốc độ trên máy này.
Cảnh, vật và nhãn là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả huấn luyện và đo thật.
Chạy: python -X utf8 yolo.py
```

---
[← Về danh sách tập](../README.md)
