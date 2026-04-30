from flask import Flask

app = Flask(__name__)


@app.route("/obi/begin", methods=["POST"])
def obi_begin():
    pass


@app.route("/obi/end", methods=["POST"])
def obi_end():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7443, threaded=False, processes=1)
