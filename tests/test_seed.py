import database as db
import seed


def _reset_db(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()


def test_seed_inserts_new_rows_and_returns_count(tmp_path, monkeypatch):
    _reset_db(tmp_path)

    fake_news = [
        {"title": "A", "summary": "sa", "link": "la", "pub_date": "pa"},
        {"title": "B", "summary": "sb", "link": "lb", "pub_date": "pb"},
    ]
    monkeypatch.setattr(seed, "fetch_news", lambda limit=10: fake_news)

    inserted = seed.seed_posts(limit=10)

    assert inserted == 2

    database = db.get_db()
    count = database.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    database.close()
    assert count == 2


def test_seed_skips_existing_title(tmp_path, monkeypatch):
    _reset_db(tmp_path)

    database = db.get_db()
    database.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        ("A", "existing"),
    )
    database.commit()
    database.close()

    fake_news = [
        {"title": "A", "summary": "sa", "link": "la", "pub_date": "pa"},
        {"title": "C", "summary": "sc", "link": "lc", "pub_date": "pc"},
    ]
    monkeypatch.setattr(seed, "fetch_news", lambda limit=10: fake_news)

    inserted = seed.seed_posts(limit=10)

    assert inserted == 1

    database = db.get_db()
    titles = [r[0] for r in database.execute("SELECT title FROM posts ORDER BY id ASC").fetchall()]
    database.close()
    assert titles == ["A", "C"]


def test_main_prints_inserted_count(tmp_path, monkeypatch, capsys):
    _reset_db(tmp_path)

    fake_news = [{"title": "A", "summary": "sa", "link": "la", "pub_date": "pa"}]
    monkeypatch.setattr(seed, "fetch_news", lambda limit=10: fake_news)

    seed.main()
    out = capsys.readouterr().out

    assert "1건 추가됨" in out
