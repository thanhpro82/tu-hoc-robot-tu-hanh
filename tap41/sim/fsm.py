"""Tập 4.1 - Bộ não hành vi: máy trạng thái hữu hạn (Chương 16, Principles of Robot Autonomy).

FSM theo §16.1: M = (S, I, O, n, s0), kiểu Mealy (quy ước của sách):
    s_{t+1} = n(s_t, i_t),   o_t = o(s_t, i_t),   t = 0, 1, 2, ... (mỗi nhịp 0,1 s)
Robot tuần tra trong phòng 8 × 6 m, có con mèo chạy lung tung (trốn sau tủ, chạy khi robot tới gần).
Ba phiên bản bộ não:
    A: TUẦN TRA ⇄ ĐUỔI (mất dấu là quay lại tuần tra ngay)
    B: A + TÌM (tới chỗ thấy mèo lần cuối, xoay nhìn quanh; mất dấu quá 8 s mới bỏ)
    C: B + VỀ SẠC + SẠC (pin < 25% thì về đốc)
Đầu vào i_t do khối "sinh sự kiện" tạo từ cảm biến, mỗi nhịp đúng 1 đầu vào theo thứ tự ưu tiên (FSM tất định).
Mọi thứ khác (thế giới, mèo, camera, pin, A*) là giả định của mô phỏng, không có trong sách.
"""
import heapq
import math

import numpy as np

DT = 0.1
O = 0.1                                   # ô lưới 10 cm
RONG, DAI = 8.0, 6.0
NX, NY = int(RONG / O), int(DAI / O)
VAT = [(2.0, 2.0, 3.0, 4.0, "tủ"), (5.0, 1.0, 6.5, 1.8, "sofa"), (5.6, 3.8, 6.6, 5.0, "bàn"), (0.0, 0.0, 1.0, 1.2, "kệ")]
DOC = (0.6, 5.3)
DIEM_TUAN = [(1.5, 4.6), (4.0, 5.2), (7.2, 5.3), (7.3, 2.8), (4.2, 0.6), (1.5, 2.2)]
TAM_NHIN, GOC_NHIN = 4.0, math.radians(45)
V_TUAN, V_DUOI, V_MEO, V_MEO_CHAY = 0.5, 0.8, 0.3, 0.9
HET_GIO_TIM = 8.0
PIN_YEU_NGUONG, PIN_DAY = 25.0, 95.0
TIEU_HAO = {"dung": 0.2, "di": 0.8, "duoi": 1.2}   # %/s (giả định)
SAC_NHANH = 4.0                                    # %/s

# ---------------- FSM: bảng n và o (Mealy) ----------------
S_ALL = ["TUAN_TRA", "DUOI", "TIM", "VE_SAC", "SAC"]
I_ALL = ["DAY_PIN", "TOI_DOC", "PIN_YEU", "THAY", "HET_GIO", "KHONG_THAY"]   # cũng là thứ tự ưu tiên
LENH = {"TUAN_TRA": "DI_DIEM_TUAN", "DUOI": "BAM_MEO", "TIM": "TOI_CHO_CUOI_XOAY", "VE_SAC": "VE_DOC", "SAC": "DUNG_SAC"}


def tao_fsm(ban):
    """Trả về (S, I, O, n, o, s0). Ô không ghi trong bảng = ở yên trạng thái cũ, giữ lệnh cũ (tự lặp)."""
    S = ["TUAN_TRA", "DUOI"] + (["TIM"] if ban in "BC" else []) + (["VE_SAC", "SAC"] if ban == "C" else [])
    I = I_ALL
    chuyen = {("TUAN_TRA", "THAY"): "DUOI"}
    if ban == "A":
        chuyen[("DUOI", "KHONG_THAY")] = "TUAN_TRA"
    else:
        chuyen.update({("DUOI", "KHONG_THAY"): "TIM", ("TIM", "THAY"): "DUOI", ("TIM", "HET_GIO"): "TUAN_TRA"})
    if ban == "C":
        for s in ("TUAN_TRA", "DUOI", "TIM"):
            chuyen[(s, "PIN_YEU")] = "VE_SAC"
        chuyen.update({("VE_SAC", "TOI_DOC"): "SAC", ("SAC", "DAY_PIN"): "TUAN_TRA"})
    n = {(s, i): chuyen.get((s, i), s) for s in S for i in I}
    o = {(s, i): LENH[n[(s, i)]] for s in S for i in I}      # lệnh xuất ra theo (s_t, i_t)
    Ox = sorted(set(o.values()))
    return S, I, Ox, n, o, "TUAN_TRA", chuyen


