"""Kiểu vẽ dùng chung cho hình minh hoạ các tập (nền tối giống video)."""
import sys

import matplotlib

if "ipykernel" not in sys.modules:  # chạy script thì vẽ ra file; trong notebook giữ hiển thị trực tiếp
    matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NEN, CHU, LUOI, VIEN = "#0b1220", "#cbd5e1", "#1e293b", "#334155"
MAU = {"xanh": "#3b82f6", "luc": "#22c55e", "cam": "#f97316", "do": "#ef4444", "vang": "#f59e0b",
       "tim": "#a855f7", "xam": "#64748b", "trang": "#e2e8f0", "hong": "#ec4899", "lam": "#06b6d4"}


def tao(n=1, m=1, rong=9, cao=5, **kw):
    """Tạo figure nền tối với n×m ô."""
    plt.close("all")  # bỏ hình vẽ dở (vd. lần vẽ trước bị lỗi giữa chừng) để notebook không hiện thừa
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, axes = plt.subplots(n, m, figsize=(rong, cao), dpi=130, squeeze=False, **kw)
    fig.patch.set_facecolor(NEN)
    for ax in axes.flat:
        trang_tri(ax)
    return fig, (axes[0, 0] if n * m == 1 else axes.flatten())


def trang_tri(ax, tieu_de=None, x=None, y=None):
    ax.set_facecolor(NEN)
    ax.tick_params(colors="#94a3b8")
    for s in ax.spines.values():
        s.set_color(VIEN)
    ax.grid(color=LUOI)
    if tieu_de:
        ax.set_title(tieu_de, color="white", fontsize=12.5, loc="left")
    if x:
        ax.set_xlabel(x, color=CHU)
    if y:
        ax.set_ylabel(y, color=CHU)


def chu_giai(ax, **kw):
    kw = {"facecolor": "#111827", "edgecolor": VIEN, "labelcolor": "#e2e8f0", "fontsize": 9.5, **kw}
    return ax.legend(**kw)


def luu(fig, ra):
    fig.tight_layout()
    fig.savefig(ra, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("đã lưu", ra)
