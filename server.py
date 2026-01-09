from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Храним лучшие результаты: один ник = один лучший результат
scores = []

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json or {}

    name = data.get("name", "Anonymous")[:12]
    score = float(data.get("score", 0))

    # Ищем существующий результат игрока
    existing = next((s for s in scores if s["name"] == name), None)

    if existing:
        # Обновляем ТОЛЬКО если новый результат лучше
        if score > existing["score"]:
            existing["score"] = score
    else:
        # Если игрока ещё нет — добавляем
        scores.append({
            "name": name,
            "score": score
        })

    # Сортируем по убыванию (кто ждал дольше — выше)
    scores.sort(key=lambda x: x["score"], reverse=True)

    # Оставляем только ТОП-10
    scores[:] = scores[:10]

    return jsonify({"status": "ok"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(scores)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
