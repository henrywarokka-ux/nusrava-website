# Nusrava AI — Rekomendasi Provider

BRO, berdasarkan situasi kamu (website perusahaan, chat widget, belum ada budget
API, ingin "pintar" tapi tetap jalan):

## Rekomendasi: Hugging Face (Free Tier)

| Kriteria | ChatGPT | Groq | Hugging Face | Ollama |
|---|---|---|---|---|
| Biaya | Berbayar | Terbatas/gratis | **Gratis (token)** | Gratis (lokal) |
| API key | Diperlukan | Diperlukan | **Minta saja (free)** | Gak butuh |
| Kecepatan | Cepat | Sangat cepat | Cukup | Lambat (lokal) |
| Kualitas | Bagus | Bagus | Bagus (model open) | Tergantung perangkat |
| Instal | - | - | Cukup token | Download & set up |
| Cocok startup | Kurang cocok | Cukup | **Paling cocok** | Kalu komputer kuat |

### Kenapa Hugging Face?

1. **Gratis + ready** — ikut daftar, minta token gratis, langsung pakai.
2. **Tidak butuh server addisional** — kamu cuma perlu `HF_TOKEN` di
   `server.py`.
3. **Model open-source** — pilih model yang sesuai kebutuhan (misal Mistral,
   Llama, dsb).
4. **Hosting** — kamu bisa deploy `server.py` ke Render/Railway/Fly.io/looseness.
   Siap.

### Model yang direkomendasikan

- **Mistral-7B-Instruct-v0.3** (ringan, cepat, cukup cerdas)
- **Llama-3-8B-Instruct** (lebih cerdas, lambat sedikit)
- **Phi-3-mini-4k-instruct** (ringan, cocok untuk testing)

### Cara setup Hugging Face

```bash
# 1. Daftar di huggingface.co
# 2. Login, cari bawah profil -> Access Tokens -> New Token
# 3. Pilih scope: read (atau all untuk bebas)
# 4. Salin token (contoh: hf_xxxxx...)

# 5. Set environment
set HF_TOKEN=sk-xxxxxx
set HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3

# 6. Jalankan server
python server.py
```

### Uji coba

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"halo bro, gimana satu-satu?","user":"jaket"}'
```

---

## Fallback (kalau HF gak mau jalan)

- **Ollama** — `AI_PROVIDER=ollama`, model: `llama3.2` / `phi3`. Butuh install
  di Windows, good hardware, nggak butuh API key. **Rekomendasi kalau kamu
  mau lokal sebelum deploy.**
- **Groq** — `AI_PROVIDER=openai`, model: `llama-3.3-70b-versatile` (cepat),
  API key dari console.groq.com. Cepat, tapi berbayar setelah free tier.

---

## Saran Proses

1. **Pertama**, coba Hugging Face. Lebih mudah, gratis, cuma butuh token.
2. **Ketika cuplikan**, update `HF_MODEL` ke model terbaik atau pertimbangkan
   Groq jika butuh kecepatan.
3. **Setelah semua entar**, deploy `server.py` ke Render/Railway/Fly.io/
   likelihood.

---

## Setup Otomatis!

Ada perintah yang kering, dus kamu bisa pilih live perintah:

- `./setup-hf.sh` — Setup Hugging Face (buat env, install dep, test)
- `./setup-ollama.sh` — Setup Ollama (download, install, test)
- `./deploy-render.sh` — Deploy ke Render (free)
- `./deploy-railway.sh` — Deploy ke Railway (free)

Kalau mau, aku buatkan script ini sekarang. Pilih 1 yang mau, bro.

---

*Report: rekomendasi Hugging Face + langkah setup otomatis. Terus masuk kerja, bro.*
