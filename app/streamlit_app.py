"""Aplikasi chatbot UAS Literasi Big Data PAI — Streamlit (UI mahasiswa).

Jalankan:
    streamlit run app/streamlit_app.py

Lihat app/README.md untuk setup lengkap & deployment.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Pastikan modul lokal di app/ bisa di-import
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from persona import build_system_prompt, list_loaded_files  # noqa: E402
from llm import chat_stream, get_provider, get_model        # noqa: E402
from storage import Storage                                  # noqa: E402
from form_generator import generate_form_markdown            # noqa: E402
from peserta_loader import (                                 # noqa: E402
    load_roster, list_nim, get_peserta, get_kelompok_anggota,
)

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))
KELAS_PASSWORD = os.getenv("KELAS_PASSWORD", "").strip()

# === Konfigurasi halaman ===
st.set_page_config(
    page_title="Asisten UAS LBDTA",
    page_icon="📚",
    layout="wide",
)

# === Inisialisasi state ===
for k, v in {
    "session_id": None,
    "messages": [],
    "kelas_authed": not bool(KELAS_PASSWORD),  # auth bypass jika tidak diset
}.items():
    st.session_state.setdefault(k, v)

storage = Storage(DB_PATH)


@st.cache_resource
def get_system_prompt() -> str:
    return build_system_prompt(REPO_ROOT)


@st.cache_resource
def get_loaded_files() -> list[str]:
    return list_loaded_files(REPO_ROOT)


@st.cache_resource
def get_roster() -> dict | None:
    return load_roster(REPO_ROOT)


# ============================================================
# Auth password kelas (jika dosen mengaktifkan KELAS_PASSWORD)
# ============================================================
def gate_kelas_password() -> None:
    if st.session_state.kelas_authed:
        return
    st.title("🔐 Akses Kelas — UAS LBDTA")
    st.markdown(
        "Aplikasi ini hanya untuk peserta mata kuliah **Literasi Big "
        "Data PAI**. Masukkan password kelas yang diberikan dosen."
    )
    with st.form("login_kelas"):
        pwd = st.text_input("Password kelas", type="password")
        ok = st.form_submit_button("🔓 Masuk", type="primary")
        if ok:
            if pwd == KELAS_PASSWORD:
                st.session_state.kelas_authed = True
                st.rerun()
            else:
                st.error("Password kelas salah. Hubungi dosen pengampu.")
    st.stop()


gate_kelas_password()


# ============================================================
# Sidebar — login / identitas mahasiswa
# ============================================================
with st.sidebar:
    st.title("📚 Asisten UAS LBDTA")
    st.caption("Literasi Big Data — Pendidikan Agama Islam")
    st.divider()

    roster = get_roster()
    use_roster = roster is not None

    st.markdown("### Identitas Mahasiswa")

    if use_roster:
        nim_list = list_nim(roster)
        st.caption(
            f"📋 Roster aktif: **{roster['total_mahasiswa']} mahasiswa** "
            f"(seed `{roster['seed']}`)"
        )
        nim_pilih = st.selectbox(
            "NIM Anda",
            options=[""] + nim_list,
            format_func=lambda x: x if x else "— pilih NIM —",
            key="nim_select",
        )
        peserta = get_peserta(roster, nim_pilih) if nim_pilih else None
    else:
        st.caption("ℹ️ Mode bebas — roster tidak terdeteksi.")
        nim_pilih = st.text_input("NIM Anda", key="nim_input_free")
        peserta = None

    # Input gender — selalu diisi mahasiswa sendiri (tidak dari roster)
    gender_pilih = st.radio(
        "Jenis kelamin",
        options=["", "Laki-laki", "Perempuan", "Tidak ingin menyebut"],
        format_func=lambda x: x if x else "— pilih —",
        horizontal=False,
        key="gender_input",
    )

    if peserta:
        st.success(f"**{peserta['nama']}**")
        kelompok_val = peserta["kelompok"]
        topik_val = peserta["topik_uas"]
        nama_val = peserta["nama"]
        st.info(
            f"Kelompok: **{kelompok_val}**\n\nTopik UAS: **{topik_val}**"
        )
        anggota_list = get_kelompok_anggota(roster, kelompok_val)
        with st.expander(f"👥 Anggota Kelompok {kelompok_val}"):
            for a in anggota_list:
                st.write(f"- `{a['nim']}` — {a['nama']}")
        anggota_val = "\n".join(
            f"{a['nim']} - {a['nama']}" for a in anggota_list
        )
    else:
        if not use_roster:
            kelompok_val = st.text_input(
                "Nomor kelompok", placeholder="contoh: K03"
            )
            anggota_val = st.text_area(
                "Anggota (1 nama per baris)", height=80
            )
            topik_val = st.selectbox(
                "Topik UAS",
                ["",
                 "1. Pemerataan kualitas pembelajaran PAI",
                 "2. Sertifikasi guru PAI",
                 "3. Investasi infrastruktur digital madrasah"],
            )
            nama_val = ""
        else:
            kelompok_val = anggota_val = topik_val = nama_val = ""

    st.divider()

    # Tombol mulai sesi
    siap_mulai = bool(
        gender_pilih and (
            (use_roster and peserta) or
            (not use_roster and (kelompok_val or anggota_val))
        )
    )
    if not gender_pilih and (peserta or kelompok_val or anggota_val):
        st.warning("Mohon pilih jenis kelamin terlebih dahulu.")

    if st.button(
        "🆕 Mulai sesi baru",
        type="primary",
        use_container_width=True,
        disabled=not siap_mulai,
    ):
        # Map gender ke kode singkat untuk konsistensi DB
        gender_code = {
            "Laki-laki": "L",
            "Perempuan": "P",
            "Tidak ingin menyebut": "X",
        }.get(gender_pilih, "")
        st.session_state.session_id = storage.create_session(
            nim=nim_pilih or "",
            nama=nama_val,
            gender=gender_code,
            kelompok=kelompok_val,
            anggota=anggota_val,
            topik=topik_val,
            provider=get_provider(),
            model=get_model(),
        )
        st.session_state.messages = []
        st.rerun()

    if st.session_state.session_id:
        sid = st.session_state.session_id
        st.success(f"Sesi aktif: `{sid[:8]}…`")
        if st.button("🗑️ Akhiri sesi"):
            st.session_state.session_id = None
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.markdown("### Sistem")
    st.caption(f"Provider: **{get_provider()}**")
    st.caption(f"Model: `{get_model()}`")

    with st.expander(f"📂 Basis pengetahuan ({len(get_loaded_files())} berkas)"):
        for f in get_loaded_files():
            st.code(f, language="text")

    with st.expander("📜 7 Aturan Asisten"):
        st.markdown("""
