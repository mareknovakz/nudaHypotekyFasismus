import json
import os
import re
import subprocess

def _consume_italic_words(text, italic_state):
    """Split a verse into words tagged with an italic flag, treating each
    '_' as an on/off toggle so spans that open/close mid-verse OR span
    multiple verses (carried via italic_state) both render correctly."""
    words = []
    state = italic_state
    for part in re.split(r'(_)', text):
        if part == '_':
            state = not state
            continue
        if not part:
            continue
        for w in part.split():
            words.append((w, state))
    return words, state

def _words_to_typst_array(words):
    items = []
    for w, italic in words:
        w_escaped = w.replace('\\', '\\\\').replace('"', '\\"')
        items.append(f'(w: "{w_escaped}", i: {"true" if italic else "false"})')
    return '(' + ', '.join(items) + (',' if items else '') + ')'

def create_typst_file(json_path, config_path, output_filename):
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)

    layout = config['layout']
    styles = config['styles']
    colophon = config['document']['colophon']
    chapter_own_page = config['layout'].get('chapter_own_page', True)
    chapter_illustration = config['layout'].get('chapter_illustration', True)

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
    typ.append(f'    #let page_num = counter(page).get().first()')
    typ.append(f'    #if calc.even(page_num) {{')
    typ.append(f'      align(left)[#page_num]')
    typ.append(f'    }} else {{')
    typ.append(f'       align(right)[#page_num]')
    typ.append(f'    }}')
    typ.append(f'  ]')
    typ.append(f')')
    
    # hyphenate: auto = dělení jen v justify blocích (próza), ne v ragged-right (poezie)
    typ.append(f'#set text(font: "Courier Prime", size: {styles["verse"]["size"]}pt, lang: "cs", hyphenate: auto)')
    
    # Global paragraph settings (prose: 1.65×, poetry: 1.5×)
    leading_val = styles["verse"]["line_spacing"] - styles["verse"]["size"]
    leading_poetry = round(styles["verse"]["size"] * 0.75, 2)  # 1.75× line spacing
    typ.append(f'#set par(first-line-indent: 1.5em, justify: true, leading: {leading_val}pt)')
    
    # Helpers
    typ.append('''
#let blank-page() = {
  page(footer: none)[]
}

#let chapter-page-break() = pagebreak(to: "odd")

#let colophon-page-break() = pagebreak(to: "even")

// Wraps a poetry verse: if it fits on one line, render normally (left).
// If it overflows, manually break it word-by-word and right-align only
// the overflowing remainder, leaving the first line at the left margin.
// `words` is an array of (w: "text", i: bool) so italics nested inside
// (or spanning across) verses keep working after manual line-splitting.
#let wrap-right(words) = layout(avail => context {
  let mk(item) = if item.i { text(style: "italic")[#item.w] } else { [#item.w] }
  let render-line(ws) = {
    let out = ()
    for (idx, item) in ws.enumerate() {
      if idx > 0 { out.push([ ]) }
      out.push(mk(item))
    }
    out.join()
  }
  if words.len() == 0 {
    []
  } else if measure(render-line(words)).width <= avail.width {
    render-line(words)
  } else {
    let lines = ()
    let current = ()
    for item in words {
      let candidate = current + (item,)
      if measure(render-line(candidate)).width > avail.width and current.len() > 0 {
        lines.push(current)
        current = (item,)
      } else {
        current = candidate
      }
    }
    lines.push(current)
    if lines.len() == 1 {
      render-line(lines.first())
    } else {
      let out = ()
      for l in lines.slice(0, -1) {
        out.push(render-line(l))
        out.push(linebreak())
      }
      out.push(align(right)[#render-line(lines.last())])
      out.join()
    }
  }
})
''')

    # Custom Heading Style
    typ.append(f'''
#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: {styles["chapter_title"]["size"]}pt, weight: "bold", font: "{styles["chapter_title"]["font"]}")
  #set par(justify: false)
  #move(dy: -1.2em)[#it.body]
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: {styles["poem_title"]["size"]}pt, weight: "bold", font: "{styles["poem_title"]["font"]}")
  #set par(first-line-indent: 0pt, justify: false)
  #v({styles["poem_title"]["space_before"]}pt, weak: true)
  #it.body
  #v({styles["poem_title"]["space_after"]}pt, weak: true)
]

#show outline.entry.where(level: 1): it => {{
  strong(it)
}}
''')

    # Chapter function — adapts to chapter_own_page and chapter_illustration settings
    chapter_lines = []
    if chapter_own_page:
        chapter_lines.append('#let chapter(title, img_path, blank: false) = [')
        chapter_lines.append('  #chapter-page-break()')
        chapter_lines.append('  #set page(footer: none)')
        chapter_lines.append('  #heading(level: 1, title)')
        chapter_lines.append('  #pagebreak()')
        chapter_lines.append(f'  #set page(footer: context [')
        chapter_lines.append(f'    #set text(size: {styles["page_number"]["size"]}pt, font: "{styles["page_number"]["font"]}")')
        chapter_lines.append(f'    #let page_num = counter(page).get().first()')
        chapter_lines.append(f'    #if calc.even(page_num) [ #align(left)[#page_num] ] else [ #align(right)[#page_num] ]')
        chapter_lines.append(f'  ])')
        if chapter_illustration:
            chapter_lines.append('  #if not blank [')
            chapter_lines.append('    #page(margin: 0pt, footer: none)[')
            chapter_lines.append('      #if img_path != "" and img_path != "404" [')
            chapter_lines.append('        #set align(center + horizon)')
            chapter_lines.append('        #image(img_path, width: 100%, height: 100%, fit: "cover")')
            chapter_lines.append('      ] else if img_path == "404" [')
            chapter_lines.append('        #set align(center + horizon)')
            chapter_lines.append('        #set text(size: 11pt, weight: "regular", font: "Courier Prime")')
            chapter_lines.append('        [404]')
            chapter_lines.append('      ] else [')
            chapter_lines.append('        #set align(center + horizon)')
            chapter_lines.append('        #set text(size: 14pt, style: "italic", font: "Courier Prime")')
            chapter_lines.append('        [[ Ilustrace ]]')
            chapter_lines.append('      ]')
            chapter_lines.append('    ]')
            chapter_lines.append('  ]')
        chapter_lines.append(']')
    else:
        chapter_lines.append('#let chapter(title, img_path, blank: false) = [')
        chapter_lines.append('  #pagebreak(weak: true)')
        chapter_lines.append('  #v(30%)')
        chapter_lines.append('  #heading(level: 1, title)')
        chapter_lines.append('  #v(2em)')
        chapter_lines.append(']')
    typ.append('\n'.join(chapter_lines))

    typ.append(f'''
#let poem-prose(title, body_content) = [
  #pagebreak(weak: true)
  #if title != "" [
    #heading(level: 2, title)
  ]
  #set par(first-line-indent: 0pt, justify: true, leading: {leading_val}pt, spacing: {styles["verse"]["line_spacing"]}pt)
  #body_content
]

#let poem-poetry(title, body_content) = [
  #pagebreak(weak: true)
  #if title != "" [
    #heading(level: 2, title)
  ]
  #set text(hyphenate: false)
  #set par(first-line-indent: 0pt, justify: false, leading: {leading_val}pt, spacing: {leading_val}pt)
  #body_content
]
''')

    # --- CONTENT GENERATION ---
    typ.append('#blank-page()')
    typ.append('#blank-page()')
    # Title Page
    typ.append('#page(footer: none, margin: 1.5cm)[')
    typ.append('  #set par(first-line-indent: 0pt)')
    typ.append('  #grid(')
    typ.append('    columns: (1fr),')
    typ.append('    rows: (1fr, 1fr),')
    typ.append('    align(center + horizon)[')
    typ.append('      #set par(justify: false)')
    typ.append('      #text(size: 22pt, weight: "bold", font: "Courier Prime")[Nuda, hypotéky,] \\')
    typ.append('      #text(size: 22pt, weight: "bold", font: "Courier Prime")[fašismus]')
    typ.append('      #v(2em)')
    typ.append(f'      #text(size: 16pt, font: "Courier Prime")[{config["document"].get("author", "Mirek Mrkvička")}]')
    typ.append('    ],')
    typ.append('    align(center + horizon)[')
    typ.append(f'      #set text(size: {styles["verse"]["size"]}pt, font: "Courier Prime", weight: "regular")')
    typ.append('      #set par(justify: false, first-line-indent: 0pt)')
    typ.append('      Nakladatelství Poezie, vole \\')
    typ.append('      Praha 2026')
    typ.append('    ],')
    typ.append('  )')
    typ.append(']')
    typ.append('#blank-page()')
    typ.append('#page(footer: none)[')
    typ.append('  #set par(first-line-indent: 0pt, justify: false)')
    typ.append('  #set align(center + top)')
    typ.append('  #v(20%)')
    typ.append('  #text(style: "italic")[ Kde ztratili víru v Boha, nacházejí poslední útočiště v hypotéce. A kde na ni nedosáhnou, tam bují fašismus.]')
    typ.append(']')
    typ.append('#blank-page()')
    typ.append('#page[')
    typ.append('  #outline(title: [Obsah #v(1em)], indent: 0pt)')
    typ.append(']')

    for kapitola in data.get('kapitoly', []):
        illus = kapitola.get("ilustrace", "")
        if illus and not illus.startswith("assets/"):
            illus = f"assets/{illus}"
        typ.append(f'#chapter("{kapitola["nazev"]}", "{illus}")')
        for basen in kapitola.get('basne', []):
            is_poetry = basen.get('isPoetry', False)
            func_name = 'poem-poetry' if is_poetry else 'poem-prose'
            typ.append(f'#{func_name}("{basen["nazev"]}", [')
            italic_state = False
            for sloka in basen.get('sloky', []):
                for vers in sloka.get('verse', []):
                    clean_vers = vers.replace('"', '\\"')
                    if clean_vers.startswith("BULLET:"):
                        content = clean_vers[len("BULLET:"):].strip()
                        typ.append(f'  - {content}')
                    elif clean_vers.startswith("ENUM:"):
                        content = clean_vers[len("ENUM:"):].strip()
                        typ.append(f'  + {content}')
                    elif is_poetry:
                        words, italic_state = _consume_italic_words(vers, italic_state)
                        typ.append(f'  #wrap-right({_words_to_typst_array(words)})')
                        typ.append('')
                    else:
                        typ.append(f'  {clean_vers}')
                if is_poetry:
                    typ.append(f'  #v({styles["verse"]["space_after_stanza"]}pt)')
                else:
                    typ.append('')
            typ.append('])')

    # Poděkování
    podek = config['document'].get('podekování', '')
    if podek:
        typ.append('#pagebreak(to: "odd")')
        typ.append('#page(footer: none)[')
        typ.append('  #set align(left + top)')
        typ.append('  #set par(first-line-indent: 0pt, justify: true)')
        typ.append(f'  #show heading.where(level: 1): it => [')
        typ.append(f'    #set align(left)')
        typ.append(f'    #set text(size: {styles["poem_title"]["size"]}pt, weight: "bold", font: "{styles["poem_title"]["font"]}")')
        typ.append(f'    #set par(first-line-indent: 0pt, justify: false)')
        typ.append(f'    #v({styles["poem_title"]["space_before"]}pt, weak: true)')
        typ.append(f'    #it.body')
        typ.append(f'    #v({styles["poem_title"]["space_after"]}pt, weak: true)')
        typ.append(f'  ]')
        typ.append('  #heading(level: 1)[Poděkování]')
        typ.append(f'  {podek}')
        typ.append(']')

    # Colophon (using consistent line breaks \)
    typ.append('#colophon-page-break()')
    typ.append('#page(footer: none)[')
    typ.append('  #set par(first-line-indent: 0pt, justify: false)')
    typ.append('  #set align(left + top)')
    if colophon.get("logo"):
        typ.append('  #align(center)[')
        typ.append(f'    #image("{colophon["logo"]}", width: 35mm)')
        typ.append('  ]')
        typ.append('  #v(2em)')
    typ.append(f'  {config["document"]["title"]} \\')
    typ.append(f'  © {config["document"].get("author", "Mirek Mrkvička")}, 2026 \\')
    typ.append(f'  Všechna práva vyhrazena. \\')
    typ.append(f'  {colophon["publisher"]} \\')
    if colophon.get("publisher_address"):
        typ.append(f'  {colophon["publisher_address"]} \\')
    typ.append(f'  {colophon["edition"]} \\')
    if colophon.get("pages"):
        typ.append(f'  {colophon["pages"]} stran \\')
    if colophon.get("editor"):
        typ.append(f'  Redakce: {colophon["editor"]} \\')
    if colophon.get("typesetting"):
        typ.append(f'  Sazba: {colophon["typesetting"]} \\')
    if colophon.get("printer"):
        typ.append(f'  Tisk: {colophon["printer"]} \\')
    if colophon.get("naklad"):
        typ.append(f'  Náklad: {colophon["naklad"]} výtisků \\')
    typ.append(f'  ISBN {config["document"]["isbn"]}')
    typ.append(']')
    

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(typ))

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_p = os.path.join(base_path, "Blok.json")
    create_typst_file(json_p, os.path.join(base_path, "export_config.json"), "Blok.typ")
