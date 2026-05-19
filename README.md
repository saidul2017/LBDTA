# LBDTA — Literasi Big Data untuk Calon Guru PAI

> **Versi modul:** ringkas **3 pertemuan** (intensif). Cocok untuk
> *workshop* atau modul pengantar. Versi panjang 16 pertemuan tersedia
> di branch `kerangka-mk-lbdta`.

Repositori mata kuliah **Literasi Big Data** untuk program studi
Pendidikan Agama Islam (PAI). Berisi rencana pembelajaran, modul,
dataset latihan, tugas, rubrik, dan notebook praktikum.

## Struktur direktori

```
LBDTA/
├── README.md
├── rps/                     # Rencana Pembelajaran Semester (3 pertemuan)
│   └── RPS-LBDTA.md
├── modul/                   # Materi per pertemuan
│   ├── M01-pondasi-literasi-data.md
│   ├── M02-praktik-analisis-data.md
│   └── M03-sintesis-etika-dan-kebijakan.md
├── tugas/                   # Lembar tugas mahasiswa
│   ├── T01-pemetaan-sumber-data.md
│   ├── T02-analisis-data-sintetis.md
│   └── T03-policy-brief-mini.md
├── rubrik/                  # Rubrik penilaian
│   ├── R01-pemetaan-sumber-data.md
│   ├── R02-analisis-data-sintetis.md
│   └── R03-policy-brief-mini.md
├── dataset/
│   └── emis-sintetis/       # Dataset sintetis madrasah (300 madrasah)
├── referensi/               # Buku, artikel, kitab rujukan
├── notebook/                # Jupyter / RMarkdown praktikum
└── .kiro/
    └── steering/            # Persona & aturan asisten AI
```

## Alur 3 Pertemuan

| Pert | Tema | Modul | Tugas | Rubrik |
|---|---|---|---|---|
| 1 | Pondasi (konsep, lanskap, pengantar etika) | M01 | T01 — Pemetaan Sumber Data (20%) | R01 |
| 2 | Praktik (cleaning, deskriptif, visualisasi) | M02 | T02 — Analisis Data Sintetis (30%) | R02 |
| 3 | Sintesis (korelasi/kausalitas, etika, *policy brief*) | M03 | T03 — *Policy Brief* Mini (40%) | R03 |

Partisipasi & refleksi: 10%.

## Cara menggunakan repo ini

### Sebagai dosen
1. Sunting `rps/RPS-LBDTA.md` agar sesuai prodi.
2. Tambahkan rujukan utama ke folder `referensi/`.
3. Sesuaikan parameter dataset di `dataset/emis-sintetis/generate.py`
   bila ingin distribusi atau ukuran berbeda, lalu jalankan ulang skrip.

### Sebagai mahasiswa
1. Baca modul pertemuan terkait di `modul/`.
2. Kerjakan tugas di `tugas/`, gunakan dataset di `dataset/`.
3. Konsultasikan progres dengan asisten AI — asisten **mengajak Anda
   berpikir**, bukan memberi jawaban langsung. Ini disengaja.
4. Setiap klaim akademis wajib **dirujuk ke sumber**.

## Etika data dalam perspektif Islam

Tiga prinsip pondasi yang dijaga sepanjang modul:

- **Amānah** — data adalah titipan; jaga kerahasiaan & integritasnya.
- **Tabayyun** (Q.S. al-Ḥujurāt: 6) — verifikasi sumber sebelum
  menyimpulkan.
- **Ṣidq & ʿadl** — kejujuran dalam pelaporan, keadilan dalam dampak.

Detail dibahas pada **Pertemuan 3**.

## Lisensi & hak cipta

Konten orisinal repo ini disusun untuk keperluan pengajaran. Sumber
pihak ketiga wajib dicantumkan referensinya secara eksplisit.
