"""Pemuat roster peserta UAS — dipakai aplikasi Streamlit untuk validasi NIM.

Membaca `peserta/roster.json` (dihasilkan `peserta/buat_kelompok.py`).
Jika berkas tidak ada (mis. dosen ingin mode bebas), aplikasi akan
fallback ke input manual.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


def roster_path(repo_root: Path) -> Path:
    return repo_root / "peserta" / "roster.json"


def load_roster(repo_root: Path) -> Optional[Dict]:
    """Muat roster dari peserta/roster.json. Return None jika tidak ada."""
    path = roster_path(repo_root)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def list_nim(roster: Optional[Dict]) -> List[str]:
    """Daftar NIM, urut sesuai roster."""
    if not roster:
        return []
    return sorted(roster.get("peserta", {}).keys())


def get_peserta(roster: Optional[Dict], nim: str) -> Optional[Dict]:
    """Ambil entri peserta berdasarkan NIM."""
    if not roster:
        return None
    return roster.get("peserta", {}).get(nim)


def get_kelompok_anggota(
    roster: Optional[Dict],
    kelompok: str,
) -> List[Dict]:
    """Ambil semua anggota dari sebuah kode kelompok (mis. 'K05')."""
    if not roster:
        return []
    out: List[Dict] = []
    for nim, data in roster.get("peserta", {}).items():
        if data.get("kelompok") == kelompok:
            out.append({"nim": nim, **data})
    return sorted(out, key=lambda x: x["nim"])
