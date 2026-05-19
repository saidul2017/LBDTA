# Folder Peserta UAS Literasi Big Data PAI

Berisi roster mahasiswa peserta UAS, pembagian kelompok, dan generator
otomatis untuk regenerate jika perlu.

## ⚠️ PERINGATAN PRIVASI — WAJIB DIBACA DOSEN

Folder ini menyimpan **data identifikasi mahasiswa** (NIM dan
nama/inisial). Sesuai prinsip *amānah* (data adalah titipan) — yang
diajarkan modul ini sendiri — dan **UU Pelindungan Data Pribadi
27/2022**, ada beberapa hal kritis:

### 1. Repositori dengan data peserta SEBAIKNYA *private*

Jika Bapak/Ibu memublikasikan repo ini di GitHub publik, **NIM nyata
mahasiswa akan dapat dilihat siapa pun**. Walau hanya inisial nama,
NIM tetap dapat di-cross-reference dengan data publik kampus.

**Rekomendasi:**

- **Setel repo ke private** sebelum dipakai produksi. Settings →
  Danger Zone → Change visibility → Private.
- Atau, *fork* repo ini ke akun pribadi yang private.

### 2. Pemisahan nama lengkap vs inisial

Untuk memberi opsi, kami menyediakan dua format peserta:

| Berkas | Isi | Status di Git |
|---|---|---|
| `peserta.csv` | NIM + **inisial** (mis. `R. N. A. H.`) | ✅ Boleh di-commit |
| `peserta-FULL.csv` | NIM + **nama lengkap** | ❌ Di-gitignore (lokal saja) |

`peserta-FULL.csv` adalah sumber kebenaran — dipakai dosen untuk
melihat nama lengkap di laptop pribadi tanpa pernah ter-upload ke
Git.

### 3. Workflow yang disarankan

```bash
# Pertama kali setup (dosen, di laptop pribadi):
# 1. Edit peserta-FULL.csv dengan nama lengkap mahasiswa
# 2. Generate versi inisial untuk repo publik:
python peserta/anonimisasi.py --mode anonimkan

# 3. Generate pembagian kelompok (otomatis pakai FULL kalau ada):
python peserta/buat_kelompok.py
```

### 4. Data sesi mahasiswa di SQLite (sessions.db)

Database `app/data/sessions.db` menyimpan **transkrip lengkap chat,
gender, NIM**. Data ini bersifat sensitif. Pertimbangkan:

- **Setelah nilai final keluar**, hapus database atau anonimkan.
- **Jangan share database** dengan pihak ketiga.
- **Pertimbangkan minta consent eksplisit** dari mahasiswa
  sebelum kelas dimulai.

---

## Berkas

| Berkas | Sumber | Keterangan |
|---|---|---|
| `peserta.csv` | input dosen | 40 mahasiswa: `no, nim, nama` (inisial) |
| `peserta-FULL.csv` | dosen (lokal) | versi nama lengkap, **tidak di-commit** |
| `anonimisasi.py` | skrip | konversi nama lengkap ↔ inisial |
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

## Cara mengubah inisial ↔ nama lengkap

```bash
# Dari nama penuh (FULL.csv) ke inisial (publik):
python peserta/anonimisasi.py --mode anonimkan

# Pulihkan nama penuh dari FULL.csv ke peserta.csv (LOKAL SAJA, jangan commit):
python peserta/anonimisasi.py --mode pulihkan

# Buat template FULL.csv kosong dari peserta.csv inisial (untuk diisi manual):
python peserta/anonimisasi.py --mode template
```
