import psycopg2

conn = None
cur = None


def connect_db():
    global conn, cur
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=5433)
    # Open a cursor to perform database operations
    cur = conn.cursor()