1. Selalu rujuk dokumen di basis pengetahuan
2. Sebut sumber saat mengutip ([berkas])
3. Hati-hati pada isu agama sensitif
4. Pendekatan Socratic — bantu berpikir kritis
5. Jelaskan makna data, bukan hanya hitungan
6. Bahasa Indonesia santun & akademis
7. Tidak mengerjakan seluruh tugas mahasiswa
        """)


# ============================================================
# Konten utama
# ============================================================
st.title("Asisten UAS — Literasi Big Data PAI")

if not st.session_state.session_id:
    st.info(
        "👈 **Pilih NIM, jenis kelamin, lalu klik Mulai sesi baru** dari "
        "sidebar."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Cara pakai")
        st.markdown("""
1. Pilih **NIM** Anda — nama, kelompok, dan topik UAS auto-terisi.
2. Pilih **jenis kelamin** Anda.
3. Klik **🆕 Mulai sesi baru**.
4. Mulai bertanya. Asisten akan **mengajak Anda berpikir**, bukan
   memberi jawaban final.
5. Sebelum submit UAS, unduh **Form Pengungkapan AI** dari tab
   "📋 Form" dan lampirkan ke berkas UAS Anda.
        """)
    with col2:
        st.markdown("### ⚠️ Perhatian")
        st.warning("""
Seluruh interaksi **terekam otomatis** dan akan dilampirkan
sebagai bukti integritas akademik (*ṣidq*) sesuai
**Petunjuk Teknis UAS §7**.

Tidak mengisi *Form Pengungkapan AI* = pelanggaran integritas,
pengurangan **20 poin**.
        """)
    st.stop()

# Sesi aktif — render tabs
tab_chat, tab_history, tab_form = st.tabs([
    "💬 Chat",
    "📜 Riwayat lengkap",
    "📋 Form Pengungkapan AI",
])

# ---------- Tab Chat ----------
with tab_chat:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Tanyakan sesuatu (mis. 'apa itu confounder?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        storage.add_message(st.session_state.session_id, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            try:
                for chunk in chat_stream(
                    get_system_prompt(),
                    st.session_state.messages,
                ):
                    full += chunk
                    placeholder.markdown(full + "▌")
                placeholder.markdown(full)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full}
                )
                storage.add_message(
                    st.session_state.session_id, "assistant", full
                )
            except Exception as e:
                err = (
                    f"⚠️ **Error LLM:** `{type(e).__name__}: {e}`\n\n"
                    "Periksa API key di `.env` (atau Secrets di Streamlit "
                    "Cloud). Lihat `app/README.md` untuk panduan."
                )
                placeholder.error(err)


# ---------- Tab Riwayat ----------
with tab_history:
    msgs = storage.get_messages(st.session_state.session_id)
    if not msgs:
        st.info("Belum ada interaksi pada sesi ini.")
    else:
        st.markdown(f"**Total pesan tersimpan:** {len(msgs)}")
        st.caption(
            "Sumber: SQLite. Riwayat ini juga akan tampil di Form "
            "Pengungkapan AI sebagai lampiran resmi UAS."
        )
        for m in msgs:
            if m["role"] == "system":
                continue
            with st.chat_message(m["role"]):
                st.caption(m.get("created_at", ""))
                st.markdown(m["content"])


# ---------- Tab Form ----------
with tab_form:
    session = storage.get_session(st.session_state.session_id)
    msgs = [
        m for m in storage.get_messages(st.session_state.session_id)
        if m["role"] != "system"
    ]

    if not session:
        st.error("Sesi tidak ditemukan.")
    elif not msgs:
        st.info(
            "Form akan ter-generate setelah Anda berinteraksi dengan "
            "asisten. Silakan kembali ke tab 💬 Chat."
        )
    else:
        form_md = generate_form_markdown(session, msgs)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button(
                "⬇️ Unduh Form (Markdown)",
                data=form_md,
                file_name=f"form-pengungkapan-ai-{session['id'][:8]}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col2:
            st.caption(
                "Konversi ke PDF: buka di editor markdown "
                "(VS Code, Typora) → Print → Save as PDF."
            )
        st.divider()
        st.markdown(form_md)
