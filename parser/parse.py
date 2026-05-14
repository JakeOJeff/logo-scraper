from bs4 import BeautifulSoup
import json
import csv

def parseHtml(url,html):
    kb = 1024
    # so i added a 100kb limit here, im not sure if this is a good idea in the long run, but its fast for now
    soup = BeautifulSoup(html[:200 * kb], 'html.parser')
    count = 0

    # add series of checks / so first will add all possible data points
    schemaJson = None
    schema = soup.find("script", type="application/ld+json")
    if schema:
        try:
            data = json.loads(schema.get_text())
            if data.get("logo"):
                schemaJson = data["logo"]
        except:
            pass

    og = soup.find('meta', property={"og:image"})
    ogImage = og.get('content') if og else None

    meta = soup.find('meta', attrs={'itemprop': 'image'})
    metaTagContent = meta.get('content') if meta else None

    link = soup.find('link', attrs={'rel': 'apple-touch-icon'})
    linkTagAppleIcon = link.get('href') if link else None
    
    svgLogo = None
    for svg in soup.find_all('svg'):
        classes = ' '.join(svg.get('class', []))
        identity = svg.get('id', '')
        aria = svg.get('aria-label', '')

        if any('logo' in x.lower() for x in [classes, identity, aria]):
            svgLogo = f"{aria or classes or identity}"
            break

    imgAlt = None
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        data_cy = img.get('data-cy', '')
        data_test = img.get('data-testid', '')

        if any( 'logo' in x.lower() for x in [alt, data_cy, data_test]):
            imgAlt = img.get('data-src') or img.get('src') or None
            break

    logo =  imgAlt  or ogImage or metaTagContent or linkTagAppleIcon or  schemaJson or svgLogo

    if logo:
        print(f"{url} | {logo}")
        with open('output/success.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url, logo])

        return True 
    else:
        print(f"{url} | no logo found")
        with open('output/unidentified.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url])
        return False




