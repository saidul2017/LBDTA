# LBDTA — Literasi Big Data untuk Calon Guru PAI

Repositori paket UAS terintegrasi untuk mata kuliah **Literasi Big
Data** prodi Pendidikan Agama Islam: kurikulum 3 pertemuan + chatbot
pendamping mahasiswa berbasis Streamlit + dasbor dosen + rubrik
penilaian terotomatisasi.

> **Versi:** ringkas 3 pertemuan (intensif). Versi 16 pertemuan
> tersedia di branch `kerangka-mk-lbdta`.

## 🚀 Quick Start untuk Dosen

| Langkah | Berkas / link |
|---|---|
| **1. Baca dokumentasi alur** | [`PANDUAN-DOSEN.md`](PANDUAN-DOSEN.md) |
| **2. Deploy ke Streamlit Cloud** | [`DEPLOY.md`](DEPLOY.md) — *step-by-step ~10 menit* |
| **3. Distribusi ke mahasiswa** | [`PANDUAN-MAHASISWA.md`](PANDUAN-MAHASISWA.md) — share ke kelas |
| **4. Refleksi kritis paket** | [`ANALISIS-KRITIS.md`](ANALISIS-KRITIS.md) — temuan & batasan |

## ⚠️ Peringatan Privasi (baca dulu)

Repositori ini berisi **NIM 40 mahasiswa nyata**. Sebelum deploy
produksi:

- **Setel repo ke private** (Settings → Danger Zone → visibility).
- Nama mahasiswa sudah di-anonimkan ke inisial di `peserta/peserta.csv`.
  Versi nama lengkap tersimpan **lokal saja** di `peserta-FULL.csv`
  (di-gitignore).
- Jangan paste API key atau password di public chat. `.env` sudah
  ada di `.gitignore`.

Detail di [`peserta/README.md`](peserta/README.md) dan
[`ANALISIS-KRITIS.md`](ANALISIS-KRITIS.md).

## Struktur Direktori

```
LBDTA/
├── README.md                    Dokumen ini
├── PANDUAN-DOSEN.md             Alur kerja dosen end-to-end
├── PANDUAN-MAHASISWA.md         Alur kerja mahasiswa
├── DEPLOY.md                    Step-by-step deploy
├── ANALISIS-KRITIS.md           Refleksi akademik (8 dimensi)
│
├── rps/                         Rencana Pembelajaran Semester
│   └── RPS-LBDTA.md             KKNI Level 6 + Bloom + maqāṣid
├── modul/                       Materi 3 pertemuan
│   ├── M01-pondasi-literasi-data.md     (+ kritik AI)
│   ├── M02-praktik-analisis-data.md
│   └── M03-sintesis-etika-dan-kebijakan.md  (+ maqāṣid + ghībah)
├── tugas/                       Lembar tugas + petunjuk UAS
│   ├── PETUNJUK-TEKNIS-UAS.md   Aturan formal mengikat
│   ├── T01-pemetaan-sumber-data.md
│   ├── T02-analisis-data-sintetis.md
│   ├── T03-policy-brief-mini.md
│   ├── template-policy-brief.md
│   └── bank-pertanyaan-pemandu.md
├── rubrik/                      Rubrik penilaian R01-R03
│
├── dataset/emis-sintetis/       Dataset sintetis (300 madrasah, DGP eksplisit)
├── notebook/                    Notebook praktikum + outputs
│
├── peserta/                     Roster, pembagian kelompok, anonimisasi
│   ├── peserta.csv              Inisial (publik)
│   ├── peserta-FULL.csv         Nama lengkap (LOKAL, gitignore)
│   ├── anonimisasi.py           Konversi nama ↔ inisial
│   ├── buat_kelompok.py         Generator pembagian (seed=1446)
│   ├── kelompok-uas.md          Tabel pembagian
│   └── roster.json              Untuk konsumsi aplikasi
│
├── app/                         Aplikasi chatbot Streamlit
│   ├── streamlit_app.py         UI mahasiswa
│   ├── pages/01_dasbor_dosen.py UI dosen (6 tab + nilai)
│   ├── persona.py               System prompt + kurikulum
│   ├── llm.py                   Wrapper LLM 5 provider
│   ├── storage.py               SQLite (sesi + pesan + nilai)
│   ├── form_generator.py        Auto-form pengungkapan AI
│   ├── peserta_loader.py        Roster lookup
│   ├── tests/test_smoke.py      Smoke test 4 modul
│   ├── requirements.txt         Pinned versions
│   ├── .env.example             Template config
│   └── README.md                Setup detail
│
└── .kiro/steering/              Persona & aturan asisten
    └── asisten-pai.md           7 aturan + transliterasi standar
```

