#!/usr/bin/env python3
"""Remove extracted doc text/figures from archive blocks that now use PDF embeds."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_JSON = ROOT / "data" / "nnn-archive.json"


def archive_block_stats(blocks: list[dict]) -> dict:
    stats = {"code": 0, "document": 0, "text": 0, "image": 0, "figures": 0}
    for block in blocks:
        btype = block.get("type")
        if btype == "section" or btype not in stats:
            continue
        stats[btype] += 1
        if btype == "document":
            for seg in block.get("segments") or []:
                if seg.get("kind") == "figures":
                    stats["figures"] += len(seg.get("images") or [])
    return stats


def strip_pdf_document(block: dict) -> list[str]:
    """Drop extracted text; return relative asset paths to delete."""
    assets: list[str] = []
    if block.get("type") != "document" or not block.get("pdf_src"):
        return assets

    for seg in block.get("segments") or []:
        if seg.get("kind") == "figures":
            for img in seg.get("images") or []:
                src = img.get("src")
                if src:
                    assets.append(src)

    title = block.get("title") or ""
    if title:
        block["title"] = f"{Path(title).stem}.pdf"

    rel = block.get("rel") or ""
    if rel:
        block["rel"] = str(Path(rel).with_suffix(".pdf"))

    for key in ("content", "segments", "figure_count", "truncated"):
        block.pop(key, None)

    return assets


def remove_asset(rel_path: str) -> bool:
    path = ROOT / rel_path
    if not path.is_file():
        return False
    path.unlink()
    for parent in path.parents:
        if parent == ROOT or not str(parent).startswith(str(ROOT / "assets")):
            break
        try:
            parent.rmdir()
        except OSError:
            break
    return True


def main() -> int:
    data = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    stripped = 0
    removed_files = 0

    for entry in data.get("employers", {}).values():
        for block in entry.get("blocks") or []:
            for rel in strip_pdf_document(block):
                if remove_asset(rel):
                    removed_files += 1
            if block.get("type") == "document" and block.get("pdf_src"):
                stripped += 1
        entry["stats"] = archive_block_stats(entry.get("blocks") or [])

    ARCHIVE_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Stripped {stripped} PDF document blocks, removed {removed_files} extracted assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
