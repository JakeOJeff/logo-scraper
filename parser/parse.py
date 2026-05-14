from bs4 import BeautifulSoup

def parseHtml(html, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')

    # add series of checks / so first will add all possible data points
    metaTagContent =  soup.find('meta', attrs={'itemprop': 'image'}).get('content')
    linkTagAppleIcon = soup.find('link', attrs={rel="apple-touch-icon"}).get('href')
    imgAlt = None
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        if logo in alt.lower()
            imgAlt = img.get('src')
            break
            