## Alur 3 Pertemuan

| Pert | Tema | Modul | Tugas | Rubrik |
|---|---|---|---|---|
| 1 | Pondasi (konsep, lanskap, etika, **kritik AI**) | M01 | T01 — Pemetaan Sumber Data (20%) | R01 |
| 2 | Praktik (cleaning, deskriptif, visualisasi) | M02 | T02 — Analisis Data Sintetis (30%) | R02 |
| 3 | Sintesis (korelasi/kausalitas, **maqāṣid + ghībah**, *policy brief*) | M03 | T03 — *Policy Brief* Mini (40%, **UAS**) | R03 |

Partisipasi & refleksi: 10%.

## Paket UAS — *Policy Brief* Mini

Tugas T03 dirancang sebagai **UAS terintegratif**. Lihat:

| Berkas | Untuk siapa |
|---|---|
| [`tugas/PETUNJUK-TEKNIS-UAS.md`](tugas/PETUNJUK-TEKNIS-UAS.md) | Mahasiswa & dosen — dokumen mengikat |
| [`tugas/template-policy-brief.md`](tugas/template-policy-brief.md) | Mahasiswa — struktur 7 bagian |
| [`tugas/bank-pertanyaan-pemandu.md`](tugas/bank-pertanyaan-pemandu.md) | Mahasiswa & dosen — Socratic prompts |
| [`rubrik/R03-policy-brief-mini.md`](rubrik/R03-policy-brief-mini.md) | Dosen — rubrik + kalibrator |
| [`notebook/01-praktikum-analisis-madrasah.py`](notebook/01-praktikum-analisis-madrasah.py) | Mahasiswa — notebook referensi |
| [`dataset/emis-sintetis/`](dataset/emis-sintetis/) | Mahasiswa — dataset + DGP |

## Pijakan Akademik

Modul ini disusun dengan rujukan:

- **KKNI Level 6** (Sarjana)
- **Permendikbudristek 53/2023** (Standar Pendidikan Tinggi)
- **Taksonomi Bloom revisi** (Anderson & Krathwohl, 2001) untuk CPMK
- **Maqāṣid al-syarīʿah** (al-Syāṭibī, Ibn ʿĀshūr, Auda) untuk etika data
- **SKB Kemenag-Mendikbud 1987** untuk transliterasi Arab-Latin

## Etika Data dalam Perspektif Islam

Modul ini menempatkan etika data sebagai pondasi, bukan sekadar
*compliance*. Kerangka:

- **Maqāṣid al-syarīʿah** — 5 *ḍarūriyyāt* (perlindungan agama, jiwa,
  akal, keturunan, harta) sebagai pijakan utama.
- Empat operasionalisasi: ***amānah*** (titipan), ***tabayyun***
  (verifikasi), ***ṣidq*** (kejujuran), ***ʿadl*** (keadilan).
- ***Ghībah* dalam analisis data** — risiko membicarakan kekurangan
  kelompok tertentu via temuan data tanpa kemaslahatan.

Detail di [`modul/M03-sintesis-etika-dan-kebijakan.md`](modul/M03-sintesis-etika-dan-kebijakan.md).

## Kontak & Bantuan

- Pertanyaan teknis: lihat [`app/README.md`](app/README.md)
  bagian Troubleshooting
- Pertanyaan akademis: dosen pengampu
- Pertanyaan tentang AI sebagai sumber: lihat M01 §5 *Kritik
  Epistemologis terhadap Asisten AI*

## Lisensi & Hak Cipta

Konten orisinal repo ini disusun untuk keperluan pengajaran. Sumber
pihak ketiga (kutipan kitab, artikel, dataset publik) wajib
dicantumkan referensinya secara eksplisit.

Untuk repo publik, **wajib** menggunakan versi peserta yang sudah
dianonimkan (lihat [`peserta/README.md`](peserta/README.md)).
