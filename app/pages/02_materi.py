"""Halaman Materi Belajar Mandiri.

Mahasiswa membaca modul M01-M03 langsung di app, tanpa perlu ke GitHub.
Progress baca tersimpan per NIM ke SQLite.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from storage import Storage             # noqa: E402
from peserta_loader import load_roster, list_nim, get_peserta  # noqa: E402

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))
KELAS_PASSWORD = os.getenv("KELAS_PASSWORD", "").strip()

st.set_page_config(
    page_title="Materi Belajar — UAS LBDTA",
    page_icon="📚",
    layout="wide",
)

# === Auth gate kelas (sama seperti streamlit_app.py) ===
if "kelas_authed" not in st.session_state:
    st.session_state.kelas_authed = not bool(KELAS_PASSWORD)
if "nim_aktif" not in st.session_state:
    st.session_state.nim_aktif = ""

if not st.session_state.kelas_authed:
    st.title("🔐 Akses Kelas — UAS LBDTA")
    with st.form("login_kelas_materi"):
        pwd = st.text_input("Password kelas", type="password")
        if st.form_submit_button("Masuk", type="primary"):
            if pwd == KELAS_PASSWORD:
                st.session_state.kelas_authed = True
                st.rerun()
            else:
                st.error("Password salah.")
    st.stop()

storage = Storage(DB_PATH)
roster = load_roster(REPO_ROOT)


# === Sidebar: pilih NIM (sinkron dengan halaman lain) ===
with st.sidebar:
    st.title("📚 Materi UAS LBDTA")
    st.caption("Halaman belajar mandiri")
    st.divider()
    if roster:
        nim_list = list_nim(roster)
        nim = st.selectbox(
            "NIM Anda",
            options=[""] + nim_list,
            index=(nim_list.index(st.session_state.nim_aktif) + 1
                   if st.session_state.nim_aktif in nim_list else 0),
            format_func=lambda x: x if x else "— pilih NIM —",
            key="materi_nim_select",
        )
        st.session_state.nim_aktif = nim
        peserta = get_peserta(roster, nim) if nim else None
        if peserta:
            st.success(peserta["nama"])
            st.caption(f"Kelompok {peserta['kelompok']}")
    else:
        nim = st.text_input("NIM", value=st.session_state.nim_aktif)
        st.session_state.nim_aktif = nim
        peserta = None


# === Konten utama ===
st.title("📚 Materi Belajar Mandiri")
st.markdown(
    "Baca modul-modul ini sebelum mengerjakan kuis di halaman "
    "**📝 Kuis Interaktif**."
)

if not st.session_state.nim_aktif:
    st.info("👈 Pilih NIM Anda di sidebar untuk mulai belajar.")
    st.stop()

# Modul yang tersedia
MODULS = [
    ("M01", "M01 — Pondasi Literasi Data",
     "Konsep big data, lanskap data PAI, etika pengantar, kritik AI",
     "modul/M01-pondasi-literasi-data.md"),
    ("M02", "M02 — Praktik Analisis Data",
     "Cleaning, statistika deskriptif, visualisasi",
     "modul/M02-praktik-analisis-data.md"),
    ("M03", "M03 — Sintesis Etika & Kebijakan",
     "Confounder, maqāṣid, ghībah, policy brief",
     "modul/M03-sintesis-etika-dan-kebijakan.md"),
]

# Status baca per modul
sudah_dibaca = set(storage.list_modul_dibaca(st.session_state.nim_aktif))

# Tab per modul
tabs = st.tabs([f"{m[0]} {'✅' if m[0] in sudah_dibaca else '⏳'}"
                for m in MODULS])

for tab, (kode, judul, deskripsi, path) in zip(tabs, MODULS):
    with tab:
        st.markdown(f"## {judul}")
        st.caption(deskripsi)
        st.divider()

        modul_file = REPO_ROOT / path
        if modul_file.exists():
            content = modul_file.read_text(encoding="utf-8")
            # Skip header h1 (sudah ditampilkan sebagai title)
            lines = content.split("\n")
            if lines and lines[0].startswith("# "):
                content = "\n".join(lines[1:])
            st.markdown(content)
        else:
            st.error(f"Berkas `{path}` tidak ditemukan.")

        st.divider()
        col1, col2 = st.columns([2, 1])
        with col1:
            if kode in sudah_dibaca:
                st.success(f"✅ Modul {kode} sudah Anda tandai sebagai dibaca.")
            else:
                if st.button(f"✅ Tandai {kode} sebagai sudah dibaca",
                             key=f"mark_{kode}", type="primary"):
                    storage.mark_modul_dibaca(
                        st.session_state.nim_aktif, kode
                    )
                    st.rerun()
        with col2:
            st.caption("Lanjut ke kuis di halaman **📝 Kuis Interaktif**.")

# === Ringkasan progres ===
st.divider()
st.markdown("### 📊 Ringkasan Progres Materi Anda")
total = len(MODULS)
selesai = len(sudah_dibaca)
st.progress(selesai / total if total else 0,
            text=f"{selesai} dari {total} modul selesai dibaca")
