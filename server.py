# Nusrava AI Chat API
# Endpoint: /chat
#
# Cara kerja:
# - POST /chat  { "message": "helo", "user": "nama-orang" }
# - Balasan dalam JSON: { "reply": "...", "role": "bot" }
#
# Integrasi AI:
#   - Groq (gunakan OPENAI_API_KEY=*** API key)
#   - Ollama (lokal)
#   - Hugging Face (menggunakan HF_TOKEN)
#
# Cara deploy (pilih salah satu):
#   - Render (free): dashboard Render > New Web Service > Connect repo
#   - Railway (free): railway login lalu railway up dari folder ini
#   - Fly.io: fly auth login lalu fly launch > fly deploy
#   - VPS: jalankan python server.py

import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------- Konfigurasi ----------------
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # groq | ollama | hf | openai
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API key provider AI (Groq, OpenAI)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile")

RATE_LIMIT = 5
rate_log = {}  # user -> list of timestamps

# ---------------- CORS Headers ----------------
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ---------------- AI Reply Logic ----------------
def get_ai_reply(user_message: str) -> str:
    msg = user_message.lower().strip()

    # ---------- Reserved rules ----------
    if any(k in msg for k in ["halo", "hi", "hai", "helo", "hallo"]):
        return "Halo! 👋 Ada yang bisa saya bantu hari ini?"
    if "layanan" in msg or "service" in msg:
        return "Kami punya 6 layanan: website, aplikasi, jaringan, servis komputer, sistem parkir, dan sistem antrian. Mau dibahas salah satunya?"
    if "kontak" in msg or "whatsapp" in msg or "telepon" in msg or "info" in msg:
        return "WhatsApp: 0822-3388-3288. Atau chat langsung ke saya! 📲"
    if "harga" in msg or "biaya" in msg:
        return "Harga solusi bervariasi tergantung kebutuhan Anda. Hubungi via WhatsApp biar bisa diskusikan detailnya. 🏷️"
    if "terima kasih" in msg or "makasih" in msg or "thanks" in msg or "thank you" in msg:
        return "Sama-sama! 🙏 Ada yang lain?"
    if "jam" in msg or "buka" in msg or "tutup" in msg:
        return "Jam operasi: Senin–Jumat, 08.00–17.00 WIB. 📅"
    if "kantor" in msg or "alamat" in msg:
        return "Kantor kami di Surabaya, Jawa Timur, Indonesia."
    if "apakah" in msg or "apa" in msg:
        return "Mau kita bahas layanan, kontak, jam operasi, atau struktur project-nya? Silakan tanya lagi."
    if "saya ingin" in msg or "ingin" in msg:
        return "Baik! Kalau aplikasi/bisnis, langkah pertama: konsultasi → proposal → development → deployment & support. Mau dibahas bagian mana?"

    # ---------- Groq AI ----------
    if AI_PROVIDER == "groq":
        if not OPENAI_API_KEY:
            return "Konfigurasikan OPENAI_API_KEY (Groq API key) di environment dulu."
        try:
            import requests as rq
            r = rq.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": [{"role": "user", "content": user_message}],
                    "max_tokens": 200,
                },
                timeout=30,
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "Maaf, AI sedang bermasalah.")
            else:
                return f"Maaf, server Groq balas error ({r.status_code})."
        except Exception as e:
            return f"Maaf, error koneksi ke Groq: {e}"

    # ---------- Ollama AI ----------
    if AI_PROVIDER == "ollama":
        try:
            import requests as rq
            r = rq.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                    "messages": [{"role": "user", "content": user_message}],
                    "stream": False,
                },
                timeout=30,
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("message", {}).get("content", "Maaf, AI sedang bermasalah.")
            else:
                return f"Maaf, server Ollama balas error ({r.status_code})."
        except Exception as e:
            return f"Maaf, error koneksi ke Ollama: {e}"

    # ---------- Hugging Face AI ----------
    if AI_PROVIDER == "hf":
        if not HF_TOKEN:
            return "Konfigurasikan HF_TOKEN di environment/API key dulu."
        try:
            import requests as rq
            r = rq.post(
                "https://api-inference.huggingface.co/models/" + HF_MODEL,
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"inputs": user_message, "options": {"use_cache": False}},
                timeout=30,
            )
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    data = " ".join(d.get("generated_text", "") for d in data if d.get("generated_text"))
                return data or "Maaf, AI sedang bermasalah."
            else:
                return f"Maaf, server HF balas error ({r.status_code})."
        except Exception as e:
            return f"Maaf, error koneksi ke Hugging Face: {e}"

    # ---------- OpenAI / Groq (OpenAI-compatible) ----------
    if AI_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            return "Konfigurasikan OPENAI_API_KEY di environment dulu."
        try:
            import requests as rq
            r = rq.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": [{"role": "user", "content": user_message}],
                    "max_tokens": 200,
                },
                timeout=30,
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "Maaf, AI sedang bermasalah.")
            else:
                return f"Maaf, server OpenAI balas error ({r.status_code})."
        except Exception as e:
            return f"Maaf, error koneksi ke OpenAI: {e}"

    # ---------- Default fallback ----------
    return "Maaf, saya belum paham. Coba tanya: layanan, kontak, jam, atau harga. 😊"

# ---------------- API Routes ----------------
@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Nusrava AI API is running. POST to /chat"})

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    user_message = body.get("message", "").strip()
    user_id = body.get("user", "guest")

    if not user_message:
        return jsonify({"reply": "Kirim pesan dulu, ya. Bikin kalian nggak kosong."}), 400

    # ---------- Rate limiting ----------
    now = time.time()
    if user_id not in rate_log:
        rate_log[user_id] = []
    rate_log[user_id] = [t for t in rate_log[user_id] if now - t < 60]
    if len(rate_log[user_id]) >= RATE_LIMIT:
        return jsonify({"reply": "Terlalu banyak, masak. Tunggu sebentar ya, kemaren. ⏳"}), 429
    rate_log[user_id].append(now)

    # ---------- AI call ----------
    reply = get_ai_reply(user_message)

    return jsonify({
        "reply": reply,
        "role": "bot",
        "timestamp": now,
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
