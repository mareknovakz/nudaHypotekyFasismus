# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SRC = r"c:\Repozitáře\nudaHypotekyFasismus\predmesti.jpg"
LOGO = r"c:\Repozitáře\nudaHypotekyFasismus\pvl_logo.png"
FONT = r"C:\Program Files\Scribus 1.6.5\share\fonts\URWFonts-1.41\Coronet.ttf"
OUT = r"c:\Repozitáře\nudaHypotekyFasismus\video\work\preview_credit_card2.png"

img = Image.open(SRC).convert("RGB")
sw, sh = img.size
target_ratio = W / H
src_ratio = sw / sh
if src_ratio > target_ratio:
    new_w = int(sh * target_ratio)
    left = (sw - new_w) // 2
    img = img.crop((left, 0, left + new_w, sh))
else:
    new_h = int(sw / target_ratio)
    top = (sh - new_h) // 2
    img = img.crop((0, top, sw, top + new_h))
img = img.resize((W, H), Image.LANCZOS)

draw = ImageDraw.Draw(img)

def draw_text_centered(draw, text, y, font, fill=(255, 255, 255), shadow=(0, 0, 0)):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    x = (W - w) / 2 - bbox[0]
    draw.text((x + 2, y + 2), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)

f_credit = ImageFont.truetype(FONT, 62)
f_copyright = ImageFont.truetype(FONT, 50)
f_link = ImageFont.truetype(FONT, 58)

draw_text_centered(draw, "Vydalo Poezie, vole!", 1500, f_credit)
draw_text_centered(draw, "© Mirek Mrkvička, 2026", 1650, f_copyright)
draw_text_centered(draw, "poezievole.cz", 1750, f_link)

# recolor logo ink to white, thin the strokes, keep alpha
logo = Image.open(LOGO).convert("RGBA")
r, g, b, a = logo.split()
a = a.filter(ImageFilter.MinFilter(3))
white_logo = Image.merge("RGBA", (Image.new("L", logo.size, 255),
                                   Image.new("L", logo.size, 255),
                                   Image.new("L", logo.size, 255), a))
logo = white_logo.resize((int(logo.width * 1.8), int(logo.height * 1.8)), Image.LANCZOS)
logo_x = (W - logo.width) // 2
logo_y = 1120
img.paste(logo, (logo_x, logo_y), logo)

img.save(OUT)
print("saved", OUT)
