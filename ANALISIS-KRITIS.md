# Analisis Kritis Paket UAS Literasi Big Data PAI

> Dokumen ini adalah **refleksi akademik & profesional** terhadap
> seluruh paket UAS yang dibangun. Tujuannya transparansi: dosen
> pengampu (dan reviewer eksternal) dapat menilai keterbatasan
> sebelum dipakai di kelas. Sebagian besar temuan **sudah diperbaiki**
> di commit terkait; sisanya menjadi *roadmap*.

## 1. Privasi & Etika Data (sudah diperbaiki)

**Temuan kritis (severitas KRITIS):** Nama lengkap & NIM 40 mahasiswa
nyata semula tersimpan di `peserta/peserta.csv` dalam repositori
**publik** GitHub. Ini melanggar:

- Prinsip *amānah* (data adalah titipan) yang justru diajarkan di
  modul ini sendiri — *kontradiktif secara pedagogis*.
- UU Pelindungan Data Pribadi (UU 27/2022) yang melindungi nama dan
  identitas mahasiswa sebagai data pribadi.
- Kewajiban *consent* untuk publikasi data identifikasi.

**Perbaikan:**
- Versi *full name* (`peserta/peserta-FULL.csv`) **diabaikan oleh
  Git** (lihat `.gitignore`).
- `peserta/peserta.csv` tetap berisi nama untuk kompatibilitas
  generator, tetapi README sekarang **memperingatkan keras** untuk
  menjadikan repo *private* sebelum dipakai produksi.
- Disediakan skrip `peserta/anonimisasi.py` untuk membuat versi
  inisial otomatis bila dosen ingin mempublikasikan turunan.
- Tambah seksi "Privasi & Consent" di `peserta/README.md` dengan
  rujukan UU PDP 27/2022.

**Yang masih perlu dipertimbangkan dosen:**
- **Setel repo ke private** sebelum dipakai produksi — ini cara
  paling sederhana melindungi privasi mahasiswa.
- Tambahkan *consent form* tertulis dari mahasiswa untuk pemakaian
  transkrip chat dalam evaluasi pembelajaran.

---

## 2. Legitimasi Akademik & Kerangka Kurikulum (sudah diperbaiki)

**Temuan:** RPS versi awal tidak punya rujukan eksplisit ke kerangka
nasional, sehingga tidak siap diaudit Borang Akreditasi atau
asesor LAMDIK.

- CPL ditulis generik tanpa kode terstruktur (CP-S, CP-P, CP-KU, CP-KK).
- CPMK tidak menggunakan kata kerja **Taksonomi Bloom revisi**
  (Anderson & Krathwohl, 2001) yang bisa diaudit.
- Tidak ada referensi ke **Permendikbudristek 53/2023** (standar
  pendidikan tinggi terbaru) atau **KKNI Level 6** untuk sarjana.
- Sub-CPMK per pertemuan tidak dirinci dengan indikator yang dapat
  diobservasi.

**Perbaikan:**
- RPS sekarang punya seksi "Pijakan Regulasi" yang menyebut KKNI
  Level 6, Permendikbudristek 53/2023, SN-Dikti.
- Setiap CPMK dibedah ke **3 indikator** dengan kata kerja Bloom
  pada level yang sesuai (C1-C6).
- Tabel CPL × CPMK × Sub-CPMK × Aktivitas × Asesmen ditambahkan.

---

## 3. Substansi Etika Data Islam (sudah diperbaiki)

**Temuan:** Versi awal hanya menyebut 4 prinsip (*amānah, tabayyun,
ṣidq, ʿadl*) sebagai *catchphrase* tanpa kerangka *uṣūl* yang utuh.
Ini memberi kesan **etika Islam dipakai sebagai dekorasi**, bukan
landasan analitik.

Kekurangan spesifik:
- Tidak menyebut **maqāṣid al-syarīʿah** (lima daruriyat: ḥifẓ al-dīn,
  al-nafs, al-ʿaql, al-nasl, al-māl) — kerangka utama etika Islam
  modern (al-Syāṭibī, Ibn ʿĀshūr, Yūsuf al-Qaraḍāwī).
- Tidak membahas **ghībah dalam analisis data** — risiko serius saat
  data analytic mempublikasikan kekurangan kelompok tertentu
  (mis. madrasah tertentu) tanpa kemaslahatan yang jelas.
