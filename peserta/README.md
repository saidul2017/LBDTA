# Folder Peserta UAS Literasi Big Data PAI

Berisi roster mahasiswa peserta UAS, pembagian kelompok, dan generator
otomatis untuk regenerate jika perlu.

## Berkas

| Berkas | Sumber | Keterangan |
|---|---|---|
| `peserta.csv` | input dosen | 40 mahasiswa: `no, nim, nama` |
| `buat_kelompok.py` | skrip | generator pembagian kelompok |
| `peserta_dengan_kelompok.csv` | output skrip | csv lengkap dengan kelompok & topik |
| `kelompok-uas.md` | output skrip | tabel pembagian (untuk diumumkan) |
| `roster.json` | output skrip | format yang dikonsumsi aplikasi chatbot |

## Tentang data gender

Data gender mahasiswa **TIDAK** disimpan di `peserta.csv`. Sebagai
gantinya:

1. Mahasiswa **mengisi sendiri** gender mereka saat membuka sesi
   chatbot UAS — sesuai prinsip otonomi data pribadi.
2. Data gender tersimpan di **database sesi SQLite**
   (`app/data/sessions.db`), bukan di roster.
3. Dosen dapat melihat distribusi gender lewat **Dasbor Dosen**
   setelah mahasiswa mulai memakai chatbot.

Jika dosen membutuhkan data gender lebih awal (mis. untuk pelaporan
prodi), silakan koordinasi langsung dengan administrasi atau mahasiswa.

## Cara regenerate pembagian

```bash
# Pembagian default (acak murni, seed reproducible)
python peserta/buat_kelompok.py

# Dengan seed lain
python peserta/buat_kelompok.py --seed 7
```

> **Catatan:** mengubah seed akan **mengubah komposisi kelompok**.
> Kalau Bapak/Ibu sudah mengumumkan pembagian ke mahasiswa, **JANGAN**
> regenerate kecuali ada alasan kuat.

## Privasi

`peserta.csv` berisi NIM dan nama mahasiswa nyata. Pertimbangkan:

- Jangan publikasikan ke repo publik tanpa izin mahasiswa.
- Untuk repo publik, ganti nama menjadi inisial atau nomor anonim.
- File `roster.json` ikut prinsip yang sama.
- Database `app/data/sessions.db` berisi transkrip + gender —
  pertimbangkan kebijakan retensi setelah nilai final keluar.
