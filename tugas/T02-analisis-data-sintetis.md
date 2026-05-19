# Tugas 02 — Analisis Data Madrasah (Dataset Sintetis)

**Pertemuan:** 2
**Bobot:** 30% nilai akhir
**Sifat:** Kelompok (2–3 mahasiswa)
**Tenggat:** sebelum Pertemuan 3

## Tujuan

Mahasiswa mampu membersihkan, menganalisis secara deskriptif, dan
memvisualisasikan dataset pendidikan dengan cara yang jujur dan
informatif.

## Dataset

Gunakan dataset sintetis di `dataset/emis-sintetis/`:

- `madrasah_sintetis.csv`
- `guru_pai_sintetis.csv`
- `siswa_pai_sintetis.csv`

Kamus data: `dataset/emis-sintetis/README.md`.

> **Ingat:** dataset ini **sintetis**. Tulis disclaimer ini di laporan Anda.

## Yang harus dikerjakan

### A. Pembersihan (boleh disebut "tidak ada" jika memang bersih)

1. Cek tipe data, missing values, duplikat, outlier per kolom kunci.
2. Tulis ringkasan singkat: temuan + tindakan (jika ada).

### B. Statistika deskriptif

Jawab dengan tabel/angka **dan** narasi 1–2 kalimat per pertanyaan:

1. Berapa rata-rata `rata_nilai_pai` per `jenjang`? Apakah median berbeda
   jauh dari mean? Apa artinya?
2. Berapa persentase madrasah per `akreditasi`? Sajikan tabel frekuensi.
3. Bagaimana sebaran `persen_guru_sertifikasi` antara `Negeri` vs
   `Swasta`? Sajikan ringkasan 5-angka (min, Q1, median, Q3, max).
4. Bagaimana profil literasi digital guru per `kualifikasi`?

### C. Visualisasi (3 chart wajib)

1. **Histogram** sebaran `rata_nilai_pai`.
2. **Boxplot** `rata_nilai_pai` per `akreditasi`.
3. **Scatter plot** `persen_guru_sertifikasi` (sumbu X) vs
   `rata_nilai_pai` (sumbu Y), beri *trendline* dan komentar singkat.

### D. Refleksi

- Apa pola paling menarik yang Anda temukan?
- Pola mana yang **belum bisa Anda simpulkan sebagai sebab-akibat**?
  Mengapa? (Kaitkan dengan konsep *confounder* yang akan diperdalam di
  Pertemuan 3.)

## Format penyerahan

- Notebook (Jupyter `.ipynb` atau Spreadsheet) **+** ringkasan PDF
  4–6 halaman.
- Kode harus bisa dijalankan ulang (*reproducible*) — sertakan langkah
  setup di README laporan Anda.
- Cantumkan **disclaimer dataset sintetis** di halaman pertama.

## Rubrik

Lihat `rubrik/R02-analisis-data-sintetis.md`.

## Catatan dari asisten AI

Asisten boleh membantu Anda **debug error**, **menjelaskan konsep**,
dan **mengoreksi pemilihan chart**. Asisten tidak akan **menulis
seluruh notebook** untuk Anda. Cantumkan ringkasan interaksi di lampiran.
