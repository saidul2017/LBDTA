# Modul Pertemuan 3 — Sintesis: Etika Data & Kebijakan Berbasis Bukti

> **Status:** Draft v0.2 — silakan disunting dosen pengampu.

## Sub-CPMK

Setelah pertemuan ini, mahasiswa diharapkan mampu:

1. **Membedakan korelasi dari kausalitas** dan **mengidentifikasi**
   *confounder* pada studi kasus pendidikan (Bloom C4).
2. **Menerapkan** kerangka **maqāṣid al-syarīʿah** dan empat prinsip
   etika data Islam (*amānah*, *tabayyun*, *ṣidq–ʿadl*) untuk menilai
   analisis data (Bloom C5).
3. **Menyusun** *policy brief* singkat berbasis bukti dengan
   rekomendasi pedagogis untuk pendidikan PAI (Bloom C6).

## Bahan Kajian

### 1. Korelasi vs kausalitas — perangkap klasik

Mahasiswa perlu memegang prinsip:

> **Korelasi tinggi tidak otomatis berarti satu menyebabkan yang lain.**

Tiga perangkap utama:

1. **Confounder (variabel ketiga)**
   *Contoh sintetis*: madrasah yang persentase guru bersertifikasinya
   tinggi cenderung punya nilai PAI lebih tinggi. Apakah sertifikasi
   **menyebabkan** nilai naik? Periksa dulu: bisakah dijelaskan oleh
   **akreditasi** (madrasah A → guru lebih sering disertifikasi
   *dan* nilai lebih tinggi)?
2. **Reverse causation (sebab-akibat terbalik)**
   Madrasah dengan dashboard data canggih punya nilai tinggi.
   Apakah dashboard menyebabkan nilai tinggi, atau madrasah baik
   memang lebih mampu membeli dashboard?
3. **Selection bias**
   Survei daring tentang literasi digital — siapa yang sempat dan
   mau mengisi? Yang paling melek digital. Hasil meleset.

### 2. Maqāṣid al-Syarīʿah dalam Etika Data Pendidikan

Empat prinsip operasional (*amānah, tabayyun, ṣidq, ʿadl*) yang
diperkenalkan di M01 adalah **operasionalisasi** dari kerangka yang
lebih luas: **maqāṣid al-syarīʿah** (tujuan-tujuan syariah) yang
diformulasikan ulama klasik (al-Syāṭibī dalam *al-Muwāfaqāt*) dan
diperluas ulama kontemporer (Ibn ʿĀshūr, al-Qaraḍāwī, Jasser Auda).

Lima ḍarūriyyāt (kebutuhan primer yang wajib dilindungi):

| Maqṣad | Maksud | Relevansi etika data pendidikan |
|---|---|---|
| **Ḥifẓ al-dīn** | Perlindungan agama | Data tidak boleh dipakai untuk merusak praktik beragama mahasiswa/guru/siswa. |
| **Ḥifẓ al-nafs** | Perlindungan jiwa | Data yang membahayakan keselamatan jiwa (mis. *publish* data lokasi siswa rentan) **dilarang**. |
| **Ḥifẓ al-ʿaql** | **Perlindungan akal/keilmuan** | Mahasiswa wajib menjaga **integritas keilmuan**: tidak fabrikasi data, tidak plagiarisme, tidak mengarang sumber. |
| **Ḥifẓ al-nasl** | Perlindungan keturunan/keluarga | Data anak-didik harus dilindungi; *mereka* yang akan berdampak jangka panjang. |
| **Ḥifẓ al-māl** | Perlindungan harta | Data tidak boleh dipakai untuk eksploitasi finansial (mis. bias kelas ekonomi dalam rekomendasi). |

#### Pemetaan empat prinsip → ḍarūriyyāt:

```
Amānah   →  Ḥifẓ al-māl + Ḥifẓ al-nafs + Ḥifẓ al-nasl
            (jaga titipan = jaga harta, jiwa, keturunan)

Tabayyun →  Ḥifẓ al-ʿaql + Ḥifẓ al-dīn
            (verifikasi = lindungi keilmuan & kebenaran)

Ṣidq     →  Ḥifẓ al-ʿaql
            (kejujuran = lindungi integritas keilmuan)

ʿAdl     →  semua ḍarūriyyāt
            (keadilan distributif lintas dimensi)
```

> **Catatan rujukan:** Penjelasan lebih dalam ada di *al-Muwāfaqāt*
> al-Syāṭibī, *Maqāṣid al-Syarīʿah al-Islāmiyyah* Ibn ʿĀshūr, atau
> karya kontemporer Jasser Auda *Maqasid al-Shariah as Philosophy of
> Islamic Law*. Asisten tidak akan mengarang kutipan.

### 3. Etika data Islam (operasional)

#### a. *Amānah* — data sebagai titipan
- Tidak menyebar data tanpa izin.
- Anonimisasi nyata, bukan sekadar menghapus nama.
- Akses terbatas (*least privilege*).

