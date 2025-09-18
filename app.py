from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mood detection keywords
POSITIVE = {"happy", "good", "great", "joy", "excited", "love", "awesome", "fantastic", "amazing", "glad"}
NEGATIVE = {"sad", "depressed", "angry", "upset", "unhappy", "down", "lonely", "bored"}

# Telugu fallback songs
FALLBACK_SONGS = {
    "happy": [
        "Butta Bomma – Armaan Malik",
        "Ramuloo Ramulaa – Mangli",
        "Mind Block – Blaaze"
    ],
    "sad": [
        "Samajavaragamana (Reprise) – Sid Sriram",
        "Yemito – Haricharan",
        "Nee Kallalona – Shreya Ghoshal"
    ],
    "neutral": [
        "Arere Yekkada – Shankar Mahadevan",
        "Ye Chilipi – Karthik",
        "Telusaa Telusaa – Sid Sriram"
    ]
}

def detect_mood(text):
    """Simple keyword-based mood detection"""
    t = (text or "").lower()
    for w in POSITIVE:
        if w in t:
            return "happy"
    for w in NEGATIVE:
        if w in t:
            return "sad"
    return "neutral"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_reply():
    data = request.get_json() or {}
    text = data.get("message", "")
    mood = detect_mood(text)

    songs = [{"title": s, "url": ""} for s in FALLBACK_SONGS.get(mood, FALLBACK_SONGS["neutral"])]

    reply_text = f"Detected mood: {mood}. Here are some Telugu songs 🎶"
    return jsonify({"reply": reply_text, "mood": mood, "songs": songs})

if __name__ == "__main__":
    app.run(debug=True)
