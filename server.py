from flask import Flask, request, jsonify

app = Flask(__name__)
scores = []

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    name = data.get("name", "Anonymous")[:12]
    score = float(data.get("score", 0))

    scores.append({
        "name": name,
        "score": score
    })

    scores.sort(key=lambda x: x["score"], reverse=True)
    scores[:] = scores[:10]

    return {"status": "ok"}

@app.route("/leaderboard")
def leaderboard():
    return jsonify(scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
