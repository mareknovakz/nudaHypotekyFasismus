"""
print.py — Vygeneruje Blok_production.pdf (Nuda, hypotéky, fašismus) z Blok.json.

Tenký wrapper kolem generator.py. Pro jiné knihy použij přímo:
    python generator.py <content.json>
"""

import sys
import os
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    print("--- Starting Book Generation Flow ---")

    # Remove stale PDFs before regenerating
    for old_pdf in ["Blok_production.pdf", "Blok.pdf"]:
        if os.path.exists(old_pdf):
            os.remove(old_pdf)
            print(f"Removed old: {old_pdf}")

    result = subprocess.run(
        [sys.executable, "generator.py", "Blok.json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print("\n[!] Stopping: generator.py selhal")
        sys.exit(result.returncode)

    if os.path.exists("Blok.pdf"):
        if os.path.exists("Blok_production.pdf"):
            os.remove("Blok_production.pdf")
        os.rename("Blok.pdf", "Blok_production.pdf")
        print("Renamed: Blok.pdf -> Blok_production.pdf")

    print("\n--- DONE! Print-ready PDF: Blok_production.pdf ---")


if __name__ == "__main__":
    main()
