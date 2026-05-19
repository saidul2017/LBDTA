"""SQLite storage untuk logging sesi & pesan UAS + nilai mahasiswa.

Setiap kelompok mahasiswa membuat satu sesi (session_id = UUID).
Semua pesan tersimpan dengan timestamp, dapat diaudit oleh dosen.

Nilai disimpan per-kelompok berdasarkan rubrik R03 (7 dimensi).

Schema migration: kolom baru ditambah secara dinamis untuk DB
existing yang dibuat dengan versi sebelumnya.
"""
from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


# Bobot dimensi penilaian sesuai rubrik/R03-policy-brief-mini.md
RUBRIK_R03 = [
    ("ringkasan_eksekutif", "Ringkasan eksekutif", 0.10),
    ("kekuatan_bukti",       "Kekuatan bukti (data & sumber)", 0.20),
    ("confounder_batasan",   "Kesadaran confounder & batasan", 0.20),
    ("rekomendasi",          "Kualitas rekomendasi", 0.20),
    ("etis_islam",           "Pertimbangan etis Islam", 0.15),
    ("komunikasi_visual",    "Komunikasi & visual", 0.10),
    ("sitasi_integritas",    "Sitasi & integritas akademik", 0.05),
]


def hitung_nilai_akhir(skor_dict: Dict[str, int], pengurangan: int = 0) -> float:
    """Konversi skor 1-4 per dimensi ke nilai 0-100 dengan pembobotan.

    Formula: nilai_akhir = (Σ skor_i × bobot_i) × 25 - pengurangan_etis.
    Semua skor 4 → 100. Skor 3 di semua dimensi → 75.
    """
    total = 0.0
    for kode, _label, bobot in RUBRIK_R03:
        s = skor_dict.get(kode) or 0
        total += s * bobot
    nilai = total * 25.0
    nilai -= pengurangan
    return round(max(0.0, min(100.0, nilai)), 1)


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Storage:
    """Pembungkus SQLite minimalis untuk sesi, pesan, dan nilai."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self) -> None:
        skor_cols_def = ", ".join(
            f"skor_{k} INTEGER DEFAULT 0" for k, _, _ in RUBRIK_R03
        )
        with self._conn() as c:
            c.executescript(
                f"""
                CREATE TABLE IF NOT EXISTS sessions (
                    id           TEXT PRIMARY KEY,
                    created_at   TEXT NOT NULL,
                    nim          TEXT DEFAULT '',
                    nama         TEXT DEFAULT '',
                    gender       TEXT DEFAULT '',
                    kelompok     TEXT DEFAULT '',
                    anggota      TEXT DEFAULT '',
                    topik        TEXT DEFAULT '',
                    provider     TEXT DEFAULT '',
                    model        TEXT DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  TEXT NOT NULL,
                    role        TEXT NOT NULL,
                    content     TEXT NOT NULL,
                    created_at  TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session
                    ON messages(session_id);

                CREATE TABLE IF NOT EXISTS nilai (
                    kelompok          TEXT PRIMARY KEY,
                    {skor_cols_def},
                    pengurangan_etis  INTEGER DEFAULT 0,
                    catatan           TEXT DEFAULT '',
                    nilai_akhir       REAL DEFAULT 0,
                    dinilai_oleh      TEXT DEFAULT '',
                    updated_at        TEXT DEFAULT ''
                );
                """
            )
            # Migrasi kolom sessions yang mungkin belum ada
            cols = {r[1] for r in c.execute("PRAGMA table_info(sessions)")}
            for col_name in ("nim", "nama", "gender"):
                if col_name not in cols:
                    c.execute(
                        f"ALTER TABLE sessions ADD COLUMN {col_name} "
                        "TEXT DEFAULT ''"
                    )

    # ---------- sessions ----------

    def create_session(
        self,
        nim: str = "",
        nama: str = "",
        gender: str = "",
        kelompok: str = "",
        anggota: str = "",
        topik: str = "",
        provider: str = "",
        model: str = "",
    ) -> str:
        sid = str(uuid.uuid4())
        with self._conn() as c:
            c.execute(
                "INSERT INTO sessions "
                "(id, created_at, nim, nama, gender, kelompok, anggota, "
                "topik, provider, model) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (sid, _utcnow_iso(), nim, nama, gender, kelompok, anggota,
                 topik, provider, model),
            )
        return sid

    def update_session(
        self,
        session_id: str,
        nim: Optional[str] = None,
        nama: Optional[str] = None,
        gender: Optional[str] = None,
        kelompok: Optional[str] = None,
        anggota: Optional[str] = None,
        topik: Optional[str] = None,
    ) -> None:
        sets, params = [], []
        for col, val in [
            ("nim", nim), ("nama", nama), ("gender", gender),
            ("kelompok", kelompok), ("anggota", anggota), ("topik", topik),
        ]:
            if val is not None:
                sets.append(f"{col} = ?")
                params.append(val)
        if not sets:
            return
        params.append(session_id)
        with self._conn() as c:
            c.execute(
                f"UPDATE sessions SET {', '.join(sets)} WHERE id = ?",
                params,
            )

    def get_session(self, session_id: str) -> Optional[Dict]:
        cols = ["id", "created_at", "nim", "nama", "gender", "kelompok",
                "anggota", "topik", "provider", "model"]
        with self._conn() as c:
            row = c.execute(
                f"SELECT {', '.join(cols)} FROM sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
        if not row:
            return None
        return dict(zip(cols, row))

    def list_sessions(self) -> List[Dict]:
        cols = ["id", "created_at", "nim", "nama", "gender", "kelompok",
                "anggota", "topik", "provider", "model"]
        with self._conn() as c:
            rows = c.execute(
                f"SELECT {', '.join(cols)} FROM sessions "
                "ORDER BY created_at DESC"
            ).fetchall()
        return [dict(zip(cols, r)) for r in rows]

    # ---------- messages ----------

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO messages (session_id, role, content, created_at) "
                "VALUES (?, ?, ?, ?)",
                (session_id, role, content, _utcnow_iso()),
            )

    def get_messages(self, session_id: str) -> List[Dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT role, content, created_at FROM messages "
                "WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
        return [
            {"role": r[0], "content": r[1], "created_at": r[2]}
            for r in rows
        ]

    def count_messages(self, session_id: str) -> int:
        with self._conn() as c:
            row = c.execute(
                "SELECT COUNT(*) FROM messages WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return int(row[0]) if row else 0

    # ---------- nilai (rubrik R03) ----------

    def save_nilai(
        self,
        kelompok: str,
        skor: Dict[str, int],
        pengurangan: int = 0,
        catatan: str = "",
        dinilai_oleh: str = "",
    ) -> float:
        """Simpan nilai per kelompok. Hitung otomatis nilai_akhir."""
        nilai_akhir = hitung_nilai_akhir(skor, pengurangan)
        cols = ", ".join(f"skor_{k}" for k, _, _ in RUBRIK_R03)
        placeholders = ", ".join("?" for _ in RUBRIK_R03)
        values = [int(skor.get(k, 0) or 0) for k, _, _ in RUBRIK_R03]
        update_set = ", ".join(
            f"skor_{k}=excluded.skor_{k}" for k, _, _ in RUBRIK_R03
        )
        with self._conn() as c:
            c.execute(
                f"""
                INSERT INTO nilai (kelompok, {cols}, pengurangan_etis,
                                   catatan, nilai_akhir, dinilai_oleh,
                                   updated_at)
                VALUES (?, {placeholders}, ?, ?, ?, ?, ?)
                ON CONFLICT(kelompok) DO UPDATE SET
                    {update_set},
                    pengurangan_etis=excluded.pengurangan_etis,
                    catatan=excluded.catatan,
                    nilai_akhir=excluded.nilai_akhir,
                    dinilai_oleh=excluded.dinilai_oleh,
                    updated_at=excluded.updated_at
                """,
                [kelompok, *values, int(pengurangan), catatan,
                 nilai_akhir, dinilai_oleh, _utcnow_iso()],
            )
        return nilai_akhir

    def get_nilai(self, kelompok: str) -> Optional[Dict]:
        skor_cols = [f"skor_{k}" for k, _, _ in RUBRIK_R03]
        all_cols = ["kelompok", *skor_cols, "pengurangan_etis", "catatan",
                    "nilai_akhir", "dinilai_oleh", "updated_at"]
        with self._conn() as c:
            row = c.execute(
                f"SELECT {', '.join(all_cols)} FROM nilai WHERE kelompok = ?",
                (kelompok,),
            ).fetchone()
        if not row:
            return None
        return dict(zip(all_cols, row))

    def list_nilai(self) -> List[Dict]:
        skor_cols = [f"skor_{k}" for k, _, _ in RUBRIK_R03]
        all_cols = ["kelompok", *skor_cols, "pengurangan_etis", "catatan",
                    "nilai_akhir", "dinilai_oleh", "updated_at"]
        with self._conn() as c:
            rows = c.execute(
                f"SELECT {', '.join(all_cols)} FROM nilai ORDER BY kelompok"
            ).fetchall()
        return [dict(zip(all_cols, r)) for r in rows]

    def delete_nilai(self, kelompok: str) -> None:
        with self._conn() as c:
            c.execute("DELETE FROM nilai WHERE kelompok = ?", (kelompok,))

    # ---------- kuis (skor mahasiswa per modul) ----------

    def _ensure_kuis_table(self) -> None:
        with self._conn() as c:
            c.executescript(
                """
                CREATE TABLE IF NOT EXISTS kuis_skor (
                    nim          TEXT NOT NULL,
                    modul        TEXT NOT NULL,
                    skor         INTEGER DEFAULT 0,
                    total_soal   INTEGER DEFAULT 0,
                    persen       REAL DEFAULT 0,
                    waktu_detik  INTEGER DEFAULT 0,
                    attempts     INTEGER DEFAULT 1,
                    updated_at   TEXT NOT NULL,
                    PRIMARY KEY (nim, modul)
                );
                CREATE TABLE IF NOT EXISTS progres_materi (
                    nim          TEXT NOT NULL,
                    modul        TEXT NOT NULL,
                    dibaca       INTEGER DEFAULT 0,
                    updated_at   TEXT NOT NULL,
                    PRIMARY KEY (nim, modul)
                );
                """
            )

    def save_kuis_skor(
        self,
        nim: str,
        modul: str,
        skor: int,
        total_soal: int,
        waktu_detik: int = 0,
    ) -> Dict:
        """Simpan skor kuis. Skor terbaik (tertinggi) yang dipertahankan.

        Returns dict dengan info skor lama vs baru, dan apakah ini PB.
        """
        self._ensure_kuis_table()
        persen = round(skor / total_soal * 100, 1) if total_soal else 0.0
        with self._conn() as c:
            row = c.execute(
                "SELECT skor, attempts FROM kuis_skor WHERE nim=? AND modul=?",
                (nim, modul),
            ).fetchone()
            if row is None:
                # First attempt
                c.execute(
                    """
                    INSERT INTO kuis_skor
                    (nim, modul, skor, total_soal, persen, waktu_detik,
                     attempts, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                    """,
                    (nim, modul, skor, total_soal, persen, waktu_detik,
                     _utcnow_iso()),
                )
                return {"is_new": True, "is_pb": True, "skor_lama": 0,
                        "skor_baru": skor, "persen": persen}
            old_skor, old_attempts = row
            new_attempts = old_attempts + 1
            is_pb = skor > old_skor
            if is_pb:
                c.execute(
                    """
                    UPDATE kuis_skor SET skor=?, total_soal=?, persen=?,
                       waktu_detik=?, attempts=?, updated_at=?
                    WHERE nim=? AND modul=?
                    """,
                    (skor, total_soal, persen, waktu_detik, new_attempts,
                     _utcnow_iso(), nim, modul),
                )
            else:
                # Hanya update attempt count, jaga skor terbaik
                c.execute(
                    "UPDATE kuis_skor SET attempts=?, updated_at=? "
                    "WHERE nim=? AND modul=?",
                    (new_attempts, _utcnow_iso(), nim, modul),
                )
            return {"is_new": False, "is_pb": is_pb, "skor_lama": old_skor,
                    "skor_baru": skor if is_pb else old_skor,
                    "persen": persen}

    def get_kuis_skor(self, nim: str, modul: str) -> Optional[Dict]:
        self._ensure_kuis_table()
        cols = ["nim", "modul", "skor", "total_soal", "persen",
                "waktu_detik", "attempts", "updated_at"]
        with self._conn() as c:
            row = c.execute(
                f"SELECT {', '.join(cols)} FROM kuis_skor "
                "WHERE nim=? AND modul=?",
                (nim, modul),
            ).fetchone()
        return dict(zip(cols, row)) if row else None

    def list_kuis_skor_per_nim(self, nim: str) -> List[Dict]:
        self._ensure_kuis_table()
        cols = ["nim", "modul", "skor", "total_soal", "persen",
                "waktu_detik", "attempts", "updated_at"]
        with self._conn() as c:
            rows = c.execute(
                f"SELECT {', '.join(cols)} FROM kuis_skor "
                "WHERE nim=? ORDER BY modul",
                (nim,),
            ).fetchall()
        return [dict(zip(cols, r)) for r in rows]

    def list_all_kuis_skor(self) -> List[Dict]:
        self._ensure_kuis_table()
        cols = ["nim", "modul", "skor", "total_soal", "persen",
                "waktu_detik", "attempts", "updated_at"]
        with self._conn() as c:
            rows = c.execute(
                f"SELECT {', '.join(cols)} FROM kuis_skor "
                "ORDER BY nim, modul"
            ).fetchall()
        return [dict(zip(cols, r)) for r in rows]

    # ---------- progres baca materi ----------

    def mark_modul_dibaca(self, nim: str, modul: str) -> None:
        self._ensure_kuis_table()
        with self._conn() as c:
            c.execute(
                """
                INSERT INTO progres_materi (nim, modul, dibaca, updated_at)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(nim, modul) DO UPDATE SET
                    dibaca=1, updated_at=excluded.updated_at
                """,
                (nim, modul, _utcnow_iso()),
            )

    def list_modul_dibaca(self, nim: str) -> List[str]:
        self._ensure_kuis_table()
        with self._conn() as c:
            rows = c.execute(
                "SELECT modul FROM progres_materi WHERE nim=? AND dibaca=1",
                (nim,),
            ).fetchall()
        return [r[0] for r in rows]
