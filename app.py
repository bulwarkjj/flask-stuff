""" 
app to act as a BJJ journal
stretch:
    add video abilites (either from storage and/or youtube link)
    add comment abilites
    make a public page
    make a private page
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run()
