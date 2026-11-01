# Tập 3.7 · Robot vẽ bản đồ nhà tôi

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 3.7") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 14](https://porabook.com/book/slam/)

## Tóm tắt video

Robot đi một vòng căn hộ và tự vẽ ra bản đồ, chạy bằng ROS 2 + slam_toolbox thật 🗺️🤖 Muốn xem code không? 👇

Tập 3.7 | MÙA 3: BIẾT MÌNH Ở ĐÂU | Series TỰ HỌC ROBOT TỰ HÀNH

Robot giả lập gửi LiDAR 360 tia + odometry lên ROS 2 Jazzy (Docker), slam_toolbox dựng bản đồ. Chỉ tin odometry: sau 21,7 m lệch 72 cm, chỉ 45,8% điểm quét rơi đúng tường. Lần chạy đầu, slam_toolbox khép vòng nhầm: tưởng phòng trên là phòng xuất phát, lệch 3,9 m, mọc ra "phòng ma" (chỉ 30,1% tường đúng chỗ). Thêm đồ đạc cho các phòng khác nhau + siết điều kiện khép vòng → lần 2: lệch trung bình 4,3 cm, 99,8% tường đúng chỗ, bản đồ 78,4 m². Bài học: SLAM thật phải chỉnh cẩn thận!

## Chạy thử

ROS 2 + slam_toolbox trong Docker: `docker build -t ros-slam ws` rồi chạy `ws/chay.sh`. Phân tích kết quả: `python -X utf8 sim/phan_tich.py`.

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/phan_tich.py` | Tập 3.7 - phân tích lần chạy slam_toolbox thật (ROS 2 Jazzy trong Docker, xem tap37/ws/). |
| `ws/robot_gia.py` | Tập 3.7 - Robot vẽ bản đồ nhà tôi: node ROS 2 giả lập robot + LiDAR trong căn hộ 4 phòng. |

## Giải thích trong code

**`ws/robot_gia.py`**

```text
Tập 3.7 - Robot vẽ bản đồ nhà tôi: node ROS 2 giả lập robot + LiDAR trong căn hộ 4 phòng.

Phát:  /scan (sensor_msgs/LaserScan, 360 tia, 10 Hz), /odom (nav_msgs/Odometry), TF odom -> base_link (từ odometry có trôi),
       TF tĩnh base_link -> laser.
Ghi:   tư thế thật, tư thế odometry, tư thế slam_toolbox (TF map -> base_link) mỗi 0,5 s và ảnh bản đồ /map mỗi 5 s
       vào /ws/out/ để vẽ video.
Căn hộ giống tập 3.5 (12 × 8 m). Odometry: nhiễu + quay hụt 0,5°/m (giả định) để thấy trôi.
```

**`sim/phan_tich.py`**

```text
Tập 3.7 - phân tích lần chạy slam_toolbox thật (ROS 2 Jazzy trong Docker, xem tap37/ws/).

Đọc tap37/ws/out/: tu_the.jsonl (tư thế thật / odometry / slam_toolbox mỗi 0,5 s) và map_XXX.npy (bản đồ /map mỗi 5 s).
So sánh trong hệ gốc = điểm xuất phát của robot (giống hệ odom và map của slam_toolbox lúc đầu).
- Sai số tư thế: odometry vs slam_toolbox so với tư thế thật.
- Bản đồ "chỉ odometry": quét lại LiDAR tại tư thế thật (cùng mô hình cảm biến với robot_gia.py), ghép theo tư thế odometry,
  để so với bản đồ slam_toolbox tự dựng.
- Độ chính xác bản đồ: % ô bị chiếm (hoặc điểm quét) nằm trong 10 cm quanh tường thật.
Chạy: python -X utf8 phan_tich.py
```

---
[← Về danh sách tập](../README.md)
