# Modul Pertemuan 1 — Pondasi Literasi Data Pendidikan Islam

> **Status:** Draft v0.2 — silakan disunting dosen pengampu.

## Sub-CPMK

Setelah pertemuan ini, mahasiswa diharapkan mampu:

1. **Menjelaskan** konsep **literasi data** dan **big data** (5V:
   *Volume, Velocity, Variety, Veracity, Value*) dalam konteks
   pendidikan Islam (Bloom C2).
2. **Memetakan sumber data pendidikan Islam** yang resmi dan
   **menilai** kualitasnya secara awal (Bloom C4).
3. **Menyebutkan** tiga prinsip pengantar **etika data Islam**:
   *amānah*, *tabayyun*, *ṣidq–ʿadl* (Bloom C1, dasar untuk M03).
4. **Mengkritisi** asisten AI yang akan mereka pakai sebagai mitra
   belajar — termasuk halusinasi, bias, dan batasan epistemologis
   (Bloom C5).

## Bahan Kajian

### 1. Apa itu literasi data?

Literasi data adalah kemampuan **membaca, memahami, mengkritisi,
mengkomunikasikan, dan bertindak** atas dasar data. Bagi calon guru
PAI, literasi data berarti tidak hanya bisa **menghitung**, tetapi
mampu:

- bertanya: *"Data ini dari mana? Siapa yang mengumpulkannya? Untuk apa?"*
- mengenali: *kapan data bisa dipercaya, kapan harus tabayyun*
- memutuskan: *kapan data cukup untuk bertindak, kapan butuh bukti tambahan*

### 2. Big data: 5V

| V | Maksud | Contoh di pendidikan Islam |
|---|---|---|
| **Volume** | Banyak baris/byte | EMIS jutaan record madrasah & siswa |
| **Velocity** | Mengalir cepat | Absensi harian via Simpatika |
| **Variety** | Bermacam bentuk | Tabel + teks khotbah + audio kajian |
| **Veracity** | Kebenaran/kredibilitas | Apakah data input madrasah valid? |
| **Value** | Nilai guna | Apakah analisis ini membantu siswa? |

### 3. Lanskap data pendidikan Islam

| Sumber | Pengelola | Yang bisa diambil | Catatan |
|---|---|---|---|
| **EMIS** | Kemenag | Data madrasah, siswa, guru, sarpras | Akses terbatas; statistik agregat publik |
| **Simpatika** | Kemenag | Data guru madrasah & sertifikasi | Login terbatas |
| **BPS** | Pemerintah | Statistik pendidikan agregat | Akses publik |
| **AKMI / AKM** | Kemenag/Kemdikbud | Asesmen literasi-numerasi siswa madrasah | Laporan agregat |
| **Riset/jurnal** | Akademisi | Studi kasus, dataset penelitian | Wajib sitasi |

> **Verifikasi (tabayyun):** Selalu cek tahun rilis, definisi variabel,
> dan metode pengumpulan sebelum mengutip.

### 4. Pengantar etika data Islam

Tiga prinsip yang akan diperdalam di Pertemuan 3:

- **Amānah** — data adalah titipan; jaga kerahasiaan & integritas.
- **Tabayyun** (Q.S. al-Ḥujurāt: 6) — verifikasi sumber sebelum
  menyimpulkan atau menyebarkan.
- **Ṣidq & ʿadl** — kejujuran dalam pelaporan, keadilan dalam dampak
  kebijakan.

> Penjelasan dalil & detail praktis dibahas tuntas di **Modul 3**,
> lengkap dengan kerangka *maqāṣid al-syarīʿah*.

### 5. Kritik Epistemologis terhadap Asisten AI

> Mata kuliah ini menyediakan **chatbot AI** sebagai mitra belajar
> mahasiswa. Sebelum kalian pakai, mari kita kritis pada AI itu
> sendiri — sesuai prinsip *tabayyun*.

#### a. AI bisa **mengarang** (halusinasi)

Large Language Model (LLM) seperti Gemini atau Llama bisa
menghasilkan jawaban yang **terdengar meyakinkan tapi salah** —
termasuk:

- Mengarang **ayat Al-Qur'an atau hadis** yang tidak ada.
- Mengarang **referensi buku/jurnal** dengan judul fiktif.
- Mengarang **statistik** yang tidak ada di sumber asli.
- Mengaitkan tafsir kepada ulama tertentu padahal tidak benar.

**Risiko di mata kuliah ini:** Anda mengutip "fatwa" atau "tafsir"
yang sebenarnya **tidak pernah ada**. Ini pelanggaran serius:
*ṣidq* (kejujuran) dan *amānah* terhadap khazanah keilmuan Islam.