# ---------------- thế giới ----------------
def tao_luoi():
    m = np.zeros((NY, NX), bool)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = True
    for x0, y0, x1, y1, _ in VAT:
        m[int(y0 / O):int(math.ceil(y1 / O)), int(x0 / O):int(math.ceil(x1 / O))] = True
    return m


LUOI = tao_luoi()


def phong(m, r):
    k = int(round(r / O))
    out = m.copy()
    iy, ix = np.nonzero(m)
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy <= k * k:
                out[np.clip(iy + dy, 0, NY - 1), np.clip(ix + dx, 0, NX - 1)] = True
    return out


CAN_ROBOT = phong(LUOI, 0.3)
CAN_MEO = phong(LUOI, 0.15)
TRONG_MEO = np.argwhere(~CAN_MEO)
KE = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]


def o_luoi(p):
    return min(NY - 1, max(0, int(p[1] / O))), min(NX - 1, max(0, int(p[0] / O)))


def gan_nhat_trong(can, c):
    if not can[c]:
        return c
    free = np.argwhere(~can)
    return tuple(free[np.argmin(((free - np.array(c)) ** 2).sum(1))])


def a_sao(can, a, b):
    a, b = gan_nhat_trong(can, o_luoi(a)), gan_nhat_trong(can, o_luoi(b))
    g = {a: 0.0}
    cha = {}
    h = lambda c: math.hypot(c[0] - b[0], c[1] - b[1])
    mo = [(h(a), a)]
    while mo:
        _, c = heapq.heappop(mo)
        if c == b:
            break
        for dy, dx, w in KE:
            d = (c[0] + dy, c[1] + dx)
            if 0 <= d[0] < NY and 0 <= d[1] < NX and not can[d]:
                gd = g[c] + w
                if gd < g.get(d, 1e9):
                    g[d], cha[d] = gd, c
                    heapq.heappush(mo, (gd + h(d), d))
    if b not in g:
        return []
    duong = [b]
    while duong[-1] != a:
        duong.append(cha[duong[-1]])
    return [((c[1] + 0.5) * O, (c[0] + 0.5) * O) for c in duong[::-1]]


def nhin_thay(r, th, m):
    dx, dy = m[0] - r[0], m[1] - r[1]
    d = math.hypot(dx, dy)
    if d > TAM_NHIN or abs((math.atan2(dy, dx) - th + math.pi) % (2 * math.pi) - math.pi) > GOC_NHIN:
        return False
    for k in np.linspace(0, 1, max(2, int(d / 0.05))):
        if LUOI[o_luoi((r[0] + k * dx, r[1] + k * dy))]:
            return False
    return True


