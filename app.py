from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import database as db

app = Flask(__name__)


@app.route("/")
def post_list():
    database = db.get_db()
    posts = database.execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC"
    ).fetchall()
    database.close()
    return render_template("list.html", posts=posts)


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
