from playwright.sync_api import sync_playwright
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto('https://aleph.nkp.cz/F/?func=file&file_name=service-isbn-nak')
page.wait_for_load_state('networkidle')

# --- Údaje o vydavateli ---
page.fill('input[name="N0401NAK__a"]', 'PVL, z. s.')
page.fill('input[name="N0501ADN__a"]', 'Heřmanova 1087/10, 170 00 Praha 7')
page.fill('input[name="N0601ICO__a"]', '23917121')
page.fill('input[name="N08018560_u"]', 'mareknovak.z@gmail.com')

# --- Údaje o knize (sekce P = první publikace) ---
page.fill('input[name="P07012001_a"]', 'Nuda, hypotéky, fašismus')
page.fill('input[name="P1301ZAK__b"]', 'Mrkvička, Mirek')
page.fill('input[name="P0901210__a"]', 'Praha')
page.fill('input[name="P0902210__c"]', 'PVL, z. s.')
page.fill('input[name="P0903210__d"]', '2026')
page.fill('input[name="P0801205__a"]', 'První vydání')

# Tištěná kniha - brožovaná
page.check('input[name="P1601ISB__b"]')

# Odesilatel žádosti
page.fill('input[name="P1502IST1_b"]', 'Marek Novák')

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
print("Formular vyplnen. Neodesilam. Zavri prohlizec rucne.")

# Keep browser open until user closes it
try:
    page.wait_for_event('close', timeout=0)
except:
    pass

browser.close()
pw.stop()
