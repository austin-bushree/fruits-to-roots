from fastapi import APIRouter
from app.services.db import get_db_connection

router = APIRouter()

@router.get("/api/standards")
def get_standards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM standards ORDER BY id")
    results = cursor.fetchall()
    return [{"id": row["id"], "label": f"{row['id']}: {row['title']}"} for row in results]