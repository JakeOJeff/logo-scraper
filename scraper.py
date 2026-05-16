from playwright.sync_api import sync_playwright, Playwright
from concurrent.futures import ThreadPoolExecutor

from parser import psg, parse
import csv, psutil, os, time


def startScrape(url):
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch(args=['--disable-http2'])
        page = browser.new_page(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        try:
            page.goto(url, timeout=10000, wait_until="domcontentloaded", )
            html = page.content()
            print(f"appended {url}")
            return (url, html)
        except Exception as e:
            print(f"failed {url} - {str(e).split('\n')[0]}")
            with open('output/failed.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([url, str(e).split('\n')[0]])
            return None
        finally:
            browser.close()


def run():
    # benchmarking
    funcStartTime = time.time()

    psg.clearAll() # i added db clear to test
    psg.create()

    insertStartTime = time.time()

    urls = []
    with open("websitesSmall.csv") as f:
        urls = ["https://" + line.strip() for line in f]

    with ThreadPoolExecutor(5) as executor:
        results = executor.map(startScrape, urls)


    buff = [r for r in results if r is not None]
    psg.insertHtmlSet(buff)


    parseStartTime = time.time()
    psg.parseDBHtml()
    
    process = psutil.Process(os.getpid())

    # benchmark stats
    print(f"RAM used:   {process.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"CPU time:   {process.cpu_times().user:.2f}s")
    print(f"Total Time: {time.time() - funcStartTime:.2f}s")
    print(f"Scraping/Inserting Time: {time.time() - insertStartTime:.2f}s")
    print(f"Parsing Time: {time.time() - parseStartTime:.2f}s")



if __name__ == "__main__":
    run()