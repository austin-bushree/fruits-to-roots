import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "db"
DB_PATH = BASE_DIR / "ngss.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So you get dict-like access
    return conn

def get_dci_description(group_name: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    print(DB_PATH)
    print(DB_PATH.as_posix())

    cursor.execute("""
        SELECT GROUP_CONCAT(full_idea, ' ')
        FROM dcis
        WHERE group_name = ?
    """, (group_name,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result and result[0] else ""