
import json
import re
import os

def check_typography(text):
    errors = []
    
    if not text:
        return errors

    # 1. Rovné uvozovky
    if '"' in text:
        errors.append("Nalezena rovná uvozovka (\") - použij „ “")

    # 2. Tři tečky místo výpustky
    if '...' in text:
        errors.append("Nalezeny tři tečky (...) - použij výpustku (…)")

    # 3. Spojovník místo pomlčky v textu
    if ' - ' in text:
        errors.append("Nalezen spojovník s mezerami ( - ) - použij pomlčku ( – )")

    # 4. Jednopísmenné předložky na konci slov/řádku bez vlnovky
    preps = ['k', 's', 'v', 'z', 'o', 'u', 'a', 'i']
    for p in preps:
        # Hledáme předložku následovanou obyčejnou mezerou na konci stringu nebo před dalším slovem
        if re.search(rf'\b{p}\s+', text, re.IGNORECASE):
            errors.append(f"Předložka '{p}' není spojena s dalším slovem nezlomitelnou mezerou (~)")

    # 5. Dvojité mezery
    if '  ' in text:
        errors.append("Nalezena dvojitá mezera")

    return errors

def run_proofreader():
    json_path = "Blok.json"
    report_path = "korektura_report.txt"
    
    if not os.path.exists(json_path):
        print(f"Chyba: Soubor {json_path} nenalezen.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    report = []
    report.append("=== REPORTOVÁ ZPRÁVA KOREKTORA ===\n")
    
    error_count = 0
    
    for k_idx, kapitola in enumerate(data.get('kapitoly', [])):
        chap_name = kapitola.get('nazev', f'Kapitola {k_idx+1}')
        
        for b_idx, basen in enumerate(kapitola.get('basne', [])):
            poem_name = basen.get('nazev', f'Basen {b_idx+1}')
            
            for s_idx, sloka in enumerate(basen.get('sloky', [])):
                for v_idx, vers in enumerate(sloka.get('verse', [])):
                    issues = check_typography(vers)
                    
                    if issues:
                        report.append(f"Lokalita: {chap_name} -> {poem_name}")
                        report.append(f"Verš: \"{vers}\"")
                        for issue in issues:
                            report.append(f"  [!] {issue}")
                        report.append("-" * 30)
                        error_count += len(issues)

    if error_count == 0:
        report.append("\nNebyla nalezena žádná typografická pochybení. Dobrá práce!")
    else:
        report.append(f"\nCelkem nalezeno chyb: {error_count}")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"Korektura dokoncena. Vysledek ulozen do: {report_path}")
    print(f"Nalezeno chyb: {error_count}")

if __name__ == "__main__":
    run_proofreader()
