"""
Notebook Referensi — Pertemuan 2: Praktik Analisis Data Madrasah
================================================================

Skrip ini adalah CONTOH SOLUSI untuk Pertemuan 2 (T02). Mahasiswa boleh
menggunakannya sebagai TEMPLATE awal, lalu mengembangkan analisisnya
sendiri sesuai topik UAS yang dipilih kelompok.

Cara menjalankan (dari folder ini):

    cd notebook
    pip install pandas matplotlib numpy
    python 01-praktikum-analisis-madrasah.py

Output: tabel ringkasan di stdout + 3 PNG di folder `notebook/outputs/`.

Format file ini menggunakan marker sel `# %%` yang kompatibel dengan:
- VS Code Jupyter extension (otomatis dikenali sebagai sel)
- Spyder / PyCharm Scientific Mode
- Konversi ke .ipynb via `jupytext --to ipynb 01-praktikum-...py`

DISCLAIMER: dataset yang dianalisis adalah SINTETIS (lihat
`dataset/emis-sintetis/README.md`). Pola yang ditemukan TIDAK mewakili
realitas pendidikan Islam di Indonesia.
"""

# %% [markdown]
# # Pertemuan 2 — Analisis Data Madrasah (Sintetis)
#
# **Sub-CPMK yang dilatih:**
# 1. Pembersihan data
# 2. Statistika deskriptif & pemilihan ringkasan yang tepat
# 3. Visualisasi yang jujur (*ṣidq*)
# 4. Refleksi awal tentang *confounder* (jembatan ke Pertemuan 3)

# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = os.path.join("..", "dataset", "emis-sintetis")
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)

# %% [markdown]
# ## 1. Muat data

# %%
mdr = pd.read_csv(os.path.join(DATA_DIR, "madrasah_sintetis.csv"))
guru = pd.read_csv(os.path.join(DATA_DIR, "guru_pai_sintetis.csv"))
siswa = pd.read_csv(os.path.join(DATA_DIR, "siswa_pai_sintetis.csv"))

print("Bentuk dataset:")
print(f"  madrasah : {mdr.shape}")
print(f"  guru PAI : {guru.shape}")
print(f"  hasil    : {siswa.shape}")
print()
print("Sampel madrasah (3 baris pertama):")
print(mdr.head(3))

# %% [markdown]
# ## 2. Pembersihan & inspeksi
#
# Pertanyaan minimum yang harus selalu kita ajukan ke setiap dataset
# baru:
# 1. Apakah tipe data sesuai harapan?
# 2. Berapa banyak missing value? Acak atau sistematis?
# 3. Adakah duplikat pada kolom kunci?
# 4. Adakah outlier yang mencurigakan (kemungkinan salah input)?

# %%
print("Tipe data:")
print(mdr.dtypes)
print()
print("Missing values per kolom:")
print(mdr.isnull().sum())
print()
print(f"Duplikat id_madrasah: {mdr['id_madrasah'].duplicated().sum()}")

# %%
print("Ringkasan numerik kolom kunci:")
print(mdr[["jumlah_siswa", "jumlah_guru", "rasio_siswa_guru",
           "persen_guru_sertifikasi", "akses_internet_mbps",
           "rata_nilai_pai"]].describe().round(2))

# %% [markdown]
# **Catatan untuk mahasiswa:** Pada dataset sintetis ini umumnya tidak
# ada missing value atau duplikat. Pada data nyata, hampir pasti ada.
# Tulis temuan dan tindakan Anda di brief — bahkan kalau temuannya
# "tidak ada masalah", itu tetap perlu dilaporkan.

# %% [markdown]
# ## 3. Statistika deskriptif

# %% [markdown]
# ### 3.1 Rata-rata nilai PAI per jenjang

# %%
ringkasan_jenjang = (
    mdr.groupby("jenjang")["rata_nilai_pai"]
       .agg(["count", "mean", "median", "std"])
       .round(2)
)
print(ringkasan_jenjang)

# %% [markdown]
# **Pertanyaan reflektif:** Apakah median berbeda jauh dari mean? Jika
# ya, sebaran kemungkinan asimetris (skewed). Jika tidak, sebaran
# relatif simetris. Mana yang lebih representatif untuk dilaporkan ke
# kepala madrasah?

# %% [markdown]
# ### 3.2 Distribusi akreditasi

# %%
freq_akreditasi = (
    mdr["akreditasi"].value_counts(normalize=True)
       .mul(100).round(1)
       .reindex(["A", "B", "C", "Belum Terakreditasi"])
)
print("Persentase madrasah per akreditasi (%):")
print(freq_akreditasi)

# %% [markdown]
# ### 3.3 Negeri vs Swasta — sertifikasi guru

# %%
sertifikasi_per_status = (
    mdr.groupby("status")["persen_guru_sertifikasi"]
       .describe().round(1)[["min", "25%", "50%", "75%", "max", "mean"]]
)
print(sertifikasi_per_status)

# %% [markdown]
# ### 3.4 Literasi digital guru per kualifikasi

# %%
literasi_per_kualifikasi = (
    guru.groupby("kualifikasi")["skor_literasi_digital"]
        .agg(["mean", "median", "std", "count"])
        .round(1)
        .sort_values("mean", ascending=False)
)
print(literasi_per_kualifikasi)

