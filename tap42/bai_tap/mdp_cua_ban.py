"""Bài tập tập 4.2: đường tắt hay đường vòng? Quá trình quyết định Markov (MDP, Chương 17 của sách). Dùng numpy.

Kho hàng là lưới 9 × 5; robot đi từ S = (0, 1) tới G = (8, 1). Hàng dưới cùng là cầu thang (rơi xuống là kẹt luôn), giữa kho có dãy kệ.
Lệnh u ∈ {"len", "xuong", "trai", "phai"}. Sàn trơn: với xác suất ε robot đi theo một hướng ngẫu nhiên (4 hướng đều nhau).
Chi phí (theo sách, tối thiểu hoá): mỗi bước chưa tới G tốn 1; hết T = 30 bước mà chưa tới G thì phạt thêm 100.
Làm lần lượt Bài 1 → 2 → 3, xong mỗi bài chạy:  python -X utf8 kiem_tra.py
Giữ nguyên tên hàm và tham số. Lời giải: ../sim/mdp.py (tự làm trước đã).
"""
import numpy as np

from mdp import CAU_THANG, G, HUONG, O_TRONG, S, T, buoc, g, gT  # noqa: F401  (thế giới có sẵn, trong ../sim)


def chuyen(x, u, eps):
    """Bài 1 (Eq. 17.8): xác suất chuyển p(x_{t+1} | x_t = x, u_t = u), trả về dict {ô_mới: xác_suất}.

    Với mỗi hướng d trong HUONG: xác suất đi hướng đó = (1 − ε)·[d là hướng u] + ε/4; ô tới = buoc(x, vectơ của d).
    Nhiều hướng có thể dẫn tới cùng một ô (vd. đâm tường thì đứng yên): nhớ CỘNG DỒN xác suất."""
    raise NotImplementedError("TODO Bài 1: xác suất chuyển")


def danh_gia(pi, eps):
    """Bài 2 (Eq. 17.11): chi phí kỳ vọng J_π(x) của chính sách π (hàm x → lệnh), lùi từ cuối:

        J_T(x) = gT(x);   J_t(x) = g(x) + Σ_{x'} p(x' | x, π(x))·J_{t+1}(x')     (lặp T lần)
    Trả về dict {ô: J_0(ô)} cho mọi ô trong O_TRONG."""
    raise NotImplementedError("TODO Bài 2: đánh giá chính sách")


def mo_phong(pi, eps, n=2000, seed=42):
    """Bài 3 (Monte Carlo): cho robot chạy n lần, mỗi lần T bước từ S theo π, đếm tỉ lệ tới G và tỉ lệ rơi cầu thang.

    rng = np.random.default_rng(seed); hướng ngẫu nhiên lấy theo thứ tự list(HUONG.values()). Mỗi bước, gọi rng ĐÚNG thứ tự:
        nếu rng.random() < eps: hướng = list(HUONG.values())[rng.integers(4)]    (trượt)
        ngược lại:              hướng = HUONG[pi(x)]
        x = buoc(x, hướng)
    Trả về dict {"toi": tỉ lệ kết thúc ở G, "roi": tỉ lệ kết thúc ở cầu thang}."""
    raise NotImplementedError("TODO Bài 3: mô phỏng Monte Carlo")
