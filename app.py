"""
app to act as a BJJ journal
stretch:
    add video abilites (either from storage and/or youtube link)
    add comment abilites
    make a public page
    make a private page
"""

from flask import Flask, render_template

from article_data import Articles

app = Flask(__name__)

Articles = Articles()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    return render_template("articles.html", articles=Articles)


if __name__ == "__main__":
    app.run(debug=True)