def goc(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


# ---------------- mô phỏng ----------------
def chay(ban, seed, T=90.0, co_pin=True, ghi=False):
    rng = np.random.default_rng(seed)
    S, I, Ox, n, o, s, _ = tao_fsm(ban)
    r = [1.5, 2.2, math.pi / 2]
    meo = [6.8, 2.6]
    pin = 100.0
    k_tuan = 0
    duong, dich_cu, t_lap = [], None, -1.0
    meo_duong, meo_chay = [], 0.0
    t_thay_cuoi, cho_cuoi, cho_that, v_meo = -1e9, None, None, (0.0, 0.0)
    mat_dau, t_mat, thay_truoc = [], None, False
    da_thay = False
    log = []
    thong_ke = {"thay": 0, "sau_lan_dau": 0, "bo_cuoc": 0, "chuyen": [], "t_het_pin": None, "pin_min": 100.0, "lan_sac": 0}
    chet = False
    for k in range(int(T / DT)):
        t = k * DT
        thay = (not chet) and nhin_thay(r[:2], r[2], meo)
        if thay:
            if t - t_thay_cuoi < 0.15 and cho_that is not None:      # ước lượng vận tốc mèo từ 2 lần thấy liền nhau
                v_meo = ((meo[0] - cho_that[0]) / DT, (meo[1] - cho_that[1]) / DT)
            t_thay_cuoi, cho_that, da_thay = t, tuple(meo), True
            # chỗ đoán mèo đã chạy tới: vị trí cuối + vận tốc × 1,5 s (kẹp trong phòng)
            cho_cuoi = (min(RONG - 0.4, max(0.4, meo[0] + 1.5 * v_meo[0])), min(DAI - 0.4, max(0.4, meo[1] + 1.5 * v_meo[1])))
        # khoảng mất dấu: từ lúc hết thấy tới lúc thấy lại
        if da_thay and thay_truoc and not thay:
            t_mat = t
        if thay and not thay_truoc and t_mat is not None:
            mat_dau.append(round(t - t_mat, 1))
            t_mat = None
        thay_truoc = thay
        o_doc = math.hypot(r[0] - DOC[0], r[1] - DOC[1]) < 0.25
        # ---- sinh sự kiện: đúng 1 đầu vào mỗi nhịp, theo thứ tự ưu tiên ----
        if o_doc and pin >= PIN_DAY and s == "SAC":
            i = "DAY_PIN"
        elif o_doc and s in ("VE_SAC", "SAC"):
            i = "TOI_DOC"
        elif co_pin and pin < PIN_YEU_NGUONG:
            i = "PIN_YEU"
        elif thay:
            i = "THAY"
        elif t - t_thay_cuoi > HET_GIO_TIM:
            i = "HET_GIO"
        else:
            i = "KHONG_THAY"
        lenh = o[(s, i)]
        s_moi = n[(s, i)]
        if s_moi != s:
            thong_ke["chuyen"].append((round(t, 1), s, i, s_moi))
            if s == "DUOI" and s_moi == "TUAN_TRA":
                thong_ke["bo_cuoc"] += 1
            if s_moi == "SAC":
                thong_ke["lan_sac"] += 1
        s = s_moi
        # ---- khối hành vi: thực hiện lệnh o_t ----
        v_max, xoay = V_TUAN, False
        if chet or lenh == "DUNG_SAC":
            dich = None
        elif lenh == "DI_DIEM_TUAN":
            if math.hypot(r[0] - DIEM_TUAN[k_tuan][0], r[1] - DIEM_TUAN[k_tuan][1]) < 0.3:
                k_tuan = (k_tuan + 1) % len(DIEM_TUAN)
            dich = DIEM_TUAN[k_tuan]
        elif lenh == "BAM_MEO":
            dich, v_max = tuple(meo), V_DUOI
        elif lenh == "TOI_CHO_CUOI_XOAY":
            dich = cho_cuoi
            if cho_cuoi is None or math.hypot(r[0] - cho_cuoi[0], r[1] - cho_cuoi[1]) < 0.4:
                dich, xoay = None, True
        else:  # VE_DOC
            dich = DOC
        v = w = 0.0
        if dich is not None:
            if dich != dich_cu or t - t_lap > 0.5:
                duong, dich_cu, t_lap = a_sao(CAN_ROBOT, r[:2], dich), dich, t
            while len(duong) > 1 and math.hypot(duong[0][0] - r[0], duong[0][1] - r[1]) < 0.35:
                duong.pop(0)
            if duong:
                tx, ty = duong[0]
                if lenh == "BAM_MEO" and math.hypot(meo[0] - r[0], meo[1] - r[1]) < 0.6:
                    tx, ty = r[0], r[1]                 # đã sát mèo: đứng nhìn
                e = goc(math.atan2(ty - r[1], tx - r[0]) - r[2])
                dd = math.hypot(tx - r[0], ty - r[1])
                v = v_max * max(0.0, math.cos(e)) * min(1.0, dd / 0.3) if dd > 0.05 else 0.0
                w = max(-2.0, min(2.0, 3.0 * e)) if dd > 0.05 else 0.0
        elif xoay:
            w = 1.2
        r[2] = goc(r[2] + w * DT)
        nx_, ny_ = r[0] + v * DT * math.cos(r[2]), r[1] + v * DT * math.sin(r[2])
        if not LUOI[o_luoi((nx_, ny_))]:
            r[0], r[1] = nx_, ny_
        if co_pin and not chet:
            if lenh == "DUNG_SAC" and o_doc:
                pin = min(100.0, pin + SAC_NHANH * DT)
            else:
                pin -= TIEU_HAO["duoi" if lenh == "BAM_MEO" else ("di" if v > 0.05 or abs(w) > 0.1 else "dung")] * DT
            if pin <= 0:
                pin, chet = 0.0, True
                thong_ke["t_het_pin"] = round(t, 1)
            thong_ke["pin_min"] = min(thong_ke["pin_min"], pin)
        # ---- mèo: đi lang thang, robot tới gần (< 1,8 m, thấy nhau) thì chạy trốn ----
        d_rm = math.hypot(meo[0] - r[0], meo[1] - r[1])
        if d_rm < 1.8 and thay and meo_chay <= 0:
            xa = TRONG_MEO[rng.choice(len(TRONG_MEO), 60)]
            pts = (xa[:, ::-1] + 0.5) * O
            diem = pts[np.argmax(np.hypot(pts[:, 0] - r[0], pts[:, 1] - r[1]) + rng.normal(0, 0.3, len(pts)))]
            meo_duong, meo_chay = a_sao(CAN_MEO, meo, tuple(diem)), 4.0
        if not meo_duong:
            c = TRONG_MEO[rng.integers(len(TRONG_MEO))]
            meo_duong = a_sao(CAN_MEO, meo, ((c[1] + 0.5) * O, (c[0] + 0.5) * O))
            meo_duong += [meo_duong[-1]] * int(rng.integers(10, 40)) if meo_duong else []   # dừng nghỉ một lúc
        vm = V_MEO_CHAY if meo_chay > 0 else V_MEO
        meo_chay -= DT
        buoc = vm * DT
        while meo_duong and buoc > 0:
            tx, ty = meo_duong[0]
            dd = math.hypot(tx - meo[0], ty - meo[1])
            if dd <= buoc:
                meo[0], meo[1] = tx, ty
                meo_duong.pop(0)
                buoc -= max(dd, 1e-3)
            else:
                meo[0] += buoc * (tx - meo[0]) / dd
                meo[1] += buoc * (ty - meo[1]) / dd
                buoc = 0
        thong_ke["thay"] += thay
        thong_ke["sau_lan_dau"] += da_thay
        if ghi:
            log.append({"t": round(t, 1), "r": [round(v_, 3) for v_ in r], "meo": [round(v_, 3) for v_ in meo], "s": s, "i": i, "o": lenh,
                        "pin": round(pin, 1), "thay": bool(thay), "cho_cuoi": [round(v_, 2) for v_ in cho_cuoi] if cho_cuoi else None})
    thong_ke["ti_le_thay"] = thong_ke["thay"] / max(1, thong_ke["sau_lan_dau"])
    thong_ke["mat_dau"] = mat_dau
    thong_ke["mat_dau_cuoi"] = round(T - t_mat, 1) if t_mat is not None else None   # mất dấu tới hết giờ
    thong_ke["vi_tri_cuoi"] = r
    return thong_ke, log


if __name__ == "__main__":
    import sys
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
    for ban in "AB":
        ts = [chay(ban, sd, T=90, co_pin=False)[0] for sd in seeds]
        print(ban, "thấy mèo TB %.1f%%" % (100 * np.mean([x["ti_le_thay"] for x in ts])),
              "bỏ cuộc TB %.1f" % np.mean([x["bo_cuoc"] for x in ts]), [round(100 * x["ti_le_thay"]) for x in ts])
        md = [g for x in ts for g in x["mat_dau"]]
        print("   khoảng mất dấu: trung vị %.1f s, TB %.1f s, số %d; >10 s: %d" % (np.median(md), np.mean(md), len(md), sum(g > 10 for g in md)))


# ---------------- §16.2: phân cấp và ghép song song ----------------
def dem_mui_ten(ban="C"):
    """Số mũi tên đổi trạng thái: FSM phẳng vs FSM phân cấp (gom TUAN_TRA, DUOI, TIM thành siêu trạng thái LAM_VIEC)."""
    chuyen = tao_fsm(ban)[6]
    phang = len(chuyen)
    con = {"TUAN_TRA", "DUOI", "TIM"}
    gop = {(("LAM_VIEC" if s in con else s), i, d) for (s, i), d in chuyen.items() if i == "PIN_YEU"}
    phan_cap = len([1 for (s, i) in chuyen if i != "PIN_YEU"]) + len(gop)
    return phang, phan_cap


def ghep_song_song(*may):
    """Ghép song song (Eq. 16.2) với đầu vào là bộ (i1, i2, ...): S = S1 × S2 × ..., n((s1, s2, ...), (i1, i2, ...)) = (n1(s1, i1), ...).
    Duyệt BFS từ trạng thái đầu để đếm số trạng thái tới được và số ô trong bảng n."""
    import itertools
    s0 = tuple(m[5] for m in may)
    I = list(itertools.product(*[m[1] for m in may]))
    thay, hang = {s0}, [s0]
    while hang:
        s = hang.pop()
        for i in I:
            d = tuple(m[3][(sk, ik)] for m, sk, ik in zip(may, s, i))
            if d not in thay:
                thay.add(d)
                hang.append(d)
    return len(thay), len(I), len(thay) * len(I)


def fsm_cua():
    S = ["DONG", "DANG_MO", "MO", "DANG_DONG"]
    I = ["NUT_BAM", "TOI_DINH", "TOI_DAY", "TICK"]
    ch = {("DONG", "NUT_BAM"): "DANG_MO", ("DANG_MO", "TOI_DINH"): "MO", ("MO", "NUT_BAM"): "DANG_DONG", ("DANG_DONG", "TOI_DAY"): "DONG"}
    n = {(s, i): ch.get((s, i), s) for s in S for i in I}
    return S, I, None, n, None, "DONG", ch


def fsm_den():
    S, I = ["TAT", "BAT"], ["BAM_CONG_TAC", "TICK"]
    ch = {("TAT", "BAM_CONG_TAC"): "BAT", ("BAT", "BAM_CONG_TAC"): "TAT"}
    return S, I, None, {(s, i): ch.get((s, i), s) for s in S for i in I}, None, "TAT", ch
