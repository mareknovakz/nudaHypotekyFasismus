"""
tts_impulz.py — Asynchronní český TTS pro Impulz.
Generuje MP3 soubor per kapitola pomocí edge-tts (Microsoft Neural TTS).

Použití:
    python tts_impulz.py                  # všechny kapitoly
    python tts_impulz.py --chapters 1 3   # jen kapitoly I a III
    python tts_impulz.py --voice vlasta   # ženský hlas
    python tts_impulz.py --rate -10%      # pomalejší

Výstup: audio/impulz_I.mp3, audio/impulz_II.mp3, ...
"""

import asyncio
import json
import os
import sys
import argparse
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VOICES = {
    "antonin": "cs-CZ-AntoninNeural",   # mužský
    "vlasta":  "cs-CZ-VlastaNeural",     # ženský
}

INPUT_FILE  = "impulz.json"
OUTPUT_DIR  = "audio"


def load_chapters(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["chapters"]


def chapter_to_ssml(chapter: dict) -> str:
    """Převede kapitolu na čistý text s pauzami mezi odstavci."""
    lines = []
    for para in chapter["paragraphs"]:
        text = para.strip()
        if text in ("* * *", "***"):
            lines.append("\n\n")  # delší pauza pro scene break
        else:
            lines.append(text)
    return "\n\n".join(lines)


async def generate_chapter(chapter: dict, voice: str, rate: str, output_dir: str):
    """Vygeneruje MP3 pro jednu kapitolu."""
    import edge_tts

    num = chapter["number"]
    text = chapter_to_ssml(chapter)
    outfile = os.path.join(output_dir, f"impulz_{num}.mp3")

    para_count = len(chapter["paragraphs"])
    char_count = len(text)
    print(f"  Kap. {num}: {para_count} odstavcu, {char_count} znaku -> {outfile}")

    start = time.time()
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(outfile)
    elapsed = time.time() - start

    size_mb = os.path.getsize(outfile) / 1024 / 1024
    print(f"  Kap. {num}: hotovo za {elapsed:.1f}s ({size_mb:.1f} MB)")


async def main(args):
    chapters = load_chapters(args.input)
    voice = VOICES.get(args.voice, args.voice)
    rate = args.rate

    os.makedirs(args.output, exist_ok=True)

    if args.chapters:
        roman = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",
                 7:"VII",8:"VIII",9:"IX",10:"X",11:"XI",12:"XII"}
        selected = {roman.get(c, str(c)) for c in args.chapters}
        chapters = [ch for ch in chapters if ch["number"] in selected]

    print(f"Hlas: {voice}")
    print(f"Tempo: {rate}")
    print(f"Kapitol: {len(chapters)}")
    print(f"Vystup: {args.output}/")
    print()

    for chapter in chapters:
        await generate_chapter(chapter, voice, rate, args.output)

    print(f"\nHotovo! Audio soubory v {args.output}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cesky TTS pro Impulz")
    parser.add_argument("--input",    default=INPUT_FILE, help="Vstupni JSON")
    parser.add_argument("--output",   default=OUTPUT_DIR,  help="Vystupni adresar")
    parser.add_argument("--voice",    default="antonin",   choices=list(VOICES.keys()),
                        help="Hlas: antonin (muz) nebo vlasta (zena)")
    parser.add_argument("--rate",     default="-5%",        help="Tempo: -10%% pomaleji, +10%% rychleji")
    parser.add_argument("--chapters", type=int, nargs="*", help="Jen urcite kapitoly (cisla 1-12)")
    args = parser.parse_args()
    asyncio.run(main(args))
