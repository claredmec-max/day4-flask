import database as db
import app as app_module


def _seed_posts(count):
    database = db.get_db()
    for i in range(count):
        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (f"Post {i + 1}", f"Content {i + 1}"),
        )
    database.commit()
    database.close()


def test_list_first_page_shows_10_posts_and_prev_disabled(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(25)

    client = app_module.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Post 25" in html
    assert "Post 16" in html
    assert "Post 15" not in html
    assert "1 / 3" in html
    assert 'id="prev-disabled"' in html
    assert ">다음<" in html


def test_invalid_page_defaults_to_first_page(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(12)

    client = app_module.app.test_client()
    response = client.get("/?page=abc")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Post 12" in html
    assert "Post 3" in html
    assert "Post 2" not in html
    assert "1 / 2" in html
    assert 'id="prev-disabled"' in html


def test_negative_page_clamps_to_first_page(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(12)

    client = app_module.app.test_client()
    response = client.get("/?page=-7")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Post 12" in html
    assert "Post 3" in html
    assert "Post 2" not in html
    assert "1 / 2" in html
    assert 'id="prev-disabled"' in html


def test_page_above_total_clamps_to_last_page_and_disables_next(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(12)

    client = app_module.app.test_client()
    response = client.get("/?page=999")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Post 2" in html
    assert "Post 1" in html
    assert "Post 3" not in html
    assert "2 / 2" in html
    assert 'id="next-disabled"' in html


def test_empty_posts_still_shows_single_page_and_both_disabled(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    client = app_module.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "아직 글이 없습니다." in html
    assert "1 / 1" in html
    assert 'id="prev-disabled"' in html
    assert 'id="next-disabled"' in html


def test_search_filters_title_or_content_and_keeps_pagination(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    for i in range(8):
        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (f"Python title {i + 1}", f"General content {i + 1}"),
        )
    for i in range(5):
        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (f"General title {i + 1}", f"Learn PYTHON topic {i + 1}"),
        )
    for i in range(7):
        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (f"Other title {i + 1}", f"Other content {i + 1}"),
        )
    database.commit()
    database.close()

    client = app_module.app.test_client()
    response = client.get("/?q=python&page=2")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "2 / 2" in html
    assert html.count("onclick=\"location.href='/detail/") == 3
