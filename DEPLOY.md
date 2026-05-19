# 🚀 Panduan Deploy Chatbot UAS LBDTA — Step by Step

> Dokumen ini untuk **dosen pengampu** yang akan men-deploy chatbot
> ke Streamlit Cloud (gratis). Total waktu: ~10-15 menit.

## ✅ Pra-syarat (centang semua sebelum mulai)

- [ ] Punya akun GitHub (sudah, karena repo `saidul2017/LBDTA` ada)
- [ ] **Setel repo `LBDTA` ke private** (kritis untuk privasi mahasiswa)
- [ ] Punya akun Google (untuk login Streamlit Cloud + dapat API key)
- [ ] Sudah dapat **API key Gemini** baru dari https://aistudio.google.com/apikey
- [ ] Browser modern (Chrome / Firefox / Safari)

---

## Langkah 1: Setel Repo ke Private (KRITIS — Privasi Mahasiswa)

> Walaupun nama mahasiswa sudah dianonimkan ke inisial di repo,
> **NIM masih lengkap**. Demi *amānah*, sebaiknya repo private.

1. Buka https://github.com/saidul2017/LBDTA/settings
2. Scroll ke paling bawah → **Danger Zone**
3. Klik **Change repository visibility** → **Make private** → konfirmasi.

> Streamlit Cloud bisa connect ke private repo gratis (cukup beri akses
> selama setup).

---

## Langkah 2: Dapatkan Gemini API Key Baru

> Key sebelumnya sudah ter-paste di chat — sebaiknya rotate.

1. Buka https://aistudio.google.com/apikey
2. Login dengan akun Google.
3. (Opsional, jika ada key lama) Klik 3 titik di samping key
   `AIzaSyADdV...` → **Delete**.
4. Klik **Create API Key** → pilih project (atau bikin baru).
5. **Salin** key (formatnya `AIzaSy...`) — simpan sementara di
   notepad pribadi (jangan paste di chat).

---

## Langkah 3: Login ke Streamlit Cloud

1. Buka https://share.streamlit.io
2. Klik **Sign up** atau **Continue with GitHub**.
3. Authorize Streamlit untuk akses GitHub Anda.

---

## Langkah 4: Deploy App Baru

1. Setelah login, klik tombol **Create app** (atau **New app**).
2. Pilih **Deploy a public app from GitHub**.
3. Isi form:

   | Field | Isian |
   |---|---|
   | Repository | `saidul2017/LBDTA` |
   | Branch | `main` |
   | Main file path | `app/streamlit_app.py` |
   | App URL (subdomain) | `lbdta-pai-uas` (atau pilihan Anda) |

4. **JANGAN klik Deploy dulu** — kita perlu set Secrets dulu.

---

## Langkah 5: Set Secrets (KRITIS — API Key & Password)

1. Klik **Advanced settings** di bawah form.
2. Di bagian **Secrets**, salin-tempel teks berikut (ganti `AIzaSy...`
   dengan API key Gemini Anda):

   ```toml
   LLM_PROVIDER = "gemini"
   GEMINI_API_KEY = "AIzaSy...PASTE-KEY-BARU-DI-SINI"
   LLM_MODEL = "gemini-2.5-flash"
   LLM_PROMPT_MODE = "full"
   DOSEN_PASSWORD = "dosen-lbdta-2026"
   KELAS_PASSWORD = "lbdta-kelas-2026"
   ```

3. (Opsional) Ubah `DOSEN_PASSWORD` dan `KELAS_PASSWORD` ke yang
   lebih unik bila ingin.
4. Klik **Save**.

---

## Langkah 6: Klik Deploy

1. Klik **Deploy!**.
2. Tunggu ~3-5 menit untuk build pertama (Streamlit install
   dependencies dari `app/requirements.txt`).
3. Setelah selesai, Anda akan mendapat URL seperti:
   ```
   https://lbdta-pai-uas.streamlit.app
   ```

---

## Langkah 7: Test Sebagai Mahasiswa

1. Buka URL di browser (sebaiknya **incognito** agar tidak bawa
   session login dosen).
2. Halaman pertama: **input password kelas** (`lbdta-kelas-2026`).
3. Sidebar kiri:
   - Pilih NIM mana saja dari dropdown (mis. `23104010002`).
   - Pilih jenis kelamin Anda.
   - Klik **🆕 Mulai sesi baru**.
