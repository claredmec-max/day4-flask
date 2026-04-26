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
    assert "Python title" in html or "General title" in html
    assert "Other title" not in html


def test_search_empty_result_shows_message_and_search_input_value(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(5)

    client = app_module.app.test_client()
    response = client.get("/?q=NoSuchKeyword")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "검색 결과가 없습니다" in html
    assert 'name="q"' in html
    assert 'value="NoSuchKeyword"' in html
    assert "아직 글이 없습니다." not in html


def test_pagination_links_preserve_query_string(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [(f"FindMe {i}", "body") for i in range(1, 12)]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    response = client.get("/?q=FindMe&page=1")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "?q=FindMe&amp;sort=new&amp;page=2" in html


def test_sort_default_is_newest(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [
        ("Gamma", "body"),
        ("Alpha", "body"),
        ("Beta", "body"),
    ]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert html.index("Beta") < html.index("Alpha") < html.index("Gamma")


def test_sort_oldest_changes_ordering(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [("First", "body"), ("Second", "body"), ("Third", "body")]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    newest = client.get("/?sort=new").get_data(as_text=True)
    oldest = client.get("/?sort=old").get_data(as_text=True)

    assert newest.index("Third") < newest.index("Second") < newest.index("First")
    assert oldest.index("First") < oldest.index("Second") < oldest.index("Third")


def test_invalid_sort_falls_back_to_newest(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [("First", "body"), ("Second", "body"), ("Third", "body")]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    invalid = client.get("/?sort=invalid").get_data(as_text=True)
    newest = client.get("/?sort=new").get_data(as_text=True)

    assert invalid.index("Third") < invalid.index("Second") < invalid.index("First")
    assert invalid == newest


def test_sort_title_orders_by_title_asc(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [("다람쥐", "body"), ("가방", "body"), ("나무", "body")]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    html = client.get("/?sort=title").get_data(as_text=True)

    assert html.index("가방") < html.index("나무") < html.index("다람쥐")


def test_sort_dropdown_exists_and_auto_submits(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(3)

    client = app_module.app.test_client()
    html = client.get("/").get_data(as_text=True)

    assert 'name="sort"' in html
    assert 'onchange="this.form.submit()"' in html
    assert "최신순" in html
    assert "오래된순" in html
    assert "제목순" in html
    assert '<option value="new" selected>최신순</option>' in html


def test_sort_dropdown_selected_state_changes_with_query(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    _seed_posts(3)

    client = app_module.app.test_client()
    old_html = client.get("/?sort=old").get_data(as_text=True)
    title_html = client.get("/?sort=title").get_data(as_text=True)

    assert '<option value="old" selected>오래된순</option>' in old_html
    assert '<option value="title" selected>제목순 (가나다)</option>' in title_html


def test_pagination_links_keep_q_and_sort(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [(f"Find {i}", "body") for i in range(1, 13)]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    html = client.get("/?q=Find&sort=title&page=1").get_data(as_text=True)

    assert "?q=Find&amp;sort=title&amp;page=2" in html


def test_search_sort_and_pagination_work_together(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()

    database = db.get_db()
    rows = [(f"Python {i:02d}", "match") for i in range(1, 13)]
    rows += [("Zebra", "nope"), ("Apple", "nope")]
    database.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", rows)
    database.commit()
    database.close()

    client = app_module.app.test_client()
    html = client.get("/?q=Python&sort=title&page=2").get_data(as_text=True)

    assert "2 / 2" in html
    assert html.index("Python 11") < html.index("Python 12")
    assert "Python 10" not in html
    assert "Zebra" not in html
    assert "Apple" not in html
