from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    html_content = page.content()
    print(html_content)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)