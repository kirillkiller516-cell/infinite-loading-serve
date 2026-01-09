from flask import Flask, request, jsonify
import os
import json
import time

app = Flask(__name__)

DATA_FILE = "scores.json"
RATE_LIMIT_SECONDS = 5  # защита от спама

scores = []
last_submit_time = {}  # ip -> time

# ---------- ЗАГРУЗКА ----------
def load_scores():
    global scores
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except:
            scores = []
    else:
        scores = []

# ---------- СОХРАНЕНИЕ ----------
def save_scores():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False)

load_scores()

@app.route("/submit", methods=["POST"])
def submit():
    now = time.time()
    ip = request.remote_addr

    # ---------- АНТИСПАМ ----------
    if ip in last_submit_time:
        if now - last_submit_time[ip] < RATE_LIMIT_SECONDS:
            return jsonify({"status": "too_fast"}), 429

    last_submit_time[ip] = now

    data = request.json or {}
    name = data.get("name", "Anonymous")[:12]
    score = float(data.get("score", 0))

    existing = next((s for s in scores if s["name"] == name), None)

    if existing:
        if score > existing["score"]:
            existing["score"] = score
    else:
        scores.append({
            "name": name,
            "score": score
        })

    # Сортируем всех игроков
    scores.sort(key=lambda x: x["score"], reverse=True)
    
    # ИСПРАВЛЕНИЕ: Храним топ-100 вместо топ-10
    # Это позволит игрокам видеть свое место, даже если они не в лидерах
    if len(scores) > 100:
        scores[:] = scores[:100]

    save_scores()
    return jsonify({"status": "ok"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    # Возвращаем весь список (до 100 чел), чтобы клиент мог найти игрока
    return jsonify(scores)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
