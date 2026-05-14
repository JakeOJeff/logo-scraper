import asyncio
import os
from playwright.async_api import async_playwright, Playwright
from parser import psg, parse, worker
import csv

async def run(playwright: Playwright):
    chromium = playwright.chromium

    urls = []
    with open("websites.csv") as f:
        for line in f:
            url = "https://" + line.strip()
            urls.append(url)

    psg.clearAll() # i added db clear to test
    psg.create()

    chunks = []
    NUMWORKERS = 3
    for i in range(NUMWORKERS):
        chunks.append([])

    i = 0
    for url in urls:
        chunks[i].append(url)
        i = i + 1
        if i >= NUMWORKERS:
            i = 0
        
    # instead of individualistic assigning, giving seperate browsers, with running couroutines
    async with async_playwright() as playwright:
        browser = await chromium.launch(headless=True)

        tasks = []
        for i in range(NUMWORKERS):
            task = scrapeWorker(browser, chunks[i], i)
            tasks.append(task)

        await asyncio.gather(*tasks)

        await browser.close()


    psg.parseDBHtml()

# with sync_playwright() as playwright:
#     run(playwright)