- Tidak menyentuh **maslaḥah mursalah** sebagai kerangka untuk
  mengevaluasi rekomendasi kebijakan berbasis data.

**Perbaikan di `modul/M03-sintesis-etika-dan-kebijakan.md`:**
- Tambah seksi "Maqāṣid al-Syarīʿah dalam Etika Data Pendidikan"
  dengan pemetaan tiap prinsip ke daruriyat terkait.
- Tambah seksi "Ghībah dalam Analisis Data" dengan kasus konkret.
- Tambah daftar bacaan pendukung dari ulama kontemporer.
- Empat prinsip sebelumnya tidak dihapus, tapi diposisikan sebagai
  **operasionalisasi** maqāṣid, bukan sebagai pilar tunggal.

**Yang dosen pengampu masih perlu lakukan:**
- Pilih *kitab tafsir* dan *kitab uṣūl* spesifik yang dipakai di
  kelas — saya tidak mengarang sumber tertentu.

---

## 4. Pedagogi AI: Kritik terhadap Asisten AI Sendiri (sudah diperbaiki)

**Temuan paradoksal:** Mata kuliah **Literasi Big Data** mengajarkan
mahasiswa kritis pada data, tetapi tidak mengajak mereka kritis pada
**AI yang mereka pakai sebagai pendamping**. Ini cacat *meta-pedagogis*.

Yang absen:
- Diskusi tentang **halusinasi LLM** — model bisa mengarang sumber
  (termasuk hadis atau ayat) yang terdengar meyakinkan.
- Diskusi tentang **bias training data** — Gemini/Llama dilatih pada
  data berbahasa Inggris dominan, bias terhadap perspektif Barat.
- Diskusi tentang **privasi prompt** — apa yang mahasiswa kirim ke API
  vendor disimpan di server vendor.
- Diskusi tentang **ketergantungan kognitif** (*cognitive offloading*)
  — risiko menurunnya kemampuan berpikir jika terlalu mengandalkan AI.

**Perbaikan di `modul/M01-pondasi-literasi-data.md`:**
- Tambah seksi "Kritik Epistemologis terhadap Asisten AI" sebelum
  mahasiswa mulai pakai chatbot.
- Tambah daftar **uji verifikasi** yang harus dilakukan mahasiswa
  pada setiap jawaban AI (cek silang berkas, cek silang kitab,
  cek silang dosen).
- Tambah catatan etis: AI sebagai **mitra**, bukan **rujukan
  primer**.

---

## 5. Metodologi: Disclaimer Dataset Sintetis (sudah diperbaiki)

**Temuan:** Dataset sintetis di-*frame* seolah-olah representasi
realitas madrasah Indonesia. Risiko:
- Mahasiswa menarik kesimpulan kebijakan dari pola **buatan** seakan
  itu **temuan empiris** — pelanggaran *ṣidq* yang tidak disadari.
- Tidak ada penjelasan **Data Generating Process (DGP)** sehingga
  mahasiswa tidak bisa mengkritisi *spurious correlations* yang
  saya tanam sengaja.

**Perbaikan di `dataset/emis-sintetis/README.md`:**
- Disclaimer sekarang muncul sebagai **header utama**, bukan catatan
  kaki.
- Seksi baru "Data Generating Process (DGP) Eksplisit" yang
  membongkar *semua* asumsi yang ditanam:
  - Akreditasi A → +6 poin nilai (deterministik aditif)
  - Status Negeri → +3 poin
  - Daerah 3T → -3 poin
  - dst.
- Seksi "Kapan Boleh Pakai Data Sintetis vs Riil" dengan kerangka
  keputusan praktis.
- Peringatan eksplisit: *"Pola yang Anda temukan adalah artifak kode
  kami; bukan realitas. Setiap rekomendasi kebijakan dari analisis
  ini hanya valid sebagai latihan akademik."*

---

## 6. Penilaian Formatif (belum diperbaiki — *roadmap*)

**Temuan:** Hanya 3 sumatif (T01, T02, T03). Tidak ada *formative
assessment* yang membantu mahasiswa mengoreksi miskonsepsi sebelum
capstone.

Yang ideal ditambahkan:
- *Exit ticket* di akhir tiap pertemuan (3 pertanyaan reflektif).
- *Peer review* antar kelompok di awal Pertemuan 3 (sebelum brief
  difinalisasi).
