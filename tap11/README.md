# Tập 1.1 · Vì sao xe không đi ngang được?

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 1.1") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 1](https://porabook.com/book/modeling-robot-dynamics/)

## Tóm tắt video

Vì sao đỗ xe song song khó đến thế? 🚗😵 Câu trả lời nằm trong 1 phương trình. Bạn có sợ đỗ xe song song không? 👇

Tập 1.1 | MÙA 1: BIẾT ĐI | Series TỰ HỌC ROBOT TỰ HÀNH

Robot đa hướng, xe 2 bánh và ô tô cùng thử "sang ngang 60 cm". Ràng buộc nonholonomic: bánh xe không trượt ngang (ẋ·sinθ − ẏ·cosθ = 0), mô hình ô tô θ̇ = v·tanφ/L nên bán kính quay R = L / tan φ. Mọi quỹ đạo trong video đều từ mô phỏng Python thật.

## Chạy thử

```bash
cd tap11/sim
python -X utf8 khong_di_ngang.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/khong_di_ngang.py` | Tập 1.1 - Vì sao xe không đi ngang được? (series Tự Học Robot Tự Hành) |

## Giải thích trong code

**`sim/khong_di_ngang.py`**

```text
Tập 1.1 - Vì sao xe không đi ngang được? (series Tự Học Robot Tự Hành)

Bài toán: dời robot sang ngang 0.6 m, giữ nguyên hướng nhìn về phía trước.
So sánh 3 loại robot (Chương 1, Principles of Robot Autonomy):
  - Robot đa hướng (omni): đi ngang được ngay  -> holonomic
  - Xe 2 bánh (unicycle): quay 90°, chạy, quay lại
  - Ô tô (bicycle model, Eq. 1.29): góc lái φ bị giới hạn -> phải lùi theo 2 cung tròn (đỗ xe song song)
Chạy: python khong_di_ngang.py
```

---
[← Về danh sách tập](../README.md)
