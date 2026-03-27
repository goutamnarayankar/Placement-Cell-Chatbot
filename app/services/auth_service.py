import sqlite3, secrets, hashlib, hmac, time
from typing import Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with db() as conn:
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
        conn.commit()


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()


def create_student(name: str, email: str, password: str):
    salt = secrets.token_hex(16)
    pwd = hash_password(password, salt)

    with db() as conn:
        conn.execute("""
            INSERT INTO students (name, email, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email.lower(), pwd, salt, int(time.time())))
        conn.commit()


def get_student(email: str) -> Optional[sqlite3.Row]:
    with db() as conn:
        r = conn.execute("SELECT * FROM students WHERE email=?", (email.lower(),))
        return r.fetchone()


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), stored_hash)

# simple session store
SESSIONS = {}
