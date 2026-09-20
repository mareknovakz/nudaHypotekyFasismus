"""
generator.py — Vygeneruje PDF z content JSON souboru.

Použití:
    python generator.py Hobit_content.json
    python generator.py Impulz_content.json
    python generator.py Blok.json

Hledá odpovídající config: <název>_content.json → export_config_<název>.json
Pro Blok.json použije export_config.json
"""

import sys
import os

if len(sys.argv) < 2:
    print("Použití: python generator.py <content.json>")
    sys.exit(1)

content_file = sys.argv[1]

if not os.path.exists(content_file):
    print(f"Soubor {content_file} neexistuje.")
    sys.exit(1)

# Derive config name: Hobit_content.json → export_config_hobit.json
basename = os.path.splitext(content_file)[0]
if basename.endswith("_content"):
    name = basename.replace("_content", "").lower()
    config_file = f"export_config_{name}.json"
elif basename == "Blok":
    config_file = "export_config.json"
else:
    config_file = f"export_config_{basename.lower()}.json"

if not os.path.exists(config_file):
    print(f"Config {config_file} nenalezen.")
    sys.exit(1)

output_typ = basename.split("_content")[0] + ".typ"
output_pdf = output_typ.replace(".typ", ".pdf")

print(f"Content: {content_file}")
print(f"Config:  {config_file}")
print(f"Output:  {output_pdf}")
print()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typst_gen import create_typst_file

create_typst_file(content_file, config_file, output_typ)

import subprocess
result = subprocess.run(
    [sys.executable, "generatePdf.py", output_typ],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

if os.path.exists(output_typ):
    os.remove(output_typ)

sys.exit(result.returncode)
