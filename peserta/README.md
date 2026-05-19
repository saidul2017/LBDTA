# Folder Peserta UAS Literasi Big Data PAI

Berisi roster mahasiswa peserta UAS, pembagian kelompok, dan generator
otomatis untuk regenerate jika perlu.

## Berkas

| Berkas | Sumber | Keterangan |
|---|---|---|
| `peserta.csv` | input dosen | 40 mahasiswa: `no, nim, nama, gender` |
| `buat_kelompok.py` | skrip | generator pembagian kelompok |
| `peserta_dengan_kelompok.csv` | output skrip | csv lengkap dengan kelompok & topik |
| `kelompok-uas.md` | output skrip | tabel pembagian (untuk diumumkan) |
| `roster.json` | output skrip | format yang dikonsumsi aplikasi chatbot |

## ⚠️ Disclaimer kolom `gender`

Kolom `gender` (`L`/`P`) dalam `peserta.csv` adalah **TEBAKAN HEURISTIK
asisten AI** berdasarkan pola nama Indonesia/Arab umum. **Bukan data
otoritatif.**

Ada kemungkinan tebakan keliru, terutama untuk:
- Nama unisex (mis. "Aulia", "Ardiya")
- Nama yang tidak umum
- Nama yang mengandung kombinasi tidak biasa

**Tindakan dosen:**

1. Verifikasi langsung ke administrasi prodi atau ke mahasiswa.
2. Edit `peserta.csv` jika ada yang salah.
3. Jalankan ulang: `python peserta/buat_kelompok.py`.

Kolom ini disediakan agar dosen punya **opsi** pembagian seimbang
gender (`--stratify-gender`), bukan untuk diskriminasi atau pelabelan.

## Cara regenerate pembagian

```bash
# Pembagian default (acak murni, seed reproducible)
python peserta/buat_kelompok.py

# Dengan seed lain
python peserta/buat_kelompok.py --seed 7

# Stratified by gender (sebar L/P merata antar kelompok)
python peserta/buat_kelompok.py --stratify-gender
```

> **Catatan:** mengubah seed atau opsi stratifikasi akan **mengubah
> komposisi kelompok**. Kalau Bapak/Ibu sudah mengumumkan pembagian ke
> mahasiswa, **JANGAN** regenerate kecuali ada alasan kuat.

## Privasi

`peserta.csv` berisi NIM dan nama mahasiswa nyata. Pertimbangkan:

- Jangan publikasikan ke repo publik tanpa izin mahasiswa.
- Untuk repo publik, ganti nama menjadi inisial atau nomor anonim.
- File `roster.json` ikut prinsip yang sama.
