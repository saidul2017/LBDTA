"""
Generator dataset sintetis madrasah untuk mata kuliah Literasi Big Data PAI.

PENTING:
- Dataset ini ADALAH SINTETIS (dibangkitkan dengan PRNG terkendali).
- Bukan data EMIS yang sebenarnya.
- Hanya untuk keperluan pembelajaran dan latihan praktikum.
- Dilarang digunakan untuk klaim faktual atau publikasi tanpa pernyataan
  bahwa data ini sintetis.

Output:
- madrasah_sintetis.csv  : data tingkat madrasah (1 baris = 1 madrasah)
- guru_pai_sintetis.csv  : data tingkat guru PAI (1 baris = 1 guru)
- siswa_pai_sintetis.csv : data agregat hasil belajar PAI per madrasah-kelas

Cara pakai:
    python generate.py --n-madrasah 300 --seed 1446 --outdir .
"""

from __future__ import annotations

import argparse
import csv
import os
import random
from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Parameter dunia (boleh disunting dosen pengampu agar distribusi pas konteks)
# ---------------------------------------------------------------------------

PROVINSI = [
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi",
    "Sumatera Selatan", "Lampung", "DKI Jakarta", "Jawa Barat",
    "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Banten", "Bali",
    "NTB", "Kalimantan Selatan", "Sulawesi Selatan",
]

JENJANG = ["MI", "MTs", "MA"]
STATUS = ["Negeri", "Swasta"]
AKREDITASI = ["A", "B", "C", "Belum Terakreditasi"]
DAERAH = ["Perkotaan", "Pedesaan", "3T"]  # 3T = Terdepan, Terluar, Tertinggal
KUALIFIKASI_GURU = ["S1 PAI", "S1 Non-PAI", "S2 PAI", "S2 Non-PAI", "D3/Lainnya"]

# Bobot kasar agar sebaran tidak seragam (mencerminkan realitas umum, bukan data riil)
BOBOT_JENJANG = [0.55, 0.30, 0.15]   # MI lebih banyak daripada MA
BOBOT_STATUS = [0.20, 0.80]          # mayoritas swasta
BOBOT_AKREDITASI = [0.25, 0.40, 0.25, 0.10]
BOBOT_DAERAH = [0.45, 0.45, 0.10]
BOBOT_KUALIFIKASI = [0.55, 0.20, 0.10, 0.05, 0.10]


@dataclass
class Madrasah:
    id_madrasah: str
    nama: str
    jenjang: str
    status: str
    provinsi: str
    daerah: str
    akreditasi: str
    jumlah_siswa: int
    jumlah_guru: int
    rasio_siswa_guru: float
    persen_guru_sertifikasi: float
    akses_internet_mbps: float
    perpustakaan: int   # 0/1
    lab_komputer: int   # 0/1
    rata_nilai_pai: float


@dataclass
class GuruPAI:
    id_guru: str
    id_madrasah: str
    jenis_kelamin: str
    usia: int
    kualifikasi: str
    pengalaman_tahun: int
    sertifikasi: int
    skor_literasi_digital: float
    jam_mengajar_per_minggu: int


@dataclass
class HasilBelajar:
    id_madrasah: str
    kelas: str
    rumpun_pai: str  # Akidah-Akhlak, Fikih, SKI, Quran-Hadis, Bahasa Arab
    rata_nilai: float
    persen_tuntas: float
    n_siswa: int


