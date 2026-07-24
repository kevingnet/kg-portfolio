#!/usr/bin/env python3
"""Restore specific portfolio icons without touching others."""

from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "images"
UA = {"User-Agent": "Mozilla/5.0 (compatible; KG-Portfolio/1.0)"}

FRYS_SVG_URL = "https://upload.wikimedia.org/wikipedia/commons/9/9e/Fry_s_Electronics.svg"


def restore_frys() -> None:
    dest = IMG / "frys.svg"
    req = urllib.request.Request(FRYS_SVG_URL, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if len(data) < 200:
        raise RuntimeError("Fry's logo download too small")
    dest.write_bytes(data)
    print(f"frys: restored from Wikimedia -> {dest.name} ({len(data)} bytes)")


def main() -> None:
    restore_frys()
    print("done (lcs, plastering, woodtech, posdev wordmarks are static SVG files)")


if __name__ == "__main__":
    main()
