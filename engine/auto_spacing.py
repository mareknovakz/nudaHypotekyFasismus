"""
auto_spacing.py  –  změří mezery v Blok_Slim.pdf a porovná
                    inter-verš vs inter-sloka vs inter-odstavec (próza).

Použití:
    python auto_spacing.py                    – jen změří, nic nemění
    python auto_spacing.py --apply VALUE      – zapíše space_after_stanza=VALUE do
                                               export_config.json a přegeneruje PDF
    python auto_spacing.py --apply            – použije naměřenou větší hodnotu
"""

import sys, json, statistics, os
import fitz

sys.stdout.reconfigure(encoding="utf-8")

PDF = "Blok_Slim.pdf"
CFG = "export_config.json"

POETRY_REF = ["Wine culture", "Prsty lžou", "Kachny"]
PROSE_REF  = ["Václav Klaus", "Fíkus", "3:15"]

# Minimální gap (pt) aby byl považován za inter-group (sloka/odstavec)
GROUP_THRESH = 5.0


def get_lines(page):
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    lines = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        for ln in block["lines"]:
            text = "".join(s["text"] for s in ln["spans"]).strip()
            if len(text) < 2:
                continue
            lines.append(ln["bbox"])
    lines.sort(key=lambda b: b[1])
    return lines


def classify_gaps(lines):
    """Vrátí (inter_line_gaps, inter_group_gaps) pro jednu stránku."""
    small, large = [], []
    for (_, _, _, y1), (_, y0, _, _) in zip(lines[:-1], lines[1:]):
        g = round(y0 - y1, 2)
        if g <= 0 or g > 80:        # záporné nebo příliš velké = přeskok stránky/nadpis
            continue
        if g < GROUP_THRESH:
            small.append(g)
        else:
            large.append(g)
    return small, large


def find_page(doc, title):
    for i, page in enumerate(doc):
        if title.lower() in page.get_text().lower():
            return i
    return None


def measure_refs(doc, refs, label):
    all_il, all_ig = [], []
    for title in refs:
        pg = find_page(doc, title)
        if pg is None:
            continue
        # zkus stránku s názvem i následující
        for candidate in [pg, pg + 1]:
            if candidate >= len(doc):
                continue
            lines = get_lines(doc[candidate])
            if len(lines) < 6:
                continue
            il, ig = classify_gaps(lines)
            # stránka s inter-group mezerami = stránka s obsahem (ne čistý nadpis)
            if ig:
                all_il.extend(il)
                all_ig.extend(ig)
                il_med = f"{statistics.median(il):.2f}pt" if il else "—"
                ig_med = f"{statistics.median(ig):.2f}pt"
                print(f"  [{label:7s}] '{title}' str.{candidate+1}: "
                      f"inter-line={il_med} (n={len(il)}), "
                      f"inter-group={ig_med} (n={len(ig)})")
                break
    il_med = statistics.median(all_il) if all_il else None
    ig_med = statistics.median(all_ig) if all_ig else None
    return il_med, ig_med


def main():
    args = sys.argv[1:]
    apply_mode = "--apply" in args
    forced_val = None
    if apply_mode:
        idx = args.index("--apply")
        if idx + 1 < len(args):
            try:
                forced_val = float(args[idx + 1])
            except ValueError:
                pass

    doc = fitz.open(PDF)
    print(f"\nPDF: {PDF}   threshold inter-group: >{GROUP_THRESH}pt")
    print("─" * 60)

    p_il, p_ig = measure_refs(doc, POETRY_REF, "poezie")
    r_il, r_ig = measure_refs(doc, PROSE_REF,  "próza")
    doc.close()

    print()
    print("─" * 60)
    fmt = lambda v: f"{v:.2f} pt" if v is not None else "— (nenalezeno)"
    print(f"  Poezie  inter-line  (uvnitř sloky):     {fmt(p_il)}")
    print(f"  Poezie  inter-group (mezi slokami):      {fmt(p_ig)}")
    print(f"  Próza   inter-line  (uvnitř odstavce):   {fmt(r_il)}")
    print(f"  Próza   inter-group (mezi odstavci):     {fmt(r_ig)}")

    # Načti aktuální config
    with open(CFG, encoding="utf-8-sig") as f:
        cfg = json.load(f)
    cur = cfg["styles"]["verse"]["space_after_stanza"]
    ls  = cfg["styles"]["verse"]["line_spacing"]
    sz  = cfg["styles"]["verse"]["size"]
    print(f"\n  Aktuální space_after_stanza: {cur} pt")
    print(f"  Řádkování: {ls}/{sz} = {ls/sz:.2f}×  (line_spacing v export_config.json)")

    if p_ig is None and r_ig is None:
        print("\n[!] Nepodařilo se naměřit inter-group mezery.")
        return

    candidates = [v for v in [p_ig, r_ig] if v is not None]
    target = max(candidates)
    bigger = "poezie" if (p_ig or 0) >= (r_ig or 0) else "próza"
    print(f"\n  Větší inter-group: {bigger}  →  naměřená cílová hodnota = {target:.2f} pt")

    if forced_val is not None:
        target = forced_val
        print(f"  (Přepsáno ručně na: {target} pt)")

    diff = abs((p_ig or 0) - (r_ig or 0))
    if diff < 0.5:
        print("  → Mezery jsou prakticky stejné. Nic není třeba měnit.")
        if not apply_mode:
            return

    if not apply_mode:
        print(f"\n  Doporučení: nastavit space_after_stanza = {target:.2f} pt")
        print("  Spusť s --apply [VALUE] pro zápis.")
        return

    # ── Zápis ────────────────────────────────────────────────────────────────
    new_val = round(target, 2)
    cfg["styles"]["verse"]["space_after_stanza"] = new_val
    with open(CFG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
    print(f"\n  ✓ export_config.json: space_after_stanza = {new_val} pt")

    print("  Spouštím print.py …\n")
    os.system(f'"{sys.executable}" print.py')


if __name__ == "__main__":
    main()
