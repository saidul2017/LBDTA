# Panduan Dosen — UAS Literasi Big Data PAI

> Dokumen praktis untuk Bapak/Ibu dosen pengampu. Berisi alur kerja
> end-to-end mulai dari deploy chatbot, distribusi tugas, monitoring
> selama UAS, sampai input nilai dan ekspor.

## 🗺️ Alur Singkat

```
1. DEPLOY chatbot ke Streamlit Cloud (sekali, ~10 menit)
       ↓
2. UMUMKAN ke kelas: URL chatbot + password kelas + tenggat
       ↓
3. MAHASISWA pakai chatbot untuk diskusi & menulis brief
       ↓
4. MAHASISWA submit brief PDF ke LMS / email
       ↓
5. DOSEN baca brief, isi NILAI di dasbor (per kelompok)
       ↓
6. EKSPOR CSV nilai → import ke SIA kampus
```

## 1. Persiapan Awal (sekali sebelum UAS dimulai)

### 1.1 Verifikasi data peserta

Buka `peserta/peserta.csv` di GitHub atau editor. Pastikan 40 NIM &
nama benar. Jika ada koreksi:

```bash
# edit peserta.csv lalu regenerate pembagian
python peserta/buat_kelompok.py
```

### 1.2 Dapatkan API key Gemini (gratis)

1. Buka https://aistudio.google.com/apikey
2. Login Google → **Create API Key**
3. Salin (formatnya `AIzaSy...`)

### 1.3 Deploy ke Streamlit Cloud (gratis)

1. Login ke https://share.streamlit.io
2. **New app** → pilih repo `saidul2017/LBDTA`, branch `chatbot-uas`,
   main file `app/streamlit_app.py`
3. **Advanced settings → Secrets**, tempel:
   ```toml
   LLM_PROVIDER = "gemini"
   GEMINI_API_KEY = "AIzaSy...key-anda"
   LLM_MODEL = "gemini-2.5-flash"
   LLM_PROMPT_MODE = "full"
   DOSEN_PASSWORD = "dosen-lbdta-2026"
   KELAS_PASSWORD = "lbdta-kelas-2026"
   ```
4. Klik **Deploy**. Setelah build selesai, Bapak/Ibu dapat URL,
   misalnya: `https://lbdta-pai-uas.streamlit.app`

### 1.4 Test sebagai dosen & mahasiswa

- **Sebagai mahasiswa:** buka URL → input password kelas
  `lbdta-kelas-2026` → pilih NIM mana saja → pilih gender → mulai sesi
  → tanya "apa itu confounder?" → cek tab "Form Pengungkapan AI"
- **Sebagai dosen:** klik halaman **"🎓 Dasbor Dosen"** di sidebar
  Streamlit → input `dosen-lbdta-2026` → cek 6 tab dasbor

## 2. Distribusi Tugas ke Mahasiswa

### 2.1 Yang harus Bapak/Ibu sampaikan ke kelas

Salin-tempel teks berikut ke pengumuman LMS / WAG / email:

