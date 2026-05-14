from bs4 import BeautifulSoup

def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')

    # add series of checks / so first will add all possible data points
    meta = soup.find('meta', attrs={'itemprop': 'image'})
    metaTagContent = meta.get('content') if meta else None

    link = soup.find('link', attrs={'rel': 'apple-touch-icon'})
    linkTagAppleIcon = link.get('href') if link else None
    imgAlt = None
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        if 'logo' in alt.lower():
            imgAlt = img.get('src')
            break

    if metaTagContent:
        print(metaTagContent)
    elif linkTagAppleIcon:
        print(linkTagAppleIcon)
    else:
        print(imgAlt)


