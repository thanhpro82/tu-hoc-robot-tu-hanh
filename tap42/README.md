# Tập 4.2 · Ra quyết định khi tương lai bất định

📺 Video: TikTok [@thanh82k5](https://www.tiktok.com/@thanh82k5) (tìm "Tập 4.2") · 📚 Giáo trình: Principles of Robot Autonomy, [Chương 17](https://porabook.com/book/decision-making/)

## Tóm tắt video

Đường tắt 8 bước sát cầu thang hay đường vòng 12 bước? Bạn chọn đường nào? 👇🤖

Tập 4.2 | MÙA 4: BIẾT TỰ QUYẾT ĐỊNH | Series TỰ HỌC ROBOT TỰ HÀNH

Sàn không trơn: đường tắt thắng (chi phí 8 so với 12). Nhưng sàn trơn, 20% số bước robot đi hướng ngẫu nhiên: đó là bài toán quyết định Markov (MDP) với trạng thái x, hành động u, nhiễu w ~ p(w | x, u). Ta tìm chính sách π có chi phí kỳ vọng J nhỏ nhất. Chạy 10.000 lần: đường tắt rơi cầu thang 35,3%, J = 51,13; đường vòng rơi 0,7%, J = 16,48. Chỉ cần trượt 1,94% là đường vòng đã có lợi hơn. Đi theo chuỗi lệnh cố định (vòng hở), đường vòng chỉ tới đích 34,4%; chính sách nhìn vị trí (vòng kín) tới 99,2%. Quy hoạch động còn tìm được J* = 16,24 → tập sau. Số liệu từ mô phỏng Python.

## Chạy thử

```bash
cd tap42/sim
python -X utf8 mdp.py
```

Các con số in ra chính là số liệu dùng trong video (mô phỏng có seed cố định).

## Các file

| File | Nội dung |
|---|---|
| `sim/mdp.py` | Tập 4.2 - Ra quyết định khi tương lai bất định: MDP (Chương 17, Principles of Robot Autonomy). |

## Giải thích trong code

**`sim/mdp.py`**

```text
Tập 4.2 - Ra quyết định khi tương lai bất định: MDP (Chương 17, Principles of Robot Autonomy).

Ký hiệu theo sách (§17.2.1, dạng điều khiển tối ưu, tối thiểu hoá CHI PHÍ, chân trời hữu hạn T):
    x_{t+1} = f(x_t, u_t, w_t),   w_t ~ p(w | x_t, u_t)             (Eq. 17.7–17.8)
    J_π(x_0) = E_w[ g_T(x_T) + Σ_{t=0}^{T-1} g_t(x_t, π_t(x_t), w_t) ]   (Eq. 17.11)
Thế giới (giả định, kiểu bài Markovian Drone §17.5): lưới 9 × 5 trong kho, robot đi từ S tới G.
Hàng dưới cùng là CẦU THANG: rơi xuống thì kẹt luôn (trạng thái hút). Giữa kho có dãy KỆ chắn.
u ∈ {lên, xuống, trái, phải}. Sàn trơn: với xác suất ε robot đi theo hướng ngẫu nhiên (4 hướng đều nhau),
còn lại đi đúng lệnh. Đâm tường/kệ thì đứng yên.
Chi phí: g_t = 1 mỗi bước chưa tới G (tới G thì đứng yên, chi phí 0); g_T(x) = 100·(1 − 1[x = G]).
```

---
[← Về danh sách tập](../README.md)
