# Tập 1.5 · Tìm đường như Google Maps: A*

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.5") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 4](https://porabook.com/book/motion-planning/)

## Tóm tắt video

Robot tìm đường như Google Maps bằng cách nào? 🗺️🤖 A* chỉ mở 133 ô thay vì 237 ô mà vẫn ra đường ngắn nhất. Comment "A*" để lấy code 👇

Tập 1.5 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Bản đồ chia lưới → đồ thị. Dijkstra loang đều theo chi phí đi tới C. A* ưu tiên f = C + h, với h = khoảng cách đường chim bay (không bao giờ đoán quá tay) nên vẫn tối ưu. Cùng đường dài 6,87 m, từ mô phỏng Python thật.

## Chạy thử

```bash
cd tap15/sim
python -X utf8 a_sao.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/a_sao.py` | Tập 1.5 - A*: tìm đường như Google Maps (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/a_sao.py`**

```text
Tập 1.5 - A*: tìm đường như Google Maps (series Tự Học Robot Tự Hành)

Theo Mục 4.2 / 4.2.1, Chương 4, Principles of Robot Autonomy:
  - Lưới ô: ô trống là đỉnh, ô kề nhau (8 hướng) nối bằng cạnh -> đồ thị G = (V, E).
  - Dijkstra: luôn mở ô có chi phí đi tới C(q) nhỏ nhất.
  - A*: luôn mở ô có f(q) = C(q) + h(q) nhỏ nhất, h = khoảng cách Euclid tới đích.
    h không bao giờ ước lượng quá chi phí thật (admissible) -> đường tìm được vẫn ngắn nhất.
Chạy: python a_sao.py
```

---
[← Về danh sách tập](../README.md)
