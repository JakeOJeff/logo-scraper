from playwright.sync_api import sync_playwright, Playwright
from parser import psg, parse
import csv, psutil, os, time

def run(playwright: Playwright):
    # benchmarking
    funcStartTime = time.time()

    chromium = playwright.chromium
    browser = chromium.launch()

    psg.clearAll() # i added db clear to test
    psg.create()

    page = browser.new_page()


    insertStartTime = time.time()

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
                print(f"failed {url} - {str(e).split('\n')[0]}")
                with open('output/failed.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([url, str(e).split('\n')[0]])
                continue
        psg.insertHtmlSet(buff)


    parseStartTime = time.time()
    psg.parseDBHtml()
    browser.close()
    process = psutil.Process(os.getpid())

    # benchmark stats
    print(f"RAM used:   {process.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"CPU time:   {process.cpu_times().user:.2f}s")
    print(f"Total Time: {time.time() - funcStartTime:.2f}s")
    print(f"Scraping/Inserting Time: {time.time() - insertStartTime:.2f}s")
    print(f"Parsing Time: {time.time() - parseStartTime:.2f}s")

with sync_playwright() as playwright:
    run(playwright)