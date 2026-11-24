from fastapi import APIRouter
from src.news_aggregator.database import get_connection

router = APIRouter(prefix="/news", tags=["News"])


def row_to_dict(row):
    return {
        "id": row[0],
        "title": row[1],
        "url": row[2],
        "description": row[3],
        "source": row[4],
        "category": row[5],
        "image": row[6],
        "published": row[7]
    }


@router.get("/")
def get_all_news(category: str = None, search: str = None, limit: int = 50):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM news WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [row_to_dict(row) for row in rows]


@router.get("/categories")
def get_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM news ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]

    conn.close()

    return categories


@router.get("/stats")
def get_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM news")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT category, COUNT(*) FROM news GROUP BY category"
    )
    category_counts = dict(cursor.fetchall())

    conn.close()

    return {
        "total_articles": total,
        "category_counts": category_counts
    }


@router.get("/{news_id}")
def get_article(news_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {"error": "Article not found"}

    return row_to_dict(row)