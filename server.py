# Nusrava AI Chat API
# Endpoint: /chat
#
# Cara kerja:
# - POST /chat  { "message": "helo", "user": "nama-orang" }
# - Balasan dalam JSON: { "reply": "...", "role": "bot" }
#
# Integrasi AI:
# - Ganti fungsi `get_ai_reply()` dengan provider AI kamu.
# - Contoh provider yang bisa dipakai:
#   1. Ollama (lokal) — no API key, jalankan `ollama serve` dulu
#   2. Hugging Face Inference API — gratis, minta token di huggingface.co
#   3. OpenAI / Groq / dsb — minta API key
#
# Cara deploy (pilih salah satu):
#   - Render (free): dashboard Render > New Web Service > Connect repo
#   - Railway (free): `railway login` lalu `railway up` dari folder ini
#   - Fly.io: `fly auth login` lalu `fly launch` > `fly deploy`
#   - VPS: install uvicorn/gunicorn, jalankan `python server.py`
#
# Dependency:
#   pip install -r requirements.txt
import os
import re
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------- Konfigurasi ----------------
# Ganti ke environmental variable kalau punya API key
AI_PROVIDER = os.getenv("AI_PROVIDER", "demo")  # demo | groq | ollama | hf | openai
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Ollama base URL
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Hugging Face token (set via environment)
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API key provider AI (Groq, OpenAI, dsb)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile")

# Rate limit: maksimal N request per user per 60 detik
RATE_LIMIT = 5
rate_log = {}  # user -> list of timestamps


def get_ai_reply(user_message: str) -> str:
    """
    Return balasan dari AI.

    Template default: mode "demo" (sama seperti sekarang).
    Ganti isinya sesuai provider kamu.
    """
    msg = user_message.lower().strip()

    # ==============================
    # 1. RESERVED RULES (jika ada)
    # ==============================
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

    # ==============================
    # 2. PROVIDER AI (jika user menembang lebih bebas)
    # ==============================
    provider = AI_PROVIDER

    if provider == "ollama":
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
        except Exception as e:
            return f"Maaf, error koneksi ke Ollama: {e}"

    if provider == "hf":
        try:
            import requests as rq
            if not HF_TOKEN:
                return "Konfigurasikan HF_TOKEN di environment/API key dulu."
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
        except Exception as e:
            return f"Maaf, error koneksi ke Hugging Face: {e}"

    if provider == "openai":
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
        except Exception as e:
            return f"Maaf, error koneksi ke OpenAI: {e}"

    # Groq: Gratis, cepat, OpenAI-compatible API
    if provider == "groq":
        try:
            import requests as rq
            r = rq.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile"),
                    "messages": [{"role": "user", "content": user_message}],
                    "max_tokens": 200,
                },
                timeout=30,
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "Maaf, AI sedang bermasalah.")
        except Exception as e:
            return f"Maaf, error koneksi ke Groq: {e}"

    # ==============================
    # 3. DEFAULT: DUMMY TEXT
    # ==============================
    return "Maaf, saya masih belajar. Coba tanya: layanan, kontak, jam, atau harga. 😊"


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

    # ---------------- Rate limiting ----------------
    now = __import__("time").time()
    if user_id not in rate_log:
        rate_log[user_id] = []
    rate_log[user_id] = [t for t in rate_log[user_id] if now - t < 60]
    if len(rate_log[user_id]) >= RATE_LIMIT:
        return jsonify({"reply": "Terlalu banyak, masak. Tunggu sebentar ya, kemaren. ⏳"}), 429
    rate_log[user_id].append(now)

    # ---------------- AI call ----------------
    reply = get_ai_reply(user_message)

    return jsonify({
        "reply": reply,
        "role": "bot",
        "timestamp": now,
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
