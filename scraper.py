from playwright.sync_api import sync_playwright, Playwright
from parser import psg
import csv

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch()
    psg.create()
    page = browser.new_page()

    with open("websitesSmall.csv") as f:
        for line in f:
            url = "https://" + line.strip()
            page.goto(url)
            html = page.content()
            psg.insertHtml(url, html)

    browser.close()

with sync_playwright() as playwright:
    run(playwright)