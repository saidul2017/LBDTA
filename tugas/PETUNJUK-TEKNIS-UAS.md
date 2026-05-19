# Petunjuk Teknis Ujian Akhir Semester (UAS)

**Mata Kuliah:** Literasi Big Data
**Program Studi:** Pendidikan Agama Islam
**Bentuk UAS:** *Policy Brief* Mini — capstone integratif dari Modul 1–3

> Dokumen ini bersifat mengikat. Mahasiswa **wajib** membaca seluruhnya
> sebelum mulai mengerjakan UAS.

---

## 1. Identitas UAS

| Komponen | Isian |
|---|---|
| Nama UAS | *Policy Brief* Mini Pendidikan Islam |
| Bobot terhadap nilai akhir | 40% |
| Sifat | Kelompok 2–3 mahasiswa |
| Tenggat penyerahan | *(diisi dosen — tanggal & jam, tegas)* |
| Tenggat presentasi | Akhir Pertemuan 3 *(luring/daring sesuai jadwal)* |
| Tenggat revisi tertulis | 1 minggu setelah presentasi |
| Saluran pengumpulan | *(LMS / Google Classroom / email — diisi dosen)* |
| Dosen pengampu | *(isi: nama + kontak resmi)* |

## 2. Tujuan & lingkup

UAS ini menguji **CPMK 1–5** secara terintegrasi:

1. Pemahaman konsep literasi data dan lanskap data pendidikan Islam (CPMK 1–2)
2. Kemampuan analisis data deskriptif & visualisasi (CPMK 3)
3. Kesadaran *confounder* dan batasan inferensi (CPMK 4)
4. Penyusunan rekomendasi kebijakan beretika Islam (CPMK 5)

Lingkup analisis **terbatas pada dataset sintetis** yang disediakan
(`dataset/emis-sintetis/`) ditambah **maksimal 2 sumber publik tambahan**
(EMIS publik, BPS, AKMI, atau jurnal ilmiah). Penggunaan data pribadi
nyata **dilarang**.

## 3. Pemilihan topik

Setiap kelompok memilih **satu** dari tiga pertanyaan kebijakan
(lihat `tugas/T03-policy-brief-mini.md`). Topik wajib didaftarkan ke
dosen sebelum *(diisi dosen — tanggal kunci topik)* untuk menghindari
duplikasi berlebih antar kelompok.

## 4. Format penyerahan

### 4.1 Berkas wajib

| No | Berkas | Format | Keterangan |
|---|---|---|---|
| 1 | *Policy brief* | PDF | 4–6 hal, font 11pt, spasi 1.15, margin 2.54 cm |
| 2 | Notebook analisis | `.ipynb` atau spreadsheet | harus bisa dijalankan ulang |
| 3 | *Form* pengungkapan AI | PDF (lihat §7) | wajib ditandatangani semua anggota |
| 4 | Rekaman presentasi *(jika daring)* | mp4 / link | maks 12 menit |

### 4.2 Penamaan berkas

```
UAS-LBDTA_Kelompok-{nomor}_{topik-singkat}.zip
└── 01_brief.pdf
└── 02_notebook.ipynb
└── 03_form-ai.pdf
└── 04_lampiran-data/
```

## 5. Struktur *policy brief* (wajib)

Gunakan **Template** di `tugas/template-policy-brief.md`. Brief harus
memuat 7 bagian dengan urutan:

1. Ringkasan eksekutif (1 paragraf)
2. Latar belakang
3. Temuan utama (3–5 bullet, dirujuk ke data)
4. Diskusi & batasan (minimal 1 *confounder*)
5. Rekomendasi (3 butir: aktor, jangka, indikator)
6. Pertimbangan etis Islam (*amānah, tabayyun, ṣidq, ʿadl*)
7. Daftar pustaka & data (sitasi lengkap + disclaimer dataset sintetis)

## 6. Penilaian

Penilaian menggunakan rubrik di `rubrik/R03-policy-brief-mini.md`,
dengan komposisi:

