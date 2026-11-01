# Tập 2.5 · Dựng 3D từ ảnh chụp

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 2.5") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 7](https://porabook.com/book/stereo-vision/)

## Tóm tắt video

Đi vòng quanh, chụp 12 tấm ảnh bằng 1 camera… máy tính dựng lại cả ngôi nhà 3D 🏠📸 Bạn muốn tự thử không? 👇

Tập 2.5 | MÙA 2: BIẾT NHÌN | Series TỰ HỌC ROBOT TỰ HÀNH

Structure from Motion: tìm 273 cặp điểm giống nhau giữa 2 ảnh đầu → ma trận E → 4 khả năng (R, t), chỉ 1 khả năng đặt điểm trước cả 2 camera → tam giác hoá. Ảnh không cho biết tỉ lệ (mô hình 1,01 đơn vị, thật 1,66 m). Thêm từng ảnh bằng PnP, 12 ảnh → 402 điểm. Bundle adjustment: sai số chiếu lại 3,71 px → 0,89 px. Gắn tỉ lệ bằng cạnh 2 m: điểm lệch trung bình 2,1 cm. (Ngôi nhà và ảnh là mô phỏng Python.)

## Chạy thử

```bash
cd tap25/sim
python -X utf8 sfm.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/sfm.py` | Tập 2.5 - Dựng 3D từ ảnh chụp (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/sfm.py`**

```text
Tập 2.5 - Dựng 3D từ ảnh chụp (series Tự Học Robot Tự Hành)

Theo Chương 7, Principles of Robot Autonomy, §7.3 Structure From Motion:
  - Một camera di chuyển, K đã biết; p_jk^h = K[R_k t_k] P_j^h
  - §7.3.1 hai ảnh: ước lượng F (Eq. 7.5-7.6, 8 điểm), E = K^T F K, tách E ra 4 cặp (R, t),
    chọn cặp cho các điểm có độ sâu dương ở cả hai camera, tam giác hoá (Eq. 7.8). Tỉ lệ tuyệt đối không suy ra được từ ảnh.
  - §7.3.2 thêm từng ảnh: PnP định vị camera mới bằng các điểm 3D đã có, tam giác hoá điểm mới;
    bundle adjustment (Eq. 7.9) chỉnh mọi camera và mọi điểm cùng lúc để cực tiểu sai số chiếu lại.
Mở rộng (ngoài sách): chuẩn hoá điểm khi ước lượng F, công thức tách E bằng SVD, giải PnP bằng cv2.solvePnP,
gắn tỉ lệ bằng một cạnh đo thật, căn chỉnh Umeyama để đo sai số.
Ngôi nhà mô hình, quỹ đạo camera và nhiễu là GIẢ ĐỊNH; mọi con số in ra là kết quả tính thật.
Chạy: python -X utf8 sfm.py
```

---
[← Về danh sách tập](../README.md)
