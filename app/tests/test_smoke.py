"""Tes asap (smoke tests) — tanpa memanggil LLM eksternal.

Memverifikasi modul lokal bisa di-import, system prompt terbangun,
storage berfungsi (termasuk schema baru dengan gender), dan form
generator menghasilkan output yang masuk akal.

Jalankan dari root repo:
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
    assert "asisten" in prompt.lower()
    assert "amānah" in prompt.lower() or "tabayyun" in prompt.lower()
    assert "[modul/" in prompt or "[rps/" in prompt or "Berkas:" in prompt

    files = list_loaded_files(REPO_ROOT)
    assert len(files) > 0
    assert any("modul" in f for f in files)
    assert any("PETUNJUK-TEKNIS-UAS" in f for f in files)
    print(f"OK persona — {len(files)} berkas dimuat, prompt {len(prompt)} chars")


def test_storage_roundtrip():
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    db_path = tmp / "test.db"
    from storage import Storage

    s = Storage(db_path)
    sid = s.create_session(
        nim="23104010002",
        nama="RIDWAN NI'AM AL HAKIM",
        gender="L",
        kelompok="K04",
        anggota="23104010002 - RIDWAN NI'AM AL HAKIM",
        topik="1. Pemerataan kualitas pembelajaran PAI",
        provider="groq",
        model="llama-3.3-70b-versatile",
    )
    assert sid

    s.add_message(sid, "user", "apa itu confounder?")
    s.add_message(sid, "assistant", "mari kita pikirkan bersama...")

    msgs = s.get_messages(sid)
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"

    sess = s.get_session(sid)
    assert sess["nim"] == "23104010002"
    assert sess["nama"].startswith("RIDWAN")
    assert sess["gender"] == "L"
    assert sess["kelompok"] == "K04"

    s.update_session(sid, gender="P")
    sess2 = s.get_session(sid)
    assert sess2["gender"] == "P"
    print(f"OK storage — sesi {sid[:8]}, NIM/nama/gender/kelompok ok")


def test_form_generator():
    from form_generator import generate_form_markdown, categorize_messages

    session = {
        "id": "abcd1234-5678-90ef-1234-567890abcdef",
        "created_at": "2026-05-19T03:00:00+00:00",
        "nim": "23104010002",
        "nama": "RIDWAN NI'AM AL HAKIM",
        "gender": "L",
        "kelompok": "K04",
        "anggota": "23104010002 - RIDWAN NI'AM AL HAKIM",
        "topik": "1. Pemerataan kualitas pembelajaran PAI",
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
    assert "23104010002" in md
    assert "Laki-laki" in md
    assert "K04" in md
    assert "Pesan 1" in md and "Pesan 4" in md

    cats = categorize_messages(messages)
    assert cats["Sparring argumen kebijakan"] == 1
    assert cats["Bantuan debug error kode"] == 1
    print(f"OK form_generator — output {len(md)} chars")


def test_roster_loader():
    from peserta_loader import load_roster, list_all_peserta, list_kelompok
    r = load_roster(REPO_ROOT)
    if r is None:
        print("SKIP roster_loader — peserta/roster.json tidak ada")
        return
    assert "gender" not in next(iter(r["peserta"].values())), \
        "Gender harus TIDAK ADA di roster (mahasiswa isi sendiri)"
    assert len(list_kelompok(r)) > 0
    assert len(list_all_peserta(r)) == r["total_mahasiswa"]
    print(f"OK roster — {r['total_mahasiswa']} mhs, "
          f"{len(list_kelompok(r))} kelompok, no gender field")


if __name__ == "__main__":
    test_persona_loads_knowledge_base()
    test_storage_roundtrip()
    test_form_generator()
    test_roster_loader()
    print("\n✅ Semua smoke tests lulus.")
