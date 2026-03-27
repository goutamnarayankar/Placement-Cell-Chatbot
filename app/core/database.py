import os
import sqlite3

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "data", "app.db")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with db() as conn:
        # Students table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at INTEGER
        );
        """)

        # Resume analysis table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            summary TEXT,
            skills TEXT,
            score INTEGER,
            created_at INTEGER
        );
        """)

        conn.commit()
