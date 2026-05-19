# Setup

## Setting Environment
```bash
nix develop

python -m venv .venv
source .venv/bin/activate
pip install playwright psycopg2-binary beautifulsoup4 psutil

createdb logos

python scraper.py
```


## Checking Database :

```bash
psql logos
\dt \dt rhtml 

```

#### For iwd issues in daemon :

```bash
sudo tee /etc/iwd/main.conf <<EOF
[General]
EnableNetworkConfiguration=true
EOF

sudo systemctl restart iwd
```


# Benchmarking :

## prev:

Scraped Logos: 7/9
RAM used:   77.9 MB
CPU time:   0.60s
Total Time: 51.60s
Scraping/Inserting Time: 51.44s
Parsing Time: 0.32s

## optimization mark 1:

Scraped Logos: 7/9
RAM used:   87.9 MB
CPU time:   0.62s
Total Time: 33.00s
Scraping/Inserting Time: 32.90s
Parsing Time: 0.34s

- added buffer -> sending buffer html in batches
- add simple connection pool, creating conn and putconn

## optimization mark 2:

Scraped Logos: 7/9
RAM used:   82.0 MB
CPU time:   0.56s
Total Time: 35.70s
Scraping/Inserting Time: 35.60s
Parsing Time: 0.30s

- added stream cursor instead of fetching entire html

## optimization mark 3:

Scraped Logos: 7/9
RAM used:   79.1 MB
CPU time:   0.43s
Total Time: 29.60s
Scraping/Inserting Time: 29.49s
Parsing Time: 0.14s

- added 200 kb limit when parsing ( unsure if this is good in the long run )

## scraping accuracy mark 1 :

Scraped Logos: 9/11
RAM used:   75.3 MB
CPU time:   0.51s
Total Time: 65.25s
Scraping/Inserting Time: 64.70s
Parsing Time: 0.17s

- added page closing on fail so that it doesn't mess with post-scraping on same page ( improved scrapability but reduced performance by a lot! )

## optimization mark 4:

Scraped Logos: 8/12
RAM used:   102.8 MB
CPU time:   0.66s
Total Time: 23.24s
Scraping/Inserting Time: 23.19s
Parsing Time: 0.15s

- added multithreading with 3 workers and now playwright creates its own instance in each thread and no longer shares between threads. 

Time reduced by 3 times but ram usage has spiked. More websites have been scraped but it failed to identify one as before. ( might have to add asyncio later )

## scraping accuracy mark 2:

Scraped Logos: 10/12
RAM used:   94.3 MB
CPU time:   0.70s
Total Time: 42.08s
Scraping/Inserting Time: 42.07s
Parsing Time: 0.16s

- added forced http2 disabling, reduced ram usage and improved identification, but increased time significantly

## optimization mark 5:

Scraped Logos: 9/12
RAM used:   97.8 MB
CPU time:   0.63s
Total Time: 14.31s
Scraping/Inserting Time: 14.30s
Parsing Time: 0.15s

- added forced http2 disabling and also fixed the function calls for timeout and domcontentloaded for playwright callbacks

## large test 1 ( 300 urls ):

Scraped Logos: 181/225
RAM used:   519.5 MB
CPU time:   11.33s
Total Time: 284.48s
Scraping/Inserting Time: 284.43s
Parsing Time: 4.14s

- 75% Urls Scraped | 60.33% Logos Identified | 80.4% Scraped Logos Identified


# Future plans :
 - migrate from multi-threading to asyncio
 
 - offloading a function to something like Lua, Rust Or C. I thought of using Lua atfirst because it is something I am comfortable in and better dev experience, but it heavily affects the time complexity. So it has to be written in C. The function I plan to write is to create a scoring system in python, and then analyze based on position ( like top-bottom equals to higher-lower chance ), then width, height, imHeader, words like 'logo', 'icon', 'brand', etc. And these are scored, and highest score is scraped as a logo. This is for scenarios where traditional scraping doesn't work and this is fallback

 - adding a queue system so that i can check if any previous urls have been already scraped in the db