> **🎓 UAS Literasi Big Data PAI — Information Pack**
>
> Assalāmu'alaykum wr. wb. Berikut info UAS:
>
> **1. Bentuk UAS:** Policy Brief Mini (kelompok 2-3 mahasiswa)
> Bobot 40% nilai akhir.
>
> **2. Pembagian kelompok:** Lihat di repo
> `saidul2017/LBDTA` → folder `peserta/kelompok-uas.md`. Cari NIM Anda
> di tabel "Tabel Pencarian (urut NIM)". Pembagian **mengikat**.
>
> **3. Materi UAS (wajib dibaca):**
> - `tugas/PETUNJUK-TEKNIS-UAS.md` — aturan formal
> - `tugas/T03-policy-brief-mini.md` — instruksi tugas
> - `tugas/template-policy-brief.md` — template yang disalin & diisi
> - `tugas/bank-pertanyaan-pemandu.md` — pertanyaan pemandu Socratic
> - `rubrik/R03-policy-brief-mini.md` — rubrik penilaian (transparan)
>
> **4. Asisten AI (chatbot UAS):**
> URL: https://lbdta-pai-uas.streamlit.app
> Password kelas: **lbdta-kelas-2026**
> Penggunaan **wajib** disertai Form Pengungkapan AI (auto-generate
> dari chatbot, lampirkan saat submit).
>
> **5. Submit:**
> - **Tenggat:** [TANGGAL & JAM — diisi dosen]
> - **Channel:** [LMS / Google Classroom / email — diisi dosen]
> - **Format ZIP** berisi:
>     - `01_brief.pdf` (4-6 hal)
>     - `02_notebook.ipynb` (analisis data)
>     - `03_form-ai.pdf` (download dari chatbot, dikonversi ke PDF)
> - **Nama berkas:** `UAS-LBDTA_K{nomor}_{topik-singkat}.zip`
>
> **6. Presentasi:**
> Akhir Pertemuan 3, durasi 8-10 menit + 5 menit tanya-jawab.
>
> Terima kasih, semoga sukses. _Wassalāmu'alaykum_.

### 2.2 Tindakan opsional yang sangat membantu

- **Sebar password kelas via channel pribadi** (WAG, bukan publik).
- **Backup:** simpan link Streamlit Cloud + password di Google Doc
  pribadi Bapak/Ibu, jaga-jaga lupa.
- **Sediakan office hour** 30 menit di tiap pertemuan untuk
  konsultasi langsung; mahasiswa yang stuck bisa ditolong.

## 3. Monitoring Selama UAS

### 3.1 Akses Dasbor Dosen

1. Buka URL Streamlit Cloud yang sama dengan mahasiswa.
2. Klik halaman **"🎓 Dasbor Dosen"** di sidebar Streamlit (panel kiri).
3. Input password: `dosen-lbdta-2026`.
4. Akses 6 tab:
   - **📊 Statistik** — sekilas pandang aktivitas kelas
   - **📋 Daftar Sesi** — semua sesi mahasiswa (filter per kelompok/topik)
   - **🚫 Belum Pakai** — siapa yang belum aktif (untuk follow-up)
   - **🔎 Detail Sesi** — baca transkrip + unduh form per sesi
   - **📝 Nilai** — input rubrik R03 per kelompok
   - **💾 Ekspor** — download CSV/ZIP

### 3.2 Yang perlu Bapak/Ibu pantau

| Yang dipantau | Tab | Catatan |
|---|---|---|
| Apakah semua mahasiswa sudah pakai? | 🚫 Belum Pakai | Follow-up via WAG kalau ada yg belum |
| Topik mana yang paling diminati? | 📊 Statistik | Liat bar chart per topik |
| Kelompok mana yang paling aktif? | 📊 Statistik | Liat bar chart per kelompok |
| Apakah mahasiswa pakai dengan benar? | 🔎 Detail Sesi | Sample baca 2-3 transkrip |
| Indikasi plagiarisme/joki? | 🔎 Detail Sesi | Cek pola pertanyaan tidak natural |

## 4. Penilaian Policy Brief

### 4.1 Alur penilaian

1. Mahasiswa submit `01_brief.pdf` + `02_notebook.ipynb` + `03_form-ai.pdf`
   (lewat LMS).
2. Bapak/Ibu **download & baca** 3 berkas tersebut.
3. Buka dasbor → tab **📝 Nilai** → pilih kelompok.
4. Geser slider 7 dimensi rubrik (skor 1-4 per dimensi).
5. Input pengurangan etis (jika ada pelanggaran).
6. Tulis catatan untuk kelompok.
7. Klik **💾 Simpan Nilai** → nilai akhir auto-hitung 0-100.

### 4.2 Tujuh dimensi rubrik R03

