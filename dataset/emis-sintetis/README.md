# Dataset Sintetis Madrasah (EMIS-like)

## ⚠️ DISCLAIMER UTAMA — WAJIB DIBACA

> **Dataset di folder ini adalah SINTETIS** — dibangkitkan oleh
> skrip `generate.py` dengan PRNG terkendali. **BUKAN data EMIS
> Kemenag yang sebenarnya.** Hanya untuk keperluan pembelajaran.
>
> **Setiap pola yang Anda temukan di dataset ini adalah ARTIFAK
> KODE GENERATOR, bukan refleksi realitas pendidikan Islam
> Indonesia.** Rekomendasi kebijakan dari analisis dataset ini hanya
> valid sebagai **latihan akademik**.
>
> **Dilarang** menjadikan dataset ini sebagai dasar klaim faktual,
> publikasi penelitian (selain disclaimer eksplisit), atau
> pengambilan kebijakan riil.

## Mengapa pakai data sintetis?

Dataset sintetis dipilih karena:

1. **Privasi:** Data EMIS asli berisi NSM (Nomor Statistik Madrasah)
   dan data identifikasi sekolah/guru/siswa nyata. Memakainya untuk
   latihan kelas berisiko melanggar *amānah* dan UU PDP 27/2022.
2. **Kontrol pedagogis:** Pola yang ditanam sengaja (lihat DGP di
   bawah) memungkinkan dosen mengajarkan *confounder* secara
   eksplisit.
3. **Reproducibility:** Seed PRNG terkontrol — kelas mana pun di
   institusi mana pun akan dapat dataset yang sama untuk diskusi.

**Kapan boleh pakai data riil:**
- Setelah mahasiswa lulus literasi dasar (modul ini).
- Dengan persetujuan etika penelitian institusi.
- Dengan anonimisasi yang teruji (k-anonymity ≥ 5).

## Cara membangkitkan ulang

Dari folder ini:

```bash
python generate.py --n-madrasah 300 --seed 1446 --outdir .
```

Parameter:
- `--n-madrasah` : jumlah madrasah (default 300)
- `--seed`       : seed PRNG agar hasil **reproducible**
- `--outdir`     : folder keluaran

## Berkas yang dihasilkan

1. `madrasah_sintetis.csv` — 1 baris = 1 madrasah
2. `guru_pai_sintetis.csv` — 1 baris = 1 guru PAI
3. `siswa_pai_sintetis.csv` — 1 baris = agregat hasil belajar
   (madrasah × kelas × rumpun PAI)

## Kamus Data

### `madrasah_sintetis.csv`

| Kolom | Tipe | Skala | Keterangan |
|---|---|---|---|
| `id_madrasah` | string | nominal | Pengenal unik (mis. `MDR00012`) |
| `nama` | string | nominal | Nama sintetis |
| `jenjang` | kategori | nominal | `MI` / `MTs` / `MA` |
| `status` | kategori | nominal | `Negeri` / `Swasta` |
| `provinsi` | kategori | nominal | Provinsi (subset Indonesia) |
| `daerah` | kategori | ordinal | `Perkotaan` / `Pedesaan` / `3T` |
| `akreditasi` | kategori | ordinal | `A` / `B` / `C` / `Belum Terakreditasi` |
| `jumlah_siswa` | integer | rasio | Total siswa |
| `jumlah_guru` | integer | rasio | Total guru (semua mapel) |
| `rasio_siswa_guru` | float | rasio | `jumlah_siswa / jumlah_guru` |
| `persen_guru_sertifikasi` | float | rasio | 0-100 |
| `akses_internet_mbps` | float | rasio | Estimasi bandwidth |
| `perpustakaan` | 0/1 | nominal | 1 = ada perpustakaan |
| `lab_komputer` | 0/1 | nominal | 1 = ada lab komputer |
| `rata_nilai_pai` | float | interval | Skor 40-95 |

### `guru_pai_sintetis.csv`

| Kolom | Tipe | Skala | Keterangan |
|---|---|---|---|
| `id_guru` | string | nominal | Pengenal unik |
| `id_madrasah` | string | nominal | FK ke `madrasah_sintetis.csv` |
| `jenis_kelamin` | kategori | nominal | `L` / `P` |
| `usia` | integer | rasio | Tahun |
| `kualifikasi` | kategori | ordinal | S1 PAI / S1 Non-PAI / S2 PAI / S2 Non-PAI / D3/Lainnya |
| `pengalaman_tahun` | integer | rasio | Lama mengajar |
| `sertifikasi` | 0/1 | nominal | 1 = bersertifikat |
| `skor_literasi_digital` | float | interval | 0-100 |
| `jam_mengajar_per_minggu` | integer | rasio | Jam tatap muka |

### `siswa_pai_sintetis.csv`

| Kolom | Tipe | Skala | Keterangan |
|---|---|---|---|
| `id_madrasah` | string | nominal | FK |
| `kelas` | kategori | ordinal | 1-12 sesuai jenjang |
| `rumpun_pai` | kategori | nominal | Akidah-Akhlak / Fikih / SKI / Quran-Hadis / Bahasa Arab |
| `rata_nilai` | float | interval | 40-98 |
| `persen_tuntas` | float | rasio | 0-100 |
| `n_siswa` | integer | rasio | Banyaknya siswa |

---

## Data Generating Process (DGP) — DIBONGKAR EKSPLISIT

