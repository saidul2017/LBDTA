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
