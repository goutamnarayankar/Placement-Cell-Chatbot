import os, sqlite3, time, secrets, hashlib, hmac
from typing import Optional
from fastapi import Request

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")


def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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
        conn.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            summary TEXT,
            strengths TEXT,
            improvements TEXT,
            missing_skills TEXT,
            roles TEXT,
            resume_score INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()


# ---------- AUTH + SESSION ----------
SESSIONS = {}  # token -> email


def get_student(email: str) -> Optional[sqlite3.Row]:
    if not email:
        return None
    with db() as conn:
        return conn.execute("SELECT * FROM students WHERE email=?", (email.lower(),)).fetchone()


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), stored_hash)


def create_student(name: str, email: str, password: str):
    salt = secrets.token_hex(16)
    pwd_hash = hash_password(password, salt)
    with db() as conn:
        conn.execute(
            "INSERT INTO students (name, email, password_hash, salt, created_at) VALUES (?,?,?,?,?)",
            (name, email.lower(), pwd_hash, salt, int(time.time()))
        )
        conn.commit()


def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        return None
    email = SESSIONS.get(token)
    if not email:
        return None
    return get_student(email)
