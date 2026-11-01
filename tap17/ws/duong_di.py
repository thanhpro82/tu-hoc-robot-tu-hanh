"""Đổi ô lưới sang mét, làm mượt đường A* (dùng chung cho planner_node và script xuất dữ liệu)."""
import math

import a_sao

O = a_sao.O_M


def o_sang_met(o):
    r, c = o
    return (c + 0.5) * O, (a_sao.ROWS - 1 - r + 0.5) * O


def lam_muot(pts, lan=3):
    """Cắt góc Chaikin: đường gấp khúc của lưới -> đường cong robot chạy được."""
    for _ in range(lan):
        moi = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            moi += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        pts = moi + [pts[-1]]
    return pts


def do_dai(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
