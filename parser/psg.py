from psycopg2 import pool 
from parser import parse

# 2 connections for now, add a multiconnection later ( threading? )
_pool = pool.SimpleConnectionPool(1, 2, dbname="logos")

def getConn():
    return _pool.getconn()

def putConn(conn):
    return _pool.putconn(conn)

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
    putConn(conn)
    print("created rhtml table")


def insertHtmlSet(buff):
    conn = getConn()
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO rhtml (url, html) VALUES (%s, %s)
        """, buff
        )
    conn.commit()
    putConn(conn)

def parseDBHtml():
    conn = getConn()
    count = 0
    with conn.cursor() as cur:
        cur.execute("SELECt * FROM rhtml")
        rows = cur.fetchall()
        for row in rows:
            status = parse.parseHtml(row[1],row[2]) # im parsing html and trying return possible url
            if status:
                count = count + 1

    putConn(conn)
    print(f"Scraped Logos: {count}/{len(rows)}")

def clearAll():
    conn = getConn()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE rhtml RESTART IDENTITY")
    conn.commit()
    putConn(conn)
    print("cleared data")
