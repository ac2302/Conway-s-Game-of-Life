from flask import Flask, request, render_template
from flask.json import jsonify

import game


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=['POST'])
def start():
    try:
        side = int(request.form['side'])
        rows = int(request.form['rows'])
        game.start(side=side, rows=rows)
        return render_template("index.html")
    except:
        return jsonify({"message": "error"})
