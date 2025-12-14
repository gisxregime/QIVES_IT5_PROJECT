import hashlib
import secrets
from datetime import datetime, timezone
from database import get_db_conn


# ---------------- PASSWORD HASHING ----------------
def hash_password(password, salt_hex):
    h = hashlib.sha256()
    h.update(bytes.fromhex(salt_hex) + password.encode("utf-8"))
    return h.hexdigest()


# ---------------- CREATE USER ----------------
def create_user(username, password):
    if not username or not password:
        print("Username and password cannot be empty.")
        return None

    conn = get_db_conn()
    c = conn.cursor()

    salt_hex = secrets.token_bytes(16).hex()
    pw_hash = hash_password(password, salt_hex)

    try:
        # Insert user
        c.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (username, pw_hash, salt_hex)
        )
        user_id = c.lastrowid

        # Initialize progress (chapter 1)
        c.execute(
            "INSERT INTO progress (user_id, chapter) VALUES (?, ?)",
            (user_id, 1)
        )

        conn.commit()
        print("User created successfully!")
        return user_id

    except Exception as e:
        print("Error creating user:", e)
        return None

    finally:
        conn.close()


# ---------------- VERIFY USER ----------------
def verify_user(username, password):
    conn = get_db_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()

    if not row:
        print("User not found.")
        return None

    computed = hash_password(password, row["salt"])
    if computed == row["password_hash"]:
        print("Login successful!")
        return row["id"]

    print("Incorrect password.")
    return None


# ---------------- PROGRESS ----------------
def get_user_progress(user_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT chapter FROM progress WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row["chapter"] if row else 1


def set_user_progress(user_id, chapter):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE progress SET chapter = ? WHERE user_id = ?",
        (chapter, user_id)
    )
    conn.commit()
    conn.close()


# ---------------- LOG ACTION ----------------
def log_action(user_id, action):
    conn = get_db_conn()
    c = conn.cursor()
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"

    c.execute(
        "INSERT INTO forensic_logs (user_id, action, timestamp) VALUES (?, ?, ?)",
        (user_id, action, timestamp)
    )

    conn.commit()
    conn.close()


# ---------------- SEED ----------------
def save_seed(user_id, chapter, seed):
    conn = get_db_conn()
    c = conn.cursor()

    c.execute(
        "INSERT OR REPLACE INTO seeds (user_id, chapter, seed) VALUES (?, ?, ?)",
        (user_id, chapter, seed)
    )

    conn.commit()
    conn.close()


def get_seed(user_id, chapter):
    conn = get_db_conn()
    c = conn.cursor()

    c.execute(
        "SELECT seed FROM seeds WHERE user_id = ? AND chapter = ?",
        (user_id, chapter)
    )

    row = c.fetchone()
    conn.close()
    return row["seed"] if row else None


# ---------------- EVIDENCE ----------------
def register_evidence(user_id, chapter, path):
    conn = get_db_conn()
    c = conn.cursor()

    c.execute(
        "INSERT INTO evidence_registry (user_id, chapter, file_path, description) VALUES (?, ?, ?, ?)",
        (user_id, chapter, path, "Correct next file")
    )

    conn.commit()
    conn.close()
