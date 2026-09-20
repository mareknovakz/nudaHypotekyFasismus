# -*- coding: utf-8 -*-
from PIL import Image
import os

SRC_DIR = r"c:\Repozitáře\nudaHypotekyFasismus\video"
OUT_DIR = r"c:\Repozitáře\nudaHypotekyFasismus\video\work"

# working canvas gives zoompan some headroom above final 1080x1920 output
W, H = 1350, 2400

slides = [
    "postel.png",
    "21e0f25e-d92f-494d-b60a-54b0e60d95ca.jpg",
    "314de715-4684-46e7-83c1-16896670eec5.jpg",
    "Nuda_obrazek.png",
]

for name in slides:
    img = Image.open(os.path.join(SRC_DIR, name)).convert("RGB")
    src_w, src_h = img.size
    target_ratio = W / H
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # source is wider than target -> crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # source is taller than target -> crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((W, H), Image.LANCZOS)
    out_name = os.path.splitext(name)[0] + "_prep.jpg"
    img.save(os.path.join(OUT_DIR, out_name), quality=95)
    print("saved", out_name, img.size)
