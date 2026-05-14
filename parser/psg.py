import psycopg2
from parser import parse

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

def parseDBHtml():
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("SELECt * FROM rhtml")
        rows = cur.fetchall()
        for row in rows:
            parse.parseHtml(row[1],row[2]) # im parsing html and trying return possible url



def clearAll():
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE rhtml RESTART IDENTITY")
    conn.commit()
    print("cleared data")
