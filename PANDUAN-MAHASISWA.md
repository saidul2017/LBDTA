# Panduan Mahasiswa — UAS Literasi Big Data PAI

> Bacalah panduan ini **sebelum** mulai mengerjakan UAS. Untuk
> aturan formal lengkap, baca `tugas/PETUNJUK-TEKNIS-UAS.md`.

## 🗺️ Alur Singkat

```
1. CEK kelompok & topik di peserta/kelompok-uas.md
       ↓
2. BACA materi UAS: T03, template, rubrik, petunjuk teknis
       ↓
3. AKSES chatbot UAS untuk diskusi & bantuan
       ↓
4. KERJAKAN policy brief di Word/Docs/Markdown bersama tim
       ↓
5. UNDUH Form Pengungkapan AI dari chatbot
       ↓
6. SUBMIT ZIP berisi brief + notebook + form ke LMS
```

## 1. Cek Kelompok & Topik Anda

1. Buka repo `saidul2017/LBDTA` di GitHub.
2. Buka `peserta/kelompok-uas.md`.
3. Cari NIM Anda di **"Tabel Pencarian (urut NIM)"**.
4. Catat **kode kelompok** (contoh: K05) dan **topik UAS**.
5. Hubungi anggota kelompok untuk koordinasi.

## 2. Baca Materi UAS (wajib)

| Berkas | Untuk apa |
|---|---|
| `tugas/PETUNJUK-TEKNIS-UAS.md` | **Aturan formal mengikat** — tenggat, format, sanksi |
| `tugas/T03-policy-brief-mini.md` | Instruksi tugas: 3 pilihan topik, struktur brief |
| `tugas/template-policy-brief.md` | **Template yang disalin** dan diisi tim Anda |
| `tugas/bank-pertanyaan-pemandu.md` | 28 pertanyaan Socratic untuk *self-coaching* |
| `rubrik/R03-policy-brief-mini.md` | Rubrik penilaian (transparan ke Anda) |

> Tip: cetak / save offline rubrik R03. Pakai sebagai *checklist*
> sebelum submit.

## 3. Akses Chatbot UAS

### 3.1 Login

