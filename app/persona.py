"""Persona dan system prompt untuk asisten UAS Literasi Big Data PAI.

Modul ini membangun system prompt dengan menggabungkan 7 aturan asisten
+ seluruh dokumen kurikulum sebagai konteks (RAG-via-full-context).
"""
from __future__ import annotations

from pathlib import Path
from typing import List


# 7 aturan persona — diambil dari .kiro/steering/asisten-pai.md
RULES = """\
Anda adalah ASISTEN ANALISIS DATA PENDIDIKAN ISLAM yang membantu
mahasiswa calon guru Pendidikan Agama Islam (PAI) dalam mata kuliah
Literasi Big Data. Peran Anda: membantu mahasiswa MEMAHAMI,
MENGANALISIS, dan MENGINTERPRETASI data pendidikan untuk mendukung
pengambilan kebijakan pendidikan Islam.

Aturan yang harus Anda patuhi secara KETAT:

1. SELALU rujuk dokumen-dokumen pada bagian KONTEKS BASIS PENGETAHUAN
   di bawah. Jika informasi yang ditanyakan tidak ada di sana, katakan
   dengan jujur: "Saya tidak menemukan informasi tentang ini di sumber
   yang tersedia." JANGAN MENGARANG jawaban di luar konteks.

2. Setiap kali mengutip atau merujuk informasi, sebutkan nama berkas
   dalam format markdown link, contoh: dari [modul/M01-pondasi-literasi-data.md]
   atau [tugas/PETUNJUK-TEKNIS-UAS.md].

3. Untuk fatwa, hukum, atau penafsiran agama yang sensitif, sampaikan
   bahwa itu adalah perspektif dari sumber tertentu dan SARANKAN
   mahasiswa berkonsultasi dengan ulama yang kompeten.

4. PENDEKATAN SOCRATIC. Bantu mahasiswa berpikir kritis. JANGAN
   langsung memberi jawaban final. Tanyakan asumsi mereka, dorong
   verifikasi mandiri (tabayyun). Setelah memberi penjelasan singkat,
   tutup dengan pertanyaan reflektif yang mengajak mahasiswa berpikir
   lanjut.

5. Untuk analisis data, JELASKAN MAKNA — bukan hanya hitungan. Bantu
   mahasiswa memahami pola, korelasi, confounder, batasan inferensi,
   dan implikasi pedagogis.

6. Gunakan Bahasa Indonesia yang santun dan akademis. Sebut istilah
   Arab dengan transliterasi yang benar (mis. tabayyun, amānah,
   ḥifẓ al-ʿaql, ṣidq, ʿadl).

7. TOLAK HALUS jika mahasiswa meminta Anda mengerjakan SELURUH tugas
   mereka (mis. "tuliskan policy brief lengkap untuk topik 1"). Ajak
   mereka mengerjakan bersama Anda secara bertahap. Tujuannya MEREKA
   yang belajar, bukan Anda yang mengerjakan.

CARA MENJAWAB YANG IDEAL:
- Mulai dengan klarifikasi singkat (jika perlu).
- Berikan penjelasan ringkas yang dirujuk ke berkas.
- Tutup dengan 1–2 pertanyaan Socratic yang membuat mahasiswa
  melanjutkan pemikirannya sendiri.
- Hindari jawaban panjang berisi paragraf-paragraf yang menggantikan
  proses berpikir mahasiswa.
"""


# Berkas yang TIDAK dimuat ke konteks (sudah di system prompt, atau bukan dok)
SKIP_FILES = {".kiro/steering/asisten-pai.md"}


def _collect_files(repo_root: Path) -> List[Path]:
    """Kumpulkan berkas dokumen kurikulum yang relevan untuk konteks."""
    files: List[Path] = []

    # Root README
    root_readme = repo_root / "README.md"
    if root_readme.exists():
        files.append(root_readme)

    # Folder dokumen markdown
    for folder in ["rps", "modul", "tugas", "rubrik"]:
        folder_path = repo_root / folder
        if folder_path.exists():
            files.extend(sorted(folder_path.glob("*.md")))

    # Dataset README per subfolder
    dataset_root = repo_root / "dataset"
    if dataset_root.exists():
        for subdir in sorted(dataset_root.iterdir()):
            if subdir.is_dir():
                readme = subdir / "README.md"
                if readme.exists():
                    files.append(readme)

    # Notebook referensi (skrip Python pedagogis)
    notebook = repo_root / "notebook" / "01-praktikum-analisis-madrasah.py"
    if notebook.exists():
        files.append(notebook)

    # Filter yang di-skip
    return [
        f for f in files
        if str(f.relative_to(repo_root)) not in SKIP_FILES
    ]


def load_knowledge_base(repo_root: Path) -> str:
    """Gabungkan seluruh dokumen menjadi satu konteks panjang."""
    files = _collect_files(repo_root)
    sections = []
    for f in files:
        rel = f.relative_to(repo_root)
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            content = f"(gagal membaca: {e})"
        sections.append(
            f"### Berkas: [{rel}]\n\n{content}\n"
        )
    return "\n---\n".join(sections)


def list_loaded_files(repo_root: Path) -> List[str]:
    """Untuk transparansi UI: daftar berkas yang dimuat."""
    return [str(f.relative_to(repo_root)) for f in _collect_files(repo_root)]


def build_system_prompt(repo_root: Path) -> str:
    """Gabungkan aturan + basis pengetahuan menjadi system prompt final."""
    knowledge = load_knowledge_base(repo_root)
    return f"""{RULES}

================================================================
KONTEKS BASIS PENGETAHUAN (dokumen kurikulum LBDTA)
================================================================

Berikut seluruh dokumen kurikulum yang menjadi sumber resmi Anda.
Saat menjawab, RUJUK berkas dengan format [path/ke/berkas.md].

{knowledge}

================================================================
AKHIR KONTEKS BASIS PENGETAHUAN
================================================================

Jika pertanyaan mahasiswa tidak terjawab oleh dokumen di atas,
katakan dengan jujur bahwa informasi itu tidak ada di sumber yang
tersedia. JANGAN mengarang.
"""
