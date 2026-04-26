from crawler import fetch_news
import database as db


def _to_content(item: dict) -> str:
    summary = item.get("summary", "")
    link = item.get("link", "")
    pub_date = item.get("pub_date", "")
    return f"{summary}\n링크: {link}\n발행시간: {pub_date}"


def seed_posts(limit: int = 10) -> int:
    db.init_db()
    database = db.get_db()

    inserted_count = 0
    news_items = fetch_news(limit=limit)

    for item in news_items:
        title = item.get("title", "").strip()
        if not title:
            continue

        exists = database.execute(
            "SELECT 1 FROM posts WHERE title = ? LIMIT 1",
            (title,),
        ).fetchone()

        if exists:
            continue

        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title, _to_content(item)),
        )
        inserted_count += 1

    database.commit()
    database.close()
    return inserted_count


def main():
    inserted_count = seed_posts(limit=10)
    print(f"{inserted_count}건 추가됨")


if __name__ == "__main__":
    main()
