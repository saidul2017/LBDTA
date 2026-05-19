"""Dasbor Dosen — Halaman audit & monitoring UAS.

Diakses dari sidebar Streamlit setelah `streamlit run app/streamlit_app.py`.
Dilindungi password (`DOSEN_PASSWORD` di .env atau Streamlit secrets).

Fitur:
- Statistik agregat (sesi, pesan, mahasiswa aktif, kelompok aktif)
- Visualisasi: distribusi sesi per topik, per kelompok, gender mahasiswa,
  volume pesan harian
- Tabel sesi dengan filter (kelompok, topik, min. pesan)
- Detail per sesi (transkrip + form pengungkapan AI)
- Daftar mahasiswa belum pakai chatbot
- Ekspor CSV semua sesi + ZIP semua form pengungkapan AI
"""
from __future__ import annotations

import io
import os
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from storage import Storage                           # noqa: E402
from peserta_loader import (                          # noqa: E402
    load_roster, list_all_peserta, list_kelompok,
)
from form_generator import generate_form_markdown, GENDER_LABEL  # noqa: E402

load_dotenv()

REPO_ROOT = HERE.parent
DEFAULT_DB = HERE / "data" / "sessions.db"
DB_PATH = Path(os.getenv("DB_PATH", DEFAULT_DB))

