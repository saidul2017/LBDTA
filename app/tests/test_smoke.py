"""Tes asap (smoke tests) — tanpa memanggil LLM eksternal.

Memverifikasi bahwa modul-modul lokal bisa di-import, system prompt
terbangun, storage berfungsi, dan form generator menghasilkan
output yang masuk akal.

Jalankan dari root repo:
    python -m pytest app/tests/ -v

atau tanpa pytest:
    python app/tests/test_smoke.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPO_ROOT / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def test_persona_loads_knowledge_base():
    from persona import build_system_prompt, list_loaded_files

    prompt = build_system_prompt(REPO_ROOT)
    assert "Asisten" in prompt or "asisten" in prompt
    assert "amānah" in prompt.lower() or "tabayyun" in prompt.lower()
    # System prompt harus berisi konteks dari dokumen
    assert "[modul/" in prompt or "[rps/" in prompt or "Berkas:" in prompt

    files = list_loaded_files(REPO_ROOT)
    assert len(files) > 0
    assert any("modul" in f for f in files)
    assert any("PETUNJUK-TEKNIS-UAS" in f for f in files)
    print(f"OK persona — {len(files)} berkas dimuat, prompt {len(prompt)} chars")


def test_storage_roundtrip(tmp_path: Path = None):
    if tmp_path is None:
        import tempfile
        tmp_dir = Path(tempfile.mkdtemp())
    else:
        tmp_dir = tmp_path
    db_path = tmp_dir / "test.db"

    from storage import Storage

    s = Storage(db_path)
    sid = s.create_session(
        kelompok="03",
        anggota="Ahmad\nFatimah",
        topik="2. Sertifikasi guru",
        provider="groq",
        model="llama-3.3-70b-versatile",
    )
    assert sid

    s.add_message(sid, "user", "apa itu confounder?")
    s.add_message(sid, "assistant", "mari kita pikirkan bersama...")

    msgs = s.get_messages(sid)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"

    sess = s.get_session(sid)
    assert sess["kelompok"] == "03"
    assert sess["topik"] == "2. Sertifikasi guru"

    s.update_session(sid, topik="3. Investasi infrastruktur digital madrasah")
    sess2 = s.get_session(sid)
    assert "Investasi" in sess2["topik"]

    print(f"OK storage — sesi {sid[:8]}, 2 pesan, update sukses")


def test_form_generator():
    from form_generator import generate_form_markdown, categorize_messages

    session = {
        "id": "abcd1234-5678-90ef-1234-567890abcdef",
        "created_at": "2026-05-19T03:00:00+00:00",
        "kelompok": "03",
        "anggota": "Ahmad\nFatimah",
        "topik": "2. Sertifikasi guru",
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
    }
    messages = [
        {"role": "user", "content": "apa itu confounder dalam analisis data?",
         "created_at": "2026-05-19T03:01:00+00:00"},
        {"role": "assistant", "content": "Mari kita mulai dengan pertanyaan...",
         "created_at": "2026-05-19T03:01:05+00:00"},
        {"role": "user", "content": "saya dapat error ModuleNotFoundError",
         "created_at": "2026-05-19T03:02:00+00:00"},
        {"role": "assistant", "content": "Coba periksa apakah pip install...",
         "created_at": "2026-05-19T03:02:05+00:00"},
    ]
    md = generate_form_markdown(session, messages)

    assert "Form Pengungkapan" in md
    assert "abcd1234" in md
    assert "Ahmad" in md
    assert "Sertifikasi" in md
    assert "Pesan 1" in md
    assert "Pesan 4" in md

    cats = categorize_messages(messages)
    assert cats["Sparring argumen kebijakan"] == 1  # confounder
    assert cats["Bantuan debug error kode"] == 1    # error
    print(f"OK form_generator — output {len(md)} chars, kategori benar")


if __name__ == "__main__":
    test_persona_loads_knowledge_base()
    test_storage_roundtrip()
    test_form_generator()
    print("\n✅ Semua smoke tests lulus.")
