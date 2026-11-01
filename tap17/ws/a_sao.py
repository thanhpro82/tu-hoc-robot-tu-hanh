"""Tập 1.5 - A*: tìm đường như Google Maps (series Tự Học Robot Tự Hành)

Theo Mục 4.2 / 4.2.1, Chương 4, Principles of Robot Autonomy:
  - Lưới ô: ô trống là đỉnh, ô kề nhau (8 hướng) nối bằng cạnh -> đồ thị G = (V, E).
  - Dijkstra: luôn mở ô có chi phí đi tới C(q) nhỏ nhất.
  - A*: luôn mở ô có f(q) = C(q) + h(q) nhỏ nhất, h = khoảng cách Euclid tới đích.
    h không bao giờ ước lượng quá chi phí thật (admissible) -> đường tìm được vẫn ngắn nhất.
Chạy: python a_sao.py
"""
import heapq
import math

# Bản đồ: '#' tường, 'S' xuất phát, 'G' đích, '.' ô trống (mỗi ô 0.25 m)
BAN_DO = [
    "..................",
    "..........#......G",
    "..........#.......",
    "....#######.......",
    "..........#.......",
    "..........#..#####",
    "..........#.......",
    "....#.....#.......",
    "....#.............",
    "....#.....#.......",
    "....#######.......",
    "....#.............",
    "....#.............",
    "S...#.............",
    "....#.............",
]
ROWS, COLS = len(BAN_DO), len(BAN_DO[0])
O_M = 0.25  # cạnh mỗi ô, mét


def tim(ky_tu):
    for r, dong in enumerate(BAN_DO):
        if ky_tu in dong:
            return r, dong.index(ky_tu)


START, GOAL = tim("S"), tim("G")
HUONG = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def ke(o):
    r, c = o
    for dr, dc in HUONG:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < ROWS and 0 <= nc < COLS) or BAN_DO[nr][nc] == "#":
            continue
        if dr and dc and (BAN_DO[r][nc] == "#" or BAN_DO[nr][c] == "#"):
            continue  # không cắt chéo qua góc tường
        yield (nr, nc), math.hypot(dr, dc)


def h_euclid(o):
    return math.hypot(o[0] - GOAL[0], o[1] - GOAL[1])


def tim_duong(h):
    """Label correcting với hàng đợi ưu tiên. h = 0 -> Dijkstra, h = Euclid -> A*."""
    C = {START: 0.0}
    truoc = {START: None}
    frontier = [(h(START), 0, START)]
    da_mo, thu_tu = set(), []
    dem = 0
    while frontier:
        _, _, o = heapq.heappop(frontier)
        if o in da_mo:
            continue
        da_mo.add(o)
        thu_tu.append(o)
        if o == GOAL:
            break
        for o2, chi_phi in ke(o):
            c2 = C[o] + chi_phi
            if c2 < C.get(o2, math.inf):
                C[o2], truoc[o2] = c2, o
                dem += 1
                heapq.heappush(frontier, (c2 + h(o2), dem, o2))
    duong, o = [], GOAL
    while o is not None:
        duong.append(o)
        o = truoc[o]
    return duong[::-1], thu_tu, C[GOAL]


DIJKSTRA = tim_duong(lambda o: 0.0)
A_SAO = tim_duong(h_euclid)

if __name__ == "__main__":
    tong_o = sum(dong.count(".") for dong in BAN_DO) + 2
    print(f"Lưới {ROWS}x{COLS}, {tong_o} ô trống, mỗi ô {O_M} m, nối 8 hướng")
    for ten, (duong, mo, chi_phi) in [("Dijkstra", DIJKSTRA), ("A*", A_SAO)]:
        print(f"{ten:8s}: mở {len(mo):3d} ô, đường đi {len(duong)} ô, dài {chi_phi * O_M:.2f} m")
