# -*- coding: utf-8 -*-
from PIL import Image

W, H = 1080, 1920
top = (150, 200, 235)
bottom = (40, 95, 160)

img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)

img.save(r"c:\Repozitáře\nudaHypotekyFasismus\video\work\end_card_bg.jpg", quality=95)
print("saved end_card_bg.jpg")
