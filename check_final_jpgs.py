from PIL import Image
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Hardkódovaný seznam používaných obrázků
used_images = [
    "DreamCoreObdelnik.jpg",
    "pole.jpg",
    "koně.jpg",
    "predmesti.jpg",
    "věž.jpg",
    "dveře.jpg",
    "postel3.jpg"
]

# Rozměry stránky se spadávkou v palcích (pro Slim 115x185mm)
PAGE_W_IN = 115 / 25.4
PAGE_H_IN = 185 / 25.4

print(f"{'Název souboru':<25} | {'Metadata DPI':<12} | {'Pixely':<12} | {'Reálné DPI na stránce'}")
print("-" * 85)

for img_name in used_images:
    if os.path.exists(img_name):
        with Image.open(img_name) as img:
            dpi = img.info.get('dpi', (0, 0))
            w, h = img.size
            
            # Výpočet reálného DPI:
            # Protože Typst používá "fit: cover", obrázek se roztáhne tak, 
            # aby zakryl celou plochu (115x185mm).
            # Reálné rozlišení je limitováno tou stranou, která se musí roztáhnout víc.
            scale_w = w / PAGE_W_IN
            scale_h = h / PAGE_H_IN
            real_dpi = min(scale_w, scale_h)
            
            print(f"{img_name:<25} | {str(int(dpi[0])):<12} | {w:4}x{h:<7} | {real_dpi:.1f} DPI")
    else:
        print(f"{img_name:<25} | {'NENALEZENO':<12} | {'-':<12} | -")

print("\nPoznámka: 'Reálné DPI' zohledňuje, že Typst obrázek roztáhne na celou plochu 115x185mm.")
print("Pokud je toto číslo nad 300, je obrázek i po oříznutí a roztažení perfektně ostrý.")
