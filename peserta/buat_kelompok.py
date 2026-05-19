"""Pembagi otomatis mahasiswa ke kelompok UAS Literasi Big Data PAI.

Strategi default:
- Acak urutan mahasiswa dengan SEED yang reproducible.
- Bagi menjadi 14 kelompok: 12 kelompok @ 3 orang + 2 kelompok @ 2 orang
  (total = 12*3 + 2*2 = 40).
- Distribusikan 3 topik UAS secara round-robin agar seimbang
  (5 + 5 + 4 = 14).

Strategi opsional `--stratify-gender`:
- Sebar L/P berimbang antar kelompok dengan algoritma
  alokasi-bergantian setelah pengacakan dalam tiap gender.

Cara pakai:
    python peserta/buat_kelompok.py                        # default
    python peserta/buat_kelompok.py --seed 7               # seed lain
    python peserta/buat_kelompok.py --stratify-gender      # seimbang gender

Output:
    peserta/peserta_dengan_kelompok.csv  (csv lengkap)
    peserta/kelompok-uas.md              (tabel pembagian per kelompok)
    peserta/roster.json                  (untuk konsumsi aplikasi chatbot)

PENTING: untuk reproducibility, simpan SEED yang dipakai. Hasil
pembagian akan SAMA PERSIS untuk seed + opsi yang sama.
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
    """Acak peserta lalu bagi ke kelompok dengan ukuran sesuai pola.

    Pure random — tidak memperhatikan gender atau atribut lain.
    """
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


def assign_kelompok_stratified(peserta: List[Dict], seed: int) -> List[Dict]:
    """Bagi seimbang antar kelompok berdasarkan kolom `gender`.

    Algoritma:
    1. Acak antrean L dan P secara terpisah dengan seed yang sama.
    2. Untuk tiap kelompok, ambil dari antrean yang paling 'kurang
       terwakili' dulu (round-robin gender), berhenti saat ukuran
       kelompok tercapai.
    """
    rng = random.Random(seed)

    laki = [p for p in peserta if p.get("gender", "").upper() == "L"]
    perempuan = [p for p in peserta if p.get("gender", "").upper() == "P"]
    lain = [p for p in peserta if p.get("gender", "").upper() not in ("L", "P")]

    rng.shuffle(laki)
    rng.shuffle(perempuan)
    rng.shuffle(lain)

    # Antrean prioritas: dari kategori paling banyak ke paling sedikit
    # tapi alokasi gantian agar tiap kelompok dapat campuran.
    out: List[Dict] = []
    queue_l, queue_p, queue_x = list(laki), list(perempuan), list(lain)

    for k_idx, ukuran in enumerate(UKURAN_KELOMPOK, start=1):
        nomor_kelompok = f"K{k_idx:02d}"
        topik = TOPIK_UAS[(k_idx - 1) % len(TOPIK_UAS)]
        for slot_idx in range(ukuran):
            # Pilih antrean: yang paling banyak sisa-nya, atau lain jika ada
            options = [
                ("L", queue_l), ("P", queue_p), ("X", queue_x),
            ]
            options = [(g, q) for g, q in options if q]
            if not options:
                break
            options.sort(key=lambda x: -len(x[1]))
            # Untuk slot pertama tiap kelompok, ambil dari antrean terbanyak
            # Untuk slot berikutnya, alternasi (kalau bisa) supaya seimbang
            if slot_idx == 0:
                _, q = options[0]
            else:
                # Coba ambil gender berbeda dari yang sudah masuk kelompok ini
                already = {o["gender"] for o in out if o["kelompok"] == nomor_kelompok}
                preferred = [
                    (g, q) for g, q in options if g not in already
                ]
                _, q = (preferred or options)[0]
            p = q.pop(0)
            out.append({**p, "kelompok": nomor_kelompok, "topik_uas": topik})

    return out


def tulis_csv(rows: List[Dict], path: Path) -> None:
    fieldnames = ["no", "nim", "nama", "gender", "kelompok", "topik_uas"]
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
        n_l = sum(1 for a in anggota if a.get("gender", "").upper() == "L")
        n_p = sum(1 for a in anggota if a.get("gender", "").upper() == "P")
        lines.append(f"### Kelompok {kode}")
        lines.append("")
        lines.append(f"**Topik UAS:** {topik}")
        lines.append(f"**Komposisi:** {len(anggota)} orang ({n_l} L, {n_p} P)")
        lines.append("")
        lines.append("| No | NIM | Nama | Gender* |")
        lines.append("|---|---|---|---|")
        for i, a in enumerate(anggota, 1):
            g = a.get("gender", "?")
            lines.append(f"| {i} | `{a['nim']}` | {a['nama']} | {g} |")
        lines.append("")
    lines.append(
        "_*Kolom Gender adalah tebakan heuristik, bukan otoritatif. "
        "Lihat `peserta/README.md` untuk disclaimer._"
    )
    lines.append("")

    lines.append("## Tabel Pencarian (urut NIM)")
    lines.append("")
    lines.append("| NIM | Nama | Gender* | Kelompok | Topik |")
    lines.append("|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: x["nim"]):
        topik_singkat = r["topik_uas"].split(".")[0]
        g = r.get("gender", "?")
        lines.append(
            f"| `{r['nim']}` | {r['nama']} | {g} | "
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
    ])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tulis_roster_json(
    rows: List[Dict],
    seed: int,
    stratified: bool,
    path: Path,
) -> None:
    """Format yang mudah dikonsumsi aplikasi Streamlit (lookup by NIM)."""
    roster = {
        "seed": seed,
        "stratified_gender": stratified,
        "tanggal_generate": date.today().isoformat(),
        "total_mahasiswa": len(rows),
        "topik_uas": TOPIK_UAS,
        "peserta": {
            r["nim"]: {
                "nama": r["nama"],
                "gender": r.get("gender", ""),
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
    p.add_argument("--input", type=Path, default=HERE / "peserta.csv")
    p.add_argument(
        "--stratify-gender",
        action="store_true",
        help="Sebar L/P berimbang antar kelompok",
    )
    args = p.parse_args()

    peserta = baca_peserta(args.input)
    assert len(peserta) == sum(UKURAN_KELOMPOK), (
        f"Jumlah peserta ({len(peserta)}) tidak sama dengan kapasitas "
        f"kelompok ({sum(UKURAN_KELOMPOK)}). Sesuaikan UKURAN_KELOMPOK."
    )

    if args.stratify_gender:
        rows = assign_kelompok_stratified(peserta, args.seed)
    else:
        rows = assign_kelompok(peserta, args.seed)

    csv_path = HERE / "peserta_dengan_kelompok.csv"
    md_path = HERE / "kelompok-uas.md"
    json_path = HERE / "roster.json"

    tulis_csv(rows, csv_path)
    tulis_markdown(rows, args.seed, md_path)
    tulis_roster_json(rows, args.seed, args.stratify_gender, json_path)

    mode = "stratified-gender" if args.stratify_gender else "pure-random"
    print(f"OK. Pembagian seed={args.seed} ({mode}):")
    print(f"  - {csv_path}")
    print(f"  - {md_path}")
    print(f"  - {json_path}")


if __name__ == "__main__":
    main()
