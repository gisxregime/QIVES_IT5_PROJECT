import sqlite3
from config import DB_FILE


def get_db_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row["name"] == column for row in cursor.fetchall())


def init_db():
    conn = get_db_conn()
    c = conn.cursor()

    # USERS
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # PROGRESS
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER PRIMARY KEY
        )
    """)

    # REPAIR PROGRESS
    if not column_exists(c, "progress", "chapter"):
        c.execute("ALTER TABLE progress ADD COLUMN chapter INTEGER NOT NULL DEFAULT 1")

    # SCORE
    c.execute("""
        CREATE TABLE IF NOT EXISTS score (
            user_id INTEGER,
            chapter INTEGER,
            score INTEGER,
            PRIMARY KEY (user_id, chapter)
        )
    """)

    # SCORE SESSION (OPTIONAL / FUTURE)

    #c.execute("""
    #    CREATE TABLE IF NOT EXISTS score_session (
    #        user_id INTEGER,
    #        chapter INTEGER,
    #        start_time INTEGER,
    #        command_count INTEGER,
    #        PRIMARY KEY (user_id, chapter)
    #    )
    #""")

    # LOGS
    c.execute("""
        CREATE TABLE IF NOT EXISTS forensic_logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            action TEXT,
            timestamp TEXT
        )
    """)

    # EVIDENCE
    c.execute("""
        CREATE TABLE IF NOT EXISTS evidence_registry (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            chapter INTEGER,
            file_path TEXT,
            description TEXT
        )
    """)

    # SEEDS
    c.execute("""
        CREATE TABLE IF NOT EXISTS seeds (
            user_id INTEGER,
            chapter INTEGER,
            seed INTEGER,
            PRIMARY KEY (user_id, chapter)
        )
    """)

    conn.commit()
    conn.close()
