# Dataset Sintetis Madrasah (EMIS-like)

> **DISCLAIMER PENTING**
> Dataset di folder ini **SINTETIS** — dibangkitkan oleh skrip `generate.py`
> dengan PRNG terkendali. **BUKAN** data EMIS Kemenag yang sebenarnya.
> Hanya untuk keperluan pembelajaran. Dilarang dipakai sebagai dasar klaim
> faktual, publikasi, atau pengambilan kebijakan riil.

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
3. `siswa_pai_sintetis.csv` — 1 baris = agregat hasil belajar (madrasah × kelas × rumpun PAI)

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
| `persen_guru_sertifikasi` | float | rasio | 0–100 |
| `akses_internet_mbps` | float | rasio | Estimasi bandwidth |
| `perpustakaan` | 0/1 | nominal | 1 = ada perpustakaan |
| `lab_komputer` | 0/1 | nominal | 1 = ada lab komputer |
| `rata_nilai_pai` | float | interval | Skor 40–95 |

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
| `skor_literasi_digital` | float | interval | 0–100 |
| `jam_mengajar_per_minggu` | integer | rasio | Jam tatap muka |

### `siswa_pai_sintetis.csv`

| Kolom | Tipe | Skala | Keterangan |
|---|---|---|---|
| `id_madrasah` | string | nominal | FK |
| `kelas` | kategori | ordinal | 1–12 sesuai jenjang |
| `rumpun_pai` | kategori | nominal | Akidah-Akhlak / Fikih / SKI / Quran-Hadis / Bahasa Arab |
| `rata_nilai` | float | interval | 40–98 |
| `persen_tuntas` | float | rasio | 0–100 |
| `n_siswa` | integer | rasio | Banyaknya siswa |

## Pola yang sengaja ditanam (untuk latihan analitik)

Skrip menanam beberapa pola sebab–akibat dan **confounder** agar mahasiswa
berlatih membedakan **korelasi vs kausalitas**:

1. Akreditasi A → cenderung nilai PAI lebih tinggi (~+6 poin).
2. Status Negeri → persen sertifikasi guru lebih tinggi.
3. Daerah 3T → akses internet rendah & nilai PAI sedikit lebih rendah.
4. Sertifikasi guru berkorelasi positif dengan nilai PAI **karena** ada
   variabel ketiga (akreditasi & status). Mahasiswa diharapkan menemukan
   *confounder* ini, bukan menyimpulkan bahwa sertifikasi → langsung
   meningkatkan nilai.
5. Literasi digital guru berkorelasi negatif dengan usia.
6. Rumpun **SKI** rata-rata 2 poin lebih rendah dari rata-rata madrasah,
   **Akidah-Akhlak** sedikit lebih tinggi.

> **Penting untuk pembelajaran:** Pola di atas adalah *artificial pattern*.
> Jangan menyamakannya dengan realitas pendidikan Islam Indonesia.
