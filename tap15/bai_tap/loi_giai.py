"""Lời giải bài tập tập 1.5 (viết lại code video thành hàm nhận bản đồ). Tự làm a_sao_cua_ban.py trước rồi hãy mở!"""
import heapq
import math

HUONG = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def ke(o, ban_do):
    r, c = o
    ra = []
    for dr, dc in HUONG:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < len(ban_do) and 0 <= nc < len(ban_do[0])) or ban_do[nr][nc] == "#":
            continue
        if dr and dc and (ban_do[r][nc] == "#" or ban_do[nr][c] == "#"):
            continue
        ra.append(((nr, nc), math.hypot(dr, dc)))
    return ra


def h_euclid(o, dich):
    return math.hypot(o[0] - dich[0], o[1] - dich[1])


def tim_duong(bat_dau, dich, ban_do, h):
    C, truoc = {bat_dau: 0.0}, {bat_dau: None}
    hang_doi, da_mo, dem = [(h(bat_dau), 0, bat_dau)], set(), 0
    while hang_doi:
        _, _, o = heapq.heappop(hang_doi)
        if o in da_mo:
            continue
        da_mo.add(o)
        if o == dich:
            break
        for o2, cp in ke(o, ban_do):
            if C[o] + cp < C.get(o2, math.inf):
                C[o2], truoc[o2] = C[o] + cp, o
                dem += 1
                heapq.heappush(hang_doi, (C[o2] + h(o2), dem, o2))
    duong, o = [], dich
    while o is not None:
        duong.append(o)
        o = truoc[o]
    return duong[::-1], len(da_mo), C[dich]
