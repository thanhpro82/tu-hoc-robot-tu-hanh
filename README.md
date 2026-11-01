<div align="center">

# 🤖 Tự Học Robot Tự Hành

**Học robot tự hành bằng tiếng Việt: xem video 60 giây, rồi tự viết code cho robot chạy.**

[![TikTok](https://img.shields.io/badge/TikTok-@thanh82k5-000000?logo=tiktok)](https://www.tiktok.com/@thanh82k5)
[![Giáo trình](https://img.shields.io/badge/Giáo_trình-Principles_of_Robot_Autonomy-8C1515)](https://porabook.com/book/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Số tập](https://img.shields.io/badge/35_tập-4_mùa-ef4444)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

Code của series TikTok **"Tự Học Robot Tự Hành"**, đi theo giáo trình **Principles of Robot Autonomy** (Stanford, đọc miễn phí tại
[porabook.com](https://porabook.com/book/)). Mỗi video có một thư mục riêng. Mọi con số trong video (lệch bao nhiêu cm, đúng bao nhiêu %, …)
đều lấy từ chính code này: bạn chạy lại sẽ thấy đúng các số đó.

## Bạn sẽ xây gì

Đi hết series, bạn tự tay ghép được một robot giao đồ trong căn hộ, mỗi mùa thêm một "giác quan":

```text
 Mùa 0          Mùa 1               Mùa 2              Mùa 3                 Mùa 4                Tập cuối
 Khởi động ──► Biết đi ──────────► Biết nhìn ───────► Biết mình ở đâu ───► Biết quyết định ───► Robot giao đồ
 mô phỏng,     mô hình xe, PID,    camera, stereo,    Kalman, bộ lọc hạt,   máy trạng thái, MDP, ghép cả 4 mùa:
 ROS 2         A*, RRT             CNN, YOLO          SLAM, kết hợp cảm biến Q-learning, học bắt chước  89/100 lượt giao thành công
```

## Trong repo này

| Ở đâu | Dùng khi nào |
|---|---|
| [README.md](README.md) | Đọc đầu tiên: lộ trình, cài đặt, danh sách tập (file này) |
| `tapXX/README.md` | Bài học của từng tập: bài toán, cách chạy, kết quả mong đợi |
| `tapXX/sim/` | Code mô phỏng tạo ra số liệu trong video (với các tập có bài tập, đây cũng là **lời giải**) |
| `tapXX/bai_tap/` | 📝 Bài tập để bạn tự viết code, kèm `kiem_tra.py` tự chấm ✅ / ❌ |
| `tapXX/*.ipynb` | Notebook làm bài ngay trên Google Colab, không cần cài gì |
| `tapXX/ws/` | Các tập chạy ROS 2 thật trong Docker (1.7, 3.7, 3.9) |
| `chung/` | Bộ chấm dùng chung cho mọi bài tập |

## Cách học một tập

1. **Xem video** 60 giây trên TikTok để nắm ý chính.
2. **Đọc `README.md` của tập**: bài toán, sơ đồ, mục tiêu.
3. **Chạy mô phỏng**, so với kết quả mong đợi trong README.
4. **Làm bài tập** (tập có 📝): tự viết phần cốt lõi, chạy `kiem_tra.py` tới khi ✅ hết. Tự làm xong rồi hãy mở lời giải trong `sim/`.
5. **Thử thách**: đổi tham số (hệ số PID, số hạt, nhiễu cảm biến, …) và tự giải thích kết quả.
6. **Đọc chương sách** tương ứng để hiểu sâu.

## Bắt đầu

**Không muốn cài gì:** bấm nút **Colab** ở các tập có 📝 trong bảng bên dưới.

**Trên máy:**

```bash
git clone https://github.com/thanhpro82/tu-hoc-robot-tu-hanh.git
cd tu-hoc-robot-tu-hanh
pip install -r requirements.txt
python -X utf8 tap02/sim/robot_dau_tien.py     # thử tập 0.2: robot đầu tiên (mở cửa sổ hình)
```

- Python 3.10 trở lên. PyTorch bản CPU là đủ (các tập học mạng nơ-ron chạy nhanh hơn nếu có GPU).
- Luôn chạy với `python -X utf8 ...` để in tiếng Việt đúng trên Windows.
- Các tập ROS 2 (0.3, 1.7, 3.7, 3.9) chạy trong Docker, xem README của từng tập.
- Mới bắt đầu? Đi theo thứ tự 0.2 → 1.1 → 1.2 → 1.3 … vì tập sau dùng lại kiến thức (và cả code) của tập trước.

## Danh sách tập

📝 = có bài tập tự chấm và notebook Colab (18/35 tập, đang bổ sung dần) · ▶️ = chạy mô phỏng, đổi tham số để khám phá

### Mùa 0 · Khởi động

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **0.2** | Robot đầu tiên trong mô phỏng | Giới thiệu | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap02/tap02_robot_dau_tien.ipynb) | [`tap02/`](tap02/) |
| **0.3** | ROS 2: hệ thần kinh của robot | Giới thiệu | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap03/tap03_ros_mini.ipynb) | [`tap03/`](tap03/) |

### Mùa 1 · Chuyển động & điều khiển

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **1.1** | Vì sao xe không đi ngang được? | Ch.1 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap11/tap11_khong_di_ngang.ipynb) | [`tap11/`](tap11/) |
| **1.2** | Nhắm mắt mà chạy: điều khiển vòng hở | Ch.2 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap12/tap12_vong_ho.ipynb) | [`tap12/`](tap12/) |
| **1.3** | PID: thuật toán quan trọng nhất | Ch.3 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap13/tap13_pid.ipynb) | [`tap13/`](tap13/) |
| **1.4** | Bám quỹ đạo: robot chạy hình số 8 | Ch.3 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap14/tap14_bam_quy_dao.ipynb) | [`tap14/`](tap14/) |
| **1.5** | Tìm đường như Google Maps: A* | Ch.4 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap15/tap15_a_sao.ipynb) | [`tap15/`](tap15/) |
| **1.6** | Tìm đường bằng may rủi: RRT & PRM | Ch.4 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap16/tap16_rrt.ipynb) | [`tap16/`](tap16/) |
| **1.7** | Tổng kết Mùa 1: tự đi từ A đến B | Ch.1–4 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap17/tap17_a_den_b.ipynb) | [`tap17/`](tap17/) |

