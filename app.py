"""
app to act as a BJJ journal
stretch:
    add video abilites (either from storage and/or youtube link)
    add comment abilites
    make a public page
    make a private page
"""

from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize app
app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"

# Initialize DB
db = SQLAlchemy()
db.init_app(app)


# user db model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()
    db.session.commit()


# modeling the database
class Post(db.Model):
    """
    defining attributes for the DB
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False, default="N/A")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash("User created successfully")

    return render_template('create_user.html')


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["post"]
        post_author = request.form["author"]
        new_post = Post(
            title=post_title, content=post_content, posted_by=post_author
        )

        with app.app_context():
            db.session.add(new_post)
            db.session.commit()

        return redirect("/posts")
    else:
        all_posts = Post.query.order_by(Post.posted_on).all()
        return render_template("posts.html", posts=all_posts)


@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["post"]
        post_author = request.form["author"]
        new_post = Post(
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
    to_edit = Post.query.get_or_404(id)
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
    to_delete = Post.query.get_or_404(id)

    with app.app_context():
        db.session.delete(to_delete)
        db.session.commit()

    return redirect("/posts")


if __name__ == "__main__":
    app.run(debug=True)
