"""Pembagi otomatis mahasiswa ke kelompok UAS Literasi Big Data PAI.

Strategi:
- Acak urutan mahasiswa dengan SEED yang reproducible.
- Bagi menjadi 14 kelompok: 12 kelompok @ 3 orang + 2 kelompok @ 2 orang
  (total = 12*3 + 2*2 = 40).
- Distribusikan 3 topik UAS secara round-robin agar seimbang
  (5 + 5 + 4 = 14).

Cara pakai:
    python peserta/buat_kelompok.py            # default
    python peserta/buat_kelompok.py --seed 7   # seed lain

Output:
    peserta/peserta_dengan_kelompok.csv  (csv lengkap)
    peserta/kelompok-uas.md              (tabel pembagian per kelompok)
    peserta/roster.json                  (untuk konsumsi aplikasi chatbot)

PENTING: untuk reproducibility, simpan SEED yang dipakai. Hasil
pembagian akan SAMA PERSIS untuk seed yang sama.

Catatan: data gender mahasiswa TIDAK ada di roster. Mahasiswa mengisi
sendiri saat login chatbot. Lihat peserta/README.md.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import date
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
DEFAULT_SEED = 1446  # konsisten dengan dataset/emis-sintetis

TOPIK_UAS = [
    "1. Pemerataan kualitas pembelajaran PAI",
    "2. Sertifikasi guru PAI",
    "3. Investasi infrastruktur digital madrasah",
]

# 14 kelompok: 12 @ 3 orang + 2 @ 2 orang = 40
UKURAN_KELOMPOK = [3] * 12 + [2] * 2


def baca_peserta(path: Path) -> List[Dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def assign_kelompok(peserta: List[Dict], seed: int) -> List[Dict]:
    """Acak peserta lalu bagi ke kelompok dengan ukuran sesuai pola."""
    rng = random.Random(seed)
    indeks = list(range(len(peserta)))
    rng.shuffle(indeks)

    out: List[Dict] = []
    posisi = 0
    for k_idx, ukuran in enumerate(UKURAN_KELOMPOK, start=1):
        nomor_kelompok = f"K{k_idx:02d}"
        topik = TOPIK_UAS[(k_idx - 1) % len(TOPIK_UAS)]
        for _ in range(ukuran):
            if posisi >= len(indeks):
                break
            p = peserta[indeks[posisi]]
            out.append({**p, "kelompok": nomor_kelompok, "topik_uas": topik})
            posisi += 1
    return out


def tulis_csv(rows: List[Dict], path: Path) -> None:
    fieldnames = ["no", "nim", "nama", "kelompok", "topik_uas"]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def tulis_markdown(rows: List[Dict], seed: int, path: Path) -> None:
    grup: Dict[str, List[Dict]] = {}
    for r in rows:
        grup.setdefault(r["kelompok"], []).append(r)

    lines = [
        "# Pembagian Kelompok UAS - Literasi Big Data PAI",
        "",
        "> Pembagian otomatis berdasarkan acak terkendali. ",
        f"> **Seed:** `{seed}` (jangan diubah agar reproducible). ",
        f"> **Tanggal generate:** {date.today().isoformat()}",
        "",
        "## Ringkasan",
        "",
        f"- Total mahasiswa: **{len(rows)}**",
        f"- Total kelompok: **{len(grup)}**",
        "- Komposisi: **12 kelompok @ 3 orang + 2 kelompok @ 2 orang**",
        "",
    ]

    per_topik: Dict[str, int] = {}
    for r in rows:
        per_topik[r["topik_uas"]] = per_topik.get(r["topik_uas"], 0) + 1
    lines.append("### Distribusi topik UAS (per mahasiswa)")
    lines.append("")
    for t in TOPIK_UAS:
        lines.append(f"- **{t}** - {per_topik.get(t, 0)} mahasiswa")
    lines.append("")

    lines.append("### Distribusi kelompok per topik")
    lines.append("")
    by_topik: Dict[str, List[str]] = {t: [] for t in TOPIK_UAS}
    for k, anggota in grup.items():
        by_topik[anggota[0]["topik_uas"]].append(k)
    for t in TOPIK_UAS:
        kel_list = ", ".join(sorted(by_topik[t])) or "-"
        lines.append(f"- **{t}** - {kel_list} ({len(by_topik[t])} kelompok)")
    lines.append("")

    lines.append("## Daftar Kelompok")
    lines.append("")
    for kode in sorted(grup):
        anggota = grup[kode]
        topik = anggota[0]["topik_uas"]
        lines.append(f"### Kelompok {kode}")
        lines.append("")
        lines.append(f"**Topik UAS:** {topik}")
        lines.append("")
        lines.append("| No | NIM | Nama |")
        lines.append("|---|---|---|")
        for i, a in enumerate(anggota, 1):
            lines.append(f"| {i} | `{a['nim']}` | {a['nama']} |")
        lines.append("")

    lines.append("## Tabel Pencarian (urut NIM)")
    lines.append("")
    lines.append("| NIM | Nama | Kelompok | Topik |")
    lines.append("|---|---|---|---|")
    for r in sorted(rows, key=lambda x: x["nim"]):
        topik_singkat = r["topik_uas"].split(".")[0]
        lines.append(
            f"| `{r['nim']}` | {r['nama']} | "
            f"**{r['kelompok']}** | Topik {topik_singkat} |"
        )
    lines.append("")

    lines.extend([
        "---",
        "",
        "## Catatan",
        "",
        "1. Pembagian ini **mengikat**. Permintaan pindah kelompok harus ",
        "   diajukan ke dosen pengampu dengan alasan yang sah.",
        "2. Setiap kelompok wajib **mendaftarkan ulang topik** di asisten ",
        "   chatbot UAS untuk memulai sesi resmi.",
        "3. Bila ada perbaikan data peserta (NIM/nama), edit ",
        "   `peserta/peserta.csv` lalu jalankan ulang ",
        f"   `python peserta/buat_kelompok.py --seed {seed}`.",
        "4. **Gender** mahasiswa diisi sendiri saat membuka sesi chatbot.",
    ])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tulis_roster_json(rows: List[Dict], seed: int, path: Path) -> None:
    """Format yang mudah dikonsumsi aplikasi Streamlit (lookup by NIM)."""
    roster = {
        "seed": seed,
        "tanggal_generate": date.today().isoformat(),
        "total_mahasiswa": len(rows),
        "topik_uas": TOPIK_UAS,
        "peserta": {
            r["nim"]: {
                "nama": r["nama"],
                "kelompok": r["kelompok"],
                "topik_uas": r["topik_uas"],
            }
            for r in rows
        },
    }
    path.write_text(
        json.dumps(roster, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--input", type=Path, default=None,
                   help="Default: pakai peserta-FULL.csv jika ada (lokal "
                        "saja, nama lengkap), fallback ke peserta.csv "
                        "(versi inisial untuk publik).")
    args = p.parse_args()

    # Prioritas: peserta-FULL.csv (lokal, nama lengkap) > peserta.csv (publik, inisial)
    if args.input:
        input_path = args.input
    else:
        full_path = HERE / "peserta-FULL.csv"
        public_path = HERE / "peserta.csv"
        if full_path.exists():
            input_path = full_path
            print(f"ℹ️  Pakai {full_path.name} (nama lengkap, lokal).")
        else:
            input_path = public_path
            print(f"ℹ️  Pakai {public_path.name} (versi publik). "
                  f"Hasil pembagian akan menampilkan inisial saja.")

    peserta = baca_peserta(input_path)
    assert len(peserta) == sum(UKURAN_KELOMPOK), (
        f"Jumlah peserta ({len(peserta)}) tidak sama dengan kapasitas "
        f"kelompok ({sum(UKURAN_KELOMPOK)}). Sesuaikan UKURAN_KELOMPOK."
    )

    rows = assign_kelompok(peserta, args.seed)

    csv_path = HERE / "peserta_dengan_kelompok.csv"
    md_path = HERE / "kelompok-uas.md"
    json_path = HERE / "roster.json"

    tulis_csv(rows, csv_path)
    tulis_markdown(rows, args.seed, md_path)
    tulis_roster_json(rows, args.seed, json_path)

    print(f"OK. Pembagian dengan seed={args.seed}:")
    print(f"  - {csv_path}")
    print(f"  - {md_path}")
    print(f"  - {json_path}")


if __name__ == "__main__":
    main()
