import sqlite3

DB_NAME = "data.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price_per_gram REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY,
        jeweler_price_per_gram REAL,
        usd_rate REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS estimates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metal TEXT,
        weight REAL,
        stones TEXT,
        total REAL
    )
    """)

    cur.execute("INSERT OR IGNORE INTO settings VALUES (1,300,0)")

    conn.commit()
    conn.close()