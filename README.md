# Tự Học Robot Tự Hành 🤖

Code của series TikTok **"Tự Học Robot Tự Hành"** ([@thanh82k5](https://www.tiktok.com/@thanh82k5)): học robot tự hành bằng tiếng Việt theo giáo trình
**Principles of Robot Autonomy** (Stanford, đọc miễn phí tại [porabook.com](https://porabook.com/book/)).

Mỗi video có một thư mục code riêng. Mọi con số trong video (lệch bao nhiêu cm, đúng bao nhiêu %, …) đều lấy từ chính code này:
bạn chạy lại sẽ thấy đúng các số đó, rồi thử đổi tham số để tự khám phá.

## Cách học

1. Xem video (60 giây) trên TikTok.
2. Mở thư mục của tập đó, đọc `README.md`: tóm tắt, cách chạy, giải thích từng file.
3. Chạy code, đổi tham số (hệ số PID, số hạt, nhiễu cảm biến, …) và xem kết quả thay đổi thế nào.
4. Đọc chương tương ứng trong sách để hiểu sâu.

## Cài đặt

```bash
git clone https://github.com/thanhpro82/tu-hoc-robot-tu-hanh.git
cd tu-hoc-robot-tu-hanh
pip install -r requirements.txt
```

- Python 3.10 trở lên. PyTorch bản CPU là đủ (một số tập học mạng nơ-ron sẽ chạy nhanh hơn nếu có GPU).
- Luôn chạy với `python -X utf8 ...` để in tiếng Việt đúng trên Windows.
- Các tập ROS 2 (0.3, 1.7, 3.7, 3.9) chạy trong Docker, xem README của từng tập.

## Danh sách tập

### Mùa 0 · Khởi động

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| 0.2 | Robot đầu tiên trong mô phỏng | Giới thiệu | [`tap02/`](tap02/) |
| 0.3 | ROS 2: hệ thần kinh của robot | Giới thiệu | [`tap03/`](tap03/) |

### Mùa 1 · Chuyển động & điều khiển

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| 1.1 | Vì sao xe không đi ngang được? | Ch.1 | [`tap11/`](tap11/) |
| 1.2 | Nhắm mắt mà chạy: điều khiển vòng hở | Ch.2 | [`tap12/`](tap12/) |
| 1.3 | PID: thuật toán quan trọng nhất | Ch.3 | [`tap13/`](tap13/) |
| 1.4 | Bám quỹ đạo: robot chạy hình số 8 | Ch.3 | [`tap14/`](tap14/) |
| 1.5 | Tìm đường như Google Maps: A* | Ch.4 | [`tap15/`](tap15/) |
| 1.6 | Tìm đường bằng may rủi: RRT & PRM | Ch.4 | [`tap16/`](tap16/) |
| 1.7 | Tổng kết Mùa 1: tự đi từ A đến B | Ch.1–4 | [`tap17/`](tap17/) |

### Mùa 2 · Nhận thức (thị giác)

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| 2.1 | Giác quan của robot | Ch.5 | [`tap21/`](tap21/) |
| 2.2 | Camera thực ra là cái hộp có lỗ | Ch.6 | [`tap22/`](tap22/) |
| 2.3 | Hiệu chỉnh camera bằng bàn cờ | Ch.6 | [`tap23/`](tap23/) |
| 2.4 | Hai mắt để đoán khoảng cách | Ch.7 | [`tap24/`](tap24/) |
| 2.5 | Dựng 3D từ ảnh chụp | Ch.7 | [`tap25/`](tap25/) |
| 2.6 | Thị giác máy tính cổ điển | Ch.8 | [`tap26/`](tap26/) |
| 2.7 | Deep learning nhìn thế giới thế nào | Ch.9 | [`tap27/`](tap27/) |
| 2.8 | YOLO: robot nhận ra người và đồ vật | Ch.10 | [`tap28/`](tap28/) |
| 2.9 | Tổng kết Mùa 2: robot đi theo bạn | Ch.5–10 | [`tap29/`](tap29/) |

### Mùa 3 · Định vị & bản đồ

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| 3.1 | "Tôi đang ở đâu?": robot nghĩ bằng xác suất | Ch.11 | [`tap31/`](tap31/) |
| 3.2 | Kalman Filter dễ hiểu nhất | Ch.11 | [`tap32/`](tap32/) |
| 3.3 | EKF & UKF: Kalman cho thế giới cong | Ch.12 | [`tap33/`](tap33/) |
| 3.4 | Particle Filter: ngàn phỏng đoán | Ch.12 | [`tap34/`](tap34/) |
| 3.5 | Định vị trên bản đồ có sẵn | Ch.13 | [`tap35/`](tap35/) |
| 3.6 | SLAM: con gà hay quả trứng? | Ch.14 | [`tap36/`](tap36/) |
| 3.7 | Robot vẽ bản đồ nhà tôi | Ch.14 | [`tap37/`](tap37/) |
| 3.8 | Kết hợp cảm biến & theo dõi vật thể | Ch.15 | [`tap38/`](tap38/) |
| 3.9 | Tổng kết Mùa 3: tự dẫn đường trong nhà | Ch.11–15 | [`tap39/`](tap39/) |

### Mùa 4 · Ra quyết định & học

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| 4.1 | Bộ não hành vi: máy trạng thái | Ch.16 | [`tap41/`](tap41/) |
| 4.2 | Ra quyết định khi tương lai bất định | Ch.17 | [`tap42/`](tap42/) |
| 4.3 | Quy hoạch động: nhìn trước mọi nước đi | Ch.17 | [`tap43/`](tap43/) |
| 4.4 | Học tăng cường: robot học từ thất bại | Ch.18 | [`tap44/`](tap44/) |
| 4.5 | Deep RL: luyện robot trong mô phỏng | Ch.18 | [`tap45/`](tap45/) |
| 4.6 | Học bắt chước: robot học từ người lái | Ch.19 | [`tap46/`](tap46/) |
| 4.7 | Tương lai: Physical AI & robot nền tảng | Prospects | [`tap47/`](tap47/) |

### Tập cuối

| Tập | Nội dung | Giáo trình | Code |
|---|---|---|---|
| F | Robot tự hành hoàn chỉnh: nhiệm vụ giao đồ trong nhà | Ch. 3–16 | [`tapF/`](tapF/) |

## Ghi chú

- Code tự viết để giải thích, **không chép** chữ hay hình của sách; ký hiệu và phương pháp theo đúng sách, phần nào ngoài sách được ghi là "mở rộng" / "giả định" ngay trong code.
- Các tập sau dùng lại code tập trước (vd. 2.9 dùng YOLO của 2.8, tập cuối dùng bản đồ của 3.5), nên hãy giữ nguyên cấu trúc thư mục.
- Series không liên kết chính thức với tác giả hay Stanford.

## Giấy phép

MIT, xem [LICENSE](LICENSE).
