from bs4 import BeautifulSoup
import json

def parseHtml(url,html):
    soup = BeautifulSoup(html, 'html.parser')
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
        if 'logo' in alt.lower():
            imgAlt = img.get('src')
            break

    logo =  ogImage or schemaJson or metaTagContent or linkTagAppleIcon or imgAlt or svgLogo

    if logo:
        print(f"{url} | {logo}")
        return True 
    else:
        print(f"{url} | no logo found")
        return False




