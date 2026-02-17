import sqlite3

DB = "data.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init():
    c = conn()
    cur = c.cursor()

    # ---------- detect old settings table ----------
    try:
        cur.execute("PRAGMA table_info(settings)")
        cols = [x[1] for x in cur.fetchall()]
        if "jeweler" not in cols or "usd" not in cols:
            cur.execute("DROP TABLE IF EXISTS settings")
    except:
        pass

    # ---------- tables ----------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
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

    # ---------- ensure settings row ----------
    cur.execute("SELECT COUNT(*) FROM settings")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO settings(id,jeweler,usd) VALUES(1,300,0)")

    c.commit()
    c.close()
