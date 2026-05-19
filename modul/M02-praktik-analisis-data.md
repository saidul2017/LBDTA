# Modul Pertemuan 2 — Praktik Analisis Data Madrasah

> **Status:** Draft v0.1 — silakan disunting dosen pengampu.

## Sub-CPMK

Setelah pertemuan ini, mahasiswa diharapkan mampu:

1. Membersihkan dataset pendidikan: menangani missing value, duplikat,
   tipe data salah, dan inkonsistensi.
2. Menghitung dan menafsirkan **statistika deskriptif** (mean, median,
   modus, standar deviasi, kuartil) untuk data madrasah.
3. Memilih jenis **visualisasi** yang tepat sesuai jenis variabel dan
   menyajikan satu *data story* sederhana.

## Bahan Kajian

### 1. Alur kerja analisis (mini-pipeline)

```
   ingest  →  inspect  →  clean  →  aggregate  →  visualize  →  interpret
```

### 2. Pembersihan data — *checklist* minimum

- **Tipe data**: angka di kolom angka, kategori di kolom kategori.
- **Missing values**: berapa banyak? acak atau sistematis?
- **Duplikat**: apakah ada `id_madrasah` muncul dua kali?
- **Outlier**: apakah ada `rasio_siswa_guru = 250`? Salah input?
- **Konsistensi label**: `"Negeri"` vs `"NEGERI"` vs `"negri"`.

### 3. Statistika deskriptif yang relevan untuk pendidikan

| Pertanyaan | Statistik yang sesuai |
|---|---|
| "Berapa rata-rata nilai PAI?" | mean, median |
| "Apakah sebaran merata atau timpang?" | std deviation, IQR |
| "Berapa madrasah berakreditasi A vs C?" | tabel frekuensi & persen |
| "Apakah Negeri & Swasta beda?" | mean per kelompok + boxplot |

### 4. Memilih visualisasi

| Variabel | Chart yang tepat |
|---|---|
| 1 numerik | histogram, density |
| 1 kategori | bar chart |
| 1 numerik × 1 kategori | boxplot, violin |
| 2 numerik | scatter plot |
| Banyak kategori berurutan | ordered bar / lollipop |

> **Anti-pola:** pie chart >5 irisan, 3D chart, sumbu Y dipotong tanpa
> penjelasan, warna yang menyesatkan. Diskusi etika visualisasi akan
> dilanjutkan di Modul 3 (*ṣidq* dalam visual).

### 5. Dataset latihan

Gunakan tiga berkas di `dataset/emis-sintetis/`:

- `madrasah_sintetis.csv`
- `guru_pai_sintetis.csv`
- `siswa_pai_sintetis.csv`

Lihat kamus data di `dataset/emis-sintetis/README.md`.

> **Pengingat:** dataset ini **sintetis**. Pola yang ditemukan tidak
> mewakili realitas madrasah Indonesia.

## Aktivitas Kelas (100 menit)

| Menit | Aktivitas |
|---|---|
| 0–10 | Pembuka, *recap* P1 |
| 10–25 | Mini-lecture: alur analisis & checklist cleaning |
| 25–60 | **Praktikum 1** — bersihkan `madrasah_sintetis.csv`, hitung deskriptif per `jenjang` |
| 60–85 | **Praktikum 2** — buat 2 visualisasi: (a) sebaran nilai PAI per akreditasi, (b) hubungan persen sertifikasi vs nilai PAI |
| 85–95 | *Show & tell* dua kelompok + diskusi visual |
| 95–100 | Penutup, briefing T02 |

## Tool

Boleh memilih salah satu sesuai kesiapan kelas:

- **Spreadsheet** (Excel/Google Sheets/LibreOffice) — pivot table, chart
- **Python** + Pandas + Matplotlib/Seaborn (Jupyter)
- **R** + Tidyverse + ggplot2 (RMarkdown)

## Bahan Bacaan

*(dosen mohon mengisi)*
- Bab *data cleaning* dan *visualization* dari buku rujukan utama.

## Penugasan

Lihat `tugas/T02-analisis-data-sintetis.md`.
