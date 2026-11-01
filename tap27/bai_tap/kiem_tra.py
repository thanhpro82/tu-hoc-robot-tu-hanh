"""Tự chấm bài tập tập 2.7. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())

Không import thẳng ../sim/cnn.py (file đó huấn luyện 2 mạng ngay khi import, mất ~35 giây); chỉ nạp phần tạo dữ liệu.
"""
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parents[1])]
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

_NGUON = (_D.parent / "sim" / "cnn.py").read_text(encoding="utf8")
DL = {}
exec(compile(_NGUON.split("X_HOC, Y_HOC = bo_du_lieu(1500)")[0], "cnn.py", "exec"), DL)   # hàm ve_anh, bo_du_lieu, SimpleCNN gốc...
SO_THAM_SO_VIDEO = {"SimpleCNN": 36356, "conv1": 208}     # in ra khi chạy sim/cnn.py


def du_lieu(n, seed):
    """Sinh n ảnh vạch dẫn đường bằng đúng hàm của video (RNG riêng để kết quả lặp lại được)."""
    DL["RNG"] = np.random.default_rng(seed)
    return DL["bo_du_lieu"](n)


def hoc_nhanh(Lop, so_vong=4, seed=27):
    """Huấn luyện mạng Lop() vài vòng trên 1500 ảnh (Adam, cross-entropy như video), trả về (mạng, độ chính xác trên 1000 ảnh thử)."""
    torch.manual_seed(seed)
    Xh, yh = du_lieu(1500, seed)
    Xt, yt = du_lieu(1000, seed + 1)
    m = Lop()
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    for _ in range(so_vong):
        perm = torch.randperm(len(Xh))
        for i in range(0, len(Xh), 64):
            idx = perm[i:i + 64]
            opt.zero_grad()
            nn.functional.cross_entropy(m(Xh[idx]), yh[idx]).backward()
            opt.step()
    with torch.no_grad():
        return m, float((m(Xt).argmax(1) == yt).float().mean())


def bai_1(ns):
    f = ham(ns, "lop_tich_chap")
    rng = np.random.default_rng(1)
    X, W = rng.normal(size=(9, 11)), rng.normal(size=(3, 3))
    dap = torch.nn.functional.conv2d(torch.tensor(X)[None, None], torch.tensor(W)[None, None]).numpy()[0, 0] + 0.5
    Y = np.asarray(f(X, W, 0.5))
    assert Y.shape == (7, 9), f"ảnh 9×11, bộ lọc 3×3, không đệm viền: kết quả phải 7×9, bạn ra {Y.shape}"
    assert gan(Y, dap, 1e-9), "Y[i, j] = Σ X[i+u, j+v]·W[u, v] + b chưa đúng (lớp tích chập trong deep learning KHÔNG lật bộ lọc)"
    return "khớp torch.nn.functional.conv2d: 1 bộ lọc 3×3 dùng chung cho mọi vị trí (9 tham số + 1 bias)"


def bai_2(ns):
    f = ham(ns, "max_pool")
    A = np.array([[1, 3, 2, 0], [4, 2, 1, 5], [0, 0, 7, 1], [2, 6, 3, 3]], dtype=float)
    assert gan(f(A), [[4, 5], [6, 7]]), f"max pooling ví dụ 4×4 phải ra [[4, 5], [6, 7]], bạn ra {f(A)}"
    B = np.random.default_rng(2).normal(size=(16, 16))
    assert gan(f(B), torch.nn.functional.max_pool2d(torch.tensor(B)[None, None], 2).numpy()[0, 0]), "chưa khớp max_pool2d trên ảnh 16×16"
    return "mỗi ô 2×2 giữ số lớn nhất: ảnh nhỏ đi 4 lần, dịch vài pixel vẫn ra gần như cùng kết quả"


def bai_3(ns):
    Lop = ham(ns, "SimpleCNN")
    m = Lop()
    n = sum(p.numel() for p in m.parameters())
    n1 = sum(p.numel() for p in m.conv1.parameters())
    assert n1 == SO_THAM_SO_VIDEO["conv1"], f"conv1 phải có 208 tham số (8 bộ lọc 5×5 + 8 bias), bạn có {n1}"
    assert n == SO_THAM_SO_VIDEO["SimpleCNN"], f"cả mạng phải có 36356 tham số như video, bạn có {n}"
    out = m(torch.zeros(5, 1, 32, 32))
    assert tuple(out.shape) == (5, 4), f"5 ảnh vào phải ra (5, 4), bạn ra {tuple(out.shape)}"
    _, acc = hoc_nhanh(Lop)
    assert acc > 0.8, f"học 4 vòng mà chỉ đúng {acc * 100:.1f}% ảnh thử (lời giải đạt ~95%), kiểm tra lại forward"
    return f"36356 tham số như video; tự học 4 vòng (thay vì 12 như video) đã đúng {acc * 100:.1f}% trên 1000 ảnh thử"


BAI = [("Bài 1 · lớp tích chập", bai_1), ("Bài 2 · max pooling", bai_2), ("Bài 3 · SimpleCNN bằng PyTorch", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "cnn_cua_ban", loi_giai)
