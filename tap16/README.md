# Tập 1.6 · Tìm đường bằng may rủi: RRT & PRM

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.6") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 4](https://porabook.com/book/motion-planning/)

## Tóm tắt video

Thuật toán tìm đường mọc như một cái cây 🌳🤖 RRT tìm ra đường ở nơi A* bó tay. Comment "RRT" để lấy code 👇

Tập 1.6 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Lưới ô bùng nổ khi robot nhiều khớp (6 khớp × 100 nấc = 1 nghìn tỷ ô). RRT gieo điểm ngẫu nhiên: q_rand → q_near → q_new → gắn vào cây. 30 lần chạy: 70% tìm ra đường sau 500 vòng, 100% sau 1000 vòng. RRT* nối lại các nhánh: 26,23 m → 16,65 m. Số liệu từ mô phỏng Python thật.

## Chạy thử

```bash
cd tap16/sim
python -X utf8 rrt.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/rrt.py` | Tập 1.6 - RRT: tìm đường bằng cách gieo ngẫu nhiên (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/rrt.py`**

```text
Tập 1.6 - RRT: tìm đường bằng cách gieo ngẫu nhiên (series Tự Học Robot Tự Hành)

Theo Mục 4.4.2, Chương 4, Principles of Robot Autonomy. Mỗi vòng lặp RRT:
  1. lấy mẫu q_rand (xác suất ALPHA lấy luôn đích q_G: goal biasing)
  2. tìm đỉnh gần nhất q_near trên cây T (khoảng cách Euclid)
  3. tiến từ q_near về phía q_rand một đoạn BUOC -> q_new, kiểm tra không va chạm
  4. gắn q_new vào cây với cạnh từ q_near
RRT* (mở rộng, theo Karaman & Frazzoli 2011 mà sách trích dẫn): khi gắn q_new thì chọn cha
tốt nhất trong bán kính r, rồi "nối lại" (rewire) các đỉnh lân cận nếu đi qua q_new rẻ hơn.
Chạy: python rrt.py
```

---
[← Về danh sách tập](../README.md)
