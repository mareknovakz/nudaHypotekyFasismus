import json
import os
import xml.etree.ElementTree as ET

def escape_xml(s):
    if not isinstance(s, str): return str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")

def create_guaranteed_sla(json_path, config_path):
    # Load data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    doc_cfg = config['document']
    layout = config['layout']
    styles = config['styles']
    width = layout['width_pt']
    height = layout['height_pt']
    m = layout['margins_pt']

    # Page Calculation
    pages = []
    pages.append({'type': 'blank', 'side': 'R'})
    pages.append({'type': 'blank', 'side': 'L'})
    pages.append({'type': 'title', 'side': 'R', 'text': doc_cfg['title']})
    pages.append({'type': 'blank', 'side': 'L'})
    pages.append({'type': 'quote', 'side': 'R', 'text': "Kde ztratili víru v Boha, nacházejí poslední útočiště v hypotéce. A kde na ni nedosáhnou, tam bují fašismus."})
    
    toc_page_index = len(pages)
    pages.append({'type': 'toc', 'side': 'L', 'items': []})
    
    for kap in data.get('kapitoly', []):
        if pages[-1]['side'] == 'R':
            pages.append({'type': 'blank', 'side': 'L'})
        pages.append({'type': 'chapter', 'side': 'R', 'text': kap['nazev'].upper()})
        pages[-1]['toc_ref'] = True
        pages.append({'type': 'illustration', 'side': 'L', 'text': '[Ilustrace]'})
        
        for basen in kap.get('basne', []):
            side = 'R' if pages[-1]['side'] == 'L' else 'L'
            pages.append({'type': 'poem', 'side': side, 'title': basen['nazev'], 'stanzas': basen.get('sloky', [])})
            pages[-1]['toc_ref'] = True

    if pages[-1]['side'] == 'R':
        pages.append({'type': 'blank', 'side': 'L'})
    
    if "colophon" in doc_cfg:
        col = doc_cfg["colophon"]
        col_text = [
            f"Text © {doc_cfg.get('author', 'Mirek Mrkvička')}, 2026",
            f"Vydal: {col.get('publisher', '')}",
            f"{col.get('edition', '')}",
            f"Sazba a obálka: {col.get('typesetting', '')}",
            f"Tisk: {col.get('printer', '')}",
            "",
            f"ISBN {doc_cfg.get('isbn', '')}"
        ]
        pages.append({'type': 'colophon', 'side': 'L', 'lines': col_text})

    toc_items = []
    for i, p in enumerate(pages):
        if p.get('toc_ref'):
            indent = "" if p['type'] == 'chapter' else "    "
            title = p.get('text') if p['type'] == 'chapter' else p.get('title')
            toc_items.append({'text': f"{indent}{title}", 'page': i + 1})
    pages[toc_page_index]['items'] = toc_items

    # Manual XML Generation (to control attribute order and spacing exactly)
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<SCRIBUSUTF8NEW Version="1.6.5">')
    
    # DOCUMENT
    xml.append(f'    <DOCUMENT ANZPAGES="{len(pages)}" PAGEWIDTH="{width}" PAGEHEIGHT="{height}" BORDERLEFT="{m["inner"]}" BORDERRIGHT="{m["outer"]}" BORDERTOP="{m["top"]}" BORDERBOTTOM="{m["bottom"]}" PRESET="0" BleedTop="7.087" BleedLeft="7.087" BleedRight="7.087" BleedBottom="7.087" ORIENTATION="0" PAGESIZE="{layout["page_size"]}" FIRSTNUM="1" BOOK="1" AUTOSPALTEN="1" ABSTSPALTEN="11" UNITS="1" DFONT="Courier Prime Regular" DSIZE="11" DLINEADV="18.15" DGAP="0" FORCEDOCLAYOUT="1">')
    
    # Boilerplate
    for n in ["PDF 1.3", "PDF 1.4", "PDF 1.5", "PDF 1.6", "PDF/X-1a", "PDF/X-3", "PDF/X-4", "PostScript"]:
        xml.append(f'        <CheckProfile Name="{n}" autoCheck="1" checkGlyphs="1" checkOverflow="1"/>')
    xml.append('        <COLOR NAME="Black" SPACE="CMYK" C="0" M="0" Y="0" K="100"/>')
    xml.append('        <COLOR NAME="White" SPACE="CMYK" C="0" M="0" Y="0" K="0"/>')
    xml.append('        <HYPHEN/>')
    xml.append('        <CHARSTYLE CNAME="Default Character Style" DefaultStyle="1" FONT="Arial Regular" FONTSIZE="12"/>')
    xml.append('        <STYLE NAME="Default Paragraph Style" DefaultStyle="1" ALIGN="0" LINESP="15"/>')
    xml.append('        <LAYERS NUMMER="0" LEVEL="0" NAME="Background" SICHTBAR="1" DRUCKEN="1" EDIT="1" SELECT="0" FLOW="1"/>')
    xml.append('        <PageSets>')
    xml.append('            <Set Name="Facing Pages" FirstPage="1" Rows="1" Columns="2">')
    xml.append('                <PageNames Name="Left Page"/><PageNames Name="Right Page"/>')
    xml.append('            </Set>')
    xml.append('        </PageSets>')
    xml.append(f'        <Sections Number="0" Name="Section 1" From="0" To="{len(pages)-1}" Type="Type_1_2_3" Start="1" Active="1"/>')
    
    # Master Pages
    xml.append(f'        <MASTERPAGE PAGEXPOS="100" PAGEYPOS="20" PAGEWIDTH="{width}" PAGEHEIGHT="{height}" BORDERLEFT="{m["inner"]}" BORDERRIGHT="{m["outer"]}" BORDERTOP="{m["top"]}" BORDERBOTTOM="{m["bottom"]}" NUM="0" NAM="Normal Left" MNAM="" Size="{layout["page_size"]}" Orientation="0" LEFT="1" PRESET="0"/>')
    xml.append(f'        <MASTERPAGE PAGEXPOS="100" PAGEYPOS="20" PAGEWIDTH="{width}" PAGEHEIGHT="{height}" BORDERLEFT="{m["inner"]}" BORDERRIGHT="{m["outer"]}" BORDERTOP="{m["top"]}" BORDERBOTTOM="{m["bottom"]}" NUM="1" NAM="Normal Right" MNAM="" Size="{layout["page_size"]}" Orientation="0" LEFT="0" PRESET="0"/>')

    # PAGES
    for i, p in enumerate(pages):
        is_left = (p['side'] == 'L')
        page_x = 100 if is_left else 100 + width
        page_y = 20 + (i // 2) * (height + 40)
        m_name = "Normal Left" if is_left else "Normal Right"
        xml.append(f'        <PAGE PAGEXPOS="{page_x}" PAGEYPOS="{page_y}" PAGEWIDTH="{width}" PAGEHEIGHT="{height}" BORDERLEFT="{m["inner"]}" BORDERRIGHT="{m["outer"]}" BORDERTOP="{m["top"]}" BORDERBOTTOM="{m["bottom"]}" NUM="{i}" NAM="" MNAM="{m_name}" Size="{layout["page_size"]}" Orientation="0" LEFT="0" PRESET="0"/>')

    # PAGEOBJECTS
    for i, p in enumerate(pages):
        is_left = (p['side'] == 'L')
        page_x = 100 if is_left else 100 + width
        page_y = 20 + (i // 2) * (height + 40)
        m_l = m['outer'] if is_left else m['inner']
        m_r = m['inner'] if is_left else m['outer']
        fw = width - m_l - m_r
        fh = height - m['top'] - m['bottom']

        # Page Number Frame (Skip for blank, title, chapter, and toc pages)
        if p['type'] not in ['blank', 'title', 'chapter', 'toc']:
            xml.append(f'        <PAGEOBJECT XPOS="{page_x + m_l}" YPOS="{page_y + height - m["bottom"] + 10}" WIDTH="{fw}" HEIGHT="20" OwnPage="{i}" PTYPE="4" FRTYPE="0" LAYER="0" NEXTITEM="-1" BACKITEM="-1" COLUMNS="1" COLGAP="0">')
            xml.append('            <StoryText><DefaultStyle/>')
            xml.append(f'                <ITEXT FONT="{escape_xml(styles["page_number"]["font"])}" FONTSIZE="{styles["page_number"]["size"]}" CH="{i+1}"/>')
            xml.append('                <para ALIGN="1"/><trail ALIGN="1"/>')
            xml.append('            </StoryText>')
            xml.append('        </PAGEOBJECT>')

        # Content Frame
        if p['type'] != 'blank':
            xml.append(f'        <PAGEOBJECT XPOS="{page_x + m_l}" YPOS="{page_y + m["top"]}" WIDTH="{fw}" HEIGHT="{fh}" OwnPage="{i}" ItemID="{2000+i}" PTYPE="4" FRTYPE="0" LAYER="0" NEXTITEM="-1" BACKITEM="-1" COLUMNS="1" COLGAP="0">')
            xml.append(f'            <path value="M0 0 L{fw} 0 L{fw} {fh} L0 {fh} L0 0 Z"/>')
            xml.append('            <StoryText><DefaultStyle/>')
            
            if p['type'] == 'title':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["chapter_title"]["font"])}" FONTSIZE="24" CH="{escape_xml(p["text"])}"/>')
                xml.append('                <para ALIGN="1" VOR="100"/>')
            elif p['type'] == 'quote':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["verse"]["font"])}" FONTSIZE="12" CH="{escape_xml(p["text"])}"/>')
                xml.append('                <para ALIGN="1" VOR="120"/>')
            elif p['type'] == 'colophon':
                # Print at bottom
                voor = fh - 150
                for i, cl in enumerate(p['lines']):
                    xml.append(f'                <ITEXT FONT="{escape_xml(styles["verse"]["font"])}" FONTSIZE="10" CH="{escape_xml(cl)}"/>')
                    spc = voor if i == 0 else 0
                    xml.append(f'                <para ALIGN="0" VOR="{spc}" NACH="5"/>')
            elif p['type'] == 'toc':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["toc_title"]["font"])}" FONTSIZE="18" CH="OBSAH"/>')
                xml.append('                <para ALIGN="1" NACH="20"/>')
                for item in p['items']:
                    xml.append(f'                <ITEXT FONT="{escape_xml(styles["toc_item"]["font"])}" FONTSIZE="11" CH="{escape_xml(item["text"])} .... {item["page"]}"/>')
                    xml.append('                <para ALIGN="0" NACH="5"/>')
            elif p['type'] == 'chapter':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["chapter_title"]["font"])}" FONTSIZE="{styles["chapter_title"]["size"]}" CH="{escape_xml(p["text"])}"/>')
                xml.append('                <para ALIGN="1" VOR="150"/>')
            elif p['type'] == 'poem':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["poem_title"]["font"])}" FONTSIZE="{styles["poem_title"]["size"]}" CH="{escape_xml(p["title"])}"/>')
                xml.append(f'                <para ALIGN="0" NACH="{styles["poem_title"]["space_after"]}"/>')
                for sloka in p.get('stanzas', []):
                    for v in sloka.get('verse', []):
                        xml.append(f'                <ITEXT FONT="{escape_xml(styles["verse"]["font"])}" FONTSIZE="{styles["verse"]["size"]}" CH="{escape_xml(v)}"/>')
                        xml.append('                <para ALIGN="0"/>')
                    xml.append(f'                <para ALIGN="0" NACH="{styles["verse"]["space_after_stanza"]}"/>')
            elif p['type'] == 'illustration':
                xml.append(f'                <ITEXT FONT="{escape_xml(styles["verse"]["font"])}" FONTSIZE="14" CH="[ Ilustrace ]"/>')
                xml.append('                <para ALIGN="1" VOR="200"/>')
                
            xml.append('                <trail ALIGN="0"/>')
            xml.append('            </StoryText>')
            xml.append('        </PAGEOBJECT>')

    xml.append('    </DOCUMENT>')
    xml.append('</SCRIBUSUTF8NEW>')
    
    final_xml = "\n".join(xml)
    output_path = os.path.join(os.path.dirname(json_path), doc_cfg['output_file'])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_xml)
    
    print(f"Guaranteed Scribus file generated: {output_path} ({len(pages)} pages)")

if __name__ == "__main__":
    base_path = r"c:\Users\Marek\Desktop\nudaHypotekyFasismus"
    create_guaranteed_sla(
        os.path.join(base_path, "Blok.json"),
        os.path.join(base_path, "export_config.json")
    )
