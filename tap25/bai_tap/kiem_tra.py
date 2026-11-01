"""Tự chấm bài tập tập 2.5. Chạy: python -X utf8 kiem_tra.py   (thêm --loi-giai để chấm thử lời giải)
Trong notebook: cham(globals())
"""
import sys
from pathlib import Path

import numpy as np

_D = Path(__file__).resolve().parent
sys.path[:0] = [str(_D), str(_D.parent / "sim"), str(_D.parents[1])]
import sfm as goc  # noqa: E402  (mô phỏng trong video: dựng lại cả ngôi nhà lúc import, mất vài giây)
from chung.cham import cham as _cham, chay_tu_dong_lenh, gan, ham  # noqa: E402

CHUNG = sorted(set(goc.QUAN_SAT[0]) & set(goc.QUAN_SAT[1]))
P1_ANH = np.array([goc.QUAN_SAT[0][j] for j in CHUNG])
P2_ANH = np.array([goc.QUAN_SAT[1][j] for j in CHUNG])


def hai_anh_voi(tim_F, tam_giac, dem):
    """Chạy bước hai ảnh của video bằng hàm của bạn: trả về số điểm trước camera của 4 nghiệm."""
    F = tim_F(P1_ANH, P2_ANH)
    E = goc.K.T @ F @ goc.K
    U, _, Vt = np.linalg.svd(E.T)
    if np.linalg.det(U) < 0:
        U = -U
    if np.linalg.det(Vt) < 0:
        Vt = -Vt
    Wz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    P1 = goc.K @ np.hstack([np.eye(3), np.zeros((3, 1))])
    dem_4 = []
    for R, t in [(U @ Wz @ Vt, U[:, 2]), (U @ Wz @ Vt, -U[:, 2]), (U @ Wz.T @ Vt, U[:, 2]), (U @ Wz.T @ Vt, -U[:, 2])]:
        X = tam_giac(P1, goc.K @ np.hstack([R, t[:, None]]), P1_ANH, P2_ANH)
        dem_4.append(dem(R, t, X))
    return dem_4


def _chuan(F):
    F = np.asarray(F, dtype=float)
    F = F / np.linalg.norm(F)
    return F * np.sign(F.flat[np.argmax(np.abs(F))])


def bai_1(ns):
    F = ham(ns, "tim_F")(P1_ANH, P2_ANH)
    assert np.shape(F) == (3, 3), f"F phải là ma trận 3×3, bạn ra hình {np.shape(F)}"
    assert gan(_chuan(F), _chuan(goc.tim_F(P1_ANH, P2_ANH)), 1e-6), "F chưa khớp đáp án (chuẩn hoá → outer(a, b) → SVD → ép hạng 2 → bỏ chuẩn hoá)"
    loi = np.abs(np.einsum("ni,ij,nj->n", np.column_stack([P1_ANH, np.ones(len(CHUNG))]), F,
                           np.column_stack([P2_ANH, np.ones(len(CHUNG))]))) / np.linalg.norm(F)
    return f"{len(CHUNG)} cặp điểm chung → F hạng {np.linalg.matrix_rank(F, tol=1e-9 * np.abs(F).max())}; p1ᵀFp2 trung bình {loi.mean():.1e} (≈ 0)"


def bai_2(ns):
    f = ham(ns, "tam_giac")
    (R, t), (R1, t1) = goc.CAM_THAT[0], goc.CAM_THAT[1]
    P1, P2 = goc.K @ np.hstack([R, t[:, None]]), goc.K @ np.hstack([R1, t1[:, None]])
    ids = CHUNG[:30]
    x1, _ = goc.chieu(R, t, goc.P_THAT[ids])
    x2, _ = goc.chieu(R1, t1, goc.P_THAT[ids])
    X = np.asarray(f(P1, P2, x1, x2))
    assert X.shape == (30, 3), f"phải trả về mảng (30, 3), bạn ra {X.shape}"
    assert gan(X, goc.P_THAT[ids], 1e-6), "với camera thật và pixel không nhiễu, tam giác hoá phải ra đúng điểm 3D thật"
    X = np.asarray(f(P1, P2, P1_ANH, P2_ANH))
    loi = np.linalg.norm(X - goc.P_THAT[CHUNG], axis=1)
    return f"không nhiễu: ra đúng điểm thật; với pixel nhiễu 0.7 px: lệch trung bình {loi.mean() * 100:.1f} cm"


def bai_3(ns):
    f = ham(ns, "dem_truoc_camera")
    X = np.array([[0, 0, 2.0], [0, 0, -1.0], [0, 0, 5.0]])
    assert f(np.eye(3), np.array([0, 0, 0.0]), X) == 2, "2 trong 3 điểm có z > 0 ở cả hai camera (camera 2 trùng camera 1)"
    assert f(np.eye(3), np.array([0, 0, -3.0]), X) == 1, "t = (0, 0, −3) nên z2 = z − 3: chỉ điểm z = 5 nằm trước cả hai camera"
    dem_4 = hai_anh_voi(ham(ns, "tim_F"), ham(ns, "tam_giac"), f)
    assert dem_4 == goc.DEM_4, f"4 nghiệm phải cho {goc.DEM_4} điểm trước camera như video, bạn ra {dem_4}"
    return f"4 nghiệm (R, t) cho {dem_4} điểm trước cả hai camera: chỉ một nghiệm đúng, như video"


BAI = [("Bài 1 · ma trận cơ bản F", bai_1), ("Bài 2 · tam giác hoá", bai_2), ("Bài 3 · chọn nghiệm (R, t)", bai_3)]


def cham(ns):
    return _cham(ns, BAI)


if __name__ == "__main__":
    import loi_giai
    chay_tu_dong_lenh(BAI, "sfm_cua_ban", loi_giai)
