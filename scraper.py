from playwright.sync_api import sync_playwright, Playwright
from parser import psg, parse
import csv

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()

    # psg.clearAll() # i added db clear to test
    # psg.create()

    page = browser.new_page()

    # with open("websitesSmall.csv") as f:
    #     for line in f:
    #         url = "https://" + line.strip()
    #         try:
    #             page.goto(url, timeout=10000)
    #             html = page.content()
    #             psg.insertHtml(url, html)
    #         except Exception as e:
    #             print(f"failed {url} - {e}")
    #             continue

    psg.parseDBHtml()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)