> Bagian ini sengaja **membongkar semua asumsi** yang ditanam ke
> dataset. Mahasiswa harus baca ini **setelah** mereka selesai
> menganalisis (di Pertemuan 3), agar bisa membandingkan temuan
> mereka dengan **kebenaran tanah** (*ground truth*) yang
> dikonstruksi.

### Variabel yang dibangkitkan dengan distribusi prior

```
jenjang ~ Categorical(MI=0.55, MTs=0.30, MA=0.15)
status ~ Categorical(Negeri=0.20, Swasta=0.80)
daerah ~ Categorical(Perkotaan=0.45, Pedesaan=0.45, 3T=0.10)
akreditasi ~ Categorical(A=0.25, B=0.40, C=0.25, Belum=0.10)
provinsi ~ Uniform(17 provinsi subset)
```

### Pola sebab-akibat yang DITANAM (bukan ditemukan)

Berikut formula deterministik yang generator pakai. **Mahasiswa
yang menjalankan analisis akan "menemukan" pola ini, tetapi pola
ini adalah keputusan desain, bukan realitas.**

#### Pola 1: Akreditasi → Nilai PAI

```
nilai_pai = 70.0
         + {A: +6, B: +2, C: -2, Belum: -6}[akreditasi]
         + (Negeri: +3, Swasta: 0)[status]
         + {Perkotaan: +2, Pedesaan: 0, 3T: -3}[daerah]
         + (persen_sertifikasi - 50) * 0.05
         + (internet_mbps - 10) * 0.05
         + Normal(0, 4)   # noise
         clamp(40, 95)
```

#### Pola 2: Akreditasi → Sertifikasi guru

```
p_sertifikasi = 0.45
              + (Negeri: +0.20, Swasta: 0)[status]
              + {A: +0.15, B: 0, C: -0.10, Belum: -0.20}[akreditasi]
              clamp(0.05, 0.95)
```

> **Implikasi pedagogis:** Korelasi antara *sertifikasi guru* dan
> *nilai PAI* yang akan ditemukan mahasiswa **sebagian besar adalah
> efek dari akreditasi sebagai confounder** (yang mempengaruhi
> keduanya). Inilah yang akan didiskusikan di M03.

#### Pola 3: Daerah → Akses internet

```
internet_mbps ~ Uniform per daerah:
    Perkotaan: U(10, 80)
    Pedesaan: U(2, 20)
    3T: U(0, 5)
```

#### Pola 4: Rumpun PAI → Nilai

```
nilai_rumpun = nilai_pai_madrasah
             + {Akidah-Akhlak: +1.0, Fikih: 0,
                SKI: -2.0, Quran-Hadis: +0.5,
                Bahasa Arab: -1.0}[rumpun]
             + Normal(0, 3)
             clamp(40, 98)
```

> **Implikasi pedagogis:** Perbedaan nilai antar rumpun PAI di
> dataset ini adalah **artifak** keputusan saya (penulis
> generator), **bukan refleksi realitas pedagogis** mata pelajaran
> tertentu lebih sulit. Mahasiswa yang menyimpulkan "SKI lebih
> sulit dari Akidah-Akhlak" dari dataset ini **mengambil ghībah
> sistematis** terhadap mata pelajaran/guru SKI tanpa dasar
> empiris yang valid.

#### Pola 5: Usia guru → Literasi digital

```
skor_literasi = 60.0
              - (usia - 35) * 0.4
              + {Perkotaan: +5, Pedesaan: 0, 3T: -5}[daerah]
              + {S2 PAI: +5, S2 Non-PAI: +5, S1 PAI: 0,
                 S1 Non-PAI: -2, D3/Lainnya: -5}[kualifikasi]
              + Normal(0, 8)
              clamp(0, 100)
```

### Apa yang TIDAK dimodelkan?

Banyak realitas pendidikan Islam yang **tidak ada di dataset ini**:

- Latar belakang sosioekonomi siswa
- Karakter & dinamika kelas
- Kepemimpinan kepala madrasah
- Kultur sekolah (mis. nuansa pesantren vs umum)
- Faktor pedagogis kontekstual
- Variabel emosi-spiritual siswa

**Implikasi untuk policy brief mahasiswa:** Setiap rekomendasi
kebijakan yang Anda buat dari dataset ini **terbatas pada variabel
yang ada di sini**. Variabel yang tidak terobservasi (seperti yang
disebut di atas) berperan sebagai potential *unobserved confounders*
— Anda harus mengakuinya secara eksplisit di Bagian 4 (Diskusi &
Batasan) brief.

---

## Pengingat Etis

Mahasiswa yang menggunakan dataset ini wajib:

1. **Mencantumkan disclaimer "data sintetis"** di setiap dokumen
   yang Anda buat (notebook, brief, presentasi).
2. **Tidak mempublikasikan** turunan dataset ini di luar konteks
   kelas tanpa disclaimer.
3. **Tidak menyimpulkan** realitas Indonesia dari pola yang
   ditemukan; pola tersebut adalah artifak generator.
4. **Tidak memakai dataset ini** untuk bias analisis yang merugikan
   kelompok tertentu (mata pelajaran, jenjang, daerah, gender,
   kualifikasi guru).

Pelanggaran terhadap aturan ini = pelanggaran *ṣidq* dan
*ḥifẓ al-ʿaql* (perlindungan integritas keilmuan).
