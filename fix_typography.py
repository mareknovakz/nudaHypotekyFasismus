
import json
import re
import os

def apply_fixes(text):
    if not text: return ""
    
    # 1. Dvojité mezery pryč
    text = re.sub(r' +', ' ', text)

    # 2. Náhrada rovných uvozovek za české 99 a 66
    # Tato regex logika hledá slova v uvozovkách
    text = re.sub(r'(^|[\s\(])"([^"]+)"', r'\1„\2“', text)
    # Zbytek osamocených uvozovek (pokud zbyly) zkusíme chytit aspoň jako dolní
    text = text.replace(' "', ' „')

    # 3. Výpustka
    text = re.sub(r'\.{3,}', '…', text)

    # 4. Pomlčky (spojovník obklopený mezerami)
    text = text.replace(' - ', ' – ')

    # 5. Nezlomitelné mezery za jednopísmenné předložky a spojky
    preps = ['k', 's', 'v', 'z', 'o', 'u', 'a', 'i', 'K', 'S', 'V', 'Z', 'O', 'U', 'A', 'I']
    # Spustíme dvakrát kvůli případům jako "v a z"
    for _ in range(2):
        for p in preps:
            # Hledáme předložku na začátku řádku nebo po mezeře/uvozovce, následovanou mezerou
            text = re.sub(rf'(^|[\s„"\'\(\[])({p})\s+', r'\1\2~', text)
            
    return text

def fix_json():
    json_path = "Blok.json"
    backup_path = "Blok_backup_before_fix.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Záloha pro jistotu
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Procházení a opravy
    for kapitola in data.get('kapitoly', []):
        for basen in kapitola.get('basne', []):
            for sloka in basen.get('sloky', []):
                new_verses = []
                for vers in sloka.get('verse', []):
                    new_verses.append(apply_fixes(vers))
                sloka['verse'] = new_verses

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Oprava dokoncena. Zaloha vytvorena v Blok_backup_before_fix.json")

if __name__ == "__main__":
    fix_json()
