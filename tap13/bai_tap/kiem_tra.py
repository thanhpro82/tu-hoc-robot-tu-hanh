"""Tự chấm bài tập tập 1.3. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải gốc)

Mỗi bài kiểm tra 2 bước:
  1. Thử hàm với vài con số tính tay được.
  2. Cho robot chạy 16 giây bằng PID của bạn trong đúng mô phỏng của video, so độ lệch cuối với lời giải.
Trong notebook thì gọi: cham(globals())
"""
import sys
from pathlib import Path

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D.parent / "sim"), str(_D.parents[1])]
import pid as goc  # noqa: E402  (mô phỏng và lời giải dùng trong video)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

SAI_SO_CHO_PHEP = 0.05  # cm


def _vong_kin(PID, kp, ki, kd, ten):
    cua_ban = goc.lech_cuoi(goc.chay(PID(kp, ki, kd)))
    dap_an = goc.lech_cuoi(goc.KET_QUA[ten])
    assert abs(cua_ban - dap_an) <= SAI_SO_CHO_PHEP, \
        f"chạy vòng kín {ten}: robot lệch cuối {cua_ban:+.1f} cm, đáp án {dap_an:+.1f} cm"
    return cua_ban


def bai_1(ns):
    PID = ham(ns, "PID")
    w = PID(2.0, 0, 0).lenh(0.3)
    assert gan(w, 0.6), f"Kp = 2, e = 0.3 phải ra ω = 0.6, bạn ra {w}"
    w = PID(1.5, 0, 0).lenh(-0.2)
    assert gan(w, -0.3), f"Kp = 1.5, e = −0.2 phải ra ω = −0.3, bạn ra {w}"
    return f"chỉ P: robot lắc qua lắc lại quanh vạch như video (lệch TB 3 s cuối {_vong_kin(PID, 1.5, 0, 0, 'P'):+.1f} cm)"


def bai_2(ns):
    PID = ham(ns, "PID")
    c = PID(0, 0, 2.0)
    w1, w2 = c.lenh(0.3), c.lenh(0.2)
    assert gan(w1, 0.0), f"bước đầu chưa có e_trước nên de/dt = 0, ω phải = 0, bạn ra {w1}"
    assert gan(w2, -20.0), f"e: 0.3 → 0.2 trong dt = 0.01 s nên de/dt = −10, với Kd = 2 thì ω = −20, bạn ra {w2}"
    return f"PD: robot lệch {_vong_kin(PID, 1.5, 0, 2.8, 'PD'):+.1f} cm (hết lắc nhưng bánh yếu vẫn kéo lệch)"


def bai_3(ns):
    PID = ham(ns, "PID")
    c = PID(0, 5.0, 0)
    w1, w2 = c.lenh(0.3), c.lenh(0.3)
    assert gan(w1, 0.015), f"sau bước 1: ∫e dt = 0.3·0.01 = 0.003, Ki = 5 → ω = 0.015, bạn ra {w1}"
    assert gan(w2, 0.03), f"sau bước 2: ∫e dt = 0.006 → ω = 0.03, bạn ra {w2}"
    return f"PID: robot lệch {_vong_kin(PID, 1.5, 0.6, 2.8, 'PID'):+.1f} cm (I đã khử phần lệch còn lại)"


BAI = [("Bài 1 · thành phần P", bai_1), ("Bài 2 · thành phần D", bai_2), ("Bài 3 · thành phần I", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    chay_tu_dong_lenh(BAI, "pid_cua_ban", goc)
