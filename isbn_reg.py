import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto('https://aleph.nkp.cz/F/?func=file&file_name=service-nak-rgk')
page.wait_for_load_state('networkidle')

page.fill('input[name="pas"]', 'IsBN-13')
page.click('input[type="submit"]')
page.wait_for_load_state('networkidle')

# First fill ICO and try "Nacist data z registru"
page.fill('input[name="P0701ICO__a"]', '23917121')
try:
    page.click('input[value="Načíst data z registru"]', timeout=5000)
    page.wait_for_load_state('networkidle')
    print("Clicked 'Nacist data z registru'")
    import time
    time.sleep(3)
except Exception as e:
    print(f"Registry button: {e}")

# Fill/overwrite fields
fill = {
    'P0501NAK__a': 'PVL, z. s.',
    'P0701ICO__a': '23917121',
    'P0802ADN__u': 'Hermanova 1087/10, 170 00 Praha 7',
    'P1001TEL__a': '607178462',
    'P12018560_u': 'mareknovak.z@gmail.com',
    'P1501CIN__z': 'vydavatelska cinnost, podpora poezie',
    'P1801GAR__a': 'Marek Novak',
    'P1803GAR__t': '607178462',
    'P1804GAR__e': 'mareknovak.z@gmail.com',
    'P1901ZAM__a': 'beletrie, poezie',
}

print("\n=== FILLING ===")
for name, value in fill.items():
    try:
        el = page.locator(f'input[name="{name}"]')
        if el.count() > 0:
            el.fill(value)
            print(f"  OK: {name} = {value}")
        else:
            print(f"  NOT FOUND: {name}")
    except Exception as e:
        print(f"  ERR: {name} - {e}")

print("\nForm filled. Use 'Tisknout' to export PDF, 'Odeslat' to submit.")
print("Close browser when done.")
sys.stdout.flush()

try:
    page.wait_for_event('close', timeout=0)
except:
    pass

browser.close()
pw.stop()
