# Rencana Pembelajaran Semester (RPS) — Versi Ringkas 3 Pertemuan

> **Catatan:** Dokumen ini adalah **draft template** versi *intensif* — hanya
> 3 pertemuan. Cocok untuk **workshop, modul tambahan, atau pengantar**
> sebelum mata kuliah penuh. Bukan kutipan dokumen resmi Kemenag/Diktis.
> Dosen pengampu wajib menyesuaikan dengan konteks lembaga.

## 1. Identitas Mata Kuliah / Modul

| Komponen | Isian |
|---|---|
| Nama | Literasi Big Data (versi ringkas) |
| Kode | *(isi sesuai kurikulum)* |
| Bobot | 1 SKS *(saran: 3 × 100 menit + tugas mandiri)* |
| Program Studi | Pendidikan Agama Islam (PAI) |
| Prasyarat | Statistika Pendidikan / Pengantar TIK |
| Dosen Pengampu | *(isi)* |

## 2. Deskripsi Modul

Modul intensif **3 pertemuan** yang membekali calon guru PAI dengan literasi
data pendidikan Islam. Mahasiswa dilatih membaca, menganalisis, dan
menafsirkan data pendidikan dengan landasan etika Islam (*amānah*,
*tabayyun*, *ṣidq*, *ʿadl*), serta menyusun rekomendasi kebijakan berbasis
bukti.

## 3. Capaian Pembelajaran

### 3.1 CPMK (5 butir, dipertahankan dari versi penuh)

| Kode | Rumusan |
|---|---|
| CPMK-1 | Menjelaskan konsep literasi data, big data, dan relevansinya bagi pendidikan Islam. |
| CPMK-2 | Mengidentifikasi sumber data pendidikan Islam yang sahih dan menilai kualitasnya. |
| CPMK-3 | Membersihkan, menganalisis, dan memvisualisasikan dataset pendidikan menggunakan tool dasar. |
| CPMK-4 | Menginterpretasi pola data dengan kesadaran *confounder* dan batasan inferensi. |
| CPMK-5 | Menyusun rekomendasi kebijakan / pembelajaran PAI berbasis data dengan landasan etika Islam. |

## 4. Rencana Pembelajaran (3 Pertemuan)

| Pert | Tema | Sub-CPMK | Aktivitas | Asesmen |
|---|---|---|---|---|
| **1** | **Pondasi**: Konsep big data, lanskap data pendidikan Islam (EMIS, Simpatika, BPS, AKMI), pengantar etika data Islam | CPMK 1, 2 | Mini-lecture, eksplorasi portal data, diskusi kasus | T01: Pemetaan Sumber Data (individu) |
| **2** | **Praktik**: Pembersihan data, statistika deskriptif, visualisasi & *data storytelling* | CPMK 3 | Praktikum dataset sintetis madrasah, *live coding* spreadsheet/Python | T02: Notebook Analisis (kelompok 2–3) |
| **3** | **Sintesis**: Korelasi vs kausalitas, etika mendalam (*amānah, tabayyun, ṣidq, ʿadl*), penyusunan *policy brief* | CPMK 4, 5 | Studi kasus *confounder*, simulasi panel kebijakan | T03: *Policy Brief* Mini (kelompok 2–3) |

### Sebaran waktu tiap pertemuan (saran 100 menit)

```
0–10    Pembuka, doa, apersepsi
10–35   Konsep / mini-lecture
35–80   Aktivitas inti (diskusi / praktikum / studi kasus)
80–95   Sintesis dosen + tanggapan
95–100  Penutup, refleksi, penugasan
```

## 5. Penilaian

| Komponen | Bobot | Keterangan |
|---|---|---|
| T01 — Pemetaan Sumber Data | 20% | Individu, ~3 hari setelah P1 |
| T02 — Notebook Analisis | 30% | Kelompok, dikumpulkan sebelum P3 |
| T03 — *Policy Brief* Mini | 40% | Kelompok, dipresentasikan akhir P3 |
| Partisipasi & refleksi | 10% | Aktif diskusi, jurnal belajar |

> **Catatan etika:** Plagiarisme dan fabrikasi data adalah pelanggaran berat
> yang bertentangan dengan prinsip *ṣidq*. Tugas yang terbukti melanggar
> dinilai nol.

## 6. Metode

- **Ceramah-diskusi singkat** untuk konsep
- **Praktikum berbasis dataset sintetis** (`dataset/emis-sintetis/`)
- **Project-Based Learning** untuk *capstone* berupa *policy brief* mini
- **Pendampingan asisten AI** dengan pendekatan Socratic
  (lihat `.kiro/steering/asisten-pai.md`)

## 7. Referensi (saran awal)

### Utama
- Provost, F., & Fawcett, T. *Data Science for Business* — bab pengantar.
- Wickham, H., & Grolemund, G. *R for Data Science* — bab visualisasi
  (versi daring tersedia).
- Kemenag RI. Dokumen tata kelola data EMIS *(versi terbaru)*.

### Perspektif Islam
- Kitab tafsir Q.S. al-Ḥujurāt: 6 (prinsip *tabayyun*) — pilihan tafsir
  diserahkan dosen pengampu.
- Buku/artikel etika informasi dalam Islam — mohon ditambahkan.

### Sumber data publik
- EMIS Kemenag — `emispendis.kemenag.go.id`
- Simpatika — `simpatika.kemenag.go.id`
- BPS — `bps.go.id`
- Pusat Asesmen Kemdikbudristek (AKMI/AKM)

## 8. Tata Tertib

1. Setiap klaim akademis wajib bersumber.
2. Penggunaan asisten AI **diperbolehkan dan didorong** sebagai mitra
   belajar; mahasiswa **wajib menyatakan penggunaannya** di laporan dan
   tetap bertanggung jawab atas isi tugas.
3. Data pribadi nyata (nama siswa, NISN, dsb.) **tidak boleh** dipakai
   tanpa izin dan anonimisasi. Untuk latihan gunakan dataset sintetis.

---

*Versi 0.2 — 3 pertemuan ringkas. Mohon disunting sebelum dipakai.*
