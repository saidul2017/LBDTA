"""Halaman Kuis Interaktif (Kahoot-style).

Mahasiswa kerjakan kuis per modul. Soal satu per satu dengan instant
feedback. Skor terbaik tersimpan, mahasiswa boleh ulang.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from storage import Storage             # noqa: E402
from peserta_loader import load_roster, list_nim, get_peserta  # noqa: E402
from quiz_data import (                 # noqa: E402
    QUIZ_BY_MODUL, get_quiz, total_soal, get_modul_list,
)

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))
KELAS_PASSWORD = os.getenv("KELAS_PASSWORD", "").strip()

st.set_page_config(
    page_title="Kuis Interaktif — UAS LBDTA",
    page_icon="📝",
    layout="centered",
)

# === Auth gate ===
if "kelas_authed" not in st.session_state:
    st.session_state.kelas_authed = not bool(KELAS_PASSWORD)
if "nim_aktif" not in st.session_state:
    st.session_state.nim_aktif = ""

if not st.session_state.kelas_authed:
    st.title("🔐 Akses Kelas — UAS LBDTA")
    with st.form("login_kelas_kuis"):
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


# === Inisialisasi state kuis ===
QUIZ_KEYS = ["quiz_state", "quiz_modul", "quiz_idx", "quiz_jawaban",
             "quiz_benar", "quiz_start_time"]
for k in QUIZ_KEYS:
    if k not in st.session_state:
        st.session_state[k] = None

if st.session_state.quiz_state is None:
    st.session_state.quiz_state = "pilih"  # pilih → soal → feedback → selesai


def reset_quiz() -> None:
    for k in QUIZ_KEYS:
        st.session_state[k] = None
    st.session_state.quiz_state = "pilih"


# === Sidebar ===
with st.sidebar:
    st.title("📝 Kuis Interaktif")
    st.caption("Kahoot-style, ulang sebanyak mau")
    st.divider()

    if roster:
        nim_list = list_nim(roster)
        nim = st.selectbox(
            "NIM Anda",
            options=[""] + nim_list,
            index=(nim_list.index(st.session_state.nim_aktif) + 1
                   if st.session_state.nim_aktif in nim_list else 0),
            format_func=lambda x: x if x else "— pilih NIM —",
            key="kuis_nim_select",
        )
        st.session_state.nim_aktif = nim
        peserta = get_peserta(roster, nim) if nim else None
        if peserta:
            st.success(peserta["nama"])
    else:
        nim = st.text_input("NIM", value=st.session_state.nim_aktif)
        st.session_state.nim_aktif = nim
        peserta = None

    st.divider()
    st.markdown("### Skor Saya")
    if st.session_state.nim_aktif:
        skor_list = storage.list_kuis_skor_per_nim(st.session_state.nim_aktif)
        if skor_list:
            for s in skor_list:
                st.metric(
                    s["modul"],
                    f"{s['persen']:.0f}/100",
                    f"{s['attempts']}× attempt",
                )
        else:
            st.caption("Belum kerjakan kuis.")


# === Konten utama ===
nim = st.session_state.nim_aktif

if not nim:
    st.title("📝 Kuis Interaktif")
    st.info("👈 Pilih NIM Anda di sidebar untuk mulai kuis.")
    st.stop()

# ============================================================
# STATE: pilih modul
# ============================================================
if st.session_state.quiz_state == "pilih":
    st.title("📝 Kuis Interaktif — Pilih Modul")
    st.markdown(
        "Pilih modul yang ingin Anda kerjakan. Anda dapat mengulang "
        "sebanyak yang Anda mau — **skor terbaik** akan tersimpan."
    )

    for kode in get_modul_list():
        q = get_quiz(kode)
        existing = storage.get_kuis_skor(nim, kode)

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### {q['judul']}")
                st.caption(q["deskripsi"])
                st.caption(f"📊 {len(q['soal'])} soal pilihan ganda")
            with col2:
                if existing:
                    st.metric(
                        "Skor terbaik",
                        f"{existing['persen']:.0f}/100",
                        f"{existing['attempts']}× coba",
                    )
                else:
                    st.caption("Belum dikerjakan")

            if st.button(
                f"▶️ Mulai Kuis {kode}",
                key=f"start_{kode}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.quiz_state = "soal"
                st.session_state.quiz_modul = kode
                st.session_state.quiz_idx = 0
                st.session_state.quiz_jawaban = []
                st.session_state.quiz_benar = 0
                st.session_state.quiz_start_time = time.time()
                st.rerun()

    st.divider()
    st.caption(
        "💡 **Tips:** Baca modul dulu di halaman **📚 Materi Belajar** "
        "sebelum mengerjakan kuis. Bobot kuis = **10%** nilai akhir UAS."
    )


# ============================================================
# STATE: soal (jawab) atau feedback (lihat hasil)
# ============================================================
elif st.session_state.quiz_state in ("soal", "feedback"):
    modul = st.session_state.quiz_modul
    q = get_quiz(modul)
    idx = st.session_state.quiz_idx
    soal_list = q["soal"]
    s = soal_list[idx]

    # Header progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption(f"**{q['judul']}**")
    with col2:
        st.caption(f"Soal **{idx + 1} / {len(soal_list)}**")
    with col3:
        st.caption(f"✅ Benar: **{st.session_state.quiz_benar}**")

    st.progress((idx + 1) / len(soal_list))
    st.divider()

    # Soal
    st.markdown(f"### {s['soal']}")
    st.write("")

    if st.session_state.quiz_state == "soal":
        # Mode jawab
        with st.form(f"q_{modul}_{idx}"):
            pilihan = st.radio(
                "Pilih jawaban Anda:",
                options=range(4),
                format_func=lambda i: f"{chr(65+i)}. {s['opsi'][i]}",
                index=None,
                key=f"radio_{modul}_{idx}",
            )
            submit = st.form_submit_button(
                "📤 Submit Jawaban", type="primary",
                use_container_width=True,
                disabled=False,
            )

            if submit:
                if pilihan is None:
                    st.warning("Pilih salah satu jawaban dulu.")
                else:
                    st.session_state.quiz_jawaban.append(pilihan)
                    if pilihan == s["jawaban"]:
                        st.session_state.quiz_benar += 1
                    st.session_state.quiz_state = "feedback"
                    st.rerun()

    else:  # feedback
        # Mode tampilkan hasil
        jawaban_user = st.session_state.quiz_jawaban[-1]
        is_benar = jawaban_user == s["jawaban"]

        if is_benar:
            st.success(
                f"✅ **BENAR!** Jawaban: **{chr(65 + s['jawaban'])}. "
                f"{s['opsi'][s['jawaban']]}**"
            )
        else:
            st.error(
                f"❌ **Salah.** Jawaban Anda: "
                f"{chr(65 + jawaban_user)}. {s['opsi'][jawaban_user]}"
            )
            st.info(
                f"✅ **Jawaban benar:** {chr(65 + s['jawaban'])}. "
                f"{s['opsi'][s['jawaban']]}"
            )

        with st.expander("💡 **Penjelasan**", expanded=True):
            st.markdown(s["penjelasan"])
            st.caption(f"📖 Rujukan: `{s['rujukan']}`")

        st.write("")
        # Tombol next
        if idx + 1 < len(soal_list):
            if st.button("➡️ Soal Berikutnya", type="primary",
                         use_container_width=True):
                st.session_state.quiz_idx += 1
                st.session_state.quiz_state = "soal"
                st.rerun()
        else:
            if st.button("🏁 Lihat Hasil Akhir", type="primary",
                         use_container_width=True):
                st.session_state.quiz_state = "selesai"
                # Simpan skor
                waktu = int(time.time() - st.session_state.quiz_start_time)
                hasil = storage.save_kuis_skor(
                    nim=nim,
                    modul=modul,
                    skor=st.session_state.quiz_benar,
                    total_soal=len(soal_list),
                    waktu_detik=waktu,
                )
                st.session_state.quiz_hasil = hasil
                st.rerun()


# ============================================================
# STATE: selesai
# ============================================================
elif st.session_state.quiz_state == "selesai":
    modul = st.session_state.quiz_modul
    q = get_quiz(modul)
    benar = st.session_state.quiz_benar
    total = len(q["soal"])
    persen = round(benar / total * 100, 1)
    waktu = int(time.time() - st.session_state.quiz_start_time)
    hasil = st.session_state.get("quiz_hasil", {})

    st.title("🏁 Hasil Kuis")
    st.markdown(f"### {q['judul']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Skor", f"{benar}/{total}")
    col2.metric("Persen", f"{persen:.0f}/100")
    col3.metric("Waktu", f"{waktu // 60}m {waktu % 60}d")
    col4.metric("Status", "✅ Lulus" if persen >= 70 else "⚠️ Coba lagi")

    if hasil.get("is_pb"):
        if hasil.get("is_new"):
            st.success("🎉 **Skor pertama Anda tercatat!**")
        else:
            st.success(
                f"🎉 **Personal Best baru!** Skor sebelumnya: "
                f"{hasil.get('skor_lama')}/{total} → sekarang {benar}/{total}"
            )
    else:
        st.info(
            f"Skor terbaik Anda tetap **{hasil.get('skor_lama')}/{total}** "
            f"(attempt ini: {benar}/{total})."
        )

    st.divider()

    if persen == 100:
        st.balloons()
        st.success(
            "🌟 **Sempurna!** Anda menguasai modul ini. "
            "Lanjut ke modul berikutnya."
        )
    elif persen >= 80:
        st.success(
            "👏 **Sangat baik.** Pemahaman Anda kuat. Coba ulang untuk "
            "score sempurna kalau ada waktu."
        )
    elif persen >= 70:
        st.info(
            "👍 **Lulus.** Pemahaman cukup. Ada baiknya baca ulang bagian "
            "yang Anda belum kuasai."
        )
    elif persen >= 50:
        st.warning(
            "⚠️ **Perlu belajar lagi.** Baca modul lebih teliti, lalu "
            "coba lagi. Anda bisa lakukan ini."
        )
    else:
        st.error(
            "❌ **Belum lulus.** Sebaiknya baca modul dulu di halaman "
            "**📚 Materi Belajar**, lalu kembali ke kuis ini."
        )

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔁 Ulang Kuis Ini", type="primary",
                     use_container_width=True):
            reset_quiz()
            st.session_state.quiz_state = "soal"
            st.session_state.quiz_modul = modul
            st.session_state.quiz_idx = 0
            st.session_state.quiz_jawaban = []
            st.session_state.quiz_benar = 0
            st.session_state.quiz_start_time = time.time()
            st.rerun()
    with col2:
        if st.button("📚 Pilih Modul Lain", use_container_width=True):
            reset_quiz()
            st.rerun()
    with col3:
        if st.button("📊 Lihat Progres", use_container_width=True):
            st.switch_page("pages/04_progres_saya.py")
