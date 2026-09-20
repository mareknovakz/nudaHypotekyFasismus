import json
import os
import re
import subprocess
import sys

# Set UTF-8 for stdout to prevent crashes on non-ASCII characters in Windows CMD/PS
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def sanitize_text(text):
    if not text: return ""
    text = re.sub(r'The following table:?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\|?\s*-+\s*\|\s*-+\s*\|?', '', text)
    text = re.sub(r'\|', '', text)
    return text.strip()

def apply_czech_typography(text):
    if not text: return ""
    # Straight quotes to Czech quotes
    text = re.sub(r'(^|[\s\(])"([^"]+)"', r'\1„\2“', text)
    text = text.replace(' "', ' „')
    
    # Ellipsis
    text = re.sub(r'\.{2,}', '…', text)
    
    # Dashes
    text = text.replace(' - ', ' – ')
    if text.startswith('- '):
        text = '– ' + text[2:]
        
    # Non-breaking spaces for Czech prepositions and conjunctions
    preps = ['k', 's', 'v', 'z', 'o', 'u', 'a', 'i', 'K', 'S', 'V', 'Z', 'O', 'U', 'A', 'I']
    for _ in range(2):
        for p in preps:
            text = re.sub(rf'(^|[\s„"\'\(\[])({p})\s+', r'\1\2~', text)
            
    return text

