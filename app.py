from flask import Flask, render_template
from generateHTML import generate

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    generate()
    app.run()
