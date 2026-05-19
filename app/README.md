# Chatbot UAS — Literasi Big Data PAI

Aplikasi web Streamlit yang menjadi **pendamping mahasiswa** selama
mengerjakan UAS *Policy Brief* Mini, mematuhi 7 aturan persona yang
sudah dirancang dosen pengampu (lihat `.kiro/steering/asisten-pai.md`).

> **Tujuan:** mahasiswa terbantu *berpikir*, bukan dijawabkan
> tugasnya. Setiap interaksi terekam dan ter-sertakan sebagai bukti
> integritas akademik (*ṣidq*) saat submit UAS.

## Fitur

- 💬 **Mahasiswa** — chat dengan persona asisten PAI (7 aturan, Socratic)
- 🎓 **Dosen** — dasbor terpisah dengan password: statistik, transkrip,
  daftar mahasiswa belum pakai, ekspor CSV/ZIP
- 📚 Akses langsung ke **seluruh dokumen kurikulum** (RPS, modul,
  tugas, rubrik, dataset README, notebook referensi) sebagai konteks
- 👤 **Login NIM** — mahasiswa pilih dari roster 40 nama; nama,
  kelompok, topik UAS auto-terisi (anti-impersonasi)
- 📜 Riwayat per sesi tersimpan di SQLite (audit trail)
- 📋 **Auto-generate Form Pengungkapan AI** dari riwayat — siap
  dilampirkan ke UAS sesuai `tugas/PETUNJUK-TEKNIS-UAS.md` §7
- 🔌 Provider LLM **fleksibel**: Groq (default), Gemini, OpenAI,
  Anthropic, Ollama
- 🔍 Sidebar transparan: dosen/mahasiswa bisa lihat berkas mana saja
  yang dimuat sebagai basis pengetahuan

## Quick start (laptop dosen)

```bash
# dari root repo
cd app
pip install -r requirements.txt
cp .env.example .env
# Edit .env — minimal isi GROQ_API_KEY (gratis, lihat di bawah)

streamlit run streamlit_app.py
```

Buka http://localhost:8501. Selesai.

## Mendapatkan API key gratis

### 🥇 Groq (rekomendasi default)

1. Buka https://console.groq.com → login dengan Google.
2. Menu **API Keys** → **Create API Key**.
3. Tempel ke `.env` sebagai `GROQ_API_KEY=...`.
4. Limit gratis: ~30 request/menit. Cukup untuk ~30 mahasiswa
   sekaligus.

### 🥈 Google Gemini

1. https://aistudio.google.com/apikey → buat API key.
2. Di `.env`, ubah `LLM_PROVIDER=gemini` + isi `GEMINI_API_KEY=...`.

### 🥉 OpenAI / Anthropic

Berbayar; gunakan jika sudah ada budget atau akun. Ubah
`LLM_PROVIDER` dan isi key yang sesuai di `.env`.

### 🏠 Ollama (offline)

Jika ingin tanpa internet (mis. lab kampus tanpa akses luar):

```bash
# Install Ollama dari https://ollama.com
ollama pull llama3.2
# di .env: LLM_PROVIDER=ollama, LLM_MODEL=llama3.2
```

## Deploy gratis ke cloud

### Streamlit Community Cloud (paling mudah)

1. Push branch ini ke GitHub.
2. Buka https://share.streamlit.io → **New app**.
3. Pilih repo, branch `chatbot-uas`, main file: `app/streamlit_app.py`.
4. **Advanced settings → Secrets** — isi:
   ```toml
   LLM_PROVIDER = "groq"
   GROQ_API_KEY = "gsk_..."
   LLM_MODEL = "llama-3.3-70b-versatile"
   ```
5. Klik **Deploy**. Aplikasi akan tersedia di
   `https://<nama-acak>.streamlit.app` — bagikan URL ini ke mahasiswa.

### Hugging Face Spaces

1. Buat Space baru: https://huggingface.co/new-space
   → SDK: **Streamlit** → Hardware: **CPU basic (gratis)**.
2. Push isi folder `app/` ke Space repo (atau hubungkan dari GitHub).
3. **Settings → Variables and secrets** — isi `GROQ_API_KEY` dst.
4. Aplikasi otomatis terbangun.

## Cara mahasiswa menggunakan

1. Buka URL aplikasi (atau jalan lokal).
2. Sidebar → isi **nomor kelompok**, **anggota**, **topik UAS**.
3. Klik **🆕 Mulai sesi baru**.
4. Tanya apa pun. Asisten akan mengajak berpikir, bukan menjawab
   final.
