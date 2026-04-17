import sqlite3
from pathlib import Path


# =========================
# 📁 PATH DB (COMPATIBLE CLOUD)
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "finazdb.db"   # ← importante: sin /data/


# =========================
# 🔌 CONEXIÓN
# =========================

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 🧱 INIT DB
# =========================

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # CLIENTS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # =========================
    # TRANSACTIONS (MEJOR QUE ledger)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        amount REAL,
        date TEXT,
        profile TEXT
    )
    """)

    # =========================
    # CATEGORIES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id TEXT,
        user_id TEXT,
        color TEXT,
        PRIMARY KEY (id, user_id)
    )
    """)

    # =========================
    # CONCEPT ↔ CATEGORY
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS concept_categories (
        concept_id TEXT,
        category_id TEXT,
        user_id TEXT,
        PRIMARY KEY (concept_id, user_id)
    )
    """)

    # =========================
    # ÍNDICE PARA EVITAR DUPLICADOS
    # =========================
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_tx
    ON transactions(description, amount, date, profile)
    """)

    conn.commit()
    conn.close()