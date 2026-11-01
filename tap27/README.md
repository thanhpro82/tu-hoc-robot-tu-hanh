# Tập 2.7 · Deep learning nhìn thế giới thế nào

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.7") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 9](https://porabook.com/book/deep-learning-perception/)

## Tóm tắt video

Không ai dạy, máy tự học cách nhìn vạch dẫn đường 🧠👀 Bạn muốn tự train một mạng CNN không? 👇

Tập 2.7 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Mạng tích chập (CNN) học từ 1.500 ảnh 32×32: đi thẳng, rẽ trái, rẽ phải hay dừng. 8 bộ lọc 5×5 tự học, bản đồ kích hoạt sáng lên ở mép vạch. ReLU + max pooling 2×2 thu nhỏ dần. Từ 24,4% (đoán bừa) lên 98,2% sau 12 vòng học. Nhờ dùng chung bộ lọc: CNN chỉ 36.356 tham số, mạng nối đầy đủ cần 263.428 mà vẫn kém hơn (96,8%). Vạch dịch xa hơn lúc học: CNN 62,6%, mạng đầy đủ 53,4%. Transformer cắt ảnh thành 16 mảnh nhưng cần nhiều dữ liệu hơn. (Ảnh tự tạo, huấn luyện thật bằng PyTorch.)

## Chạy thử

```bash
cd tap27/sim
python -X utf8 cnn.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/cnn.py` | Tập 2.7 - Deep learning nhìn thế giới thế nào (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/cnn.py`**

```text
Tập 2.7 - Deep learning nhìn thế giới thế nào (series Tự Học Robot Tự Hành)

Theo Chương 9, Principles of Robot Autonomy:
  - §9.1.1 lớp tích chập Y_ij = Σ_u Σ_v X_(i+u, j+v) W_uv + b (Eq. 9.1), nhiều bộ lọc -> nhiều bản đồ kích hoạt, ReLU sau tích chập
  - §9.1.2 max pooling 2×2 bước 2, lớp nối đầy đủ; dùng chung tham số, tương tác thưa, bất biến tịnh tiến
  - Bài tập 1 của chương: SimpleCNN = 2 lớp tích chập (ReLU + max pooling) + 2 lớp nối đầy đủ
  - §9.2.2 ViT: cắt ảnh H×W thành mảnh P×P -> N = HW/P² token
Mở rộng (ngoài sách): bộ dữ liệu ảnh vạch dẫn đường tự tạo, hàm mất mát cross-entropy và tối ưu Adam
(sách không nêu), so sánh với mạng nối đầy đủ, phép thử dịch ảnh.
Ảnh và nhãn là GIẢ ĐỊNH (tạo bằng code); mọi con số in ra là kết quả huấn luyện thật.
Chạy: python -X utf8 cnn.py
```

---
[← Về danh sách tập](../README.md)
