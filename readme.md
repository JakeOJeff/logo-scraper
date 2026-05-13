nix develop

python -m venv .venv
source .venv/bin/activate
pip install playwright psycopg2-binary

createdb logos

python scraper.py