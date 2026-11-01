"""Vẽ: (trên) sai số vị trí theo thời gian: chỉ cảm biến, chỉ tích phân gia tốc kế, Kalman của bạn;
(dưới) hệ số Kalman K và độ bất định σ theo thời gian.

Chạy: python -X utf8 ve_do_thi.py            -> dùng hàm của bạn, ra ket_qua.png
      python -X utf8 ve_do_thi.py --loi-giai  -> dùng lời giải
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import kalman as goc  # noqa: E402
from chung import ve as V  # noqa: E402
from kiem_tra import DS_U, DS_Z, MU0, P, SIG0, _rms  # noqa: E402


def ve(ns, ra="ket_qua.png"):
    lay = (lambda t: ns[t]) if isinstance(ns, dict) else (lambda t: getattr(ns, t))
    mu, Sig, Ks, sig = MU0, SIG0, [], []
    p_hat = []
    for u, z in zip(DS_U, DS_Z):
        mu, Sig = lay("du_doan")(mu, Sig, u)
        mu, Sig, K = lay("cap_nhat")(mu, Sig, z)
        p_hat.append(mu[0]); Ks.append(float(np.asarray(K)[0, 0])); sig.append(float(np.sqrt(Sig[0, 0])))
    t = [r["t"] for r in goc.LOG]
    dr = np.array([r["dr"] for r in goc.LOG])
    fig, (a, b) = V.tao(2, 1, rong=11, cao=6.4, sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})
    a.plot(t, (np.array(DS_Z) - P) * 100, color=V.MAU["xam"], lw=1, label=f"chỉ cảm biến: RMS {_rms(np.array(DS_Z) - P) * 100:.1f} cm")
    a.plot(t, (dr - P) * 100, color=V.MAU["do"], lw=2, label=f"chỉ gia tốc kế: cuối lệch {abs(dr[-1] - P[-1]):.2f} m")
    a.plot(t, (np.array(p_hat) - P) * 100, color=V.MAU["cam"], lw=2.2, label=f"Kalman: RMS {_rms(np.array(p_hat) - P) * 100:.1f} cm")
    a.set_ylim(-110, 110)
    V.trang_tri(a, "Sai số vị trí (cm)", None, "đo/ước lượng − thật (cm)")
    V.chu_giai(a, loc="lower left", fontsize=8.8)
    b.plot(t, Ks, color=V.MAU["vang"], lw=2, label="K (vị trí)")
    b2 = b.twinx()
    b2.plot(t, np.array(sig) * 100, color=V.MAU["lam"], lw=2, label="σ sau cập nhật (cm)")
    b2.tick_params(colors="#94a3b8")
    b2.set_ylabel("σ (cm)", color=V.CHU)
    V.trang_tri(b, f"K giảm từ {Ks[0]:.3f} còn {Ks[-1]:.3f}: càng về sau càng tin dự đoán", "thời gian (s)", "K")
    b.legend(handles=b.get_lines() + b2.get_lines(), facecolor="#111827", edgecolor=V.VIEN, labelcolor="#e2e8f0", fontsize=8.8, loc="upper right")
    V.luu(fig, ra)


if __name__ == "__main__":
    if "--loi-giai" in sys.argv:
        import loi_giai
        ve(loi_giai, sys.argv[-1] if sys.argv[-1].endswith(".png") else "ket_qua.png")
    else:
        import kalman_cua_ban
        ve(kalman_cua_ban)