def extract_poems(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    target_titles = [
        "Pan Pták si vzal sick day",
        "Přesně takhle to chtěl",
        "Pan Pták si dělá zbrojní průkaz",
        "Bodíky sbíráte?"
    ]
    
    extracted = {title: None for title in target_titles}
    
    for kapitola in data.get('kapitoly', []):
        for basen in kapitola.get('basne', []):
            nazev = basen.get('nazev', '').strip()
            # Normalize title to match target_titles
            matched_title = None
            if nazev == "Pan Pták si vzal sick day":
                matched_title = "Pan Pták si vzal sick day"
            elif nazev == "Přesně takhle to chtěl":
                matched_title = "Přesně takhle to chtěl"
            elif nazev == "Pan Pták si dělá zbrojní průkaz":
                matched_title = "Pan Pták si dělá zbrojní průkaz"
            elif nazev == "Bodíky sbíráte?":
                matched_title = "Bodíky sbíráte?"
                
            if matched_title:
                extracted[matched_title] = basen
                
    # Double check if everything is found
    for title, val in extracted.items():
        if val is None:
            print(f"Warning: Poem '{title}' not found in JSON!", file=sys.stderr)
            
    return [extracted[t] for t in target_titles if extracted[t] is not None]

def generate_typst_content(poems):
    preface_raw = (
        "Dobrý večer, jsem Mirek Mrkvička a přečtu vám něco ze své sbírky Nuda, hypotéky, fašismus. "
        "Sbírku píšu, protože věřím, že každý z nás má v sobě kousek svého vnitřního fašismu a že "
        "lidská nátura má přirozené sklony k nekrofilnímu sadismu."
    )
    preface = apply_czech_typography(preface_raw)
    
    font_name = "EB Garamond"
    
    typ = []
    
    # 1. Page settings
    typ.append(f'''#set page(
  width: 110mm + 5mm,
  height: 180mm + 5mm,
  margin: (inside: 65pt + 2.5mm, outside: 45pt + 2.5mm, top: 60pt + 2.5mm, bottom: 60pt + 2.5mm),
  footer-descent: 20pt,
  footer: none
)''')
    
    # Footer function
    typ.append(f'''#let default_footer() = context {{
  set text(size: 9pt, font: "{font_name}")
  let page_num = counter(page).at(here()).first()
  if calc.even(page_num) [ #align(left)[#page_num] ] else [ #align(right)[#page_num] ]
}}''')
    
    # Global text settings
    typ.append(f'#set text(font: "{font_name}", size: 10.5pt, lang: "cs", hyphenate: false)')
    typ.append('#set par(justify: true, leading: 8.5pt)')
    
    # Heading custom styles
    typ.append(f'''#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: 20pt, weight: "bold", font: "{font_name}")
  #set par(justify: false)
  #it.body
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: 15pt, weight: "bold", font: "{font_name}")
  #set par(first-line-indent: 0pt, justify: false)
  #v(20pt, weak: true)
  #it.body
  #v(15pt, weak: true)
]''')
    
    # 2. Cover / Title Page
    typ.append('#set align(center + horizon)')
    typ.append(f'#text(size: 24pt, weight: "bold", font: "{font_name}")[Nuda, hypotéky, \\ fašismus]')
    typ.append('#v(1.5em)')
    typ.append(f'#text(size: 14pt, style: "italic", font: "{font_name}")[Autorský výběr básní]')
    typ.append('#v(2em)')
    typ.append(f'#text(size: 16pt, weight: "medium", font: "{font_name}")[Mirek Mrkvička]')
    typ.append('#pagebreak()')
    
    # 3. Preface / Introduction Page
    typ.append('#set page(footer: none)')
    typ.append('#set align(center + horizon)')
    typ.append(f'#text(size: 16pt, weight: "bold", font: "{font_name}")[Úvod]')
    typ.append('#v(1.5em)')
    typ.append(f'#set align(left + horizon)')
    typ.append(f'#set par(first-line-indent: 1.5em, leading: 10pt)')
    typ.append(f'#text(size: 11.5pt, style: "italic", font: "{font_name}")[{preface}]')
    typ.append('#pagebreak(to: "odd")')
    
    # 4. Poetry Pages
    typ.append('#set page(footer: default_footer())')
    typ.append('#set align(left + top)')
    
    for basen in poems:
        title = apply_czech_typography(basen["nazev"])
        typ.append(f'#heading(level: 2, [{title}])')
        typ.append('#set par(first-line-indent: 0pt, justify: true, leading: 8.5pt)')
        typ.append('  #v(5pt)')
        
        for sloka in basen.get('sloky', []):
            for vers in sloka.get('verse', []):
                clean_vers = sanitize_text(vers)
                clean_vers = clean_vers.replace('"', '\\"')
                typ.append(f'  {clean_vers} \\')
            typ.append('  #v(16pt)')
            
        typ.append('#pagebreak(weak: true)')
        
    return "\n".join(typ)

def compile_pdf(typ_path, pdf_path):
    # Find the tinymist binary dynamically in the extensions directory
    extensions_dir = os.path.expanduser(r"~\.antigravity\extensions")
    tinymist_path = "typst"  # fallback
    
    if os.path.exists(extensions_dir):
        tinymist_folders = [f for f in os.listdir(extensions_dir) if f.startswith("myriad-dreamin.tinymist")]
        if tinymist_folders:
            latest_folder = sorted(tinymist_folders)[-1]
            executable = os.path.join(extensions_dir, latest_folder, "out", "tinymist.exe")
            if os.path.exists(executable):
                tinymist_path = executable
                
    cmd = f'"{tinymist_path}" compile --no-pdf-tags "{typ_path}" "{pdf_path}"'
    print(f"Executing: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode == 0:
        print(f"Success! Compiled to {pdf_path}")
    else:
        print("Error during compilation:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "Blok.json")
    typ_path = os.path.join(base_path, "Vyber_Mrkvicka.typ")
    pdf_path = os.path.join(base_path, "Vyber_Mrkvicka.pdf")
    
    print("Extracting poems...")
    poems = extract_poems(json_path)
    print(f"Extracted {len(poems)} poems.")
    
    print("Generating Typst content...")
    typst_content = generate_typst_content(poems)
    
    with open(typ_path, 'w', encoding='utf-8') as f:
        f.write(typst_content)
    print(f"Wrote Typst code to {typ_path}")
    
    print("Compiling PDF...")
    compile_pdf(typ_path, pdf_path)

if __name__ == "__main__":
    main()