5. Sebelum submit UAS:
   - Buka tab **📋 Form Pengungkapan AI** → klik **⬇️ Unduh Form**.
   - Konversi ke PDF (mis. via VS Code → Print → Save as PDF).
   - Lampirkan ke submission UAS sebagai `03_form-ai.pdf`.

## Audit untuk dosen

Database SQLite di `app/data/sessions.db` menyimpan **semua sesi
& pesan**. Dua cara akses:

### Cara 1 — Dasbor Dosen (web)

Setelah Bapak/Ibu set `DOSEN_PASSWORD` di `.env`, buka aplikasi
lalu klik halaman **🎓 Dasbor Dosen** di sidebar Streamlit.

Fitur dasbor:
- Statistik agregat (sesi, pesan, mahasiswa aktif, kelompok aktif)
- Tabel sesi dengan filter (kelompok, topik, min. pesan)
- Detail per sesi (transkrip + Form Pengungkapan AI)
- Daftar mahasiswa **belum pakai** chatbot (untuk follow-up)
- Ekspor CSV semua sesi
- Ekspor ZIP semua Form Pengungkapan AI sekaligus

### Cara 2 — SQL langsung

```sql
-- Daftar semua sesi
SELECT id, created_at, kelompok, topik
FROM sessions
ORDER BY created_at DESC;

-- Pesan kelompok tertentu
SELECT role, content, created_at
FROM messages
WHERE session_id = 'xxx-xxxx-xxxx'
ORDER BY id;

-- Hitung volume interaksi per kelompok
SELECT s.kelompok, COUNT(m.id) AS jumlah_pesan
FROM sessions s
LEFT JOIN messages m ON s.id = m.session_id
GROUP BY s.kelompok
ORDER BY jumlah_pesan DESC;
```

Atau gunakan GUI seperti [DB Browser for SQLite](https://sqlitebrowser.org/).

## Struktur kode

| Berkas | Fungsi |
|---|---|
| `streamlit_app.py` | UI mahasiswa (3 tab: Chat, Riwayat, Form AI) |
| `pages/01_dasbor_dosen.py` | Dasbor dosen (auth + statistik + ekspor) |
| `persona.py` | System prompt: 7 aturan + pemuat dokumen kurikulum |
| `peserta_loader.py` | Pemuat `peserta/roster.json` untuk login NIM |
| `llm.py` | Wrapper LLM provider-agnostic |
| `storage.py` | Logging sesi & pesan ke SQLite |
| `form_generator.py` | Auto-generate Form Pengungkapan AI |
| `requirements.txt` | Dependensi Python |
| `.env.example` | Template variabel lingkungan |
| `.streamlit/config.toml` | Tema warna |

## Mengubah persona / aturan

Edit konstanta `RULES` di `app/persona.py`. Untuk perubahan permanen
yang konsisten dengan workflow Kiro, sunting juga
`.kiro/steering/asisten-pai.md` di root repo.

## Mengubah dokumen yang dimuat

Edit fungsi `_collect_files()` di `app/persona.py`. Default memuat:

- `README.md` (root)
- Semua `.md` di `rps/`, `modul/`, `tugas/`, `rubrik/`
- `README.md` di setiap subfolder `dataset/`
- `notebook/01-praktikum-analisis-madrasah.py`

Berkas `.kiro/steering/asisten-pai.md` **dilewati** (sudah ada di
system prompt sebagai aturan).

## Catatan keamanan & privasi

- ⚠️ **JANGAN commit `.env`** — sudah ada di `.gitignore`.
- Database SQLite menyimpan semua transkrip mahasiswa. Pertimbangkan
  pengaturan retensi (mis. hapus setelah nilai final keluar).
- Streamlit Cloud bersifat **publik**. Untuk privasi, deploy di
  server kampus atau gunakan password (tambahkan auth Streamlit).
- API key punya kuota / biaya. Pantau penggunaan di dashboard
  provider masing-masing.

## Troubleshooting

| Gejala | Solusi |
|---|---|
| `GROQ_API_KEY belum di-set` | Buat `.env` dari `.env.example` & isi key |
| `ModuleNotFoundError: groq` | Jalankan `pip install -r requirements.txt` |
| Respons LLM lama | Cek koneksi internet; coba provider lain |
| Streamlit Cloud build gagal | Pastikan main file = `app/streamlit_app.py` |
| Riwayat hilang setelah restart | DB di-mount di volume sementara cloud — gunakan PostgreSQL untuk persistensi (kustomisasi lanjut) |

## Lisensi

Kode di folder ini bagian dari repo LBDTA. Lihat lisensi di README
root.
