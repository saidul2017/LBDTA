"""Halaman Progres Saya — dashboard pribadi mahasiswa.

Mahasiswa lihat ringkasan: progres baca materi, skor kuis, perbandingan
dengan rata-rata kelas.
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
from quiz_data import get_modul_list, get_quiz, total_soal  # noqa: E402

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))
KELAS_PASSWORD = os.getenv("KELAS_PASSWORD", "").strip()

st.set_page_config(
    page_title="Progres Saya — UAS LBDTA",
    page_icon="📊",
    layout="wide",
)

# === Auth gate ===
if "kelas_authed" not in st.session_state:
    st.session_state.kelas_authed = not bool(KELAS_PASSWORD)
if "nim_aktif" not in st.session_state:
    st.session_state.nim_aktif = ""

if not st.session_state.kelas_authed:
    st.title("🔐 Akses Kelas — UAS LBDTA")
    with st.form("login_kelas_progres"):
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


# === Sidebar ===
with st.sidebar:
    st.title("📊 Progres Saya")
    st.divider()
    if roster:
        nim_list = list_nim(roster)
        nim = st.selectbox(
            "NIM Anda",
            options=[""] + nim_list,
            index=(nim_list.index(st.session_state.nim_aktif) + 1
                   if st.session_state.nim_aktif in nim_list else 0),
            format_func=lambda x: x if x else "— pilih NIM —",
            key="progres_nim_select",
        )
        st.session_state.nim_aktif = nim
        peserta = get_peserta(roster, nim) if nim else None
        if peserta:
            st.success(peserta["nama"])
            st.caption(
                f"Kelompok {peserta['kelompok']} | "
                f"{peserta['topik_uas']}"
            )
    else:
        nim = st.text_input("NIM", value=st.session_state.nim_aktif)
        st.session_state.nim_aktif = nim
        peserta = None


# === Konten utama ===
nim = st.session_state.nim_aktif
if not nim:
    st.title("📊 Progres Saya")
    st.info("👈 Pilih NIM Anda di sidebar.")
    st.stop()

st.title(f"📊 Progres Belajar — {nim}")
if peserta:
    st.caption(
        f"**{peserta['nama']}** | Kelompok **{peserta['kelompok']}** | "
        f"Topik UAS: {peserta['topik_uas']}"
    )

st.divider()

# === Ringkasan progres ===
modul_dibaca = set(storage.list_modul_dibaca(nim))
skor_list = storage.list_kuis_skor_per_nim(nim)
skor_per_modul = {s["modul"]: s for s in skor_list}

modul_kodes = get_modul_list()
total_modul = len(modul_kodes)
selesai_baca = sum(1 for k in modul_kodes if k in modul_dibaca)
selesai_kuis = sum(
    1 for k in modul_kodes
    if k in skor_per_modul and skor_per_modul[k]["persen"] >= 70
)

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "📖 Modul dibaca",
    f"{selesai_baca}/{total_modul}",
    f"{selesai_baca/total_modul*100:.0f}%",
)
col2.metric(
    "🎯 Kuis lulus (≥70)",
    f"{selesai_kuis}/{total_modul}",
    f"{selesai_kuis/total_modul*100:.0f}%",
)
rata_persen = (
    sum(s["persen"] for s in skor_list) / len(skor_list)
    if skor_list else 0
)
col3.metric(
    "📊 Rata-rata skor kuis",
    f"{rata_persen:.0f}/100" if skor_list else "—",
)
total_attempt = sum(s["attempts"] for s in skor_list)
col4.metric("🔁 Total attempt", total_attempt if skor_list else "—")

st.divider()

# === Tabel detail per modul ===
st.markdown("### Detail Per Modul")
detail_rows = []
for kode in modul_kodes:
    q = get_quiz(kode)
    skor = skor_per_modul.get(kode)
    detail_rows.append({
        "Modul": q["judul"],
        "Baca": "✅" if kode in modul_dibaca else "⏳",
        "Skor Kuis": (
            f"{skor['skor']}/{skor['total_soal']} ({skor['persen']:.0f}%)"
            if skor else "—"
        ),
        "Status Kuis": (
            "✅ Lulus" if skor and skor["persen"] >= 70
            else "⚠️ <70" if skor else "—"
        ),
        "Attempt": skor["attempts"] if skor else "—",
    })

st.dataframe(detail_rows, use_container_width=True, hide_index=True)

# === Perbandingan dengan kelas ===
st.divider()
st.markdown("### 📈 Perbandingan dengan Rata-rata Kelas")

all_skor = storage.list_all_kuis_skor()
if all_skor and roster:
    rata_kelas_per_modul: dict = {}
    for s in all_skor:
        rata_kelas_per_modul.setdefault(s["modul"], []).append(s["persen"])
    chart_data = {}
    for kode in modul_kodes:
        kelas_list = rata_kelas_per_modul.get(kode, [])
        rata_kelas = sum(kelas_list) / len(kelas_list) if kelas_list else 0
        saya = (
            skor_per_modul[kode]["persen"]
            if kode in skor_per_modul else 0
        )
        chart_data[kode] = {"Anda": saya, "Rata-rata kelas": rata_kelas}
    st.bar_chart(chart_data)
else:
    st.info(
        "Data perbandingan akan tampil setelah mahasiswa lain juga "
        "mulai mengerjakan kuis."
    )

# === Sertifikat ===
st.divider()
st.markdown("### 🏆 Sertifikat Penyelesaian")
if selesai_kuis == total_modul and selesai_baca == total_modul:
    st.balloons()
    st.success(
        "🌟 **SELAMAT!** Anda telah menyelesaikan SEMUA modul + kuis "
        "dengan skor ≥70. Tinggal lanjutkan ke pengerjaan UAS "
        "*Policy Brief* (T03)."
    )
else:
    sisa_baca = [k for k in modul_kodes if k not in modul_dibaca]
    sisa_kuis = [
        k for k in modul_kodes
        if k not in skor_per_modul or skor_per_modul[k]["persen"] < 70
    ]
    if sisa_baca:
        st.info(f"📖 Belum baca modul: {', '.join(sisa_baca)}")
    if sisa_kuis:
        st.info(
            f"🎯 Kuis belum lulus (skor <70): "
            f"{', '.join(sisa_kuis)}"
        )

# === Action ===
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📚 Buka Materi", use_container_width=True):
        st.switch_page("pages/02_materi.py")
with col2:
    if st.button("📝 Kerjakan Kuis", use_container_width=True):
        st.switch_page("pages/03_kuis.py")
with col3:
    if st.button("💬 Diskusi dengan AI", use_container_width=True):
        st.switch_page("streamlit_app.py")
