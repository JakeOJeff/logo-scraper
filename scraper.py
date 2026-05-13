from playwright.sync_api import sync_playwright, Playwright
from parser import psg

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    psg.create()
    page = browser.new_page()

    url = "https://example.com"
    page.goto(url)
    htmlContent = page.content()
    
    print(htmlContent)
    
    psg.insertHtml(url, htmlContent)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)