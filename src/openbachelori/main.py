import json


from flask import Flask, request
import jsonlines


import openbachelori.config


app = Flask(__name__)


obi_state_dict: dict = None


@app.route("/obi/begin", methods=["POST"])
def obi_begin():
    global obi_state_dict
    obi_state_dict = request.json


@app.route("/obi/update", methods=["POST"])
def obi_update():
    global obi_state_dict

    obi_state_dict.update(request.json)


@app.route("/obi/end", methods=["POST"])
def obi_end():
    global obi_state_dict

    obi_state_dict.update(request.json)

    with jsonlines.open("data/tmp.jsonl", mode="a") as writer:
        writer.write(obi_state_dict)

    obi_state_dict = None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7443, threaded=False, processes=1)
