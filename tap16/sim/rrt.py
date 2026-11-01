"""Tập 1.6 - RRT: tìm đường bằng cách gieo ngẫu nhiên (series Tự Học Robot Tự Hành)

Theo Mục 4.4.2, Chương 4, Principles of Robot Autonomy. Mỗi vòng lặp RRT:
  1. lấy mẫu q_rand (xác suất ALPHA lấy luôn đích q_G: goal biasing)
  2. tìm đỉnh gần nhất q_near trên cây T (khoảng cách Euclid)
  3. tiến từ q_near về phía q_rand một đoạn BUOC -> q_new, kiểm tra không va chạm
  4. gắn q_new vào cây với cạnh từ q_near
RRT* (mở rộng, theo Karaman & Frazzoli 2011 mà sách trích dẫn): khi gắn q_new thì chọn cha
tốt nhất trong bán kính r, rồi "nối lại" (rewire) các đỉnh lân cận nếu đi qua q_new rẻ hơn.
Chạy: python rrt.py
"""
import math
import random

W, H = 10.0, 8.4  # kích thước không gian, mét
Q_S, Q_G = (0.8, 0.8), (9.2, 7.6)
TUONG = [  # (x, y, rộng, cao)
    (2.5, 0.0, 0.6, 5.6),
    (5.2, 2.8, 0.6, 5.6),
    (7.4, 0.0, 0.6, 4.4),
    (2.5, 6.6, 2.0, 0.6),
]
BUOC = 0.5
ALPHA = 0.1
DIEM_DICH = 0.4  # coi là tới đích khi cách đích dưới 0.4 m


def trong_tuong(x, y, le=0.1):
    return any(tx - le <= x <= tx + tw + le and ty - le <= y <= ty + th + le for tx, ty, tw, th in TUONG)


def khong_va_cham(a, b):
    """CollisionFree cho đoạn a -> b: kiểm tra các điểm cách nhau 5 cm."""
    n = max(1, int(math.dist(a, b) / 0.05))
    return all(not trong_tuong(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1))


def rrt(seed=2, toi_da=3000, sao=False, tiep_sau_dich=0):
    """Trả về: danh sách đỉnh, cha, chi phí, thứ tự (q_rand, q_new) và lịch sử độ dài đường tốt nhất."""
    rng = random.Random(seed)
    V, cha, cost = [Q_S], [-1], [0.0]
    lich_su, ghi = [], []
    tot_nhat, i_dich, lan_dau = math.inf, None, None
    for k in range(toi_da):
        q_rand = Q_G if rng.random() < ALPHA else (rng.uniform(0, W), rng.uniform(0, H))
        i_near = min(range(len(V)), key=lambda i: math.dist(V[i], q_rand))
        q_near = V[i_near]
        d = math.dist(q_near, q_rand)
        if d < 1e-9:
            continue
        s = min(1.0, BUOC / d)
        q_new = (q_near[0] + (q_rand[0] - q_near[0]) * s, q_near[1] + (q_rand[1] - q_near[1]) * s)
        if not (0 <= q_new[0] <= W and 0 <= q_new[1] <= H) or not khong_va_cham(q_near, q_new):
            ghi.append((q_rand, None))
            continue
        p, c = i_near, cost[i_near] + math.dist(q_near, q_new)
        if sao:  # chọn cha rẻ nhất trong bán kính r
            r = 1.2
            lan_can = [i for i in range(len(V)) if math.dist(V[i], q_new) <= r]
            for i in lan_can:
                ci = cost[i] + math.dist(V[i], q_new)
                if ci < c and khong_va_cham(V[i], q_new):
                    p, c = i, ci
        V.append(q_new)
        cha.append(p)
        cost.append(c)
        j = len(V) - 1
        if sao:  # nối lại các đỉnh lân cận qua q_new nếu rẻ hơn
            for i in lan_can:
                ci = c + math.dist(q_new, V[i])
                if ci < cost[i] and khong_va_cham(q_new, V[i]):
                    cha[i], cost[i] = j, ci
                    # cập nhật chi phí cho cả nhánh con của i
                    hang = [i]
                    while hang:
                        u = hang.pop()
                        for w, pw in enumerate(cha):
                            if pw == u:
                                cost[w] = cost[u] + math.dist(V[u], V[w])
                                hang.append(w)
        ghi.append((q_rand, q_new))
        if math.dist(q_new, Q_G) < DIEM_DICH and c + math.dist(q_new, Q_G) < tot_nhat:
            i_dich = j
        if i_dich is not None:
            tot_nhat = cost[i_dich] + math.dist(V[i_dich], Q_G)
            lan_dau = lan_dau or (k + 1)
        lich_su.append(tot_nhat)
        if i_dich is not None and not sao and k + 1 >= (lan_dau + tiep_sau_dich):
            break
    duong = []
    i = i_dich
    while i is not None and i >= 0:
        duong.append(V[i])
        i = cha[i]
    duong = duong[::-1] + [Q_G] if duong else []
    return {"V": V, "cha": cha, "ghi": ghi, "duong": duong, "dai": tot_nhat, "vong_tim_thay": lan_dau, "lich_su": lich_su}


RRT = rrt(sao=False)
RRT_SAO = rrt(sao=True, toi_da=2500)


def dai_sau(ket_qua, n):
    v = ket_qua["lich_su"][min(n, len(ket_qua["lich_su"])) - 1]
    return v


if __name__ == "__main__":
    print(f"Không gian {W}x{H} m, bước {BUOC} m, goal bias α = {ALPHA}")
    print(f"Lưới 100 nấc/khớp: robot 2 khớp = {100**2:,} ô, cánh tay 6 khớp = {100**6:,} ô")
    print(f"RRT : tìm thấy đường sau {RRT['vong_tim_thay']} vòng, cây {len(RRT['V'])} đỉnh, đường dài {RRT['dai']:.2f} m")
    for n in (300, 800, 1500, 2500):
        print(f"RRT*: sau {n:4d} vòng, đường tốt nhất dài {dai_sau(RRT_SAO, n):.2f} m")
    print(f"Đường thẳng xuất phát→đích (không tính tường): {math.dist(Q_S, Q_G):.2f} m")


def ti_le_tim_thay(so_lan=30, moc=(250, 500, 1000, 2000, 4000)):
    """Đầy đủ theo xác suất: chạy RRT nhiều lần, tỉ lệ đã tìm ra đường sau N vòng."""
    vong = [rrt(seed=100 + s, toi_da=max(moc))["vong_tim_thay"] for s in range(so_lan)]
    return {n: sum(1 for v in vong if v is not None and v <= n) / so_lan for n in moc}


if __name__ == "__main__":
    for n, p in ti_le_tim_thay().items():
        print(f"Sau {n:4d} vòng: {p * 100:.0f}% số lần chạy đã tìm ra đường")
