from flask import Flask, render_template, request
from search import search

# Creates flask GUI for document index

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results", methods=["GET"])
def results():
    q = request.args.get("q")
    return render_template("results.html", q=q, results = search(q), results_len = len(list(search(q))))

if __name__ == "__main__":
    app.run(port=5000)