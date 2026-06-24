import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "yoi-dev-secret-change-in-prod")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Groq uses an OpenAI-compatible API — key comes from GROQ_API_KEY in .env
groq = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """You are YOI (Your Own Inspiration), a warm and empathetic AI companion for emotional support, motivation, and study assistance. You support both English and Hindi.

Guidelines:
- Be warm, compassionate, and encouraging
- Use emojis naturally (🦋 💜 🌸 ✨ 🌟)
- Keep responses concise (2–4 sentences)
- For emotional distress, acknowledge feelings first, then offer support
- For study or academic topics, give practical actionable tips
- For AI/tech questions, give clear helpful explanations
- Never give medical advice; recommend professional help for serious mental health concerns
- If someone seems in crisis, always suggest speaking to a trusted adult or counsellor"""

MOOD_KEYWORDS = {
    "happy": ["happy", "excited", "joyful", "great", "amazing", "wonderful", "fantastic", "thrilled", "proud", "good"],
    "sad": ["sad", "upset", "depressed", "crying", "cry", "hopeless", "helpless", "broken", "udaas", "dukhi", "unhappy"],
    "anxious": ["stressed", "stress", "anxious", "anxiety", "worried", "overwhelmed", "panic", "nervous", "pareshan", "scared"],
    "angry": ["angry", "anger", "furious", "mad", "irritated", "frustrated", "annoyed"],
}


def detect_mood(message):
    msg = message.lower()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(k in msg for k in keywords):
            return mood
    return "neutral"


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
@limiter.limit("20 per minute")
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    raw = data.get("message", "")
    if not isinstance(raw, str):
        return jsonify({"error": "Invalid message"}), 400

    user_message = raw.strip()[:1000]
    if not user_message:
        return jsonify({"reply": "🦋 Please type something — I'm here to listen!", "mood": "neutral"})

    if "history" not in session:
        session["history"] = []

    session["history"].append({"role": "user", "content": user_message})
    if len(session["history"]) > 20:
        session["history"] = session["history"][-20:]

    mood = detect_mood(user_message)

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + session["history"]
        response = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        session["history"].append({"role": "assistant", "content": reply})
        session.modified = True
    except Exception as e:
        print("Groq error:", e)
        reply = "🦋 I'm having a little trouble connecting right now. Please try again in a moment."

    return jsonify({"reply": reply, "mood": mood})


@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=5008)
