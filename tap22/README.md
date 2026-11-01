# Tập 2.2 · Camera thực ra là cái hộp có lỗ

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.2") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 6](https://porabook.com/book/camera-models/)

## Tóm tắt video

Mọi camera đều bắt đầu từ một cái hộp có lỗ 📦📷 Và một bức ảnh luôn đánh mất độ sâu. Bạn từng tự làm camera lỗ kim chưa? 👇

Tập 2.2 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Camera lỗ kim: ảnh lộn ngược, lỗ nhỏ thì nét mà tối, lỗ to sáng ×256 mà mờ → cần thấu kính. Chiếu x = f·X/Z: hộp 30 cm ở 1 m cao 150 px, ở 4 m chỉ 37,5 px. Hộp 30 cm ở 1 m và 60 cm ở 2 m trông y hệt nhau. Ma trận K, p = K[R t]P với 11 bậc tự do. (Camera giả định 640×480, α = 500 px.)

## Chạy thử

```bash
cd tap22/sim
python -X utf8 pinhole.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/pinhole.py` | Tập 2.2 - Camera là cái hộp có lỗ (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/pinhole.py`**

```text
Tập 2.2 - Camera là cái hộp có lỗ (series Tự Học Robot Tự Hành)

Theo Chương 6, Principles of Robot Autonomy:
  - Eq. 6.1: x = f·X/Z, y = f·Y/Z
  - Eq. 6.7 / 6.11: u = α·X/Z + u0, v = β·Y/Z + v0, K = [[α, γ, u0], [0, β, v0], [0, 0, 1]]
  - Eq. 6.17: p^h = K [R t] P_W^h  (11 bậc tự do: 5 nội + 3 quay + 3 tịnh tiến)
Thông số camera dưới đây là GIẢ ĐỊNH (camera 640×480 điển hình), con số in ra là kết quả tính thật.
Chạy: python pinhole.py
```

---
[← Về danh sách tập](../README.md)
