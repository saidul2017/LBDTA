# Modul Pertemuan 3 — Sintesis: Etika Data & Kebijakan Berbasis Bukti

> **Status:** Draft v0.1 — silakan disunting dosen pengampu.

## Sub-CPMK

Setelah pertemuan ini, mahasiswa diharapkan mampu:

1. Membedakan **korelasi** dari **kausalitas** dan mengenali *confounder*
   pada studi kasus pendidikan.
2. Menerapkan tiga prinsip etika data Islam (*amānah*, *tabayyun*,
   *ṣidq–ʿadl*) untuk menilai analisis data.
3. Menyusun **policy brief** singkat berbasis bukti dengan rekomendasi
   pedagogis untuk pendidikan PAI.

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

### 2. Etika data Islam (mendalam)

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

> **Catatan rujukan:** Untuk dalil dan tafsir lengkap, mohon merujuk
> kitab tafsir mu'tabar pilihan dosen pengampu. Asisten tidak akan
> mengarang sumber.

### 3. Empat dilema etis yang sering muncul

| Dilema | Pertanyaan reflektif |
|---|---|
| **Anonimisasi semu** — nama dihapus tapi sekolah + kelas masih mengidentifikasi siswa | Apakah anonimisasi cukup? |
| **Cherry-picking** — hanya menyajikan grafik yang mendukung argumen | Apakah ini *ṣidq*? |
| **Bias label** — guru dengan kualifikasi tertentu dilabeli "kurang kompeten" | Apa *confounder*-nya? |
| **Skala ketidakadilan** — model prioritaskan madrasah perkotaan | Siapa yang dirugikan? |

### 4. Anatomi *policy brief* yang baik

```
1. Ringkasan eksekutif    (1 paragraf — masalah + rekomendasi utama)
2. Latar belakang          (data agregat, konteks pendidikan PAI)
3. Temuan utama            (3–5 bullet, tiap temuan dirujuk ke data)
4. Diskusi & batasan       (confounder yang belum terjawab, risiko)
5. Rekomendasi             (3 butir, jelas siapa pelakunya)
6. Pertimbangan etis       (amānah, tabayyun, ṣidq, ʿadl)
7. Daftar pustaka & data   (sitasi semua sumber)
```

Panjang ideal: **4–6 halaman** termasuk visualisasi.

## Aktivitas Kelas (100 menit)

| Menit | Aktivitas |
|---|---|
| 0–10 | Pembuka, *recap* P2 |
| 10–30 | Mini-lecture: korelasi vs kausalitas + etika mendalam |
| 30–60 | **Studi kasus berkelompok** — temukan *confounder* di dataset sintetis |
| 60–85 | **Workshop** menyusun kerangka *policy brief* |
| 85–95 | Presentasi 2 kelompok + tanggapan |
| 95–100 | Penutup, briefing T03 (capstone) |

## Bahan Bacaan

*(dosen mohon mengisi)*
- Tafsir Q.S. al-Ḥujurāt: 6 dari kitab tafsir pilihan.
- Bab *causal inference for non-statisticians* dari buku rujukan utama.

## Penugasan

Lihat `tugas/T03-policy-brief-mini.md`.
