from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=True)
page = browser.new_page()
page.goto('https://aleph.nkp.cz/F/?func=file&file_name=service-isbn-nak')

# Get all input and select elements
inputs = page.eval_on_selector_all('input, select, textarea', """els => els.map(el => ({
    tag: el.tagName,
    type: el.type || '',
    name: el.name || '',
    id: el.id || '',
    value: el.value || '',
    placeholder: el.placeholder || ''
}))""")

for inp in inputs:
    print(f"{inp['tag']:10} name={inp['name']:30} type={inp['type']:15} id={inp['id']}")

browser.close()
pw.stop()
