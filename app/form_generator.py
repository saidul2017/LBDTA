"""Generator Form Pengungkapan Penggunaan Asisten AI.

Sesuai PETUNJUK-TEKNIS-UAS.md §7. Form ini dibuat OTOMATIS dari
riwayat chat agar mahasiswa tidak bisa "menyembunyikan" penggunaan
AI — setiap interaksi tercatat dan dilampirkan saat submit UAS.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List


# Kategori penggunaan AI sesuai PETUNJUK-TEKNIS-UAS §7.
# Urutan dict ini = urutan prioritas pencocokan. Kategori paling
# spesifik dicek lebih dulu agar tidak ditangkap oleh kategori
# generik (mis. "apa itu confounder?" → Sparring, bukan Klarifikasi).
KATEGORI_KEYWORDS = {
    "Bantuan debug error kode": [
        "error", "debug", "bug", "tidak jalan", "exception",
        "traceback", "modulenotfound", "syntax",
    ],
    "Saran pemilihan visualisasi": [
        "chart", "grafik", "visual", "plot", "histogram",
        "scatter", "boxplot", "bar chart", "diagram",
    ],
    "Sparring argumen kebijakan": [
        "rekomendasi", "policy", "kebijakan", "argumen",
        "alasan", "sebab", "confounder", "kausalitas", "korelasi",
    ],
    "Koreksi tata bahasa": [
        "bahasa", "kalimat", "tulisan", "ejaan", "edit",
        "transliterasi", "rapi",
    ],
    "Klarifikasi konsep / definisi": [
        "apa itu", "jelaskan", "definisi", "maksud", "arti",
        "perbedaan", "contoh dari",
    ],
}


def categorize_messages(messages: List[Dict]) -> Dict[str, int]:
    """Hitung berapa kali tiap kategori muncul di pesan mahasiswa."""
    cats = {k: 0 for k in KATEGORI_KEYWORDS}
    cats["Lainnya"] = 0
    for m in messages:
        if m.get("role") != "user":
            continue
        content = (m.get("content") or "").lower()
        matched = False
        for cat, kws in KATEGORI_KEYWORDS.items():
            if any(kw in content for kw in kws):
                cats[cat] += 1
                matched = True
                break
        if not matched and content.strip():
            cats["Lainnya"] += 1
    return cats


def generate_form_markdown(
    session: Dict,
    messages: List[Dict],
) -> str:
    """Bangun form pengungkapan AI dalam format Markdown."""
    cats = categorize_messages(messages)
    user_msgs = [m for m in messages if m["role"] == "user"]
    bot_msgs = [m for m in messages if m["role"] == "assistant"]
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    sid = session.get("id", "____")
    short_sid = sid[:8] if sid != "____" else "____"

    lines: List[str] = [
        "# Form Pengungkapan Penggunaan Asisten AI",
        "",
        "_Dokumen ini wajib dilampirkan saat submit UAS sesuai_ "
        "_`tugas/PETUNJUK-TEKNIS-UAS.md` §7._",
        "",
        "---",
        "",
        "## A. Identitas Sesi",
        "",
        f"- **Mata kuliah:** Literasi Big Data — Pendidikan Agama Islam",
        f"- **Sesi UAS ID:** `{sid}`",
        f"- **ID singkat:** `{short_sid}`",
        f"- **Tanggal sesi dimulai:** {session.get('created_at', '____')}",
        f"- **Tanggal form digenerate:** {now_iso}",
        f"- **Provider asisten:** {session.get('provider', '____')} "
        f"(model: `{session.get('model', '____')}`)",
        "",
        "## B. Identitas Kelompok",
        "",
        f"- **Nomor kelompok:** {session.get('kelompok') or '____'}",
        f"- **Anggota:**",
    ]

    anggota = (session.get("anggota") or "").strip()
    if anggota:
        for line in anggota.split("\n"):
            line = line.strip()
            if line:
                lines.append(f"  - {line}")
    else:
        lines.append("  - ____")

    lines.extend([
        "",
        f"- **Topik UAS yang dipilih:** {session.get('topik') or '____'}",
        "",
        "## C. Statistik Penggunaan",
        "",
        f"- Total pertanyaan mahasiswa: **{len(user_msgs)}**",
        f"- Total respons asisten: **{len(bot_msgs)}**",
        "",
        "### Kategori penggunaan (terdeteksi otomatis dari isi pesan)",
        "",
    ])

    for cat, count in cats.items():
        check = "[x]" if count > 0 else "[ ]"
        lines.append(f"- {check} **{cat}** — {count} interaksi")

    lines.extend([
        "",
        "## D. Pernyataan & Tanda Tangan",
        "",
        "Kami yang bertanda tangan di bawah ini menyatakan bahwa:",
        "",
        "1. Seluruh argumen, interpretasi, dan rekomendasi dalam ",
        "   *policy brief* UAS kami adalah **hasil pemikiran kami sendiri**.",
        "2. Asisten AI digunakan sebagai **mitra berpikir**, bukan ",
        "   pengganti proses belajar.",
        "3. Transkrip lengkap interaksi (Bagian E di bawah) adalah ",
        "   bukti otentik proses kami, dan kami **tidak menyembunyikan** ",
        "   bagian apa pun.",
        "",
        "**Bagian dokumen UAS yang BUKAN sepenuhnya hasil pemikiran kami** ",
        "(jika ada — isi manual; tulis 'tidak ada' jika seluruhnya orisinal):",
        "",
        "_______________________________________________________________",
        "_______________________________________________________________",
        "",
        "**Tanda Tangan:**",
        "",
        "| # | Nama Anggota | Tanda Tangan |",
        "|---|---|---|",
        "| 1 | _____________________ | _____________________ |",
        "| 2 | _____________________ | _____________________ |",
        "| 3 | _____________________ | _____________________ |",
        "",
        f"**Tanggal:** {datetime.now().strftime('%d %B %Y')}",
        "",
        "---",
        "",
        "## E. Lampiran — Transkrip Lengkap Interaksi",
        "",
        f"_Berikut **{len(messages)} pesan** yang tercatat secara otomatis. ",
        "Tidak boleh diedit oleh mahasiswa._",
        "",
    ])

    if not messages:
        lines.append("_(belum ada interaksi)_")
    else:
        for i, m in enumerate(messages, 1):
            role = "🧑 **Mahasiswa**" if m["role"] == "user" else "🤖 **Asisten**"
            ts = m.get("created_at", "")
            lines.append(f"### Pesan {i} — {role}")
            if ts:
                lines.append(f"_{ts}_")
            lines.append("")
            lines.append(m["content"])
            lines.append("")

    return "\n".join(lines)
