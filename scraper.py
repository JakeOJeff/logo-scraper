from playwright.sync_api import sync_playwright

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("httpp://example.com")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)