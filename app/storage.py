"""SQLite storage untuk logging sesi & pesan UAS.

Setiap kelompok mahasiswa membuat satu sesi (session_id = UUID).
Semua pesan tersimpan dengan timestamp, dapat diaudit oleh dosen.
"""
from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Storage:
    """Pembungkus SQLite minimalis untuk sesi & pesan."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self) -> None:
        with self._conn() as c:
            c.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id           TEXT PRIMARY KEY,
                    created_at   TEXT NOT NULL,
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
                """
            )

    # ---------- sessions ----------

    def create_session(
        self,
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
                "(id, created_at, kelompok, anggota, topik, provider, model) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (sid, _utcnow_iso(), kelompok, anggota, topik, provider, model),
            )
        return sid

    def update_session(
        self,
        session_id: str,
        kelompok: Optional[str] = None,
        anggota: Optional[str] = None,
        topik: Optional[str] = None,
    ) -> None:
        sets, params = [], []
        for col, val in [
            ("kelompok", kelompok),
            ("anggota", anggota),
            ("topik", topik),
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
        with self._conn() as c:
            row = c.execute(
                "SELECT id, created_at, kelompok, anggota, topik, "
                "provider, model FROM sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
        if not row:
            return None
        cols = ["id", "created_at", "kelompok", "anggota", "topik",
                "provider", "model"]
        return dict(zip(cols, row))

    def list_sessions(self) -> List[Dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT id, created_at, kelompok, anggota, topik, "
                "provider, model FROM sessions ORDER BY created_at DESC"
            ).fetchall()
        cols = ["id", "created_at", "kelompok", "anggota", "topik",
                "provider", "model"]
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
