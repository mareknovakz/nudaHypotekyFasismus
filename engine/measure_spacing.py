"""
measure_spacing.py – automaticky změří řádkování v Blok_Slim.pdf
a porovná básně vs prózu.

Jak to funguje:
  - pymupdf vrátí přesné bbox každého textového řádku (žádné screenshoty)
  - stránky se automaticky klasifikují jako poezie/próza
    podle variability délky řádků (krátké/nerovnoměrné = poezie)
  - výsledek: průměrné řádkování v bodech pro oba typy

Použití:
    python measure_spacing.py [cesta_k_pdf]
"""

import sys
import statistics
import fitz  # pymupdf

# Windows PowerShell může mít CP1250 – přepni stdout na UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


PDF = "Blok_Slim.pdf"


def get_line_bboxes(page) -> list[tuple[float, float, float, float]]:
    """Vrátí seznam (x0, y0, x1, y1) textových řádků na stránce."""
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    lines = []
    for block in blocks:
        if block.get("type") != 0:  # pouze textové bloky
            continue
        for line in block.get("lines", []):
            bbox = line["bbox"]
            # přeskoč prázdné nebo velmi krátké řádky (čísla stránek apod.)
            text = "".join(s["text"] for s in line.get("spans", [])).strip()
            if len(text) < 3:
                continue
            lines.append(bbox)
    # seřadit shora dolů
    lines.sort(key=lambda b: b[1])
    return lines


def page_line_spacing(lines: list) -> list[float]:
    """Mezery od paty jednoho řádku (y1) po hlavu dalšího (y0)."""
    gaps = []
    for (_, _, _, y1), (_, y0, _, _) in zip(lines[:-1], lines[1:]):
        gap = y0 - y1
        if 0 < gap < 30:  # ignoruj velké skoky (mezera mezi odstavci/slokami)
            gaps.append(round(gap, 2))
    return gaps


def classify_page(lines: list, page_width: float) -> str:
    """
    Próza (justify): většina řádků sahá k pravému okraji textového sloupce.
    Poezie: řádky se liší délkou, pravý okraj je variabilní.

    Strategie: vezmi max x1 na stránce jako "šířka bloku".
    Spočítej, kolik % řádků se pravým okrajem blíží k tomuto maximu (±5 pt).
    Próza → typicky 50-70 %+ "plných" řádků (každý odstavec krom posledního řádku).
    Poezie → typicky pod 30 % "plných" řádků.
    """
    if len(lines) < 4:
        return "unknown"
    max_x1 = max(b[2] for b in lines)
    full = sum(1 for b in lines if b[2] >= max_x1 - 5)
    ratio = full / len(lines)
    return "prose" if ratio >= 0.35 else "poetry"


def analyze(pdf_path: str):
    doc = fitz.open(pdf_path)
    page_width = doc[0].rect.width

    poetry_gaps = []
    prose_gaps  = []
    poetry_pages = []
    prose_pages  = []

    for i, page in enumerate(doc):
        lines = get_line_bboxes(page)
        if len(lines) < 4:
            continue

        kind = classify_page(lines, page_width)
        gaps = page_line_spacing(lines)
        if not gaps:
            continue

        if kind == "poetry":
            poetry_gaps.extend(gaps)
            poetry_pages.append(i + 1)
        elif kind == "prose":
            prose_gaps.extend(gaps)
            prose_pages.append(i + 1)

    doc.close()

    print(f"\nPDF: {pdf_path}")
    print(f"Šířka stránky: {page_width:.1f} pt\n")

    def report(label, gaps, pages):
        if not gaps:
            print(f"  [{label}] žádné stránky nenalezeny")
            return
        mean   = statistics.mean(gaps)
        median = statistics.median(gaps)
        stdev  = statistics.stdev(gaps) if len(gaps) > 1 else 0
        print(f"  {label.upper()} ({len(pages)} stránek: {pages[:6]}{'…' if len(pages)>6 else ''})")
        print(f"    Průměrná mezera řádku:  {mean:.2f} pt")
        print(f"    Medián:                 {median:.2f} pt")
        print(f"    Std. odchylka:          {stdev:.2f} pt")
        print(f"    Měřeno mezer:           {len(gaps)}")
        return mean

    print("-" * 45)
    m_poetry = report("poezie", poetry_gaps, poetry_pages)
    print()
    m_prose  = report("próza",  prose_gaps,  prose_pages)
    print("-" * 45)

    if m_poetry and m_prose:
        diff = m_poetry - m_prose
        print(f"\n  Rozdíl poezie − próza: {diff:+.2f} pt")
        if abs(diff) < 0.5:
            print("  -> Radkovani je prakticky stejne (OK)")
        elif diff > 0:
            print("  → Poezie má větší mezery než próza")
        else:
            print("  → Próza má větší mezery než poezie")


def find_poem_page(doc, title: str) -> int | None:
    """Najde číslo stránky (0-based) kde se vyskytuje název básně."""
    for i, page in enumerate(doc):
        if title.lower() in page.get_text().lower():
            return i
    return None


def measure_reference_pages(pdf_path: str):
    """
    Změří řádkování na konkrétních referenčních stránkách.
    Hledá první stránku OBSAHUJÍCÍ daný text, pak vezme NÁSLEDUJÍCÍ stránku
    (název je na kapitolní stránce, text básně začíná na další).
    """
    POETRY_REFS = ["Prsty lžou", "Moje vnitřní žena", "Kachny"]
    PROSE_REFS  = ["Václav Klaus", "Fíkus", "3:15"]

    doc = fitz.open(pdf_path)
    print("\n--- Referenční stránky ---")

    def measure_title(titles, label):
        all_gaps = []
        for title in titles:
            pg = find_poem_page(doc, title)
            if pg is None:
                continue
            # text básně je na stejné nebo následující stránce
            for candidate in [pg, pg + 1]:
                if candidate >= len(doc):
                    continue
                lines = get_line_bboxes(doc[candidate])
                gaps  = page_line_spacing(lines)
                if gaps:
                    all_gaps.extend(gaps)
                    print(f"  {label:7s} '{title}': str. {candidate+1}, "
                          f"med={statistics.median(gaps):.2f} pt, "
                          f"n={len(gaps)}")
                    break
        if all_gaps:
            print(f"  {label.upper()} celkem → medián: {statistics.median(all_gaps):.2f} pt, "
                  f"průměr: {statistics.mean(all_gaps):.2f} pt\n")
        return statistics.median(all_gaps) if all_gaps else None

    m_p = measure_title(POETRY_REFS, "poezie")
    m_r = measure_title(PROSE_REFS,  "próza")

    if m_p and m_r:
        diff = m_p - m_r
        print(f"  Rozdíl medián: {diff:+.2f} pt  "
              f"({'stejné' if abs(diff) < 0.3 else 'RUZNE'})")
    doc.close()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else PDF
    analyze(path)
    measure_reference_pages(path)
