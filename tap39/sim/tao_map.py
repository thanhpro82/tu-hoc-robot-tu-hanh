"""Tập 3.9: đổi bản đồ slam_toolbox cuối cùng của tập 3.7 (map_015.npy) sang định dạng map_server của Nav2 (pgm + yaml)."""
import json
from pathlib import Path

import numpy as np
from PIL import Image

GOC = Path(__file__).resolve().parents[2]
M = np.load(GOC / "tap37/ws/out/map_015.npy")
I = json.loads((GOC / "tap37/ws/out/map_015.json").read_text())
img = np.full(M.shape, 205, np.uint8)        # chưa biết
img[M == 0] = 254                             # trống
img[M == 100] = 0                             # vật cản
OUT = GOC / "tap39/ws/map"
OUT.mkdir(parents=True, exist_ok=True)
Image.fromarray(img[::-1]).save(OUT / "nha.pgm")   # hàng 0 của ảnh là mép trên (y lớn nhất)
(OUT / "nha.yaml").write_text(
    f"image: nha.pgm\nmode: trinary\nresolution: {I['res']:.4f}\norigin: [{I['ox']:.4f}, {I['oy']:.4f}, 0.0]\n"
    "negate: 0\noccupied_thresh: 0.65\nfree_thresh: 0.25\n", encoding="utf-8")
print("bản đồ", M.shape, "trống", int((M == 0).sum()), "vật cản", int((M == 100).sum()), "->", OUT)
