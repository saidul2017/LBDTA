# Chatbot UAS — Literasi Big Data PAI

Aplikasi web Streamlit yang menjadi **pendamping mahasiswa** selama
mengerjakan UAS *Policy Brief* Mini, mematuhi 7 aturan persona yang
sudah dirancang dosen pengampu (lihat `.kiro/steering/asisten-pai.md`).

> **Tujuan:** mahasiswa terbantu *berpikir*, bukan dijawabkan
> tugasnya. Setiap interaksi terekam dan ter-sertakan sebagai bukti
> integritas akademik (*ṣidq*) saat submit UAS.

## Fitur

- 💬 **Mahasiswa** — chat dengan persona asisten PAI (7 aturan, Socratic)
- 🎓 **Dosen** — dasbor terpisah dengan password: 5 metrik, 5 chart
  visualisasi, tabel sesi + filter, daftar mahasiswa belum pakai,
  detail per sesi, ekspor CSV/ZIP
- 📚 Akses langsung ke **seluruh dokumen kurikulum** (RPS, modul,
  tugas, rubrik, dataset README, notebook referensi) sebagai konteks
- 👤 **Login NIM** — mahasiswa pilih dari roster 40 nama; nama,
  kelompok, topik UAS auto-terisi (anti-impersonasi). **Gender diisi
  sendiri oleh mahasiswa** saat login (otonomi data pribadi).
- 🔐 **Password kelas** opsional — agar URL Streamlit Cloud tidak
  diakses orang luar (set `KELAS_PASSWORD` di `.env`)
- 📜 Riwayat per sesi tersimpan di SQLite (audit trail)
- 📋 **Auto-generate Form Pengungkapan AI** dari riwayat — siap
  dilampirkan ke UAS sesuai `tugas/PETUNJUK-TEKNIS-UAS.md` §7
- 🔌 Provider LLM **fleksibel**: Groq (default), Gemini, OpenAI,
  Anthropic, Ollama

## Quick start (laptop dosen)

```bash
# dari root repo
cd app
pip install -r requirements.txt
cp .env.example .env
# Edit .env — minimal isi GEMINI_API_KEY (lihat di bawah)

streamlit run streamlit_app.py
```

Buka http://localhost:8501. Selesai.

## Password default (sudah disiapkan)

Untuk memudahkan dosen, password default sudah disetel di `.env.example`:

| Akses | Password default |
|---|---|
| **Dasbor Dosen** | `dosen-lbdta-2026` |
| **Mahasiswa (kelas)** | `lbdta-kelas-2026` |

> ⚠️ Bapak/Ibu **bisa ganti** ke password lain di `.env` jika dirasa
> perlu lebih kuat. Tapi `.env` tidak ter-commit ke Git, jadi cukup
> aman untuk pemakaian normal kelas.

## Mendapatkan API key gratis

### 🥇 Google Gemini (default & rekomendasi)

Gemini 2.5 Flash punya **1M context window**, **1M TPM**, **250 RPD**
free tier — cukup untuk kelas 40 mahasiswa tanpa upgrade.

1. Buka https://aistudio.google.com/apikey
2. Login dengan akun Google.
3. Klik **Create API Key** → pilih project (atau bikin baru).
4. Salin key → tempel ke `.env` sebagai `GEMINI_API_KEY=...`.
5. **Tidak perlu kartu kredit.** ✓

> **Catatan tentang "Gemini Pro" / "Gemini Advanced":**
> Subscription Google One AI Premium (web Gemini) **BUKAN** akses API.
> API key tetap diambil dari AI Studio dan free tier-nya sudah memadai.
> Jika Bapak/Ibu sudah upgrade Vertex AI / Tier 1 paid, bisa pakai
> `gemini-2.5-pro` dengan limit jauh lebih besar.

### 🥈 Groq (alternatif gratis, tapi rate limit ketat)

1. Buka https://console.groq.com → login dengan Google.
2. **API Keys → Create API Key**.
3. Tempel ke `.env` sebagai `GROQ_API_KEY=...` + ubah
   `LLM_PROVIDER=groq` + `LLM_PROMPT_MODE=compact`.
4. ⚠️ Free tier hanya 12K TPM — wajib pakai mode compact.

### 🥉 OpenAI / Anthropic

Berbayar; gunakan jika sudah ada budget atau akun. Ubah
`LLM_PROVIDER` dan isi key yang sesuai di `.env`.

### 🏠 Ollama (offline, mis. lab kampus tanpa internet)

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
   LLM_PROVIDER = "gemini"
   GEMINI_API_KEY = "AIza..."
   LLM_MODEL = "gemini-2.5-flash"
   LLM_PROMPT_MODE = "full"
   DOSEN_PASSWORD = "dosen-lbdta-2026"
   KELAS_PASSWORD = "lbdta-kelas-2026"
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

5 tab dasbor:
- **📊 Statistik** — 5 chart: distribusi sesi per topik, per kelompok,
  gender mahasiswa aktif, volume pesan harian, volume pesan per kelompok
- **📋 Daftar Sesi** — tabel + filter (kelompok, topik, min. pesan)
- **🚫 Belum Pakai** — daftar mahasiswa belum buka sesi (untuk follow-up)
- **🔎 Detail Sesi** — transkrip + ekspor Form Pengungkapan AI per sesi
- **💾 Ekspor** — CSV semua sesi + ZIP semua Form Pengungkapan AI sekaligus

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