| # | Dimensi | Bobot | Cek di brief |
|---|---|---|---|
| 1 | Ringkasan eksekutif | 10% | Bagian 1 — padat? rekomendasi jelas? |
| 2 | Kekuatan bukti (data & sumber) | 20% | Bagian 2-3 — multi-sumber? sitasi? |
| 3 | Kesadaran confounder & batasan | 20% | Bagian 4 — confounder spesifik? |
| 4 | Kualitas rekomendasi | 20% | Bagian 5 — aktor, jangka, indikator? |
| 5 | Pertimbangan etis Islam | 15% | Bagian 6 — 4 prinsip dibahas konkret? |
| 6 | Komunikasi & visual | 10% | Visual jujur? naratif mengalir? |
| 7 | Sitasi & integritas akademik | 5% | Sitasi konsisten? disclaimer dataset? |

### 4.3 Rumus nilai akhir

```
nilai_akhir = (Σ skor_i × bobot_i) × 25 - pengurangan_etis
```

Contoh: skor 3 di semua dimensi → 3 × 25 = **75/100**.
Skor 4 di semua dimensi → **100/100**.

### 4.4 Pengurangan etis (sesuai rubrik R03)

| Pelanggaran | Pengurangan |
|---|---|
| Tidak isi Form Pengungkapan AI | -20 |
| Cherry-picking visual menyesatkan | -15 |
| Plagiarisme parsial | nilai 0 brief |
| Plagiarisme/fabrikasi/joki total | nilai 0 UAS |

## 5. Ekspor untuk SIA Kampus

1. Buka tab **💾 Ekspor**.
2. Klik **📝 Ekspor CSV nilai UAS** → unduh `nilai-uas-YYYYMMDD.csv`.
3. CSV berisi: `kelompok, topik, anggota_nim, anggota_nama,
   skor_*, pengurangan_etis, nilai_akhir, catatan, dinilai_oleh`.
4. Buka di Excel → mapping ke format SIA kampus → upload.

## 6. Setelah UAS Selesai

### 6.1 Arsip
- Tab **💾 Ekspor** → klik **ZIP semua Form Pengungkapan AI** → arsip
  bukti integritas akademik per kelompok.
- Database SQLite (`app/data/sessions.db`) bisa di-backup dari
  Streamlit Cloud (atau pindah ke PostgreSQL untuk persistensi
  jangka panjang).

### 6.2 Refleksi (opsional)
- Tab **📊 Statistik** — lihat pola interaksi: mana topik yang sulit,
  durasi rata-rata, dll. → input untuk perbaikan kurikulum semester
  berikutnya.

### 6.3 Privasi
- Setelah nilai final keluar dan dikirim ke SIA, pertimbangkan
  **menghapus database** atau setidaknya men-anonimkan transkrip
  (sesuai prinsip *amānah* — data adalah titipan).

## 7. Troubleshooting

| Masalah | Solusi |
|---|---|
| Mahasiswa tidak bisa login | Cek apakah `KELAS_PASSWORD` benar di Secrets |
| Saya lupa password dosen | Edit Secrets di Streamlit Cloud → re-deploy |
| Chatbot lama merespons | Cek limit Gemini (250 RPD); upgrade ke Gemini 2.5 Pro Tier 1 jika perlu |
| Ada NIM mahasiswa salah | Edit `peserta/peserta.csv` di GitHub → app auto-pakai versi baru |
| Database hilang setelah Streamlit Cloud restart | Schedule backup harian via tab Ekspor; atau migrate ke PostgreSQL |
| Mahasiswa terdeteksi joki | Lihat di Detail Sesi: pola pertanyaan terlalu canggih untuk level mahasiswa, atau sangat mirip antar kelompok |

## 8. Kontak Bantuan Teknis

Untuk pertanyaan teknis tentang chatbot, edit kode, atau request
fitur baru — silakan reply di sesi Kiro berikutnya, atau buka issue
di repo GitHub.
