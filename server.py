from flask import Flask, request, jsonify

app = Flask(__name__)

scores = []

@app.route("/")
def home():
    return "Infinite Loading Server OK"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    score = data.get("score")
    if isinstance(score, (int, float)):
        scores.append(float(score))
        scores.sort()
        scores[:] = scores[:10]
    return jsonify({"status": "ok"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(scores)

if __name__ == "__main__":
    app.run()

