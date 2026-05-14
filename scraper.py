from playwright.sync_api import sync_playwright, Playwright
from parser import psg, parse
import csv

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()

    psg.clearAll() # i added db clear to test
    psg.create()

    page = browser.new_page()

    with open("websites.csv") as f:
        for line in f:
            url = "https://" + line.strip()
            try:
                page.goto(url, timeout=30000)
                page.wait_for_load_state('domcontentloaded', timeout=10000)
                html = page.content()
                psg.insertHtml(url, html)
            except Exception as e:
                print(f"failed {url} - {e}")
                with open('output/failed.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([url, e])
                continue

    psg.parseDBHtml()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)