def weighted_choice(rng: random.Random, items: List[str], weights: List[float]) -> str:
    return rng.choices(items, weights=weights, k=1)[0]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def buat_madrasah(rng: random.Random, idx: int) -> Madrasah:
    jenjang = weighted_choice(rng, JENJANG, BOBOT_JENJANG)
    status = weighted_choice(rng, STATUS, BOBOT_STATUS)
    daerah = weighted_choice(rng, DAERAH, BOBOT_DAERAH)
    akreditasi = weighted_choice(rng, AKREDITASI, BOBOT_AKREDITASI)
    provinsi = rng.choice(PROVINSI)

    # Jumlah siswa dipengaruhi jenjang & status
    base_siswa = {"MI": 180, "MTs": 240, "MA": 200}[jenjang]
    if status == "Negeri":
        base_siswa = int(base_siswa * 1.5)
    if daerah == "3T":
        base_siswa = int(base_siswa * 0.5)
    jumlah_siswa = max(30, int(rng.gauss(base_siswa, base_siswa * 0.35)))

    # Guru: rasio nasional kasar 1:15..20
    target_ratio = rng.uniform(12, 22)
    if daerah == "3T":
        target_ratio = rng.uniform(8, 14)  # guru sedikit, siswa juga sedikit
    jumlah_guru = max(4, round(jumlah_siswa / target_ratio))
    rasio = round(jumlah_siswa / jumlah_guru, 2)

    # Sertifikasi: lebih tinggi di Negeri & A
    p_sert = 0.45
    if status == "Negeri":
        p_sert += 0.20
    if akreditasi == "A":
        p_sert += 0.15
    elif akreditasi == "C":
        p_sert -= 0.10
    elif akreditasi == "Belum Terakreditasi":
        p_sert -= 0.20
    p_sert = clamp(p_sert, 0.05, 0.95)
    persen_sert = round(rng.gauss(p_sert, 0.08) * 100, 1)
    persen_sert = clamp(persen_sert, 0, 100)

    # Internet
    if daerah == "Perkotaan":
        internet = rng.uniform(10, 80)
    elif daerah == "Pedesaan":
        internet = rng.uniform(2, 20)
    else:  # 3T
        internet = rng.uniform(0, 5)
    internet = round(internet, 1)

    perpus = 1 if rng.random() < (0.85 if akreditasi in {"A", "B"} else 0.55) else 0
    lab = 1 if rng.random() < (0.70 if akreditasi == "A" else 0.45 if akreditasi == "B" else 0.20) else 0

    # Nilai PAI: dipengaruhi kombinasi (with confounders untuk latihan analisis)
    nilai = 70.0
    nilai += {"A": 6, "B": 2, "C": -2, "Belum Terakreditasi": -6}[akreditasi]
    nilai += 3 if status == "Negeri" else 0
    nilai += {"Perkotaan": 2, "Pedesaan": 0, "3T": -3}[daerah]
    nilai += (persen_sert - 50) * 0.05      # tiap +10% sertifikasi ≈ +0.5 nilai
    nilai += (internet - 10) * 0.05         # akses internet sedikit pengaruh
    nilai += rng.gauss(0, 4)                # noise
    nilai = round(clamp(nilai, 40, 95), 1)

    nama = f"M{jenjang} {provinsi.split()[0]} {idx:04d}"
    return Madrasah(
        id_madrasah=f"MDR{idx:05d}",
        nama=nama,
        jenjang=jenjang,
        status=status,
        provinsi=provinsi,
        daerah=daerah,
        akreditasi=akreditasi,
        jumlah_siswa=jumlah_siswa,
        jumlah_guru=jumlah_guru,
        rasio_siswa_guru=rasio,
        persen_guru_sertifikasi=persen_sert,
        akses_internet_mbps=internet,
        perpustakaan=perpus,
        lab_komputer=lab,
        rata_nilai_pai=nilai,
    )


def buat_guru(rng: random.Random, mdr: Madrasah, idx: int) -> GuruPAI:
    jk = "P" if rng.random() < 0.58 else "L"
    usia = int(clamp(rng.gauss(38, 9), 23, 60))
    kualifikasi = weighted_choice(rng, KUALIFIKASI_GURU, BOBOT_KUALIFIKASI)
    pengalaman = int(clamp(usia - 23 - rng.randint(0, 5), 0, 35))
    sertifikasi = 1 if rng.random() < (mdr.persen_guru_sertifikasi / 100) else 0

    # Literasi digital: dipengaruhi usia, daerah, kualifikasi
    skor = 60.0
    skor -= (usia - 35) * 0.4
    skor += {"Perkotaan": 5, "Pedesaan": 0, "3T": -5}[mdr.daerah]
    skor += {"S2 PAI": 5, "S2 Non-PAI": 5, "S1 PAI": 0,
             "S1 Non-PAI": -2, "D3/Lainnya": -5}[kualifikasi]
    skor += rng.gauss(0, 8)
    skor = round(clamp(skor, 0, 100), 1)

    jam = int(clamp(rng.gauss(24, 4), 12, 40))

    return GuruPAI(
        id_guru=f"GR{idx:06d}",
        id_madrasah=mdr.id_madrasah,
        jenis_kelamin=jk,
        usia=usia,
        kualifikasi=kualifikasi,
        pengalaman_tahun=pengalaman,
        sertifikasi=sertifikasi,
        skor_literasi_digital=skor,
        jam_mengajar_per_minggu=jam,
    )


