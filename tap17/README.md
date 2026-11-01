# Tập 1.7 · Tổng kết Mùa 1: tự đi từ A đến B

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.7") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 1–4](https://porabook.com/book/)

## Tóm tắt video

6 tập, 6 mảnh ghép: robot tự đi từ A đến B 🤖🏁 Tổng kết Mùa 1, chạy thật trong ROS 2. Mùa 2 bạn muốn học gì nhất? 👇

Tập 1.7 | TỔNG KẾT MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

3 node ROS 2: planner (A* + bo góc, 6,74 m) → controller (robot ảo có giờ giấc + bám quỹ đạo phẳng vi phân) → robot (bánh yếu, có nhiễu). Kết quả thật: tới đích sau 23,5 s, sai số lớn nhất 2,7 cm, trung bình 0,6 cm, dừng cách đích 3 mm.

## Chạy thử

ROS 2 trong Docker: xem và chạy `ws/demo.sh` (kết quả mẫu ở `ws/demo-output.txt`, log ở `ws/log.csv`).

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `ws/a_sao.py` | Tập 1.5 - A*: tìm đường như Google Maps (series Tự Học Robot Tự Hành) |
| `ws/controller_node.py` | Tập 1.7 - Node điều khiển: bám quỹ đạo theo Ví dụ 3.1.2 (tập 1.4) trên đường A* đã làm mượt. |
| `ws/duong_di.py` | Đổi ô lưới sang mét, làm mượt đường A* (dùng chung cho planner_node và script xuất dữ liệu). |
| `ws/planner_node.py` | Tập 1.7 - Node lập kế hoạch: A* trên bản đồ lưới (tập 1.5), làm mượt góc, phát /path một lần. |
| `ws/robot_node.py` | Tập 1.7 - Node robot: xe 2 bánh mô phỏng (tập 0.2/0.3), có bánh yếu và nhiễu như robot thật. |

## Giải thích trong code

**`ws/planner_node.py`**

```text
Tập 1.7 - Node lập kế hoạch: A* trên bản đồ lưới (tập 1.5), làm mượt góc, phát /path một lần.

phát /path (nav_msgs/Path), QoS transient_local để node đến sau vẫn nhận được
```

---
[← Về danh sách tập](../README.md)