| Komponen | Bobot dalam UAS |
|---|---|
| Dokumen *policy brief* | 60% |
| Presentasi & tanya-jawab | 25% |
| Notebook analisis (reproducibility) | 10% |
| Disiplin proses (topik tepat waktu, *form* AI lengkap) | 5% |

Nilai UAS akhir = (Σ komponen) × bobot UAS terhadap nilai akhir MK (40%).

## 7. Penggunaan asisten AI — wajib diungkap

Penggunaan asisten AI **diperbolehkan dan didorong** sebagai mitra
diskusi. Namun, sesuai prinsip *ṣidq*, mahasiswa **wajib mengungkapkan**
penggunaannya melalui *form* berikut (lampirkan di submission):

```
FORM PENGUNGKAPAN PENGGUNAAN ASISTEN AI

Kelompok        : ____
Anggota         : 1. ____  2. ____  3. ____
Nama asisten    : ____ (mis. Kiro, ChatGPT, Gemini)

Untuk apa saja asisten kami gunakan? (centang)
[ ] Klarifikasi konsep / definisi
[ ] Bantuan debug error kode
[ ] Saran pemilihan visualisasi
[ ] Sparring argumen kebijakan
[ ] Koreksi tata bahasa
[ ] Lainnya: ____

Bagian mana yang BUKAN hasil pemikiran kami? Sebutkan jika ada:
________________________________________________

Pernyataan:
Kami menyatakan bahwa seluruh argumen, interpretasi, dan rekomendasi
dalam dokumen ini adalah hasil pemikiran kami. Asisten AI digunakan
sebagai mitra berpikir, bukan pengganti.

Tanda tangan: 1. ____  2. ____  3. ____  Tanggal: ____
```

**Tidak mengisi *form* ini = pelanggaran integritas akademik (*ṣidq*),
sanksi sesuai §9.**

## 8. Aturan integritas akademik

1. **Plagiarisme** (mengambil teks/ide tanpa sitasi) — nilai 0.
2. **Fabrikasi data** (mengarang angka atau sumber) — nilai 0 + tindak
   lanjut sesuai tata tertib prodi.
3. **Joki / pengerjaan oleh pihak ketiga** — nilai 0 + tindak lanjut.
4. **Cherry-picking visualisasi** dengan sengaja menyesatkan —
   pengurangan minimal 15 poin meskipun teknis benar.
5. **Salin antar kelompok** — kedua kelompok dinilai 0.

## 9. Sanksi

| Pelanggaran | Sanksi |
|---|---|
| Tidak mengisi *form* AI | -20 poin (komponen disiplin) |
| Cherry-picking visual | -15 poin minimal |
| Plagiarisme parsial | nilai 0 untuk komponen brief |
| Plagiarisme total / fabrikasi / joki | nilai 0 UAS + dilaporkan ke prodi |

## 10. *Checklist* sebelum submit

Mahasiswa **wajib** mencentang semuanya sebelum mengumpulkan:

- [ ] Brief 4–6 halaman, format sesuai §4
- [ ] 7 bagian struktur lengkap (§5)
- [ ] Minimal 1 *confounder* dibahas eksplisit
- [ ] *Amānah, tabayyun, ṣidq, ʿadl* dibahas konkret di bagian 6
- [ ] 3 rekomendasi punya: aktor, jangka, indikator
- [ ] Notebook dapat dijalankan ulang dari awal
- [ ] Disclaimer "dataset sintetis" tertulis di brief & notebook
- [ ] *Form* pengungkapan AI ditandatangani semua anggota
- [ ] Semua sumber tersitasi (kitab/buku/artikel/dataset)
- [ ] Tidak ada data pribadi nyata mahasiswa/guru/siswa

## 11. Kontak & bantuan

- Pertanyaan klarifikasi tata teknis: dosen pengampu
- Bantuan teknis kode: gunakan asisten AI **dengan pengungkapan** (§7)
- Pertanyaan etika data: silakan rujuk Modul 3 dan diskusikan di kelas

---

*Versi 0.1 — disusun sebagai paket UAS. Mohon disunting dosen pengampu
sebelum disebarkan ke mahasiswa.*
