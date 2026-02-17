import sqlite3

DB = "data.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

def ensure_table(cur, name, expected_cols, create_sql):

    try:
        cur.execute(f"PRAGMA table_info({name})")
        cols = [x[1] for x in cur.fetchall()]

        if cols != expected_cols:
            cur.execute(f"DROP TABLE IF EXISTS {name}")
            cur.execute(create_sql)

    except:
        cur.execute(create_sql)

def init():

    c = conn()
    cur = c.cursor()

    ensure_table(cur,"metals",
        ["id","name","price"],
        """
        CREATE TABLE metals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
        """)

    ensure_table(cur,"stones",
        ["id","name","price"],
        """
        CREATE TABLE stones(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
        """)

    ensure_table(cur,"settings",
        ["id","jeweler","usd"],
        """
        CREATE TABLE settings(
            id INTEGER PRIMARY KEY,
            jeweler REAL DEFAULT 300,
            usd REAL DEFAULT 0
        )
        """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS estimates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        t