#### b. *Tabayyun* — verifikasi sebelum menyimpulkan
*Q.S. al-Ḥujurāt: 6* mengingatkan untuk memeriksa kebenaran berita.
Konsekuensi dalam analitik:
- Verifikasi sumber, tahun, definisi.
- Bedakan korelasi & kausalitas.
- Triangulasi — minimal dua sumber bila memungkinkan.

#### c. *Ṣidq* dan *ʿadl* — kejujuran & keadilan
- *Ṣidq*: laporkan apa adanya, termasuk hasil yang tidak signifikan
  atau bertentangan dengan harapan kita.
- *ʿadl*: cek apakah kesimpulan kita merugikan kelompok tertentu
  (mis. madrasah 3T, guru senior).

### 4. Ghībah dalam Analisis Data

> *Ghībah* adalah membicarakan kekurangan orang lain di belakangnya
> dengan cara yang tidak ia sukai (Q.S. al-Ḥujurāt: 12). Riwayat
> Bukhari-Muslim memperluas: *ghībah* tetap berdosa walau yang
> dikatakan **benar**.

Dalam konteks analisis data pendidikan, **ghībah dapat terjadi
secara sistematis** ketika kita:

- **Mempublikasikan ranking madrasah** dengan menonjolkan kelemahan
  satu institusi tanpa kemaslahatan kebijakan yang jelas.
- **Menyebut nama kelompok mahasiswa "kurang kompeten"** dalam laporan
  yang dapat diakses publik.
- **Membahas "guru sertifikasi yang tidak layak"** sebagai data
  agregat tanpa konteks fairness.

**Pertanyaan ujian etis** sebelum publikasi temuan:
1. Apakah ada **kemaslahatan kebijakan** yang jelas?
2. Apakah cara penyajian **menjaga martabat** kelompok yang dianalisis?
3. Apakah ada **alternatif penyajian** yang lebih konstruktif?

Jika ketiga pertanyaan ini tidak dijawab dengan baik, *publish*
temuan tersebut bisa **terjebak ghībah sistematis** — etika yang
harus dipertanggungjawabkan oleh calon guru PAI.

### 5. Empat dilema etis yang sering muncul

| Dilema | Pertanyaan reflektif | Maqṣad terdampak |
|---|---|---|
| **Anonimisasi semu** — nama dihapus tapi sekolah + kelas masih mengidentifikasi siswa | Apakah anonimisasi cukup? | Ḥifẓ al-nasl |
| **Cherry-picking** — hanya menyajikan grafik yang mendukung argumen | Apakah ini *ṣidq*? | Ḥifẓ al-ʿaql |
| **Bias label** — guru dengan kualifikasi tertentu dilabeli "kurang kompeten" | Apa *confounder*-nya? Apakah ini ghībah? | Ḥifẓ al-māl + ʿadl |
| **Skala ketidakadilan** — model prioritaskan madrasah perkotaan | Siapa yang dirugikan? | ʿAdl + Ḥifẓ al-nafs |

### 6. Anatomi *policy brief* yang baik

```
1. Ringkasan eksekutif    (1 paragraf — masalah + rekomendasi utama)
2. Latar belakang          (data agregat, konteks pendidikan PAI)
3. Temuan utama            (3–5 bullet, tiap temuan dirujuk ke data)
4. Diskusi & batasan       (confounder yang belum terjawab, risiko)
5. Rekomendasi             (3 butir, jelas siapa pelakunya)
6. Pertimbangan etis       (maqāṣid + amānah, tabayyun, ṣidq, ʿadl)
7. Daftar pustaka & data   (sitasi semua sumber)
```

Panjang ideal: **4–6 halaman** termasuk visualisasi.

## Aktivitas Kelas (100 menit)

| Menit | Aktivitas |
|---|---|
| 0–10 | Pembuka, *recap* P2 |
| 10–30 | Mini-lecture: korelasi vs kausalitas + maqāṣid + ghībah |
| 30–55 | **Studi kasus berkelompok** — temukan *confounder* di dataset sintetis, identifikasi maqāṣid yang dilanggar |
| 55–75 | **Peer feedback antar kelompok** — kelompok lain me-review draft brief 5 menit |
| 75–90 | **Workshop** menyusun kerangka *policy brief* final |
| 90–95 | Presentasi 1 kelompok + tanggapan |
| 95–100 | Penutup, briefing T03 (capstone) |

## Bahan Bacaan

*(dosen mohon mengisi)*
- Tafsir Q.S. al-Ḥujurāt: 6 (tabayyun) dan 12 (ghībah) dari kitab
  tafsir pilihan.
- Al-Syāṭibī, *al-Muwāfaqāt*, jilid 2 (bab maqāṣid).
- Auda, J. (2008). *Maqasid al-Shariah as Philosophy of Islamic Law:
  A Systems Approach*.
- Bab *causal inference for non-statisticians* dari buku rujukan utama.

## Penugasan

Lihat `tugas/T03-policy-brief-mini.md`.
