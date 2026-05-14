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

- added buffer -> sending buffer html in batches
- add simple connection pool, creating conn and putconn

optimization mark 2:

Scraped Logos: 7/9
RAM used:   82.0 MB
CPU time:   0.56s
Total Time: 35.70s
Scraping/Inserting Time: 35.60s
Parsing Time: 0.30s

- added stream cursor instead of fetching entire html

optimization mark 3:

Scraped Logos: 7/9
RAM used:   79.1 MB
CPU time:   0.43s
Total Time: 29.60s
Scraping/Inserting Time: 29.49s
Parsing Time: 0.14s

- added 200 kb limit when parsing ( unsure if this is good in the long run )