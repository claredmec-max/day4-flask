from flask import Flask, render_template, redirect, url_for, request
import database as db

app = Flask(__name__)


@app.route("/")
def post_list():
    page_raw = request.args.get("page", "1")
    q = request.args.get("q", "").strip()
    is_search = bool(q)

    try:
        page = int(page_raw)
    except ValueError:
        page = 1

    if page < 1:
        page = 1

    per_page = 10
    database = db.get_db()

    if is_search:
        search_term = f"%{q}%"
        total_count = database.execute(
            "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?",
            (search_term, search_term),
        ).fetchone()[0]
    else:
        total_count = database.execute("SELECT COUNT(*) FROM posts").fetchone()[0]

    total_pages = max(1, (total_count + per_page - 1) // per_page)

    if page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page
    if is_search:
        posts = database.execute(
            "SELECT id, title, content, created_at FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?",
            (search_term, search_term, per_page, offset),
        ).fetchall()
    else:
        posts = database.execute(
            "SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()
    database.close()

    return render_template(
        "list.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        has_prev=page > 1,
        has_next=page < total_pages,
        prev_page=page - 1,
        next_page=page + 1,
        q=q,
        is_search=is_search,
    )


@app.route("/detail/<int:post_id>")
def post_detail(post_id):
    database = db.get_db()
    post = database.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()
    database.close()
    if not post:
        return redirect(url_for("post_list"))
    return render_template("detail.html", post=post)


@app.route("/write", methods=["GET", "POST"])
def post_write():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        database = db.get_db()
        database.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
        )
        database.commit()
        database.close()
        return redirect(url_for("post_list"))
    return render_template("write.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def post_edit(post_id):
    database = db.get_db()
    post = database.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?",
        (post_id,),
    ).fetchone()
    if not post:
        database.close()
        return redirect(url_for("post_list"))
    if request.method == "POST":
        database.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (request.form["title"], request.form["content"], post_id),
        )
        database.commit()
        database.close()
        return redirect(url_for("post_detail", post_id=post_id))
    database.close()
    return render_template("write.html", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
def post_delete(post_id):
    database = db.get_db()
    database.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    database.commit()
    database.close()
    return redirect(url_for("post_list"))


db.init_db()

if __name__ == "__main__":
    app.run(debug=True)
