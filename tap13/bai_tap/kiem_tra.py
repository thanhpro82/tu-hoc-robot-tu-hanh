"""Tự chấm bài tập tập 1.3. Chạy: python -X utf8 kiem_tra.py

Mỗi bài có 2 bước kiểm tra:
  1. Thử hàm với vài con số tính tay được.
  2. Cho robot chạy 16 giây bằng PID của bạn trong đúng mô phỏng của video, so độ lệch cuối với lời giải.
Trong notebook thì gọi: from kiem_tra import cham; cham(PID)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
import pid as goc  # noqa: E402  (mô phỏng và lời giải dùng trong video)

SAI_SO_CHO_PHEP = 0.05  # cm


def _gan(a, b, tol=1e-9):
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=tol)


def _vong_kin(PID, kp, ki, kd, ten):
    cua_ban = goc.lech_cuoi(goc.chay(PID(kp, ki, kd)))
    dap_an = goc.lech_cuoi(goc.KET_QUA[ten])
    assert abs(cua_ban - dap_an) <= SAI_SO_CHO_PHEP, \
        f"chạy vòng kín {ten}: robot lệch cuối {cua_ban:+.1f} cm, đáp án {dap_an:+.1f} cm"
    return cua_ban


def bai_1(PID):
    w = PID(2.0, 0, 0).lenh(0.3)
    assert _gan(w, 0.6), f"Kp = 2, e = 0.3 phải ra ω = 0.6, bạn ra {w}"
    w = PID(1.5, 0, 0).lenh(-0.2)
    assert _gan(w, -0.3), f"Kp = 1.5, e = −0.2 phải ra ω = −0.3, bạn ra {w}"
    return f"chỉ P: robot lắc qua lắc lại quanh vạch như video (lệch TB 3 s cuối {_vong_kin(PID, 1.5, 0, 0, 'P'):+.1f} cm)"


def bai_2(PID):
    c = PID(0, 0, 2.0)
    w1, w2 = c.lenh(0.3), c.lenh(0.2)
    assert _gan(w1, 0.0), f"bước đầu chưa có e_trước nên de/dt = 0, ω phải = 0, bạn ra {w1}"
    assert _gan(w2, -20.0, 1e-6), f"e: 0.3 → 0.2 trong dt = 0.01 s nên de/dt = −10, với Kd = 2 thì ω = −20, bạn ra {w2}"
    return f"PD: robot lệch {_vong_kin(PID, 1.5, 0, 2.8, 'PD'):+.1f} cm (hết lắc nhưng bánh yếu vẫn kéo lệch)"


def bai_3(PID):
    c = PID(0, 5.0, 0)
    w1, w2 = c.lenh(0.3), c.lenh(0.3)
    assert _gan(w1, 0.015), f"sau bước 1: ∫e dt = 0.3·0.01 = 0.003, Ki = 5 → ω = 0.015, bạn ra {w1}"
    assert _gan(w2, 0.03), f"sau bước 2: ∫e dt = 0.006 → ω = 0.03, bạn ra {w2}"
    return f"PID: robot lệch {_vong_kin(PID, 1.5, 0.6, 2.8, 'PID'):+.1f} cm (I đã khử phần lệch còn lại)"


BAI = [("Bài 1 · thành phần P", bai_1), ("Bài 2 · thành phần D", bai_2), ("Bài 3 · thành phần I", bai_3)]


def cham(PID):
    """Chấm cả 3 bài, in kết quả, trả về số bài đạt."""
    dat = 0
    for i, (ten, f) in enumerate(BAI):
        try:
            print(f"✅ {ten}: {f(PID)}")
            dat += 1
        except NotImplementedError:
            print(f"⏳ {ten}: chưa làm")
        except AssertionError as loi:
            print(f"❌ {ten}: {loi}" + ("\n   (bài này chạy cả các thành phần trước, hãy sửa bài trước cho đạt đã)" if dat < i else ""))
        except Exception as loi:  # lỗi cú pháp, sai tên biến, ...
            print(f"💥 {ten}: code bị lỗi {type(loi).__name__}: {loi}")
    print(f"\nĐạt {dat}/{len(BAI)} bài." + ("  🎉 Xong! Thử phần Thử thách trong README nhé." if dat == len(BAI) else ""))
    return dat


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:  # tự kiểm tra bộ chấm bằng lời giải gốc
        cham(goc.PID)
    else:
        from pid_cua_ban import PID
        cham(PID)