# %% [markdown]
# ## 4. Visualisasi
#
# Tiga prinsip *ṣidq* dalam visual:
# 1. Sumbu Y mulai dari 0 untuk bar chart kuantitas (kecuali ada alasan
#    eksplisit untuk tidak).
# 2. Skala sumbu konsisten antar grafik yang dibandingkan.
# 3. Caption menjelaskan apa yang dilihat, bukan apa yang ingin pembaca
#    lihat.

# %% [markdown]
# ### 4.1 Histogram sebaran nilai PAI

# %%
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(mdr["rata_nilai_pai"], bins=30, edgecolor="white")
ax.set_title("Sebaran rata-rata nilai PAI antar madrasah (n="
             f"{len(mdr)} madrasah sintetis)")
ax.set_xlabel("Rata-rata nilai PAI")
ax.set_ylabel("Jumlah madrasah")
ax.grid(axis="y", linestyle=":", alpha=0.5)
out1 = os.path.join(OUT_DIR, "01-histogram-nilai.png")
fig.savefig(out1, dpi=120, bbox_inches="tight")
plt.close(fig)
print(f"Tersimpan: {out1}")

# %% [markdown]
# ### 4.2 Boxplot nilai PAI per akreditasi

# %%
fig, ax = plt.subplots(figsize=(8, 4))
order = ["A", "B", "C", "Belum Terakreditasi"]
data_per_akreditasi = [
    mdr.loc[mdr["akreditasi"] == a, "rata_nilai_pai"].values for a in order
]
ax.boxplot(data_per_akreditasi, labels=order, showmeans=True)
ax.set_title("Sebaran nilai PAI per akreditasi madrasah")
ax.set_xlabel("Akreditasi")
ax.set_ylabel("Rata-rata nilai PAI")
ax.grid(axis="y", linestyle=":", alpha=0.5)
out2 = os.path.join(OUT_DIR, "02-boxplot-akreditasi.png")
fig.savefig(out2, dpi=120, bbox_inches="tight")
plt.close(fig)
print(f"Tersimpan: {out2}")

# %% [markdown]
# ### 4.3 Scatter: sertifikasi vs nilai PAI (+ trendline)

# %%
x = mdr["persen_guru_sertifikasi"].values
y = mdr["rata_nilai_pai"].values
m, c = np.polyfit(x, y, 1)
xs = np.linspace(x.min(), x.max(), 100)

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(x, y, alpha=0.4, s=22)
ax.plot(xs, m * xs + c, color="firebrick",
        label=f"trendline: y = {m:.2f}x + {c:.1f}")
ax.set_title("Persen guru sertifikasi vs rata-rata nilai PAI "
             "(KORELASI, bukan sebab-akibat)")
ax.set_xlabel("Persen guru sertifikasi (%)")
ax.set_ylabel("Rata-rata nilai PAI")
ax.legend()
ax.grid(linestyle=":", alpha=0.5)
out3 = os.path.join(OUT_DIR, "03-scatter-sertifikasi.png")
fig.savefig(out3, dpi=120, bbox_inches="tight")
plt.close(fig)
print(f"Tersimpan: {out3}")

# %% [markdown]
# ## 5. Refleksi *confounder* (jembatan ke Pertemuan 3)
#
# Korelasi sertifikasi vs nilai mungkin **tampak** seperti sebab-akibat.
# Tapi mari kita periksa **akreditasi** sebagai variabel ketiga.

# %%
r_global = np.corrcoef(x, y)[0, 1]
print(f"Korelasi global Pearson r = {r_global:.3f}")
print()
print("Apakah pola tetap kuat KALAU kita kontrol akreditasi?")
print("(rata-rata sertifikasi & nilai per akreditasi)")
print()
print(
    mdr.groupby("akreditasi")[["persen_guru_sertifikasi",
                               "rata_nilai_pai"]].mean().round(2)
)
print()
print("Korelasi DI DALAM tiap kelompok akreditasi:")
for a in ["A", "B", "C", "Belum Terakreditasi"]:
    sub = mdr[mdr["akreditasi"] == a]
    if len(sub) >= 5:
        r = np.corrcoef(sub["persen_guru_sertifikasi"],
                        sub["rata_nilai_pai"])[0, 1]
        print(f"  {a:>20s}: r = {r:+.3f} (n = {len(sub)})")
    else:
        print(f"  {a:>20s}: terlalu sedikit data (n = {len(sub)})")

# %% [markdown]
# **Pertanyaan untuk *policy brief* Anda:** Jika korelasi melemah
# secara substansial setelah dikontrol untuk akreditasi, apa artinya
# bagi rekomendasi kebijakan tentang sertifikasi? Apakah sertifikasi
# sendiri yang penting, atau ada faktor sistemik lain yang justru
# mendasari?
#
# Diskusikan jawaban ini di Bagian 4 (Diskusi & Batasan) dan Bagian 6
# (Pertimbangan Etis — *tabayyun*) brief Anda.

# %%
print()
print("=== Selesai. Cek folder 'outputs/' untuk PNG. ===")
