
import json
import re

def apply_fixes(text):
    if not text: return ""
    
    # 1. Čištění mezer
    text = re.sub(r' +', ' ', text)

    # 2. České uvozovky (hledáme text v rovných uvozovkách)
    text = re.sub(r'(^|[\s\(\[])"([^"]+)"', r'\1„\2“', text)

    # 3. Výpustky
    text = re.sub(r'\.{3,}', '…', text)

    # 4. Pomlčky
    text = text.replace(' - ', ' – ')

    # 5. Čištění špatných vlnovek (v~ )
    text = re.sub(r'([ksvzouaiKSVZOUAI])~ +', r'\1~', text)

    # 6. Doplnění vlnovek za předložky
    preps = ['k', 's', 'v', 'z', 'o', 'u', 'a', 'i', 'K', 'S', 'V', 'Z', 'O', 'U', 'A', 'I']
    for _ in range(2):
        for p in preps:
            # Předložka na začátku nebo po mezeře, následovaná mezerou
            text = re.sub(rf'(^|[\s„"\'\(\[])({p}) +', r'\1\2~', text)
            
    return text

def run_fix(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for kapitola in data.get('kapitoly', []):
        for basen in kapitola.get('basne', []):
            for sloka in basen.get('sloky', []):
                sloka['verse'] = [apply_fixes(v) for v in sloka.get('verse', [])]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Hotovo: {filename}")

if __name__ == "__main__":
    run_fix('Blok_backup_before_fix.json')
