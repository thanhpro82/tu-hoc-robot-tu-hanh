"""Bài tập tập 4.3: quy hoạch động, nhìn trước mọi nước đi (Mục 17.2.2 của sách, Thuật toán 2).

Dùng lại kho hàng và mô hình của tập 4.2 (module mdp trong ../../tap42/sim): O_TRONG (mọi ô), U (4 lệnh), chuyen(x, u, eps),
g(x) chi phí mỗi bước, gT(x) phạt cuối, T = 30, S, G.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/qhd.py (tự làm trước đã).
"""
import numpy as np

from mdp import CAU_THANG, G, HUONG, O_TRONG, S, T, U, buoc, chuyen, g, gT  # noqa: F401  (kho của tập 4.2)


def bellman(x, J_sau, eps):
    """Bài 1 (Eq. 17.13–17.14): một bước Bellman tại ô x, biết J*_{t+1} (dict J_sau).

    Với mỗi lệnh u trong U: c[u] = g(x) + Σ_{x'} p(x' | x, u)·J_sau[x']     (p lấy từ chuyen(x, u, eps))
    Chọn u có c nhỏ nhất; nếu bằng nhau (so sau khi làm tròn 9 chữ số) thì lấy lệnh đứng trước trong U.
    Trả về (c nhỏ nhất, lệnh tốt nhất)."""
    raise NotImplementedError("TODO Bài 1: một bước Bellman")


def quy_hoach_dong(eps):
    """Bài 2 (Thuật toán 2): tính lùi từ t = T về 0.

    J[T][x] = gT(x);  với t = T−1, ..., 0: J[t][x], PI[t][x] = bellman(x, J[t+1], eps) cho mọi x trong O_TRONG.
    Trả về (J, PI): J là list T+1 dict, PI là list T dict (chính sách thay đổi theo thời gian!)."""
    raise NotImplementedError("TODO Bài 2: quy hoạch động lùi")


def mo_phong(PI, eps, n=2000, seed=42):
    """Bài 3: chạy n lần chính sách PI (đổi theo thời gian: ở bước t dùng PI[t][x]), đếm tỉ lệ tới G và rơi cầu thang.

    rng = np.random.default_rng(seed); mỗi bước gọi rng đúng thứ tự như tập 4.2:
        nếu rng.random() < eps: hướng = list(HUONG.values())[rng.integers(4)]   ngược lại: hướng = HUONG[PI[t][x]]
    Trả về dict {"toi": ..., "roi": ...}."""
    raise NotImplementedError("TODO Bài 3: mô phỏng chính sách tối ưu")
