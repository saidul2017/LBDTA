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
from peserta_loader import (                                 # noqa: E402
    load_roster, list_nim, get_peserta, get_kelompok_anggota,
)

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


@st.cache_resource
def get_roster() -> dict | None:
    return load_roster(REPO_ROOT)


# ============================================================
# Sidebar — login / identitas kelompok
# ============================================================
with st.sidebar:
    st.title("📚 Asisten UAS LBDTA")
    st.caption("Literasi Big Data — Pendidikan Agama Islam")
    st.divider()

    roster = get_roster()
    use_roster = roster is not None

    st.markdown("### Identitas Mahasiswa")

    if use_roster:
        # Mode terkunci: pilih NIM dari roster resmi
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

        if peserta:
            st.success(f"**{peserta['nama']}**")
            kelompok = peserta["kelompok"]
            topik = peserta["topik_uas"]
            st.info(
                f"Kelompok: **{kelompok}**\n\nTopik UAS: **{topik}**"
            )

            # Tampilkan anggota satu kelompok
            anggota_list = get_kelompok_anggota(roster, kelompok)
            with st.expander(f"👥 Anggota Kelompok {kelompok}"):
                for a in anggota_list:
                    st.write(f"- `{a['nim']}` — {a['nama']}")

            # Variabel untuk dipakai create_session
            kelompok_val = kelompok
            anggota_val = "\n".join(
                f"{a['nim']} - {a['nama']}" for a in anggota_list
            )
            topik_val = topik
        else:
            st.info("Pilih NIM Anda untuk memulai.")
            kelompok_val = anggota_val = topik_val = ""
    else:
        # Mode bebas: input manual (jika roster.json tidak ada)
        st.caption("ℹ️ Mode bebas — roster tidak terdeteksi.")
        nim_pilih = st.text_input("NIM Anda", key="nim_input_free")
        kelompok_val = st.text_input(
            "Nomor kelompok",
            placeholder="contoh: K03",
            key="kelompok_input",
        )
        anggota_val = st.text_area(
            "Anggota (1 nama per baris)",
            height=90,
            key="anggota_input",
        )
        topik_val = st.selectbox(
            "Topik UAS",
            [
                "",
                "1. Pemerataan kualitas pembelajaran PAI",
                "2. Sertifikasi guru PAI",
                "3. Investasi infrastruktur digital madrasah",
            ],
            key="topik_input",
        )

    st.divider()

    # Tombol mulai sesi
    siap_mulai = bool(
        (use_roster and peserta) or
        (not use_roster and (kelompok_val or anggota_val))
    )
    if st.button(
        "🆕 Mulai sesi baru",
        type="primary",
        use_container_width=True,
        disabled=not siap_mulai,
    ):
        st.session_state.session_id = storage.create_session(
            kelompok=kelompok_val,
            anggota=anggota_val,
            topik=topik_val,
            provider=get_provider(),
            model=get_model(),
        )
        # Simpan NIM pemicu sesi (audit)
        if nim_pilih:
            storage.add_message(
                st.session_state.session_id,
                "system",
                f"[SESSION_OPENED_BY_NIM={nim_pilih}]",
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
    st.info("👈 **Pilih NIM Anda** dan klik **Mulai sesi baru** dari sidebar.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Cara pakai")
        st.markdown("""
1. **Pilih NIM Anda** di sidebar — nama, kelompok, dan topik UAS
   akan terisi otomatis.
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
                continue  # sembunyikan pesan internal
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
