import sqlite3

DB="data.db"

def conn():
    return sqlite3.connect(DB,check_same_thread=False)

def init():
    c=conn()
    cur=c.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS metals(id INTEGER PRIMARY KEY,name TEXT,price REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS stones(id INTEGER PRIMARY KEY,name TEXT,price REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY,name TEXT,price REAL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY,jeweler REAL,usd REAL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS estimates(
        id INTEGER PRIMARY KEY,
        data TEXT,
        total REAL
    )""")

    cur.execute("INSERT OR IGNORE INTO settings VALUES(1,300,0)")

    c.commit();c.close()
