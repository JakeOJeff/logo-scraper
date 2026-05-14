nix develop

python -m venv .venv
source .venv/bin/activate
pip install playwright psycopg2-binary beautifulsoup4

createdb logos

python scraper.py


testing stuff :
psql logos
\dt \dt rhtml 


benchmarking :

prev:
Scraped Logos: 7/9
RAM used:   77.9 MB
CPU time:   0.60s
Total Time: 51.60s
Scraping/Inserting Time: 51.44s
Parsing Time: 0.32s

optimization mark 1:
Scraped Logos: 7/9
RAM used:   87.9 MB
CPU time:   0.62s
Total Time: 33.00s
Scraping/Inserting Time: 32.90s
Parsing Time: 0.34s