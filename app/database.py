import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "database.db"

def init_db():
    """Inicialization database and create table"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        price REAL NOT NULL,
        currency TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """For database connections"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
