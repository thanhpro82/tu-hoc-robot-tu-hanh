"""Tập 1.2 - Nhắm mắt mà chạy: điều khiển vòng hở (series Tự Học Robot Tự Hành)

Chương 2, Principles of Robot Autonomy: open-loop control & trajectory optimization.
  1. Tính sẵn chuỗi lệnh cho hình vuông 1 m, chạy mà không nhìn lại.
  2. Mô phỏng hoàn hảo -> về đúng chỗ cũ. Có sai số nhỏ -> lệch dần qua từng vòng.
  3. Tối ưu quỹ đạo: lệnh tốc độ nhanh nhất khi động cơ có giới hạn gia tốc = hình thang.
Chạy: python vong_ho.py
"""
import math
import random

dt = 0.01


def step(x, y, theta, v, omega):
    """Xe 2 bánh, giữ nguyên từ tập 0.2."""
    return x + v * math.cos(theta) * dt, y + v * math.sin(theta) * dt, theta + omega * dt


# ── 1. Kế hoạch vòng hở: hình vuông 1 m ─────────────────────────────────────

CANH = 1.0
V = 0.5
KE_HOACH = [(CANH / V, V, 0.0), (1.0, 0.0, math.pi / 2)] * 4  # (giây, v, ω): thẳng 2 s, quay 90° trong 1 s


def chay(ke_hoach, so_vong=1, sai_so=None, seed=0):
    """Thực thi đúng chuỗi lệnh, không hề đo lại vị trí (vòng hở).

    sai_so: robot "thật" làm khác lệnh một chút:
      v_ty_le     bánh xe nhỏ hơn thiết kế -> chạy ngắn hơn
      w_ty_le     quay hụt
      w_lech      lệch hướng do 2 động cơ không đều
      nhieu       rung lắc ngẫu nhiên
    """
    rng = random.Random(seed)
    x, y, th = 0.0, 0.0, 0.0
    path, cuoi_vong = [(x, y, th)], []
    for _ in range(so_vong):
        for giay, v, w in ke_hoach:
            for _ in range(round(giay / dt)):
                if sai_so:
                    v_thuc = v * sai_so["v_ty_le"] * (1 + rng.gauss(0, sai_so["nhieu"]))
                    w_thuc = w * sai_so["w_ty_le"] + (sai_so["w_lech"] if v else 0) + rng.gauss(0, sai_so["nhieu"])
                else:
                    v_thuc, w_thuc = v, w
                x, y, th = step(x, y, th, v_thuc, w_thuc)
                path.append((x, y, th))
        cuoi_vong.append(math.hypot(x, y))
    return path, cuoi_vong


# Bánh nhỏ hơn 2%, mỗi lần quay hụt 3% (~2.7°), lúc chạy thẳng hơi lệch phải
ROBOT_THAT = {"v_ty_le": 0.98, "w_ty_le": 0.97, "w_lech": -0.02, "nhieu": 0.05}

ly_tuong, lech_ly_tuong = chay(KE_HOACH)
thuc_te, lech_thuc_te = chay(KE_HOACH, so_vong=3, sai_so=ROBOT_THAT, seed=3)

# ── 3. Tối ưu quỹ đạo: chạy 1 m nhanh nhất với |gia tốc| <= A_MAX, |v| <= V_MAX ──

V_MAX = 0.5
A_MAX = 0.5


def hinh_thang(quang_duong=CANH, v_max=V_MAX, a_max=A_MAX):
    """Lời giải thời gian ngắn nhất (bang-bang): tăng tốc hết cỡ, chạy đều, phanh hết cỡ."""
    t_tang = v_max / a_max
    d_tang = 0.5 * a_max * t_tang**2
    if 2 * d_tang > quang_duong:  # quá ngắn, không kịp đạt v_max -> hình tam giác
        t_tang = math.sqrt(quang_duong / a_max)
        v_max = a_max * t_tang
        d_tang = quang_duong / 2
    t_deu = (quang_duong - 2 * d_tang) / v_max
    T = 2 * t_tang + t_deu
    v = []
    for i in range(round(T / dt) + 1):
        t = i * dt
        v.append(min(a_max * t, v_max, a_max * (T - t)))
    return v, T


van_toc_toi_uu, T_toi_uu = hinh_thang()

if __name__ == "__main__":
    print(f"Hình vuông lý tưởng: lệch {lech_ly_tuong[0] * 100:.1f} cm khi về đích")
    for i, d in enumerate(lech_thuc_te, 1):
        print(f"Robot có sai số, sau vòng {i}: lệch {d * 100:.0f} cm")
    quang_duong = sum(van_toc_toi_uu) * dt
    print(f"Hình thang: {T_toi_uu:.1f} s cho {quang_duong:.2f} m (v_max {V_MAX} m/s, a_max {A_MAX} m/s²)")