**Cara mitigasi:**
1. **Cek silang berkas:** Asisten ini hanya boleh merujuk berkas di
   repo `LBDTA/`. Jika menyebut sumber lain, **tidak otomatis
   valid**.
2. **Cek silang kitab:** Untuk klaim agama (tafsir, hadis, fatwa),
   **selalu konfirmasi ke kitab cetak atau database resmi**
   (mis. islamweb.net untuk hadis, Quran.com untuk ayat).
3. **Cek silang dosen:** Jika ragu, tanyakan ke dosen pengampu
   sebelum mengutip di brief.

#### b. AI mengandung **bias training data**

Model seperti Gemini dilatih pada data berbahasa Inggris dominan dan
sumber Barat. Konsekuensi:

- Perspektif **non-Barat** kurang terwakili (termasuk pemikiran Islam).
- Bias terhadap pendekatan **kuantitatif > kualitatif**.
- Bias terhadap **kebijakan neoliberal** (efisiensi > pemerataan).

**Mitigasi:** Saat asisten memberi rekomendasi, tanyakan kepada diri
sendiri: *"Apakah pendekatan ini menghormati konteks pendidikan
Islam, atau hanya menggampangkan dengan ukuran efisiensi global?"*

#### c. AI tidak **memahami konteks etis** secara mendalam

LLM dapat menyebut prinsip etika (amānah, tabayyun) tetapi tidak
benar-benar **memahami** maknanya seperti seorang ulama. AI mensimulasi
pemahaman, bukan memilikinya.

**Mitigasi:** Etika tetap pertanggungjawaban manusia. Mahasiswa,
bukan AI, yang menanggung konsekuensi moral atas rekomendasi
kebijakan.

#### d. **Privasi prompt** Anda

Saat Anda mengirim pertanyaan ke chatbot, pertanyaan itu **dikirim
ke server Google/Anthropic/Groq**. Vendor bisa menyimpannya sebagai
training data (kecuali dosen Anda set opsi opt-out).

**Mitigasi:** Jangan kirim **data pribadi nyata** (nama siswa
sungguhan, NIM mahasiswa lain, isi rapat madrasah, dll.) ke
chatbot. Pakai dataset sintetis untuk latihan.

#### e. **Cognitive offloading** — risiko jangka panjang

Studi pendidikan menunjukkan: terlalu mengandalkan AI bisa
**menurunkan** kemampuan berpikir kritis Anda sendiri. AI baik
dipakai sebagai **mitra dialog**, bukan **pengganti berpikir**.

**Mitigasi:** Sebelum bertanya ke AI, **tulis dulu jawaban Anda
sendiri**. Setelah AI menjawab, bandingkan. AI sebagai *cermin*,
bukan *kompas*.

#### Uji Verifikasi 4 Langkah (sebelum pakai jawaban AI)

```
1. CEK SUMBER : Apakah AI menyebut berkas spesifik?
                Buka berkas itu sendiri.
2. CEK FAKTA  : Cocokkan klaim numerik/historis dengan
                sumber primer.
3. CEK BIAS   : Apakah ada perspektif yang absen?
                (mis. pendidikan 3T, perempuan, marjinal)
4. CEK ETIS   : Apakah rekomendasi merugikan kelompok
                tertentu? Konsultasi ke dosen jika ragu.
```

## Aktivitas Kelas (100 menit)

| Menit | Aktivitas |
|---|---|
| 0–10 | Pembuka: ayat & kontrak belajar |
| 10–30 | Mini-lecture: literasi data, 5V, lanskap sumber |
| 30–50 | **Demo halusinasi LLM**: dosen tunjukkan AI mengarang ayat/hadis fiktif. Diskusi: bagaimana mendeteksinya? |
| 50–80 | **Eksplorasi berkelompok**: buka 1 portal data publik, jawab 5 pertanyaan tabayyun (siapa, kapan, definisi, batas, lisensi) |
| 80–90 | Presentasi cepat 2 kelompok |
| 90–100 | Sintesis dosen, briefing T01, penutup |

## Bahan Bacaan

*(dosen mohon mengisi)*
- Bab pengantar literasi data dari buku rujukan utama.
- Halaman pengantar portal EMIS/Simpatika.
- Bender, E. M., et al. (2021). *On the Dangers of Stochastic Parrots*
  — kritik akademik terhadap LLM.

## Penugasan

Lihat `tugas/T01-pemetaan-sumber-data.md`.