4. Tab **💬 Chat**: ketik *"Apa itu confounder?"*.
5. Verifikasi:
   - Asisten merespons dalam Bahasa Indonesia ✓
   - Mengutip berkas dengan format `[modul/M03-...md]` ✓
   - Diakhiri pertanyaan reflektif ✓
6. Tab **📋 Form Pengungkapan AI**: klik **⬇️ Unduh Form**.

> **Jika gagal:** error LLM biasanya karena API key salah. Cek
> Secrets di Streamlit Cloud (Manage app → Settings → Secrets).

---

## Langkah 8: Test Sebagai Dosen

1. Di URL yang sama (atau buka tab baru), klik **🎓 Dasbor Dosen**
   di **sidebar Streamlit kiri** (panel hierarki halaman).
2. Input password: `dosen-lbdta-2026`.
3. Test 6 tab:
   - **📊 Statistik** — harus tampil chart sesi yang baru dibuat
   - **📋 Daftar Sesi** — sesi mahasiswa terlihat
   - **🚫 Belum Pakai** — daftar 39 NIM lain (yang belum aktif)
   - **🔎 Detail Sesi** — bisa baca transkrip + unduh form
   - **📝 Nilai** — pilih K01, geser slider, simpan, cek nilai akhir
   - **💾 Ekspor** — coba klik **CSV nilai UAS** (akan unduh CSV)

---

## Langkah 9: Bagikan ke Mahasiswa

Pakai template pengumuman di [`PANDUAN-DOSEN.md` Bagian 2.1](PANDUAN-DOSEN.md).

Yang harus disampaikan:
- **URL chatbot** (mis. `https://lbdta-pai-uas.streamlit.app`)
- **Password kelas** (`lbdta-kelas-2026`)
- **Tenggat UAS** (isi sesuai jadwal kampus)
- **Channel submit** (LMS / Google Classroom / email)

> Sebar via **WAG kelas atau pengumuman LMS resmi** — jangan publik.

---

## 🔄 Update App (Setelah Deploy)

Saat ada perubahan kode di repo:

1. Push commit baru ke branch `main` di GitHub.
2. Streamlit Cloud akan **auto-redeploy** (~1-2 menit).
3. Tidak perlu klik apa-apa.

Untuk perubahan secrets (mis. ganti password):

1. Streamlit Cloud → app Anda → **⋮ Manage app** → **Settings**
   → **Secrets**.
2. Edit, klik **Save**.
3. App auto-restart dengan secrets baru.

---

## 🆘 Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| Build gagal saat deploy | `requirements.txt` salah path | Pastikan main file = `app/streamlit_app.py` |
| `GEMINI_API_KEY belum di-set` | Lupa set secrets | Manage app → Secrets, isi key |
| `Quota exceeded` di Gemini | Lebih dari 250 RPD | Tunggu 24 jam atau upgrade Tier 1 paid |
| Mahasiswa tidak bisa login | Password kelas salah | Cek `KELAS_PASSWORD` di Secrets |
| Saya lupa password dosen | — | Edit Secrets di Streamlit Cloud → restart |
| App lambat | Cold start setelah idle | Normal di tier gratis; klik refresh |
| Database hilang setelah update | Streamlit Cloud volume sementara | Untuk produksi, pertimbangkan PostgreSQL |

---

## 📋 Checklist Final Sebelum Hari-H UAS

- [ ] App deploy berhasil, URL tersedia
- [ ] Test sebagai mahasiswa lancar (chat berhasil, unduh form berhasil)
- [ ] Test sebagai dosen lancar (6 tab dasbor jalan, simpan nilai berhasil)
- [ ] Repo GitHub di-set **private**
- [ ] Petunjuk Teknis UAS sudah diisi tenggat & saluran submit
- [ ] Pengumuman ke mahasiswa sudah disebar via channel resmi
- [ ] PANDUAN-MAHASISWA.md di-share ke kelas
- [ ] (Opsional) Backup database harian sudah dipikirkan

---

## 🎉 Selamat — Deploy Selesai

Setelah semua checklist hijau, paket UAS Anda **production-ready**.

Saat hari-H UAS, Bapak/Ibu cukup pantau lewat dasbor dosen. Setelah
mahasiswa submit, baca brief PDF, lalu input nilai di tab 📝 Nilai.
Selesai — CSV nilai siap di-import ke SIA.
