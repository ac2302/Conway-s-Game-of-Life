from flask import Flask, request
from flask.json import jsonify

import game


app = Flask(__name__)


@app.route("/solve", methods=['POST'])
def hello_world():
    try:
        side = int(request.form['side'])
        rows = int(request.form['rows'])
        game.start(side=side, rows=rows)
        return jsonify({"message": "ok"})
    except:
        return jsonify({"message": "error"})