st.set_page_config(
    page_title="Dasbor Dosen — UAS LBDTA",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# Auth gate
# ============================================================
def check_password() -> None:
    expected = os.getenv("DOSEN_PASSWORD", "").strip()
    if not expected:
        st.error(
            "🔒 **Dasbor dosen belum dikonfigurasi.**\n\n"
            "Set `DOSEN_PASSWORD` di `.env` (lokal) atau Streamlit "
            "Secrets (cloud). Lihat `app/README.md` untuk panduan."
        )
        st.stop()

    if st.session_state.get("dosen_authed"):
        return

    st.title("🎓 Dasbor Dosen — UAS LBDTA")
    with st.form("login_dosen"):
        st.markdown("Masukkan password untuk mengakses dasbor.")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("🔓 Masuk", type="primary"):
            if pwd == expected:
                st.session_state.dosen_authed = True
                st.rerun()
            else:
                st.error("Password salah.")
    st.stop()


check_password()


# ============================================================
# Setup data
# ============================================================
storage = Storage(DB_PATH)
roster = load_roster(REPO_ROOT)
sesi_list = storage.list_sessions()


def hitung_durasi(messages: list[dict]) -> str:
    if len(messages) < 2:
        return "-"
    try:
        first = datetime.fromisoformat(messages[0]["created_at"])
        last = datetime.fromisoformat(messages[-1]["created_at"])
        delta = last - first
        mins = int(delta.total_seconds() // 60)
        if mins < 60:
            return f"{mins} mnt"
        return f"{mins // 60}j {mins % 60}m"
    except Exception:
        return "-"


# Susun baris untuk tabel
rows = []
nim_aktif = set()
for s in sesi_list:
    msgs = storage.get_messages(s["id"])
    msgs_visible = [m for m in msgs if m["role"] != "system"]
    nim = s.get("nim") or ""
    if nim:
        nim_aktif.add(nim)
    rows.append({
        "id": s["id"],
        "id_short": s["id"][:8],
        "created_at": s["created_at"],
        "nim": nim or "-",
        "nama": s.get("nama") or "-",
        "gender": s.get("gender") or "",
        "kelompok": s["kelompok"] or "-",
        "topik": (s["topik"] or "-").split(".")[0],
        "topik_full": s["topik"] or "-",
        "jumlah_pesan": len(msgs_visible),
        "durasi": hitung_durasi(msgs),
        "provider": s.get("provider", "-"),
    })


# ============================================================
# Header & metrik
# ============================================================
col_title, col_logout = st.columns([4, 1])
with col_title:
    st.title("🎓 Dasbor Dosen — UAS LBDTA")
    st.caption(
        f"DB: `{DB_PATH}` · "
        f"Update: {datetime.now(timezone.utc).isoformat(timespec='seconds')}"
    )
with col_logout:
    if st.button("🚪 Keluar"):
        st.session_state.dosen_authed = False
        st.rerun()

st.divider()

total_sesi = len(rows)
total_pesan = sum(r["jumlah_pesan"] for r in rows)
total_mahasiswa = roster["total_mahasiswa"] if roster else 0
mhs_aktif = len(nim_aktif)
kel_aktif = len({r["kelompok"] for r in rows if r["kelompok"] != "-"})
total_kelompok = len(list_kelompok(roster)) if roster else 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Sesi UAS", total_sesi)
m2.metric("Total pesan", total_pesan)
m3.metric(
    "Mhs aktif",
    f"{mhs_aktif}/{total_mahasiswa}" if total_mahasiswa else mhs_aktif,
    f"{mhs_aktif/total_mahasiswa*100:.0f}%" if total_mahasiswa else None,
)
m4.metric(
    "Kelompok aktif",
    f"{kel_aktif}/{total_kelompok}" if total_kelompok else kel_aktif,
)
m5.metric(
    "Pesan/sesi",
    f"{total_pesan/total_sesi:.1f}" if total_sesi else "-",
)

st.divider()


# ============================================================
# Tab utama
# ============================================================
tab_viz, tab_sesi, tab_belum, tab_detail, tab_export = st.tabs([
    "📊 Statistik",
    "📋 Daftar Sesi",
    "🚫 Belum Pakai",
    "🔎 Detail Sesi",
    "💾 Ekspor",
])

# ----- Visualisasi -----
with tab_viz:
    if not rows:
        st.info("Belum ada data untuk divisualisasikan.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Sesi per Topik UAS")
            topik_count = Counter(r["topik"] for r in rows)
            chart_topik = {f"Topik {k}": v for k, v in sorted(topik_count.items())}
            st.bar_chart(chart_topik)

        with c2:
            st.markdown("#### Sesi per Kelompok")
            kel_count = Counter(r["kelompok"] for r in rows)
            chart_kel = dict(sorted(kel_count.items()))
            st.bar_chart(chart_kel)

        c3, c4 = st.columns(2)

        with c3:
            st.markdown("#### Distribusi Gender Mahasiswa Aktif")
            st.caption("_Diisi sendiri oleh mahasiswa saat membuka sesi._")
            gender_counts = Counter()
            seen_nim = set()
            for r in rows:
                if r["nim"] != "-" and r["nim"] not in seen_nim:
                    seen_nim.add(r["nim"])
                    label = GENDER_LABEL.get(r["gender"], "Belum diisi")
                    gender_counts[label] += 1
            if gender_counts:
                st.bar_chart(dict(gender_counts))
            else:
                st.info("Belum ada data gender.")

        with c4:
            st.markdown("#### Volume Pesan per Hari")
            daily = defaultdict(int)
            for r in rows:
                date_str = r["created_at"][:10]
                daily[date_str] += r["jumlah_pesan"]
            if daily:
                chart_daily = dict(sorted(daily.items()))
                st.bar_chart(chart_daily)
            else:
                st.info("Belum ada interaksi.")

        st.markdown("#### Volume Pesan per Kelompok")
        msg_per_kel = defaultdict(int)
        for r in rows:
            msg_per_kel[r["kelompok"]] += r["jumlah_pesan"]
        if msg_per_kel:
            chart_msg = dict(sorted(msg_per_kel.items()))
            st.bar_chart(chart_msg)


# ----- Daftar sesi -----
with tab_sesi:
    if not rows:
        st.info("Belum ada sesi yang tercatat.")
    else:
        c1, c2, c3 = st.columns(3)
        kelompok_filter = c1.multiselect(
            "Kelompok",
            sorted({r["kelompok"] for r in rows}),
        )
        topik_filter = c2.multiselect(
            "Topik (1/2/3)",
            sorted({r["topik"] for r in rows}),
        )
        min_pesan = c3.number_input("Min. pesan", min_value=0, value=0)

        filtered = [
            r for r in rows
            if (not kelompok_filter or r["kelompok"] in kelompok_filter)
            and (not topik_filter or r["topik"] in topik_filter)
            and r["jumlah_pesan"] >= min_pesan
        ]

        st.markdown(f"**Menampilkan {len(filtered)} dari {len(rows)} sesi**")
        display_rows = [
            {
                "ID": r["id_short"],
                "Tanggal": r["created_at"][:19].replace("T", " "),
                "NIM": r["nim"],
                "Nama": r["nama"],
                "Gender": GENDER_LABEL.get(r["gender"], "—"),
                "Kelompok": r["kelompok"],
                "Topik": r["topik"],
                "Pesan": r["jumlah_pesan"],
                "Durasi": r["durasi"],
            }
            for r in filtered
        ]
        st.dataframe(display_rows, use_container_width=True, hide_index=True)


# ----- Belum pakai -----
with tab_belum:
    if not roster:
        st.warning(
            "Roster tidak terdeteksi. Pastikan `peserta/roster.json` ada."
        )
    else:
        all_peserta = list_all_peserta(roster)
        belum = [p for p in all_peserta if p["nim"] not in nim_aktif]
        sudah = [p for p in all_peserta if p["nim"] in nim_aktif]
        st.markdown(
            f"**{len(sudah)} sudah pakai · {len(belum)} belum pakai**"
        )
        if belum:
            st.markdown("### Mahasiswa yang BELUM membuka sesi chatbot")
            display_belum = [
                {
                    "NIM": p["nim"],
                    "Nama": p["nama"],
                    "Kelompok": p["kelompok"],
                    "Topik": p["topik_uas"].split(".")[0],
                }
                for p in belum
            ]
            st.dataframe(
                display_belum,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("✅ Semua mahasiswa sudah membuka sesi chatbot.")


# ----- Detail sesi -----
with tab_detail:
    if not rows:
        st.info("Belum ada sesi.")
    else:
        labels = [
            f"{r['id_short']} — {r['kelompok']} — "
            f"{r['nim']} ({r['nama'][:20]}) — {r['jumlah_pesan']} pesan"
            for r in rows
        ]
        idx = st.selectbox(
            "Pilih sesi",
            range(len(rows)),
            format_func=lambda i: labels[i],
        )
        r = rows[idx]
        sess = storage.get_session(r["id"])
        msgs_all = storage.get_messages(r["id"])
        msgs_visible = [m for m in msgs_all if m["role"] != "system"]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Metadata sesi")
            st.json({
                "id": sess["id"],
                "nim": sess.get("nim", ""),
                "nama": sess.get("nama", ""),
                "gender": GENDER_LABEL.get(sess.get("gender", ""), "—"),
                "kelompok": sess["kelompok"],
                "topik": sess["topik"],
                "provider": sess["provider"],
                "model": sess["model"],
                "created_at": sess["created_at"],
                "jumlah_pesan": r["jumlah_pesan"],
                "durasi": r["durasi"],
            })

        with c2:
            st.markdown("#### Aksi")
            form_md = generate_form_markdown(sess, msgs_visible)
            st.download_button(
                "⬇️ Unduh Form Pengungkapan AI (.md)",
                data=form_md,
                file_name=f"form-ai-{r['id_short']}.md",
                mime="text/markdown",
                use_container_width=True,
            )
            transcript = "\n\n".join(
                f"### {m['role'].upper()} — {m.get('created_at', '')}\n\n"
                f"{m['content']}"
                for m in msgs_visible
            )
            st.download_button(
                "⬇️ Unduh Transkrip Mentah (.txt)",
                data=transcript,
                file_name=f"transkrip-{r['id_short']}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("---")
        st.markdown("#### Transkrip percakapan")
        if not msgs_visible:
            st.info("Belum ada percakapan.")
        else:
            for m in msgs_visible:
                with st.chat_message(m["role"]):
                    st.caption(m.get("created_at", ""))
                    st.markdown(m["content"])


# ----- Ekspor -----
with tab_export:
    st.markdown("### Ekspor data UAS")
    st.caption("Untuk arsip, audit, atau analisis lanjutan di luar aplikasi.")

    if rows:
        import csv as csvmod
        buf = io.StringIO()
        fieldnames = ["id", "created_at", "nim", "nama", "gender",
                      "kelompok", "topik_full", "jumlah_pesan",
                      "durasi", "provider"]
        writer = csvmod.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
        st.download_button(
            "📊 Ekspor CSV semua sesi",
            data=buf.getvalue(),
            file_name=f"sesi-uas-{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in rows:
                sess = storage.get_session(r["id"])
                msgs = [
                    m for m in storage.get_messages(r["id"])
                    if m["role"] != "system"
                ]
                if not msgs:
                    continue
                md = generate_form_markdown(sess, msgs)
                fname = (
                    f"{r['kelompok']}_{r['nim']}_{r['id_short']}.md"
                )
                zf.writestr(fname, md)
        zip_buf.seek(0)
        st.download_button(
            "📦 Ekspor ZIP semua Form Pengungkapan AI",
            data=zip_buf.getvalue(),
            file_name=f"form-ai-{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip",
        )

    st.divider()
    st.markdown("### Daftar peserta UAS")
    if roster:
        all_peserta = list_all_peserta(roster)
        # gender per NIM dari sessions terakhir
        gender_per_nim = {}
        for r in sorted(rows, key=lambda x: x["created_at"]):
            if r["nim"] != "-" and r["gender"]:
                gender_per_nim[r["nim"]] = r["gender"]
        display_all = [
            {
                "NIM": p["nim"],
                "Nama": p["nama"],
                "Gender": GENDER_LABEL.get(
                    gender_per_nim.get(p["nim"], ""),
                    "Belum diisi",
                ),
                "Kelompok": p["kelompok"],
                "Topik": p["topik_uas"],
                "Status": (
                    "✅ Aktif" if p["nim"] in nim_aktif else "⏳ Belum"
                ),
            }
            for p in all_peserta
        ]
        st.dataframe(display_all, use_container_width=True, hide_index=True)
