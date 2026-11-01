# Tập 0.3 · ROS 2: hệ thần kinh của robot

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 0.3") · 📚 Giáo trình: Principles of Robot Autonomy, Giới thiệu

## Tóm tắt video

ROS 2 = "hệ thần kinh" của robot 🧠🤖 Node, topic, message giải thích trong 1 phút. Bạn đã từng dùng ROS chưa? 👇

Tập 0.3 | Series TỰ HỌC ROBOT TỰ HÀNH

Mình bọc robot mô phỏng ở tập trước thành một node ROS 2 (Jazzy): nghe /cmd_vel, phát /pose. Output terminal trong video là chạy thật.

## Chạy thử

ROS 2 trong Docker (image `ros:jazzy`): xem và chạy `demo.sh` (kết quả mẫu ở `demo-output.txt`).

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `robot_node.py` | Tập 0.3 - Đưa robot của tập 0.2 vào ROS 2 (series Tự Học Robot Tự Hành). |

## Giải thích trong code

**`robot_node.py`**

```text
Tập 0.3 - Đưa robot của tập 0.2 vào ROS 2 (series Tự Học Robot Tự Hành).

Node này bọc đúng hàm step() của tập 0.2:
  - nghe   /cmd_vel  (geometry_msgs/Twist): linear.x = v, angular.z = ω
  - phát   /pose     (geometry_msgs/Pose2D): x, y, theta
  - chạy 100 lần mỗi giây (dt = 0.01)

Chạy (trong ROS 2 Jazzy):
  python3 robot_node.py
  ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 1.0}}"
  ros2 topic echo /pose
```

---
[← Về danh sách tập](../README.md)
