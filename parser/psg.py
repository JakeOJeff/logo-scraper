import psycopg2

def getConn():
    return psycopg2.connect(dbname="logos")

def create():
    cur.execute(
        "CREATE TABLE RHTML ( id SERIAL PRIMARY KEY, url TEXT, html  TEXT )"
    )