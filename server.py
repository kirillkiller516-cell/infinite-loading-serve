from flask import Flask, request, jsonify
import os

app = Flask(__name__)
SCORES_FILE = "global_scores.txt"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return [float(x.strip()) for x in f.readlines()]

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        for s in scores:
            f.write(f"{s}\n")

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.json
    score = float(data["score"])

    scores = load_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]
    save_scores(scores)

    return jsonify({"status": "ok"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(load_scores())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