1. Buka URL chatbot yang dikasih dosen
   (mis. https://lbdta-pai-uas.streamlit.app).
2. Input **password kelas** yang dikasih dosen
   (mis. `lbdta-kelas-2026`). Jangan sebar password publik.
3. Sidebar kiri:
   - **Pilih NIM Anda** dari dropdown → nama, kelompok, topik
     auto-terisi.
   - **Pilih Jenis Kelamin** Anda (Laki-laki / Perempuan / Tidak
     ingin menyebut).
   - Klik **🆕 Mulai sesi baru**.

### 3.2 Cara berinteraksi

Asisten **bukan untuk dijawabkan** — dia akan **mengajak Anda berpikir**.

✅ **Pertanyaan yang bagus:**
- "Apa itu confounder dan kenapa penting dalam analisis pendidikan?"
- "Saya error `ModuleNotFoundError: pandas` di notebook, gimana cara fix?"
- "Bagaimana saya menulis ringkasan eksekutif yang padat?"
- "Saya berargumen X — apakah ini cukup kuat? Apa kelemahannya?"

❌ **Pertanyaan yang akan ditolak halus:**
- "Tuliskan policy brief lengkap, saya copas saja."
- "Tuliskan rekomendasi kebijakan untuk topik 1."
- "Buat semua tabel analisis untuk saya."

### 3.3 Apa yang asisten lakukan?

- Menjelaskan **konsep** dan mengkaitkan ke modul/rubrik.
- **Mengajukan pertanyaan reflektif** — Anda yang menjawab.
- Mengarahkan ke **berkas spesifik** di repo (mis. `[modul/M03-...md]`).
- Menolak **mengerjakan tugas** Anda — dia mendorong Anda berpikir.

## 4. Kerjakan Policy Brief Bersama Tim

### 4.1 Workflow yang disarankan

1. **Hari 1-2:** baca semua materi, diskusikan topik dengan tim,
   sketsa kerangka brief.
2. **Hari 3-5:** analisis data sintetis (notebook), eksplorasi
   confounder. Diskusikan temuan dengan asisten chatbot.
3. **Hari 6-7:** tulis brief 4-6 hal di Google Docs / Word, mengikuti
   `tugas/template-policy-brief.md`.
4. **Hari 8:** revisi terakhir, baca lagi rubrik, cek *checklist*
   submit di Petunjuk Teknis §10.
5. **Hari 9:** submit.

### 4.2 Yang harus dihasilkan tim

| # | Berkas | Format |
|---|---|---|
| 1 | Policy brief 4-6 halaman | PDF, font 11pt, spasi 1.15 |
| 2 | Notebook analisis data | `.ipynb` atau spreadsheet, _reproducible_ |
| 3 | Form Pengungkapan AI | PDF (download dari chatbot, konversi) |

## 5. Unduh Form Pengungkapan AI

**Setelah Anda selesai berinteraksi dengan chatbot**:

1. Di chatbot, buka tab **📋 Form Pengungkapan AI**.
2. Klik **⬇️ Unduh Form (Markdown)** — file `form-pengungkapan-ai-XXXXXX.md`.
3. Konversi ke PDF:
   - **Cara A (VS Code):** buka file `.md` → install ekstensi
     "Markdown PDF" → klik kanan → "Markdown PDF: Export (pdf)".
   - **Cara B (Typora):** buka file `.md` → File → Export → PDF.
   - **Cara C (online):** buka https://md-to-pdf.fly.dev → tempel
     isi `.md` → Generate.
4. Rename PDF menjadi `03_form-ai.pdf`.

> ⚠️ Tidak melampirkan Form ini = **pengurangan 20 poin** sesuai
> Petunjuk Teknis UAS §7.

## 6. Submit ke LMS / Email

### 6.1 Susun ZIP

```
UAS-LBDTA_K05_sertifikasi.zip
├── 01_brief.pdf
├── 02_notebook.ipynb
└── 03_form-ai.pdf
```

Format nama: `UAS-LBDTA_K{nomor}_{topik-singkat}.zip`. Contoh:
- `UAS-LBDTA_K01_pemerataan.zip`
- `UAS-LBDTA_K05_sertifikasi.zip`
- `UAS-LBDTA_K09_infrastruktur.zip`

### 6.2 Submit lewat saluran resmi

- Saluran: **[LMS / Google Classroom / email — diisi dosen]**
- Pastikan **upload ZIP**, bukan file terpisah.
- Pastikan submit **sebelum tenggat** — file yang masuk setelah
  tenggat **akan ditolak** sesuai Petunjuk Teknis §1.

## 7. Presentasi

- **Durasi:** 8-10 menit per kelompok + 5 menit tanya-jawab.
- **Pastikan semua anggota** siap menjawab pertanyaan dosen, tidak
  boleh "itu bagian teman saya".
- Slide tidak wajib, tapi disarankan; bisa pakai Google Slides.

## 8. Pertanyaan Sering Diajukan (FAQ)

**Q: Apakah saya boleh pakai chatbot lain (ChatGPT, Claude, dsb)?**
A: Boleh, tapi **wajib diungkapkan** di kolom "Bagian dokumen UAS yang
BUKAN sepenuhnya hasil pemikiran kami" pada Form Pengungkapan AI.
Tidak diungkapkan = pelanggaran *ṣidq* = pengurangan poin.

**Q: Kalau chatbot lama merespons / error, gimana?**
A: Refresh browser. Kalau masih error, hubungi dosen via WAG.
Tenggat tidak akan ditunda kecuali ada pemberitahuan resmi.

**Q: Saya lupa download Form sebelum tutup browser?**
A: Login ulang dengan NIM yang sama → riwayat sesi sebelumnya akan
muncul → buka tab Form Pengungkapan AI.

**Q: Saya ingin minta extension tenggat?**
A: Hubungi dosen langsung, bukan via chatbot. Alasan harus sah
(sakit dengan surat dokter, urusan keluarga, dll).

**Q: Bagaimana cara konversi `.md` ke PDF tanpa install software?**
A: Gunakan https://md-to-pdf.fly.dev (gratis, online). Atau buka
GitHub → file `.md` Anda → klik "Print" di browser → "Save as PDF".

**Q: Pembagian kelompok saya kurang cocok, boleh ganti?**
A: Hubungi dosen dengan alasan sah. Pembagian ini reproducible
(seed terkontrol), jadi kalau diganti, kelompok lain juga ikut
berubah — biasanya dosen tidak akan ganti kecuali ada alasan kuat.

## 9. Aturan Etika Singkat

Sesuai prinsip Islam yang dipakai sepanjang mata kuliah:

- **Amānah** — data adalah titipan; jaga kerahasiaan & integritas.
- **Tabayyun** — verifikasi sumber sebelum menyimpulkan; bedakan
  korelasi dari kausalitas.
- **Ṣidq** — laporkan apa adanya, akui keterbatasan.
- **ʿAdl** — adil pada kelompok yang dirugikan rekomendasi Anda.

Bawa keempatnya secara konkret ke dalam Bagian 6 brief Anda.

---

_Wassalāmu'alaykum wr. wb. Selamat mengerjakan, semoga sukses._
