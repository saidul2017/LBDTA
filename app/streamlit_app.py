"""Aplikasi chatbot UAS Literasi Big Data PAI — Streamlit.

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

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))

# === Konfigurasi halaman ===
st.set_page_config(
    page_title="Asisten UAS LBDTA",
    page_icon="📚",
    layout="wide",
)

# === Inisialisasi state ===
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

storage = Storage(DB_PATH)


@st.cache_resource
def get_system_prompt() -> str:
    return build_system_prompt(REPO_ROOT)


@st.cache_resource
def get_loaded_files() -> list[str]:
    return list_loaded_files(REPO_ROOT)


# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.title("📚 Asisten UAS LBDTA")
    st.caption("Literasi Big Data — Pendidikan Agama Islam")
    st.divider()

    st.markdown("### Identitas Kelompok")
    kelompok = st.text_input(
        "Nomor kelompok",
        key="kelompok_input",
        placeholder="contoh: 03",
    )
    anggota = st.text_area(
        "Anggota (1 nama per baris)",
        key="anggota_input",
        height=90,
        placeholder="Ahmad Fulan\nFatimah binti X\n...",
    )
    topik = st.selectbox(
        "Topik UAS",
        [
            "",
            "1. Pemerataan kualitas pembelajaran PAI",
            "2. Sertifikasi guru PAI",
            "3. Investasi infrastruktur digital madrasah",
        ],
        key="topik_input",
    )

    if st.button("🆕 Mulai sesi baru", type="primary", use_container_width=True):
        if not kelompok and not anggota:
            st.warning("Mohon isi minimal nomor kelompok atau anggota.")
        else:
            st.session_state.session_id = storage.create_session(
                kelompok=kelompok,
                anggota=anggota,
                topik=topik,
                provider=get_provider(),
                model=get_model(),
            )
            st.session_state.messages = []
            st.rerun()

    if st.session_state.session_id:
        # auto-update identitas jika diubah
        storage.update_session(
            st.session_state.session_id,
            kelompok=kelompok,
            anggota=anggota,
            topik=topik,
        )
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
    st.info("👈 **Mulai sesi baru** dari sidebar setelah mengisi identitas kelompok.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Cara pakai")
        st.markdown("""
1. Isi **nomor kelompok**, **anggota**, dan **topik UAS** di sidebar.
2. Klik **🆕 Mulai sesi baru**.
3. Mulai bertanya. Asisten akan **mengajak Anda berpikir**, bukan
   memberi jawaban final.
4. Sebelum submit UAS, unduh **Form Pengungkapan AI** dari tab
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
    # Tampilkan riwayat sesi aktif
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Tanyakan sesuatu (mis. 'apa itu confounder?')"):
        # 1. Catat & tampilkan pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        storage.add_message(st.session_state.session_id, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Stream balasan asisten
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
            with st.chat_message(m["role"]):
                st.caption(m.get("created_at", ""))
                st.markdown(m["content"])


# ---------- Tab Form ----------
with tab_form:
    session = storage.get_session(st.session_state.session_id)
    msgs = storage.get_messages(st.session_state.session_id)

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
