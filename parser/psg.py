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
