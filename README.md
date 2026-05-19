# LBDTA — Literasi Big Data untuk Calon Guru PAI

Repositori mata kuliah **Literasi Big Data** untuk program studi Pendidikan
Agama Islam (PAI). Berisi rencana pembelajaran, modul, dataset latihan,
tugas, rubrik, dan notebook praktikum.

> **Status:** kerangka awal (versi 0.1). Konten masih perlu disesuaikan oleh
> dosen pengampu sesuai kurikulum prodi, jumlah SKS, dan profil mahasiswa.

## Struktur direktori

```
LBDTA/
├── README.md                # Dokumen ini
├── rps/                     # Rencana Pembelajaran Semester
├── modul/                   # Materi per pertemuan
├── referensi/               # Buku, artikel, kitab rujukan
├── dataset/                 # Data latihan & sintetis
│   └── emis-sintetis/
├── notebook/                # Jupyter / RMarkdown praktikum
├── tugas/                   # Lembar tugas mahasiswa
├── rubrik/                  # Rubrik penilaian
└── .kiro/
    └── steering/            # Persona & aturan asisten AI
```

## Cara menggunakan repo ini

### Sebagai dosen
1. Sunting `rps/RPS-LBDTA.md` agar sesuai prodi (CPL, SKS, jumlah peserta).
2. Tambahkan rujukan utama ke folder `referensi/` (PDF, link, atau ringkasan).
3. Sesuaikan parameter dataset di `dataset/emis-sintetis/generate.py` jika
   ingin distribusi atau ukuran berbeda, lalu jalankan ulang skrip.
4. Tambahkan modul pertemuan berikutnya di `modul/` dengan format yang sama.

### Sebagai mahasiswa
1. Baca modul pertemuan terkait di `modul/`.
2. Kerjakan tugas yang tertaut di `tugas/`, gunakan dataset di `dataset/`.
3. Konsultasikan progres dengan asisten AI — asisten akan **mengajak Anda
   berpikir**, bukan memberi jawaban langsung. Ini disengaja.
4. Setiap klaim akademis Anda harus **dirujuk ke sumber** (dokumen di
   `referensi/`, dataset, atau pustaka eksternal yang valid).

## Etika data dalam perspektif Islam

Mata kuliah ini menempatkan etika data sebagai pondasi, bukan sekadar
*compliance*. Tiga prinsip utama yang dijadikan rujukan etis:

- **Amānah** — data adalah titipan; pengelola wajib menjaga kerahasiaan
  dan integritasnya.
- **Tabayyun** (Q.S. al-Ḥujurāt: 6) — verifikasi sumber sebelum menarik
  kesimpulan atau menyebarkan informasi.
- **Ṣidq & ʿadl** — kejujuran dalam pelaporan hasil dan keadilan dalam
  pengambilan kebijakan berbasis data.

Detail dibahas pada **Pertemuan 3** modul.

## Lisensi & hak cipta

Konten orisinal repo ini disusun untuk keperluan pengajaran. Sumber pihak
ketiga (kutipan kitab, artikel, dataset publik) wajib dicantumkan
referensinya secara eksplisit pada dokumen pemakai.
