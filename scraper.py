from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("http://example.com")
    texts = page.get_by_role("link").all_text_contents()
    print(texts)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)