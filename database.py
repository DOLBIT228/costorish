import sqlite3

DB = "data.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY,
        jeweler REAL DEFAULT 300,
        usd REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS estimates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        total REAL
    )
    """)

    cur.execute("INSERT OR IGNORE INTO settings(id,jeweler,usd) VALUES(1,300,0)")

    c.commit()
    c.close()
