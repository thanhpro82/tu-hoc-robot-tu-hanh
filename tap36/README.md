# Tập 3.6 · SLAM: con gà hay quả trứng?

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.6") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 14](https://porabook.com/book/slam/)

## Tóm tắt video

Muốn biết mình ở đâu thì cần bản đồ. Muốn vẽ bản đồ thì phải biết mình ở đâu 🐔🥚 Robot giải bài toán này thế nào? 👇

Tập 3.6 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

SLAM: robot đi một vòng hành lang, mỗi mét quét LiDAR, vừa đi vừa ghép bản đồ. Bánh xe quay hụt chút ít → về chỗ cũ lệch 2,46 m, tường vẽ thành 2 lớp. Graph SLAM: 58 nút (tư thế), 57 "dây chun" (đo đường đi). Quay về chỗ xuất phát, so lần quét cuối với lần quét đầu (ICP khớp 1,8 cm) → thêm dây khép vòng → kéo căng cả lưới. Sai trung bình còn 13 cm, bản đồ nét từ 49,8% lên 81,1%. Nhưng khép nhầm chỗ thì bản đồ méo nặng hơn! (Mô phỏng Python.)

## Chạy thử

```bash
cd tap36/sim
python -X utf8 slam.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/slam.py` | Tập 3.6 - SLAM: con gà hay quả trứng? (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/slam.py`**

```text
Tập 3.6 - SLAM: con gà hay quả trứng? (series Tự Học Robot Tự Hành)

Theo Chương 14, Principles of Robot Autonomy:
  - Full SLAM (Định nghĩa 14.2, Eq. 14.2): ước lượng cả quỹ đạo và bản đồ; định vị cần bản đồ, vẽ bản đồ cần định vị
  - Front-end (§14.2): khép vòng = tìm lại chỗ cũ + kiểm tra hình học; căn quét bằng ICP (§14.2.5)
  - Graph SLAM (§14.7): nút = tư thế, cạnh = ràng buộc tương đối (odometry, khép vòng);
    r_ij = z_ij ⊖ h_ij(x_i, x_j), Ω_ij = R_ij⁻¹, x* = argmin Σ r_ijᵀ Ω_ij r_ij, giải bằng Gauss–Newton / LM, cố định tư thế đầu
  - Khép vòng nối hai đầu xa nhau của quỹ đạo, sai số dồn lại được rải đều dọc đường
Mở rộng / giả định: hành lang vòng quanh khối nhà 20 × 14 m, LiDAR 90 tia, nhiễu odometry (2% quãng đường, 1°/m, lệch hướng
nhẹ), coi như đã nhận ra chỗ cũ (bước tìm lại chỗ cũ không mô phỏng), ICP điểm–điểm, giải bằng scipy least_squares (LM).
Mọi con số in ra là kết quả chạy thật.
Chạy: python -X utf8 slam.py
```

---
[← Về danh sách tập](../README.md)
