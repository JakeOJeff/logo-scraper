import asyncio

dbLock = asyncio.Lock()

async def scrapeUrl(page, url):
    try:
        response = await page.goto(url, timeout=30000, wait_until='domcontentloaded')

        html = await page.content()
        async with dbLock:
            psg.insertHtml(url, html)
        print(f"scraped/inserted {url}")
    except Exception as e:
        err = str(e).split('\n')[0]
        print(f"failed {url} - {err}")
        with open('output/failed.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url, err])
                
        try:
            await page.goto('about:blank', timeout=5000)
        except:
            pass

async def scrapeWorker(browser, urls, workerId):
    page = await browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    for url in urls:
        await scrapeUrl(page, url)
    await page.close()