# 🤖 CLI AI — Terminal AI Assistant (Ollama)

AI berbasis percakapan yang berjalan **100% lokal & gratis** di terminal,  
tanpa internet, tanpa biaya, tanpa GUI.

---

## 📋 Daftar Isi

1. [Kebutuhan Sistem](#kebutuhan-sistem)
2. [Instalasi](#instalasi)
3. [Download Model AI](#download-model-ai)
4. [Cara Menjalankan](#cara-menjalankan)
5. [Perintah dalam Chat](#perintah-dalam-chat)
6. [Mematikan & Membersihkan RAM](#mematikan--membersihkan-ram)
7. [Konfigurasi](#konfigurasi)
8. [Troubleshooting](#troubleshooting)
9. [Pertanyaan Umum](#pertanyaan-umum)

---

## Kebutuhan Sistem

| Komponen | Minimum | Rekomendasi |
|----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| Storage | 5GB (per model) | 20GB+ |
| OS | Linux / macOS | Linux |
| Python | 3.8+ | 3.10+ |
| Internet | Hanya saat download model | — |

---

## Instalasi

### Langkah 1 — Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verifikasi instalasi:
```bash
ollama --version
```

---

### Langkah 2 — Install library Python

```bash
pip install ollama
```

---

### Langkah 3 — Simpan script

Buat folder dan simpan file `chat_ollama.py` di dalamnya:

```bash
mkdir ~/cli-ai
cd ~/cli-ai
# taruh chat_ollama.py di sini
```

---

## Download Model AI

Download **salah satu** model berikut (sesuai kebutuhan):

| Perintah | Model | RAM | Keunggulan |
|----------|-------|-----|------------|
| `ollama pull llama3.1:8b` | LLaMA 3.1 8B | ~5GB | Paling pintar & serbaguna ✅ |
| `ollama pull mistral:7b` | Mistral 7B | ~4GB | Cepat, bagus untuk kode |
| `ollama pull gemma2:9b` | Gemma2 9B | ~6GB | Akurat, buatan Google |
| `ollama pull qwen2.5:7b` | Qwen2.5 7B | ~5GB | Kuat di coding & matematika |
| `ollama pull deepseek-r1:8b` | DeepSeek-R1 8B | ~5GB | Reasoning mendalam |

**Rekomendasi untuk RAM 16GB+:** `llama3.1:8b`

```bash
ollama pull llama3.1:8b
```

Proses download sekitar 5–15 menit tergantung kecepatan internet.  
**Setelah terdownload, model tidak butuh internet lagi.**

Cek model yang sudah terdownload:
```bash
ollama list
```

---

## Cara Menjalankan

### Langkah 1 — Jalankan Ollama (Terminal 1)

```bash
ollama serve
```

Biarkan terminal ini tetap terbuka. Jika muncul `Ollama is running` → sudah siap.

### Langkah 2 — Jalankan Chat AI (Terminal 2)

```bash
cd ~/cli-ai
python3 chat_ollama.py
```

---

### Verifikasi Ollama aktif (opsional)

```bash
curl http://localhost:11434
# Output: Ollama is running ✓
```

---

## Perintah dalam Chat

Setelah program berjalan, ketik perintah berikut kapan saja:

| Perintah | Fungsi |
|----------|--------|
| `/help` | Tampilkan daftar perintah |
| `/clear` | Bersihkan layar terminal |
| `/reset` | Hapus riwayat percakapan sesi ini |
| `/history` | Tampilkan ringkasan riwayat percakapan |
| `/save` | Simpan percakapan ke file `.txt` |
| `/model` | Ganti model AI (dari yang sudah terdownload) |
| `/models` | Lihat semua model yang ada di komputer |
| `/pull` | Download model baru langsung dari dalam chat |
| `/system` | Ubah kepribadian / system prompt AI |
| `/stats` | Toggle tampilan statistik (token/detik, waktu respons) |
| `/config` | Tampilkan konfigurasi aktif |
| `/exit` | Keluar dari program |

**Tips:** Tekan `↑` / `↓` untuk navigasi riwayat input sebelumnya.

---

## Mematikan & Membersihkan RAM

### Keluar dari chat
Ketik `/exit` atau tekan `Ctrl+C` di terminal chat.

### Matikan Ollama (bebaskan RAM)

**Cara 1** — Di terminal yang menjalankan `ollama serve`, tekan `Ctrl+C`

**Cara 2** — Dari terminal mana saja:
```bash
pkill ollama
```

**Cara 3** — Via systemctl:
```bash
systemctl stop ollama
```

### Verifikasi RAM sudah bebas
```bash
curl http://localhost:11434
# Harus muncul: Connection refused ✓
```

> **Catatan:** Selama `ollama serve` masih berjalan, model tetap dimuat di RAM  
> meskipun chat Python-nya sudah ditutup.

---

## Konfigurasi

Konfigurasi tersimpan otomatis di `~/.cli_ai_ollama/config.json`:

```json
{
  "model": "llama3.1:8b",
  "system_prompt": "Kamu adalah asisten AI yang sangat cerdas...",
  "max_history": 50,
  "show_stats": false,
  "stream": true
}
```

Riwayat percakapan tersimpan di `~/.cli_ai_ollama/history.json` dan  
otomatis dilanjutkan di sesi berikutnya.

Untuk reset riwayat permanen:
```bash
rm ~/.cli_ai_ollama/history.json
```

---

## Troubleshooting

**`❌ Ollama tidak berjalan!`**
```bash
ollama serve   # jalankan di terminal terpisah
```

**`❌ Model error: not found`**
```bash
ollama list                  # cek model yang ada
ollama pull llama3.1:8b      # download model
# atau ketik /pull di dalam chat
```

**AI menjawab lambat**
- Normal untuk respons pertama (model loading)
- Respons berikutnya jauh lebih cepat
- Coba model yang lebih kecil: `mistral:7b`

**AI menjawab "tidak bisa berjalan tanpa internet"**
- Itu **jawaban keliru dari model**, bukan kondisi aktual
- Program ini murni lokal, tidak ada koneksi internet
- Buktikan: matikan WiFi, program tetap berjalan normal

**Port 11434 sudah dipakai**
```bash
pkill ollama
ollama serve
```

---

## Pertanyaan Umum

**Apakah butuh internet untuk pakai AI-nya?**  
Tidak. Internet hanya dibutuhkan saat pertama kali download model (`ollama pull`).  
Setelah itu 100% offline.

**Apakah data percakapan dikirim ke server?**  
Tidak. Semua proses terjadi di komputer sendiri. Tidak ada data yang keluar.

**Berapa lama model bertahan di RAM?**  
Selama `ollama serve` berjalan. Setelah `pkill ollama`, RAM langsung bebas.

**Bisa ganti model di tengah percakapan?**  
Bisa. Ketik `/model` lalu pilih model lain. Riwayat percakapan tetap tersimpan.

**Di mana model disimpan?**  
```bash
~/.ollama/models/
```

**Cara hapus model yang tidak dipakai:**
```bash
ollama rm nama-model
# contoh:
ollama rm mistral:7b
```

---

## Struktur File

```
~/cli-ai/
└── chat_ollama.py        ← Program utama

~/.cli_ai_ollama/         ← Data pengguna (dibuat otomatis)
├── config.json           ← Konfigurasi
└── history.json          ← Riwayat percakapan

~/.ollama/models/         ← Model AI (dikelola Ollama)
```