### Mùa 2 · Nhận thức (thị giác)

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **2.1** | Giác quan của robot | Ch.5 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap21/tap21_cam_bien.ipynb) | [`tap21/`](tap21/) |
| **2.2** | Camera thực ra là cái hộp có lỗ | Ch.6 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap22/tap22_camera.ipynb) | [`tap22/`](tap22/) |
| **2.3** | Hiệu chỉnh camera bằng bàn cờ | Ch.6 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap23/tap23_hieu_chinh.ipynb) | [`tap23/`](tap23/) |
| **2.4** | Hai mắt để đoán khoảng cách | Ch.7 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap24/tap24_stereo.ipynb) | [`tap24/`](tap24/) |
| **2.5** | Dựng 3D từ ảnh chụp | Ch.7 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap25/tap25_sfm.ipynb) | [`tap25/`](tap25/) |
| **2.6** | Thị giác máy tính cổ điển | Ch.8 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap26/tap26_do_vach.ipynb) | [`tap26/`](tap26/) |
| **2.7** | Deep learning nhìn thế giới thế nào | Ch.9 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap27/tap27_cnn.ipynb) | [`tap27/`](tap27/) |
| **2.8** | YOLO: robot nhận ra người và đồ vật | Ch.10 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap28/tap28_yolo.ipynb) | [`tap28/`](tap28/) |
| **2.9** | Tổng kết Mùa 2: robot đi theo bạn | Ch.5–10 | 📝 Bài tập + tự chấm · [![Colab](https://img.shields.io/badge/Colab-mở-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/thanhpro82/tu-hoc-robot-tu-hanh/blob/main/tap29/tap29_di_theo.ipynb) | [`tap29/`](tap29/) |

### Mùa 3 · Định vị & bản đồ

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **3.1** | "Tôi đang ở đâu?": robot nghĩ bằng xác suất | Ch.11 | ▶️ Chạy & đổi tham số | [`tap31/`](tap31/) |
| **3.2** | Kalman Filter dễ hiểu nhất | Ch.11 | ▶️ Chạy & đổi tham số | [`tap32/`](tap32/) |
| **3.3** | EKF & UKF: Kalman cho thế giới cong | Ch.12 | ▶️ Chạy & đổi tham số | [`tap33/`](tap33/) |
| **3.4** | Particle Filter: ngàn phỏng đoán | Ch.12 | ▶️ Chạy & đổi tham số | [`tap34/`](tap34/) |
| **3.5** | Định vị trên bản đồ có sẵn | Ch.13 | ▶️ Chạy & đổi tham số | [`tap35/`](tap35/) |
| **3.6** | SLAM: con gà hay quả trứng? | Ch.14 | ▶️ Chạy & đổi tham số | [`tap36/`](tap36/) |
| **3.7** | Robot vẽ bản đồ nhà tôi | Ch.14 | ▶️ Chạy & đổi tham số | [`tap37/`](tap37/) |
| **3.8** | Kết hợp cảm biến & theo dõi vật thể | Ch.15 | ▶️ Chạy & đổi tham số | [`tap38/`](tap38/) |
| **3.9** | Tổng kết Mùa 3: tự dẫn đường trong nhà | Ch.11–15 | ▶️ Chạy & đổi tham số | [`tap39/`](tap39/) |

### Mùa 4 · Ra quyết định & học

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **4.1** | Bộ não hành vi: máy trạng thái | Ch.16 | ▶️ Chạy & đổi tham số | [`tap41/`](tap41/) |
| **4.2** | Ra quyết định khi tương lai bất định | Ch.17 | ▶️ Chạy & đổi tham số | [`tap42/`](tap42/) |
| **4.3** | Quy hoạch động: nhìn trước mọi nước đi | Ch.17 | ▶️ Chạy & đổi tham số | [`tap43/`](tap43/) |
| **4.4** | Học tăng cường: robot học từ thất bại | Ch.18 | ▶️ Chạy & đổi tham số | [`tap44/`](tap44/) |
| **4.5** | Deep RL: luyện robot trong mô phỏng | Ch.18 | ▶️ Chạy & đổi tham số | [`tap45/`](tap45/) |
| **4.6** | Học bắt chước: robot học từ người lái | Ch.19 | ▶️ Chạy & đổi tham số | [`tap46/`](tap46/) |
| **4.7** | Tương lai: Physical AI & robot nền tảng | Prospects | ▶️ Chạy & đổi tham số | [`tap47/`](tap47/) |

### Tập cuối

| Tập | Nội dung | Giáo trình | Học thế nào | Thư mục |
|---|---|---|---|---|
| **F** | Robot tự hành hoàn chỉnh: nhiệm vụ giao đồ trong nhà | Ch. 3–16 | ▶️ Chạy & đổi tham số | [`tapF/`](tapF/) |

## Ghi chú

- Code tự viết để giải thích, **không chép** chữ hay hình của sách. Ký hiệu và phương pháp theo đúng sách; phần nào ngoài sách được ghi là "mở rộng" hoặc "giả định" ngay trong code và mục *Giới hạn cần biết* của từng tập.
- Các tập sau dùng lại code tập trước (ví dụ 2.9 dùng YOLO của 2.8, tập cuối dùng bản đồ của 3.5), nên hãy giữ nguyên cấu trúc thư mục.
- Thấy lỗi hay có câu hỏi? Mở [Issue](https://github.com/thanhpro82/tu-hoc-robot-tu-hanh/issues) hoặc bình luận dưới video.
- Series không liên kết chính thức với tác giả sách hay Stanford.

## Giấy phép

MIT, xem [LICENSE](LICENSE).
