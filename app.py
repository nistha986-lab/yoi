from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Motivational quotes
motivational_quotes = [
    "✨ Believe in yourself. You are capable of amazing things.",
    "🌸 Small progress is still progress.",
    "💜 Every day is a fresh start.",
    "🦋 Keep going. Your future self will thank you.",
    "🌟 Success comes from consistency."
]

@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()

    # Greetings
    if any(word in user_message for word in ["hi", "hello", "hey", "hy"]):
        reply = "🦋 Hello! I'm YOI. How are you feeling today?"

    # Name
    elif "name" in user_message:
        reply = "🦋 My name is YOI (Your Own Inspiration)."

    # Who are you
    elif "who are you" in user_message:
        reply = "🦋 I am YOI, your emotional companion and study assistant."

    # How are you
    elif "how are you" in user_message:
        reply = "😊 I'm doing great! Thank you for asking."

    # Motivation
    elif "motivate" in user_message or "motivation" in user_message:
        reply = random.choice(motivational_quotes)

    # Emotional support
    elif any(word in user_message for word in ["sad", "upset", "depressed", "crying"]):
        reply = (
            "💜 I'm sorry you're feeling this way. "
            "Remember that difficult moments are temporary. "
            "You are stronger than you think."
        )

    # Hindi emotional support
    elif any(word in user_message for word in ["udaas", "dukhi", "pareshan"]):
        reply = (
            "💜 Mujhe afsos hai ki aap udaas mehsoos kar rahe hain. "
            "Aap bahut strong hain aur yeh samay bhi guzar jayega."
        )

    # Assignment help
    elif "assignment" in user_message:
        reply = (
            "📚 Sure! Tell me:\n"
            "• Subject\n"
            "• Topic\n"
            "• Word Limit\n"
            "and I'll help you."
        )

    # AI
    elif "what is ai" in user_message or user_message == "ai":
        reply = "🤖 AI enables machines to perform human-like tasks."

    # ML
    elif "machine learning" in user_message or user_message == "ml":
        reply = "📊 Machine Learning is where computers learn from data."

    # LLM
    elif "llm" in user_message:
        reply = "🧠 LLM stands for Large Language Model."

    # Thanks
    elif "thank" in user_message:
        reply = "😊 You're welcome! I'm always here to help."

    # Bye
    elif "bye" in user_message:
        reply = "👋 Goodbye! Have a wonderful day."

    else:
        reply = f"🦋 You said: {user_message}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)