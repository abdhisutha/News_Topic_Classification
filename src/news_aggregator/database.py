import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "news.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE,
            description TEXT,
            source TEXT,
            category TEXT,
            image TEXT,
            published TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def save_news(articles):
    conn = get_connection()
    cursor = conn.cursor()

    saved = 0

    for article in articles:
        cursor.execute("""
            INSERT OR IGNORE INTO news
            (title, url, description, source, category, image, published)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article.get("title"),
            article.get("url"),
            article.get("description"),
            article.get("source"),
            article.get("category"),
            article.get("image", ""),
            article.get("published", "")
        ))

        saved += cursor.rowcount

    conn.commit()
    conn.close()

    print(f"{saved} new articles saved!")


def get_news(category=None):
    conn = get_connection()
    cursor = conn.cursor()

    if category:
        cursor.execute(
            "SELECT * FROM news WHERE category=? ORDER BY id DESC",
            (category,)
        )
    else:
        cursor.execute("SELECT * FROM news ORDER BY id DESC")

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_news_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM news")
    count = cursor.fetchone()[0]

    conn.close()
    return count


if __name__ == "__main__":
    initialize_database()