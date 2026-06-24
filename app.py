from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are YOI (Your Own Inspiration).

You are:
- Friendly and supportive
- Emotional companion
- Assignment helper
- Motivational coach

You can communicate in:
- English
- Hindi

Always be polite, positive, and helpful.
"""


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message", "")

    try:

        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "grok-3-mini",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            print(data)
            reply = "⚠️ Unable to get response from YOI."

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "reply": "⚠️ YOI is currently unavailable."
        })


if __name__ == "__main__":
    app.run(debug=True,port=5008)