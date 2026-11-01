# Tập 3.9 · Tổng kết Mùa 3: tự dẫn đường trong nhà

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.9") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 11–15](https://porabook.com/book/)

## Tóm tắt video

Bấm một điểm trên bản đồ, robot tự đi ra bếp, kể cả khi cửa bị đóng 🚪🤖 Chạy bằng ROS 2 + Nav2 thật. Muốn xem code không? 👇

Tập 3.9 | 🏁 TỔNG KẾT MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Ghép cả Mùa 3: bản đồ slam_toolbox từ tập 3.7 + AMCL (bộ lọc hạt) để định vị + Nav2 tìm đường (Dijkstra trên bản đồ chi phí) và bám đường. Cố tình bấm vị trí ban đầu lệch 43 cm: sau 2 giây AMCL kéo sai số xuống dưới 10 cm, cả chuyến lệch trung bình 4,3 cm. Đường đầu tiên 10,94 m đi qua cửa phòng dưới, nhưng cửa đóng (không có trên bản đồ): cách cửa 2,15 m LiDAR thấy vật cản, Nav2 lập lại đường vòng qua phòng trên. Tới bếp sau 35,6 s, đi 13,91 m, dừng cách đích 6,1 cm, 0 va chạm. Nếu chỉ tin odometry: lệch 80 cm.

## Chạy thử

ROS 2 + Nav2 trong Docker: `docker build -t ros-nav ws` rồi chạy `ws/chay.sh`. Phân tích kết quả: `python -X utf8 sim/phan_tich.py`.

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/phan_tich.py` | Tập 3.9 - Phân tích lần chạy Nav2 thật (tap39/ws/out): AMCL sửa vị trí bấm lệch, cửa đóng -> lập lại đường, tới bếp. |
| `sim/tao_map.py` | Tập 3.9: đổi bản đồ slam_toolbox cuối cùng của tập 3.7 (map_015.npy) sang định dạng map_server của Nav2 (pgm + yaml). |
| `ws/ra_lenh.py` | Tập 3.9 - "Bấm" ước lượng vị trí ban đầu (lệch cố ý) rồi ra lệnh Nav2 đi tới bếp, ghi lại mọi thứ để vẽ video. |
| `ws/robot_nav.py` | Tập 3.9 - Tổng kết Mùa 3: robot giả lập cho Nav2 trong căn hộ của tập 3.7. |
| `ws/tao_params.py` | Tập 3.9: tạo nav2.yaml từ file tham số mặc định của nav2_bringup, chỉ sửa những chỗ cần cho robot giả lập. |

## Giải thích trong code

**`ws/robot_nav.py`**

```text
Tập 3.9 - Tổng kết Mùa 3: robot giả lập cho Nav2 trong căn hộ của tập 3.7.

Nhận: /cmd_vel (geometry_msgs/Twist) từ Nav2, robot hai bánh v, ω (mô hình unicycle).
Phát: /scan (360 tia, 10 Hz), /odom + TF odom -> base_link (odometry trôi như tập 3.7), TF tĩnh base_link -> laser.
Thế giới hôm nay khác bản đồ: cửa giữa hai phòng dưới (x = 6 m, y 1,6–2,6 m) bị ĐÓNG (giả định, để Nav2 phải tìm đường khác).
Ghi: tư thế thật + odometry mỗi 0,1 s vào /ws/out/robot.jsonl (đồng hồ time.time() dùng chung với ra_lenh.py).
```

**`sim/phan_tich.py`**

```text
Tập 3.9 - Phân tích lần chạy Nav2 thật (tap39/ws/out): AMCL sửa vị trí bấm lệch, cửa đóng -> lập lại đường, tới bếp.

Hệ map = hệ bản đồ slam_toolbox tập 3.7 (gốc ở chỗ xuất phát X0 của thế giới). Tư thế thật đổi sang hệ map bằng cách trừ X0.
```

---
[← Về danh sách tập](../README.md)
