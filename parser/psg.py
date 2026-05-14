import psycopg2

def getConn():
    return psycopg2.connect(dbname="logos")

def create():
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rhtml (
                id SERIAL PRIMARY KEY,
                url TEXT,
                html TEXT
            )
        """)
        conn.commit()
    print("created rhtml table")


def insertHtml(url, html):
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rhtml (url, html) VALUES (%s, %s)
        """, (url, html)
        )
    conn.commit()
    print(f"inserted {url}")

def clearAll():
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM rhtml;
            TRUNCATE rhtml; 
        """)
    conn.commit()
    print("cleared data")
