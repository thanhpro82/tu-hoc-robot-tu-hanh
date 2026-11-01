# Tập 2.3 · Hiệu chỉnh camera bằng bàn cờ

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.3") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 6](https://porabook.com/book/camera-models/)

## Tóm tắt video

Camera rẻ tiền bẻ cong cả đường thẳng 📷🌀 Một tờ giấy in bàn cờ là sửa được. Bạn từng hiệu chỉnh camera chưa? 👇

Tập 2.3 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Méo thùng kéo góc ảnh lệch 36,6 px, robot tin camera lý tưởng thì đoán sai 5 cm ở 2 m. Chụp 10 tấm bàn cờ (54 góc ô mỗi tấm), mỗi tấm cho một homography H = K[r1 r2 t], giải Vb = 0 ra K (phương pháp Zhang). Bỏ qua méo: sai số chiếu lại 5,66 px. Tinh chỉnh thêm hệ số k: còn 0,41 px, điểm ở 2 m chỉ lệch 4,5 mm. (Camera và ảnh chụp là mô phỏng Python, kết quả khớp OpenCV.)

## Chạy thử

```bash
cd tap23/sim
python -X utf8 hieu_chinh.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/hieu_chinh.py` | Tập 2.3 - Hiệu chỉnh camera bằng bàn cờ (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/hieu_chinh.py`**

```text
Tập 2.3 - Hiệu chỉnh camera bằng bàn cờ (series Tự Học Robot Tự Hành)

Theo Chương 6, Principles of Robot Autonomy:
  - Eq. 6.4: méo xuyên tâm  [u_d, v_d] = (1 + k r²)[u - u_cd, v - v_cd] + [u_cd, v_cd]
  - §6.5.2 (Zhang): bàn cờ phẳng Z_W = 0 -> p^h = H P̃_W^h, H = K[r1 r2 t] (Eq. 6.26-6.27)
    r1 ⟂ r2 -> 2 phương trình mỗi ảnh theo B = K^-T K^-1 (Eq. 6.28-6.31), Vb = 0 (Eq. 6.32),
    b = vectơ kỳ dị nhỏ nhất (Eq. 6.33), lấy K dạng đóng (Eq. 6.34), R, t (Eq. 6.35-6.36).
  - Tinh chỉnh: cực tiểu tổng bình phương sai lệch ‖p_ij - p̂_ij‖² bằng Levenberg-Marquardt, giống Eq. 6.47.
Mở rộng (ngoài sách): chuẩn hoá điểm khi tìm H (Hartley), đưa k vào bước tinh chỉnh, tên gọi "sai số chiếu lại"
(RMS), đối chiếu với cv2.calibrateCamera.
Camera "thật", bàn cờ, các góc chụp và nhiễu là GIẢ ĐỊNH; mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 hieu_chinh.py
```

---
[← Về danh sách tập](../README.md)
