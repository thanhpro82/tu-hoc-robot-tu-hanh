# Tập 1.4 · Bám quỹ đạo: robot chạy hình số 8

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.4") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 3](https://porabook.com/book/closed-loop-control/)

## Tóm tắt video

Robot vẽ số 8 gần như hoàn hảo dù bánh xe lệch 🤖♾️ Bí quyết: tính sẵn + sửa sai. Comment nếu muốn xem code 👇

Tập 1.4 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Bám quỹ đạo = đuổi theo một "robot ảo": đúng chỗ, đúng lúc. Phẳng vi phân: từ x(t), y(t) suy ra luôn lệnh tính sẵn. Chỉ tính sẵn (vòng hở) thì lệch 56 cm. Thêm PD trên x và y (như Ví dụ 3.1.2 của giáo trình) thì còn dưới 1 cm. Số liệu từ mô phỏng Python thật.

## Chạy thử

```bash
cd tap14/sim
python -X utf8 bam_quy_dao.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/bam_quy_dao.py` | Tập 1.4 - Bám quỹ đạo: robot vẽ số 8 gần như hoàn hảo (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/bam_quy_dao.py`**

```text
Tập 1.4 - Bám quỹ đạo: robot vẽ số 8 gần như hoàn hảo (series Tự Học Robot Tự Hành)

Theo đúng Ví dụ 3.1.2, Chương 3, Principles of Robot Autonomy:
  - Unicycle mở rộng (dynamic extension): trạng thái (x, y, v, θ), lệnh (a, ω).
  - x, y là "đầu ra phẳng" (differential flatness): v, θ, a, ω đều suy ra được từ x(t), y(t).
  - Điều khiển ảo (Eq. 3.7):  w1 = ẍ_d + kp·(x_d - x) + kd·(ẋ_d - ẋ)   (tương tự w2 cho y)
  - Đổi về lệnh thật:         [a, ω] = J⁻¹(θ, v)·[w1, w2],   J = [[cosθ, -v·sinθ], [sinθ, v·cosθ]]
Phần ẍ_d, ÿ_d là tính sẵn (feedforward), phần kp, kd là sửa sai (feedback).
Chạy: python bam_quy_dao.py
```

---
[← Về danh sách tập](../README.md)
