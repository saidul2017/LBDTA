"""Persona dan system prompt untuk asisten UAS Literasi Big Data PAI.

Modul ini membangun system prompt dengan menggabungkan 7 aturan asisten
+ dokumen kurikulum sebagai konteks.

Dua mode:
- `compact` (default) — ringkas, ~3-5K token, cocok untuk Groq free tier
  (limit 12K TPM). Dokumen besar di-truncate; mahasiswa diarahkan
  membuka berkas detail di repo bila perlu.
- `full` — semua dokumen utuh, ~15K token. Cocok untuk Gemini, OpenAI,
  Anthropic, atau Groq paid tier dengan limit besar.

Pilih mode lewat env var: LLM_PROMPT_MODE=compact|full (default: compact).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple


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
- Tutup dengan 1-2 pertanyaan Socratic yang membuat mahasiswa
  melanjutkan pemikirannya sendiri.
- Hindari jawaban panjang berisi paragraf-paragraf yang menggantikan
  proses berpikir mahasiswa.
"""


SKIP_FILES = {".kiro/steering/asisten-pai.md"}


# Pengaturan budget per berkas untuk mode compact (chars).
# None = full content. Angka = max chars (di-truncate ke batas paragraf).
COMPACT_BUDGET = {
    # Penting & wajib utuh
    "tugas/PETUNJUK-TEKNIS-UAS.md": None,
    "tugas/template-policy-brief.md": None,
    "rps/RPS-LBDTA.md": 2500,
    "rubrik/R01-pemetaan-sumber-data.md": None,
    "rubrik/R02-analisis-data-sintetis.md": None,
    "rubrik/R03-policy-brief-mini.md": None,
    "tugas/T01-pemetaan-sumber-data.md": 1500,
    "tugas/T02-analisis-data-sintetis.md": 1500,
    "tugas/T03-policy-brief-mini.md": 2000,
    # Modul: cukup intro
    "modul/M01-pondasi-literasi-data.md": 800,
    "modul/M02-praktik-analisis-data.md": 800,
    "modul/M03-sintesis-etika-dan-kebijakan.md": 1200,
    # Dataset: kamus data ringkas
    "dataset/emis-sintetis/README.md": 1200,
}

# Berkas yang DI-SKIP saat mode compact (terlalu panjang, ada di repo)
COMPACT_SKIP = {
    "tugas/bank-pertanyaan-pemandu.md",
    "notebook/01-praktikum-analisis-madrasah.py",
    "README.md",
}


def _collect_files(repo_root: Path) -> List[Path]:
    """Kumpulkan berkas dokumen kurikulum yang relevan untuk konteks."""
    files: List[Path] = []
    root_readme = repo_root / "README.md"
    if root_readme.exists():
        files.append(root_readme)
    for folder in ["rps", "modul", "tugas", "rubrik"]:
        folder_path = repo_root / folder
        if folder_path.exists():
            files.extend(sorted(folder_path.glob("*.md")))
    dataset_root = repo_root / "dataset"
    if dataset_root.exists():
        for subdir in sorted(dataset_root.iterdir()):
            if subdir.is_dir():
                readme = subdir / "README.md"
                if readme.exists():
                    files.append(readme)
    notebook = repo_root / "notebook" / "01-praktikum-analisis-madrasah.py"
    if notebook.exists():
        files.append(notebook)
    return [
        f for f in files
        if str(f.relative_to(repo_root)) not in SKIP_FILES
    ]


def _truncate(text: str, max_chars: int) -> Tuple[str, bool]:
    """Potong teks ke max_chars di batas paragraf terdekat."""
    if len(text) <= max_chars:
        return text, False
    cut = text[:max_chars]
    idx = cut.rfind("\n\n")
    if idx > max_chars * 0.5:
        cut = cut[:idx]
    return cut, True


def load_knowledge_base(repo_root: Path, mode: str = "compact") -> str:
    """Gabungkan dokumen menjadi konteks panjang."""
    files = _collect_files(repo_root)
    sections = []
    for f in files:
        rel = str(f.relative_to(repo_root))
        if mode == "compact" and rel in COMPACT_SKIP:
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            content = f"(gagal membaca: {e})"

        truncated = False
        if mode == "compact":
            budget = COMPACT_BUDGET.get(rel)
            if budget is not None:
                content, truncated = _truncate(content, budget)

        suffix = (
            f"\n\n_(Dokumen ini di-truncate untuk efisiensi. "
            f"Buka berkas asli `{rel}` di repo untuk versi lengkap.)_"
            if truncated else ""
        )
        sections.append(f"### Berkas: [{rel}]\n\n{content}{suffix}\n")
    return "\n---\n".join(sections)


def list_loaded_files(repo_root: Path, mode: str = "compact") -> List[str]:
    """Untuk transparansi UI: daftar berkas yang dimuat."""
    files = _collect_files(repo_root)
    out = []
    for f in files:
        rel = str(f.relative_to(repo_root))
        if mode == "compact" and rel in COMPACT_SKIP:
            continue
        budget = COMPACT_BUDGET.get(rel) if mode == "compact" else None
        marker = "" if budget is None else f" (<={budget} chars)"
        out.append(f"{rel}{marker}")
    return out


def get_mode() -> str:
    return os.getenv("LLM_PROMPT_MODE", "compact").lower().strip()


def build_system_prompt(repo_root: Path) -> str:
    """Gabungkan aturan + basis pengetahuan menjadi system prompt final."""
    mode = get_mode()
    knowledge = load_knowledge_base(repo_root, mode=mode)
    extra_note = (
        "\n\n**CATATAN MODE COMPACT:** Beberapa berkas di-truncate untuk "
        "efisiensi token. Jika mahasiswa minta detail spesifik dari modul/"
        "tugas/notebook yang tidak tampak di konteks, ARAHKAN mereka "
        "membuka berkas asli di repo `LBDTA/` (mis. `notebook/01-"
        "praktikum-analisis-madrasah.py` untuk kode lengkap)."
        if mode == "compact" else ""
    )
    return f"""{RULES}{extra_note}

================================================================
KONTEKS BASIS PENGETAHUAN (dokumen kurikulum LBDTA)
================================================================

Berikut dokumen kurikulum yang menjadi sumber resmi Anda.
Saat menjawab, RUJUK berkas dengan format [path/ke/berkas.md].

{knowledge}

================================================================
AKHIR KONTEKS BASIS PENGETAHUAN
================================================================

Jika pertanyaan mahasiswa tidak terjawab oleh dokumen di atas,
katakan dengan jujur bahwa informasi itu tidak ada di sumber yang
tersedia. JANGAN mengarang.
"""
