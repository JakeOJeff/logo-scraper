import asyncio
from playwright.async_api import async_playwright, Playwright
from parser import psg, parse
import csv

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=True)

    psg.clearAll() # i added db clear to test
    psg.create()

    page = await browser.new_page()

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
                    writer.writerow([url, str(e).split('\n')[0]])
                
                try:
                    page.goto('about:blank', timeout=50000)
                except:
                    pass
                continue

    psg.parseDBHtml()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)