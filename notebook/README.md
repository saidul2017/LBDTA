# Notebook Praktikum

Folder ini berisi notebook referensi & ruang kerja mahasiswa.

## Berkas

- `01-praktikum-analisis-madrasah.py` — **notebook referensi** untuk
  Pertemuan 2 / Tugas T02. Menjalankan pipeline lengkap: muat → bersihkan
  → deskriptif → visualisasi → refleksi *confounder*.

## Cara menjalankan referensi

### Opsi A — sebagai skrip Python biasa

```bash
cd notebook
pip install pandas matplotlib numpy
python 01-praktikum-analisis-madrasah.py
```

Hasil: 3 berkas PNG di folder `notebook/outputs/` dan ringkasan
tabel di terminal.

### Opsi B — buka sebagai notebook Jupyter

File `.py` di atas memakai marker sel `# %%`. Bisa dibuka langsung
sebagai notebook di:

- **VS Code** + ekstensi *Jupyter* → klik "Run Cell" di tiap sel
- **Spyder / PyCharm Scientific Mode** → otomatis dikenali sel demi sel
- **Jupyter Lab** → konversi dulu:
  ```bash
  pip install jupytext
  jupytext --to ipynb 01-praktikum-analisis-madrasah.py
  jupyter lab 01-praktikum-analisis-madrasah.ipynb
  ```

## Aturan untuk mahasiswa

1. **Jangan langsung mengubah** notebook referensi. Buat salinan dengan
   nama `Kelompok-XX-analisis.{py,ipynb}` lalu kerjakan di sana.
2. Sertakan **disclaimer dataset sintetis** di sel pertama notebook
   Anda.
3. Notebook harus **dapat dijalankan ulang dari awal** (kernel restart
   → run all). Jika tidak, akan dikurangi nilai *reproducibility*.
4. Sertakan minimal: **1 langkah pembersihan**, **2 ringkasan
   deskriptif**, **3 visualisasi**, dan **1 refleksi confounder** —
   sesuai instruksi di `tugas/T02-analisis-data-sintetis.md`.

## Output yang dihasilkan referensi

Setelah dijalankan, akan muncul:

```
outputs/
├── 01-histogram-nilai.png      # sebaran rata-rata nilai PAI
├── 02-boxplot-akreditasi.png   # nilai PAI per akreditasi
└── 03-scatter-sertifikasi.png  # sertifikasi vs nilai (korelasi)
```

Plus tabel di terminal — termasuk korelasi sertifikasi-nilai **dipecah
per akreditasi**, untuk memantik diskusi *confounder* di Pertemuan 3.
