from flask import Flask, request, jsonify, render_template
from rag import answer
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/query", methods=["POST"])
def query_fitforge():
    data = request.get_json()
    question = data.get("question", "")
    return jsonify({"answer": answer(question)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)