"""Bài tập tập 1.5: tự viết thuật toán A* tìm đường trên lưới ô.

Bản đồ là list các chuỗi: '#' là tường, ký tự khác là ô đi được. Một ô viết là (hàng, cột).
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/a_sao.py và loi_giai.py (tự làm trước đã).
"""
import heapq
import math

HUONG = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]   # 8 hướng


def ke(o, ban_do):
    """Bài 1: các ô kề với ô o mà robot đi sang được, kèm chi phí bước đi.

    - Đi 8 hướng: ngang/dọc tốn 1, chéo tốn √2.
    - Bỏ ô ngoài bản đồ và ô tường '#'.
    - Không cắt chéo qua góc tường: đi chéo chỉ được khi CẢ HAI ô ngang/dọc bên cạnh đều trống.
    Trả về list các tuple ((hàng, cột), chi_phí)."""
    raise NotImplementedError("TODO Bài 1: list ((r, c), chi_phí)")


def h_euclid(o, dich):
    """Bài 2: heuristic của A*, khoảng cách đường chim bay (Euclid) từ ô o tới ô đích, tính theo đơn vị ô."""
    raise NotImplementedError("TODO Bài 2: khoảng cách Euclid")


def tim_duong(bat_dau, dich, ban_do, h):
    """Bài 3: A* (h = heuristic) — với h luôn bằng 0 thì chính là Dijkstra.

    Dùng hàng đợi ưu tiên (heapq) theo f = C + h(ô):
      - C[o]: chi phí ngắn nhất đã biết từ bat_dau tới o;  truoc[o]: ô đứng trước o trên đường đó.
      - Mỗi vòng lấy ô có f nhỏ nhất ra "mở" (bỏ qua nếu đã mở rồi). Gặp đích thì dừng.
      - Với mỗi ô kề o2 (dùng hàm ke của Bài 1): nếu C[o] + chi_phí < C[o2] thì cập nhật C, truoc, và đẩy o2 vào hàng đợi.
    Trả về (duong, so_o_da_mo, chi_phi):
      duong = list ô từ bat_dau tới dich, so_o_da_mo = số ô đã lấy ra mở, chi_phi = C[dich] (đơn vị ô)."""
    raise NotImplementedError("TODO Bài 3: A*")
