

async def scrape_urL(page, url)
    try:
        response = await page.goto(url, timeout=30000, wait_until='domcontentloaded')

        html = await()