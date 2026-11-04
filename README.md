# PT Nusrava Teknologi Nusantara

Website perusahaan untuk **PT Nusrava Teknologi Nusantara**, penyedia
solusi teknologi: website, aplikasi, infrastruktur jaringan, servis komputer,
sistem parkir, dan sistem antrian.

---

## Struktur File

```
nusrava-website/
├── index.html          # Halaman utama (semuanya dalam satu file)
└── README.md           # Dokumentasi (ini file)
```

---

## Cara Buka Lokal

Cukup buka `index.html` di browser:

```bash
# Windows
start index.html

# Linux / Mac
open index.html
# atau
xdg-open index.html
```

---

## Cara Upload ke GitHub

1. Buat akun GitHub (github.com)
2. Klik **+ New repository**
   - Repository name: `nusrava-website`
   - Is public (biar bisa diakses orang lain)
   - JANGAN centang "Add a README file" (kita sudah punya README kita sendiri)
3. Klik **Create repository**
4. Di bagian "…or push an existing repository from the command line":
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Nusrava company website"
   git branch -M main
   git remote add origin https://github.com/username/nusrava-website.git
   git push -u origin main
   ```
5. Buka `https://github.com/username/nusrava-website` — file `index.html`
   akan tampil, dan kamu bisa klik untuk melihat siap dijalankan.

---

## Fitur Website

- **Hero** yang bersih dengan gradient text
- **Layanan** 6 produk: website, aplikasi, jaringan, servis komputer, parkir, antrian
- **Proses kerja** 4 langkah
- **Testimoni** pelanggan
- **Kontak** lengkap + form kirim pesan
- **Chat widget** (default: demo mode, lihat bagian bawah)

---

## Fitur Chat Widget (API — kenalan ke AI)

Chat widget di `index.html` sekarang **bukan cuma demo template**. Setiap kali user mengirim, widget
mengirim `POST` ke `server.py` (dijalankan di endpoint API kamu). Server dibalikkan balasan, lalu
ditampilkan di chat dengan animasi natural.

### Cara kerja
- `POST /chat`  →  `{ "message": "...", "user": "..." }`
- Balasan: `{ "reply": "...", "role": "bot", "timestamp": ... }`
- Rate limit: 5 request/user per 60 detik (terdapat di `server.py`)

### Koneksi ke AI (pilih 1 di `server.py`)
| Opsi | Konfigurasi | Note |
|---|---|---|
| **Ollama (localhost)** | `AI_PROVIDER=ollama` | Gratis, butuh RAM 4GB+ |
| **Hugging Face** | `AI_PROVIDER=hf`, `HF_TOKEN`, `HF_MODEL` | Gratis, minta token di HF |
| **OpenAI / Groq** | `AI_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_MODEL` | Cepat, berbayar |

Ganti `AI_PROVIDER` di `server.py` sesuai yang kamu pakai.

---

## Style Guide

- Warna primer: purple `#6366F1`
- Warna aksen: green `#10B981`
- Font: sistem
- Layout: responsif

---

## Kontak (from site, hardcoded)

```text
WhatsApp: 0822-3388-3288
Email: contact@nusrava.id
Alamat: Surabaya, Jawa Timur, Indonesia
```

---

## Lokasi

Ini adalah **starter template** untuk PT Nusrava. Sesuaikan:
1. `index.html` — isi, foto, kontak
2. `README.md` — nama repo, deskripsi, link GitHub
3. `server.py` — hubungkan ke AI aslinya

---

## Langkah Lanjut (opsional)

Untuk halaman berikutnya, lanjutkan dengan kata "lanjut" atau minta saya buat file tambahan:
- **`assets/`** — gambar, logo, icon
- **`css/`** — pemisahan CSS (bisa lanjut dari sini)
- **`js/`** — pemisahan JavaScript (bisa lanjut dari sini)
- **`.gitignore`** — jika butuh file lokal
- **`docs/`** — dokumentasi teknis, API, skema data, spreadsheet, dll