RUMPUN = ["Akidah-Akhlak", "Fikih", "SKI", "Quran-Hadis", "Bahasa Arab"]


def buat_hasil_belajar(rng: random.Random, mdr: Madrasah) -> List[HasilBelajar]:
    # Daftar kelas tergantung jenjang
    kelas_map = {
        "MI": ["1", "2", "3", "4", "5", "6"],
        "MTs": ["7", "8", "9"],
        "MA": ["10", "11", "12"],
    }
    out: List[HasilBelajar] = []
    for kelas in kelas_map[mdr.jenjang]:
        for rumpun in RUMPUN:
            # SKI biasanya lebih sulit, Bahasa Arab variatif
            adj = {"Akidah-Akhlak": 1.0, "Fikih": 0.0, "SKI": -2.0,
                   "Quran-Hadis": 0.5, "Bahasa Arab": -1.0}[rumpun]
            nilai = round(clamp(mdr.rata_nilai_pai + adj + rng.gauss(0, 3), 40, 98), 1)
            tuntas = round(clamp((nilai - 60) * 2.5 + rng.gauss(50, 5), 0, 100), 1)
            n = max(5, int(mdr.jumlah_siswa / len(kelas_map[mdr.jenjang]) * rng.uniform(0.85, 1.15)))
            out.append(HasilBelajar(
                id_madrasah=mdr.id_madrasah,
                kelas=kelas,
                rumpun_pai=rumpun,
                rata_nilai=nilai,
                persen_tuntas=tuntas,
                n_siswa=n,
            ))
    return out


def write_csv(path: str, rows: List, header: List[str], to_dict) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(to_dict(r))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n-madrasah", type=int, default=300)
    p.add_argument("--seed", type=int, default=1446)
    p.add_argument("--outdir", type=str, default=".")
    args = p.parse_args()

    rng = random.Random(args.seed)
    os.makedirs(args.outdir, exist_ok=True)

    madrasah: List[Madrasah] = []
    guru: List[GuruPAI] = []
    hasil: List[HasilBelajar] = []

    guru_idx = 1
    for i in range(1, args.n_madrasah + 1):
        m = buat_madrasah(rng, i)
        madrasah.append(m)
        # Sebagian guru di tiap madrasah adalah guru PAI (sekitar 20–35%)
        n_guru_pai = max(1, int(m.jumlah_guru * rng.uniform(0.20, 0.35)))
        for _ in range(n_guru_pai):
            guru.append(buat_guru(rng, m, guru_idx))
            guru_idx += 1
        hasil.extend(buat_hasil_belajar(rng, m))

    write_csv(
        os.path.join(args.outdir, "madrasah_sintetis.csv"),
        madrasah,
        ["id_madrasah", "nama", "jenjang", "status", "provinsi", "daerah",
         "akreditasi", "jumlah_siswa", "jumlah_guru", "rasio_siswa_guru",
         "persen_guru_sertifikasi", "akses_internet_mbps", "perpustakaan",
         "lab_komputer", "rata_nilai_pai"],
        lambda m: m.__dict__,
    )
    write_csv(
        os.path.join(args.outdir, "guru_pai_sintetis.csv"),
        guru,
        ["id_guru", "id_madrasah", "jenis_kelamin", "usia", "kualifikasi",
         "pengalaman_tahun", "sertifikasi", "skor_literasi_digital",
         "jam_mengajar_per_minggu"],
        lambda g: g.__dict__,
    )
    write_csv(
        os.path.join(args.outdir, "siswa_pai_sintetis.csv"),
        hasil,
        ["id_madrasah", "kelas", "rumpun_pai", "rata_nilai",
         "persen_tuntas", "n_siswa"],
        lambda h: h.__dict__,
    )

    print(f"OK. Generated:")
    print(f"  madrasah_sintetis.csv  : {len(madrasah)} baris")
    print(f"  guru_pai_sintetis.csv  : {len(guru)} baris")
    print(f"  siswa_pai_sintetis.csv : {len(hasil)} baris")
    print(f"  outdir = {args.outdir}, seed = {args.seed}")


if __name__ == "__main__":
    main()
