"""
app to act as a BJJ journal
stretch:
    add video abilites (either from storage and/or youtube link)
    add comment abilites
    make a public page
    make a private page
"""

from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"

# Initialize DB
db = SQLAlchemy()
db.init_app(app)


# modeling the database
class BlogDB(db.Model):
    """
    defining attributes for the DB
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False, default="N/A")
    posted_by = db.Column(db.String(100), nullable=False, default="N/A")
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        """
        making it human readable
        """
        return self.title


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["post"]
        post_author = request.form["author"]
        new_post = BlogDB(
            title=post_title, content=post_content, posted_by=post_author
        )

        with app.app_context():
            db.session.add(new_post)
            db.session.commit()

        return redirect("/posts")
    else:
        all_posts = BlogDB.query.order_by(BlogDB.posted_on).all()
        return render_template("posts.html", posts=all_posts)


@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["post"]
        post_author = request.form["author"]
        new_post = BlogDB(
            title=post_title, content=post_content, posted_by=post_author
        )

        with app.app_context():
            db.session.add(new_post)
            db.session.commit()

        return redirect("/posts")
    else:
        return render_template("new_post.html")


@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    to_edit = BlogDB.query.get_or_404(id)
    if request.method == "POST":
        to_edit.title = request.form["title"]
        to_edit.author = request.form["author"]
        to_edit.content = request.form["post"]

        with app.app_context():
            db.session.commit()

        return redirect("/posts")

    else:
        return render_template("edit.html", post=to_edit)


@app.route("/posts/delete/<int:id>")
def delete(id):
    to_delete = BlogDB.query.get_or_404(id)

    with app.app_context():
        db.session.delete(to_delete)
        db.session.commit()

    return redirect("/posts")


if __name__ == "__main__":
    app.run(debug=True)
