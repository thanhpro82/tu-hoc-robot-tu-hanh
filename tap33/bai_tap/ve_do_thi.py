"""Vẽ: (trái) Phần A, 1500 mẫu Monte Carlo sau khi đi thẳng 2 m với hướng mơ hồ ±35°, cùng elip 2σ của EKF và UKF (hàm của bạn);
(phải) Phần B, đường đi thật, chỉ odometry, EKF và UKF (lần chạy của video).

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import ekf_ukf as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import rms  # noqa: E402


def _elip(ax, mu, cov, mau, nhan):
    w, v = np.linalg.eigh(cov)
    t = np.linspace(0, 2 * np.pi, 100)
    pts = (v @ np.diag(2 * np.sqrt(np.maximum(w, 0))) @ np.vstack([np.cos(t), np.sin(t)])).T + mu
    ax.plot(pts[:, 0], pts[:, 1], color=mau, lw=2.2, label=nhan)
    ax.plot(*mu, "o", color=mau, ms=6)


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    Fa = lay("F_jac")(goc.MU_A, goc.U_A, goc.DT_A)
    X, Wm, Wc = lay("diem_sigma")(goc.MU_A, goc.SIG_A)
    Y = np.array([goc.f(x, goc.U_A, goc.DT_A) for x in X])
    mu_u = Wm @ Y[:, :2]
    cov_u = sum(Wc[i] * np.outer(Y[i, :2] - mu_u, Y[i, :2] - mu_u) for i in range(len(X)))
    fig, (a, b) = V.tao(1, 2, rong=12.5, cao=5.2)
    a.scatter(goc.MC_MAU[:, 0], goc.MC_MAU[:, 1], s=4, color=V.MAU["xam"], alpha=0.6, label="Monte Carlo (sự thật)")
    _elip(a, goc.MC_MU, goc.MC_COV, "white", "elip của sự thật")
    _elip(a, goc.EKF_MU, (Fa @ goc.SIG_A @ Fa.T)[:2, :2], V.MAU["do"], "EKF (tuyến tính hoá)")
    _elip(a, mu_u, cov_u, V.MAU["luc"], "UKF (7 điểm sigma)")
    a.scatter(Y[:, 0], Y[:, 1], marker="x", color=V.MAU["luc"], s=40)
    V.trang_tri(a, "Đi thẳng 2 m khi hướng mơ hồ ±35°", "x (m)", "y (m)")
    a.set_aspect("equal", adjustable="datalim")
    V.chu_giai(a, loc="upper left", fontsize=8.5)
    L = goc.LOG_B
    for key, mau, nhan in [("x", "white", "thật"), ("dr", V.MAU["xam"], f"chỉ odometry: {rms(L, 'dr') * 100:.0f} cm"),
                           ("ekf", V.MAU["do"], f"EKF: {rms(L, 'ekf') * 100:.1f} cm"), ("ukf", V.MAU["luc"], f"UKF: {rms(L, 'ukf') * 100:.1f} cm")]:
        P = np.array([r[key][:2] for r in L])
        b.plot(P[:, 0], P[:, 1], color=mau, lw=2 if key != "x" else 2.6, label=nhan)
    b.scatter(goc.MOC[:, 0], goc.MOC[:, 1], marker="*", s=220, color=V.MAU["vang"], label="mốc", zorder=5)
    V.trang_tri(b, "Định vị 60 s, đo 2 mốc mỗi giây (RMS)", "x (m)", "y (m)")
    b.set_aspect("equal", adjustable="datalim")
    V.chu_giai(b, loc="lower right", fontsize=8.5)
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import ekf_ukf_cua_ban
        ve(ekf_ukf_cua_ban)
