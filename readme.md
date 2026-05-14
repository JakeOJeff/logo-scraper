nix develop

python -m venv .venv
source .venv/bin/activate
pip install playwright psycopg2-binary beautifulsoup4

createdb logos

python scraper.py


testing stuff :
psql logos
\dt \dt rhtml 