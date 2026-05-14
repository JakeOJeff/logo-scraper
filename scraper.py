from playwright.sync_api import sync_playwright, Playwright
from parser import psg, parse
import csv

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()

    psg.clearAll() # i added db clear to test
    psg.create()

    page = browser.new_page()

    with open("websitesSmall.csv") as f:
        buff = []
        for line in f:
            url = "https://" + line.strip()
            try:
                page.goto(url, timeout=10000)
                page.wait_for_load_state('domcontentloaded', timeout=10000)
                html = page.content()
                buff.append((url, html))
                print(f"appended {url}")
            except Exception as e:
                print(f"failed {url} - {e}")
                with open('output/failed.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([url, str(e).split('\n')[0]])
                continue
        psg.insertHtmlSet(buff)


    psg.parseDBHtml()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)