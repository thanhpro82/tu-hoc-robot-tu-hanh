"""Lời giải bài tập tập 2.8 (viết lại các hàm iou_tam, nms, ap_lop của ../sim/yolo.py bằng Python thuần).
Tự làm yolo_cua_ban.py trước rồi hãy mở!"""
import numpy as np


def iou(a, b):
    ax0, ay0, ax1, ay1 = a[0] - a[2] / 2, a[1] - a[3] / 2, a[0] + a[2] / 2, a[1] + a[3] / 2
    bx0, by0, bx1, by1 = b[0] - b[2] / 2, b[1] - b[3] / 2, b[0] + b[2] / 2, b[1] + b[3] / 2
    giao = max(0.0, min(ax1, bx1) - max(ax0, bx0)) * max(0.0, min(ay1, by1) - max(ay0, by0))
    return giao / (a[2] * a[3] + b[2] * b[3] - giao + 1e-9)


def nms(du_doan, nguong=0.5):
    giu = []
    for d in sorted(du_doan, key=lambda d: -d[1]):
        if all(d[0] != g[0] or iou(d[2:], g[2:]) < nguong for g in giu):
            giu.append(d)
    return giu


def ap_lop(du_doan, that, c, nguong_iou=0.5):
    ds = sorted([(s, k, box) for k, dd in enumerate(du_doan) for (cc, s, *box) in dd if cc == c], key=lambda z: -z[0])
    n_that = sum(1 for v in that for x in v if x[0] == c)
    da_khop = [set() for _ in that]
    tp = []
    for s, k, box in ds:
        best, bi = 0, -1
        for vi, v in enumerate(that[k]):
            if v[0] == c and vi not in da_khop[k]:
                u = iou(box, v[1:])
                if u > best:
                    best, bi = u, vi
        if best >= nguong_iou:
            da_khop[k].add(bi)
            tp.append(1)
        else:
            tp.append(0)
    tp = np.array(tp)
    tpc, fpc = np.cumsum(tp), np.cumsum(1 - tp)
    rec = tpc / max(n_that, 1)
    pre = tpc / np.maximum(tpc + fpc, 1)
    pre_mono = np.maximum.accumulate(pre[::-1])[::-1] if len(pre) else pre
    return float(np.sum(np.diff(np.concatenate([[0], rec])) * pre_mono)), rec, pre
