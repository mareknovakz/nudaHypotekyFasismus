# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SRC = r"C:\Repozitáře\nudaHypotekyFasismus\dveře.jpg"
LOGO = r"C:\Repozitáře\nudaHypotekyFasismus\pvl_logo.png"
FONT = r"C:\Program Files\Scribus 1.6.5\share\fonts\URWFonts-1.41\Coronet.ttf"
OUT = r"C:\Repozitáře\nudaHypotekyFasismus\video\work\preview_credit_card.png"

# cover-crop the source photo to 1080x1920
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

draw_text_centered(draw, "Vydalo Poezie, vole!", 1560, f_credit)
draw_text_centered(draw, "© Mirek Mrkvička, 2026", 1650, f_copyright)

# composite logo, upscaled a bit, centered above the text
logo = Image.open(LOGO).convert("RGBA")
logo = logo.resize((int(logo.width * 1.6), int(logo.height * 1.6)), Image.LANCZOS)
logo_x = (W - logo.width) // 2
logo_y = 1330
img.paste(logo, (logo_x, logo_y), logo)

img.save(OUT)
print("saved", OUT)
