import json
import os
import subprocess

def create_typst_file(json_path, config_path, output_filename):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    layout = config['layout']
    styles = config['styles']
    colophon = config['document']['colophon']

    typ = []
    
    # --- SETUP SECTION ---
    typ.append(f'#set page(')
    
    # Page size detection
    ps = layout.get('page_size', 'A5')
    if ps == "B6":
        content_w, content_h = 125, 176
    elif ps == "130x200":
        content_w, content_h = 130, 200
    elif ps == "110x180":
        content_w, content_h = 110, 180
    else:
        # A5 default
        content_w, content_h = 148, 210
    
    # Add 2.5mm bleed to all sides (5mm total to width/height)
    typ.append(f'  width: {content_w}mm + 5mm,')
    typ.append(f'  height: {content_h}mm + 5mm,')
    
    # Margins: Add 2.5mm bleed to each side. 
    typ.append(f'  margin: (inside: {layout["margins_pt"]["inner"]}pt + 2.5mm, outside: {layout["margins_pt"]["outer"]}pt + 2.5mm, top: {layout["margins_pt"]["top"]}pt + 2.5mm, bottom: 80pt + 2.5mm),')
    typ.append(f'  footer-descent: 30pt,')
    typ.append(f'  footer: context [')
    typ.append(f'    #set text(size: {styles["page_number"]["size"]}pt, font: "{styles["page_number"]["font"]}")')
    typ.append(f'    #let page_num = counter(page).at(here()).first()')
    typ.append(f'    #if calc.even(page_num) {{')
    typ.append(f'      align(left)[#page_num]')
    typ.append(f'    }} else {{')
    typ.append(f'       align(right)[#page_num]')
    typ.append(f'    }}')
    typ.append(f'  ]')
    typ.append(f')')
    
    # Global text settings: STRICTLY disable hyphenation
    typ.append(f'#set text(font: "Courier Prime", size: {styles["verse"]["size"]}pt, lang: "cs", hyphenate: false)')
    
    # Global paragraph settings (implementing the requested 1.65 line spacing)
    leading_val = styles["verse"]["line_spacing"] - styles["verse"]["size"]
    typ.append(f'#set par(first-line-indent: 1.5em, justify: true, leading: {leading_val}pt)')
    
    # Helpers
    typ.append('''
#let blank-page() = {
  page(footer: none)[]
}

#let chapter-page-break() = {
  // Goal: Chapters start on ODD pages. 
  // If we are on an ODD page, we must add an EVEN blank page first.
  context {
    if calc.odd(here().page()) {
        blank-page()
    } else {
        pagebreak(weak: true)
    }
  }
}

#let colophon-page-break() = {
  // Goal: Colophon usually on EVEN (Left) page.
  context {
    if calc.even(here().page()) {
        blank-page()
    } else {
        pagebreak(weak: true)
    }
  }
}
''')

    # Custom Heading Style
    typ.append(f'''
#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: {styles["chapter_title"]["size"]}pt, weight: "bold", font: "{styles["chapter_title"]["font"]}")
  #set par(justify: false)
  #it.body
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: {styles["poem_title"]["size"]}pt, weight: "bold", font: "{styles["poem_title"]["font"]}")
  #set par(first-line-indent: 0pt, justify: false)
  #v({styles["poem_title"]["space_before"]}pt, weak: true)
  #it.body
  #v({styles["poem_title"]["space_after"]}pt, weak: true)
]
''')

    # Define the chapter function with 3mm safety margin to "fill the rectangle"
    typ.append(f'''
#let chapter(title, img_path, blank: false) = {{
  chapter-page-break()
  // Manual footer suppression for chapter page
  set page(footer: none)
  heading(level: 1, title)
  pagebreak()
  // Reset footer for illustration
  set page(footer: context [
    #set text(size: {styles["page_number"]["size"]}pt, font: "{styles["page_number"]["font"]}")
    #let page_num = counter(page).at(here()).first()
    #if calc.even(page_num) {{ align(left)[#page_num] }} else {{ align(right)[#page_num] }}
  ])
  
  if not blank {{
    // margin: 3mm results in 0.5mm safe space inside the 2.5mm bleed/trim
    page(margin: 3mm, {{
      if img_path != "" and img_path != "404" {{
        set align(center + horizon)
        image(img_path, width: 100%, height: 100%, fit: "cover")
      }} else if img_path == "404" {{
        set align(center + horizon)
        set text(size: 11pt, weight: "regular", font: "Courier Prime")
        [404]
      }} else {{
        set align(center + horizon)
        set text(size: 14pt, style: "italic", font: "Courier Prime")
        [[ Ilustrace ]]
      }}
    }})
  }}
}}

#let poem(title, body_content) = {{
  pagebreak(weak: true)
  if title != "" {{
    heading(level: 2, title)
  }}
  // Re-assert leading and justify for Slim format
  set par(first-line-indent: 0pt, justify: false, leading: {leading_val}pt)
  body_content
}}
''')

    # --- CONTENT GENERATION ---
    typ.append('#blank-page()')
    typ.append('#blank-page()')
    # Title Page
    typ.append('#page(footer: none, margin: 1.5cm)[')
    typ.append('  #set par(first-line-indent: 0pt)')
    typ.append('  #set align(center + horizon)')
    typ.append('  #set par(justify: false)')
    typ.append('  #text(size: 22pt, weight: "bold", font: "Courier Prime")[Nuda, hypotéky,] \\')
    typ.append('  #text(size: 22pt, weight: "bold", font: "Courier Prime")[fašismus]')
    typ.append('  #v(2em)')
    typ.append(f'  #text(size: 16pt, font: "Courier Prime")[{config["document"].get("author", "Mirek Mrkvička")}]')
    typ.append(']')
    typ.append('#blank-page()')
    typ.append('#blank-page()')
    typ.append('#page[')
    typ.append('  #set par(first-line-indent: 0pt, justify: false)')
    typ.append('  #set align(center + top)')
    typ.append('  #v(20%)')
    typ.append('  #text(style: "italic")[ Kde ztratili víru v Boha, nacházejí poslední útočiště v hypotéce. A kde na ni nedosáhnou, tam bují fašismus.]')
    typ.append(']')
    typ.append('#blank-page()')
    typ.append('#page(footer: none)[')
    typ.append('  #outline(title: "Obsah", indent: 1em)')
    typ.append(']')
    typ.append('#blank-page()')

    for kapitola in data.get('kapitoly', []):
        typ.append(f'#chapter("{kapitola["nazev"]}", "{kapitola.get("ilustrace", "")}")')
        for basen in kapitola.get('basne', []):
            typ.append(f'#poem("{basen["nazev"]}", [')
            for sloka in basen.get('sloky', []):
                for vers in sloka.get('verse', []):
                    clean_vers = vers.replace('"', '\\"')
                    if clean_vers.startswith("BULLET:"):
                        content = clean_vers[len("BULLET:"):].strip()
                        typ.append(f'  - {content}')
                    elif clean_vers.startswith("ENUM:"):
                        content = clean_vers[len("ENUM:"):].strip()
                        typ.append(f'  + {content}')
                    else:
                        typ.append(f'  {clean_vers} \\')
                typ.append('\n  #v(1em)\n')
            typ.append('])')

    # Colophon (using consistent line breaks \)
    typ.append('#colophon-page-break()')
    typ.append('#page[')
    typ.append('  #set par(first-line-indent: 0pt, justify: false)')
    typ.append('  #set align(left + bottom)')
    typ.append(f'  {config["document"]["title"]} \\')
    typ.append(f'  © {config["document"].get("author", "Mirek Mrkvička")}, 2026 \\')
    typ.append(f'  Všechna práva vyhrazena. \\')
    typ.append(f'  {colophon["publisher"]} \\')
    typ.append(f'  {colophon["edition"]} \\')
    typ.append(f'  ISBN {config["document"]["isbn"]}')
    typ.append(']')
    
    # --- FINAL EVEN PAGE LOGIC ---
    typ.append('#context {')
    typ.append('  let last_page = counter(page).at(here()).first()')
    typ.append('  if calc.odd(last_page) {')
    typ.append('    blank-page()')
    typ.append('  }')
    typ.append('}')

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(typ))

if __name__ == "__main__":
    base_path = r"c:\Users\Marek\Desktop\nudaHypotekyFasismus"
    json_p = os.path.join(base_path, "Blok.json")
    create_typst_file(json_p, os.path.join(base_path, "export_config.json"), "Blok.typ")
    create_typst_file(json_p, os.path.join(base_path, "export_config_B6.json"), "Blok_B6.typ")
