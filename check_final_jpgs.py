import fitz
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r'c:\Repozitáře\nudaHypotekyFasismus\Blok_Slim.pdf')
total = doc.page_count
w = doc[0].rect.width * 25.4 / 72
h = doc[0].rect.height * 25.4 / 72
print(f"Stran: {total}")
print(f"Rozmer: {w:.1f}mm x {h:.1f}mm")

print("\n=== STRUKTURA ===")
for i in range(total):
    page = doc[i]
    text = page.get_text().strip()
    first_line = text.split('\n')[0][:60] if text else "[prazdna]"
    print(f"  {i+1:3d}: {first_line}")

for idx, name in [(2, 'title'), (10, 'sample'), (total-1, 'colophon')]:
    pix = doc[idx].get_pixmap(dpi=150)
    out = f'c:\\Repozitáře\\nudaHypotekyFasismus\\check_{name}.png'
    pix.save(out)
    print(f"\nSaved check_{name}.png (page {idx+1})")

doc.close()
