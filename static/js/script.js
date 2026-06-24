const STORAGE_KEY = "yoi_chat_history";
const NAME_KEY    = "yoi_user_name";
const THEME_KEY   = "yoi_theme";

const MOOD_EMOJIS = {
    happy:   "😊",
    sad:     "😢",
    anxious: "😟",
    angry:   "😠",
    neutral: "😐",
};

let userName = localStorage.getItem(NAME_KEY) || "";

document.addEventListener("DOMContentLoaded", () => {
    // Restore theme
    if (localStorage.getItem(THEME_KEY) === "light") {
        document.body.classList.add("light-mode");
        document.getElementById("theme-toggle").textContent = "☀️";
    }

    // Show name modal on first visit
    if (!userName) {
        document.getElementById("name-modal").style.display = "flex";
        setTimeout(() => document.getElementById("name-input").focus(), 100);
    } else {
        initChat();
    }

    document.getElementById("name-submit").addEventListener("click", submitName);
    document.getElementById("name-input").addEventListener("keydown", (e) => {
        if (e.key === "Enter") submitName();
    });
    document.getElementById("message").addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });
    document.getElementById("clear-btn").addEventListener("click", clearChat);
    document.getElementById("theme-toggle").addEventListener("click", toggleTheme);
});

function submitName() {
    const input = document.getElementById("name-input").value.trim();
    userName = input || "Friend";
    localStorage.setItem(NAME_KEY, userName);
    document.getElementById("name-modal").style.display = "none";
    initChat();
}

function initChat() {
    document.getElementById("welcome-text").textContent =
        `Hi ${userName}! I'm here for you. 💜`;

    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        try {
            JSON.parse(saved).forEach((msg) => {
                if (msg.type === "user") appendUser(msg.text, msg.time, false);
                else                     appendBot(msg.text, msg.time, false);
            });
        } catch {
            localStorage.removeItem(STORAGE_KEY);
            showWelcome();
        }
    } else {
        showWelcome();
    }
}

function showWelcome() {
    appendBot(`🦋 Hi ${userName}! I'm YOI — Your Own Inspiration. How are you feeling today?`);
}

function getTime() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function saveMessage(type, text, time) {
    let messages = [];
    try { messages = JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; } catch {}
    messages.push({ type, text, time });
    if (messages.length > 100) messages.splice(0, messages.length - 100);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

function buildBubble(className, text, time) {
    const div = document.createElement("div");
    div.className = className;

    const textSpan = document.createElement("span");
    textSpan.className = "msg-text";
    textSpan.textContent = text;

    const timeSpan = document.createElement("span");
    timeSpan.className = "msg-time";
    timeSpan.textContent = time;

    div.appendChild(textSpan);
    div.appendChild(timeSpan);
    return div;
}

function appendUser(text, time, save = true) {
    const chatBox = document.getElementById("chat-box");
    const t = time || getTime();
    chatBox.appendChild(buildBubble("user-message", text, t));
    chatBox.scrollTop = chatBox.scrollHeight;
    if (save) saveMessage("user", text, t);
}

function appendBot(text, time, save = true) {
    const chatBox = document.getElementById("chat-box");
    const t = time || getTime();
    const div = buildBubble("bot-message", text, t);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    if (save) saveMessage("bot", text, t);
    return div;
}

function showTyping() {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = "bot-message typing-indicator";
    div.id = "typing";
    div.setAttribute("aria-label", "YOI is typing");
    div.innerHTML = "<span></span><span></span><span></span>";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById("typing");
    if (el) el.remove();
}

function updateMood(mood) {
    const badge = document.getElementById("mood-indicator");
    badge.textContent = MOOD_EMOJIS[mood] || "😐";
    badge.setAttribute("aria-label", `Current mood: ${mood}`);
}

async function sendMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    appendUser(message);
    showTyping();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();
        removeTyping();
        appendBot(data.reply);
        if (data.mood) updateMood(data.mood);
    } catch {
        removeTyping();
        appendBot("⚠️ Sorry, something went wrong. Please try again.");
    }
}

async function clearChat() {
    if (!confirm("Clear all chat history?")) return;
    document.getElementById("chat-box").innerHTML = "";
    localStorage.removeItem(STORAGE_KEY);
    await fetch("/clear", { method: "POST" }).catch(() => {});
    appendBot(`🦋 Chat cleared! Hi ${userName}, how can I help you today?`);
    document.getElementById("mood-indicator").textContent = "😐";
}

function toggleTheme() {
    const isLight = document.body.classList.toggle("light-mode");
    document.getElementById("theme-toggle").textContent = isLight ? "☀️" : "🌙";
    localStorage.setItem(THEME_KEY, isLight ? "light" : "dark");
}
