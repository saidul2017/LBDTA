"""Skrip anonimisasi peserta untuk repo publik.

Konversi `peserta.csv` (nama lengkap) → versi inisial yang aman
dipublikasi. Misalnya:

    Ridwan Ni'am Al Hakim → R. N. A. H.

Cara pakai (dari root repo):

    # Dari nama penuh ke inisial (untuk repo publik):
    python peserta/anonimisasi.py --mode anonimkan

    # Pulihkan nama penuh dari peserta-FULL.csv (lokal saja):
    python peserta/anonimisasi.py --mode pulihkan

    # Generate template peserta-FULL.csv kosong dari peserta.csv inisial:
    python peserta/anonimisasi.py --mode template

Output yang aman commit:
    peserta/peserta.csv         — versi inisial (no, nim, nama_inisial)

Output yang TIDAK boleh commit (sudah di .gitignore):
    peserta/peserta-FULL.csv    — versi nama lengkap (sumber kebenaran)

CATATAN: peserta-FULL.csv adalah sumber kebenaran. peserta.csv adalah
turunan untuk publikasi. Generator pembagian (buat_kelompok.py)
secara otomatis pakai peserta-FULL.csv jika ada, fallback ke
peserta.csv. Ini agar dosen bisa lihat nama penuh saat membagi
kelompok di laptop pribadi, namun yang terpublikasi tetap inisial.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List, Dict

HERE = Path(__file__).resolve().parent
INPUT_FULL = HERE / "peserta-FULL.csv"
INPUT_PUBLIK = HERE / "peserta.csv"


def buat_inisial(nama: str) -> str:
    """Konversi 'Ridwan Niam Al Hakim' → 'R. N. A. H.'

    Aturan:
    - Setiap kata diambil huruf pertama, di-uppercase.
    - Pisah dengan '. '.
    - Tanda kutip dan titik di nama dibersihkan.
    """
    bersih = nama.replace("'", "").replace(".", "").strip()
    kata = [k for k in bersih.split() if k]
    return ". ".join(k[0].upper() for k in kata) + "."


def baca_csv(path: Path) -> List[Dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tulis_csv(rows: List[Dict], path: Path, fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def mode_anonimkan() -> None:
    """Baca peserta-FULL.csv → tulis peserta.csv versi inisial."""
    if not INPUT_FULL.exists():
        # Jika belum ada peserta-FULL.csv tapi peserta.csv masih punya
        # nama lengkap, anggap saja peserta.csv adalah sumber kebenaran
        # → buat backup dulu sebagai peserta-FULL.csv, lalu anonimisasi.
        if INPUT_PUBLIK.exists():
            print(f"⚠️  {INPUT_FULL.name} belum ada.")
            print(f"   Membuat backup nama lengkap dari {INPUT_PUBLIK.name} → "
                  f"{INPUT_FULL.name} (jangan commit ini).")
            INPUT_FULL.write_bytes(INPUT_PUBLIK.read_bytes())
        else:
            raise SystemExit(
                f"Error: tidak ada {INPUT_FULL.name} maupun "
                f"{INPUT_PUBLIK.name}. Buat dulu dengan kolom: no, nim, nama."
            )

    rows = baca_csv(INPUT_FULL)
    out_rows = []
    for r in rows:
        out_rows.append({
            "no": r["no"],
            "nim": r["nim"],
            "nama": buat_inisial(r["nama"]),
        })
    tulis_csv(out_rows, INPUT_PUBLIK, ["no", "nim", "nama"])
    print(f"✅ {INPUT_PUBLIK.name} ditulis dengan inisial untuk {len(out_rows)} peserta.")
    print(f"   {INPUT_FULL.name} dipertahankan dengan nama penuh (lokal).")
    print(f"   Pastikan {INPUT_FULL.name} ADA di .gitignore!")


def mode_pulihkan() -> None:
    """Baca peserta-FULL.csv → tulis peserta.csv dengan nama PENUH."""
    if not INPUT_FULL.exists():
        raise SystemExit(
            f"Error: {INPUT_FULL.name} tidak ditemukan. "
            f"Mode pulihkan hanya bisa dijalankan jika peserta-FULL.csv ada."
        )
    rows = baca_csv(INPUT_FULL)
    tulis_csv(rows, INPUT_PUBLIK, ["no", "nim", "nama"])
    print(f"⚠️  {INPUT_PUBLIK.name} sekarang berisi NAMA PENUH untuk "
          f"{len(rows)} peserta.")
    print(f"   JANGAN commit {INPUT_PUBLIK.name} dalam state ini ke repo publik!")
    print(f"   Setelah selesai pakai (mis. cetak pembagian kelompok), "
          f"jalankan ulang: python peserta/anonimisasi.py --mode anonimkan")


def mode_template() -> None:
    """Buat template peserta-FULL.csv kosong dari peserta.csv inisial."""
    if not INPUT_PUBLIK.exists():
        raise SystemExit(f"Error: {INPUT_PUBLIK.name} tidak ditemukan.")
    if INPUT_FULL.exists():
        raise SystemExit(
            f"Error: {INPUT_FULL.name} sudah ada. Hapus dulu jika ingin "
            f"buat template baru."
        )
    rows = baca_csv(INPUT_PUBLIK)
    out_rows = [
        {"no": r["no"], "nim": r["nim"],
         "nama": f"<isi nama lengkap untuk NIM {r['nim']}>"}
        for r in rows
    ]
    tulis_csv(out_rows, INPUT_FULL, ["no", "nim", "nama"])
    print(f"✅ Template {INPUT_FULL.name} dibuat. "
          f"Edit isi kolom 'nama' dengan nama penuh, lalu jalankan:")
    print(f"   python peserta/anonimisasi.py --mode anonimkan")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--mode",
        choices=["anonimkan", "pulihkan", "template"],
        required=True,
        help=(
            "anonimkan: peserta-FULL.csv → peserta.csv (inisial). "
            "pulihkan: peserta-FULL.csv → peserta.csv (nama penuh). "
            "template: peserta.csv (inisial) → peserta-FULL.csv (template kosong)."
        ),
    )
    args = p.parse_args()
    if args.mode == "anonimkan":
        mode_anonimkan()
    elif args.mode == "pulihkan":
        mode_pulihkan()
    else:
        mode_template()


if __name__ == "__main__":
    main()
