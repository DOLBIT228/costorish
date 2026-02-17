import sqlite3
import os

DB = "data.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init():

    # якщо база існує — залишаємо, якщо ні — створиться
    c = conn()
    cur = c.cursor()

    # ---- METALS ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    # ---- STONES ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    # ---- SETTINGS ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY,
        jeweler REAL NOT NULL DEFAULT 300,
        usd REAL NOT NULL DEFAULT 0
    )
    """)

    # ---- ESTIMATES ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estimates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        total REAL
    )
    """)

    # гарантований запис settings
    cur.execute("SELECT COUNT(*) FROM settings")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("INSERT INTO settings(id,jeweler,usd) VALUES(1,300,0)")

    c.commit()
    c.close()