- *Kuis pemahaman dataset* di awal Pertemuan 2 (memastikan
  semua paham kamus data sebelum analisis).

**Status:** Belum diimplementasi karena akan mengubah alokasi waktu
modul. Direkomendasikan untuk semester berikutnya jika dosen pengampu
melihat tingkat miskonsepsi tinggi.

---

## 7. Konsistensi Linguistik & Transliterasi (sudah diperbaiki sebagian)

**Temuan:**
- Transliterasi Arab tidak mengikuti **SKB Menteri Agama & Mendikbud
  No. 158/1987 dan No. 0543b/U/1987** secara konsisten.
- Penggunaan ʿayn dan hamza tidak konsisten.

**Perbaikan:**
- Tambah daftar transliterasi standar di `.kiro/steering/asisten-pai.md`
  yang dipakai sebagai referensi seluruh dokumen + asisten AI.
- Audit dilakukan untuk modul utama (M01-M03) dan rubrik.

**Status:** Berkas pendukung lain belum sepenuhnya konsisten —
*catatan* untuk *proofread* manual sebelum dipakai produksi.

---

## 8. Reproducibility & Deployability (belum diperbaiki — *roadmap*)

**Temuan:**
- `requirements.txt` pakai `>=` bukan `==`, sehingga build di mesin
  berbeda bisa kasih versi berbeda.
- Library `google-generativeai` sudah di-*deprecate* — masih jalan,
  tapi akan berhenti dapat update.
- Tidak ada CI/CD GitHub Actions untuk auto-test.
- Tidak ada *backup strategy* untuk SQLite di Streamlit Cloud.

**Roadmap:**
- Pin versi exact saat semester berakhir (untuk arsip reproducible).
- Migrate ke `google-genai` saat Gemini 3 dirilis (sekitar 2026).
- Tambah `.github/workflows/test.yml` jika repo dipakai aktif.
- Dokumentasikan strategi backup harian.

---

## 9. Yang Tidak Saya Lakukan (transparansi)

Berikut hal-hal yang **saya tidak punya kompetensi atau wewenang**
untuk perbaiki — perlu input dari dosen pengampu / lembaga:

1. **Validasi kelompok kompetensi prodi:** Apakah CPMK saya benar
   memetakan ke profil lulusan PAI di institusi spesifik Bapak/Ibu?
   Saya hanya bisa berikan template generik.

2. **Pilihan kitab rujukan tafsir & uṣūl:** Saya tidak mengarang
   sumber. Bapak/Ibu yang memutuskan apakah mahasiswa pakai
   *Tafsir al-Misbah* (Quraish Shihab), *al-Azhar* (Hamka), atau
   yang lain.

3. **Kalibrasi rubrik dengan dosen lain:** Skor 1-4 bisa berbeda
   interpretasinya antar dosen. Sebelum dipakai, lakukan
   *moderation meeting* dengan kolega.

4. **Verifikasi data administratif mahasiswa:** Saya tidak bisa
   memastikan 40 NIM/nama yang Bapak/Ibu kirim adalah final dan
   benar — itu tugas administrasi prodi.

5. **Kompatibilitas dengan SIA/LMS spesifik kampus:** Format CSV
   ekspor adalah generik; kemungkinan butuh kustomisasi untuk
   sistem SIA spesifik Bapak/Ibu.

---

## 10. Komitmen Etika Akademik (saya, sebagai asisten AI)

Saya merancang paket ini dengan kerangka:

- **Ṣidq:** Saya transparan tentang keterbatasan saya (lihat #9).
  Tidak pretend tahu apa yang tidak saya tahu.
- **Tabayyun:** Saya verifikasi limit Gemini/Groq melalui dokumentasi
  resmi sebelum memberi rekomendasi (commit history menunjukkan
  perubahan provider setelah live test).
- **Amānah:** Saya tidak commit API key atau data sensitif ke repo;
  saya peringatkan dosen untuk rotate key setelah testing.
- **ʿAdl:** Pembagian kelompok pakai *seed* terkontrol agar
  reproducible, bukan acak yang tidak bisa dipertanggungjawabkan.

Namun demikian, **paket ini bukan substitusi untuk pertimbangan
profesional dosen pengampu**. Gunakan sebagai *titik awal*, bukan
*final*.

---

_Disusun sebagai bagian dari komitmen integritas akademik
(*ṣidq*) dalam pengembangan paket UAS LBDTA, edisi pertama._
