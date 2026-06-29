import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)
page = browser.new_page()
page.goto('https://docs.google.com/forms/d/e/1FAIpQLSfeRxDRBjwGpMIxPbfe0rFw11WnaOk9ul9effHRdvkExRPDsw/viewform')
page.wait_for_load_state('networkidle')
time.sleep(3)

# Q1 - two checkboxes (3rd and 4th options)
checkboxes_q1 = page.locator('[data-params*="jednoznačně"]').first
if checkboxes_q1.count() == 0:
    # Try finding by aria labels or list items
    # Get all question containers
    pass

# Let's use a more robust approach - find all questions and their options
questions = page.locator('[role="listitem"]').all()
print(f"Found {len(questions)} sections")

for i, q in enumerate(questions):
    text = q.inner_text()[:80]
    print(f"Section {i}: {text}")

print("\n--- Filling answers ---")

# Helper to click checkbox/radio by partial text within a question section
def click_option(section_index, option_text):
    section = questions[section_index]
    try:
        option = section.locator(f'label:has-text("{option_text}")').first
        option.click()
        print(f"  Q{section_index}: clicked '{option_text[:50]}'")
        time.sleep(0.3)
    except Exception as e:
        print(f"  Q{section_index}: FAILED '{option_text[:50]}' - {e}")

# Q1 (2 answers - checkboxes)
click_option(1, "jednoznačně identifikující")
click_option(1, "každá monografická publikace")

# Q2
click_option(2, "třetí skupina číslic")

# Q3
click_option(3, "čtvrtá skupina číslic")

# Q4 (2 answers - checkboxes)
click_option(4, "svého grafika či tiskárnu")
click_option(4, "České národní agentuře ISBN")

# Q5
click_option(5, "čárový kód")

# Q6
click_option(6, "Jen a pouze ty, u nichž to vyžaduje")

# Q7
click_option(7, "je to mluvené slovo")

# Q8
click_option(8, "jedno pro knihu s přílohou, jedno pro online v PDF")

# Q9
click_option(9, "nové ISBN a do tiráže")

# Q10
click_option(10, "nezměněné vydání, takže stejné ISBN")

# Q11 (multiple answers)
click_option(11, "na konci tiráže")
click_option(11, "zadní straně obálky")
click_option(11, "záhlaví čárového kódu")
click_option(11, "rub titulního listu")

# Q12
click_option(12, "plně postačuje jedno ISBN")

# Q13
click_option(13, "My, vzhledem k formulaci")

# Q14
click_option(14, "změnu musíme ohlásit")

# Q15
click_option(15, "Podívám se do Příručky")

# Q16 - text input "debac"
try:
    section16 = questions[16]
    text_input = section16.locator('input[type="text"], textarea').first
    text_input.fill('debac')
    print("  Q16: filled 'debac'")
except Exception as e:
    print(f"  Q16: FAILED - {e}")

# Q17
click_option(17, "závazek trvající do ukončení")

print("\nForm filled. Review and submit manually.")
sys.stdout.flush()

try:
    page.wait_for_event('close', timeout=0)
except:
    pass

browser.close()
pw.stop()
