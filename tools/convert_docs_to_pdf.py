#!/usr/bin/env python3
"""Convert portfolio .doc/.docx sources to PDF and update nnn-archive.json."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_JSON = ROOT / "data" / "nnn-archive.json"
ASSETS_ARCHIVE = ROOT / "assets" / "archive"
SKIP_DOCUMENTS = frozenset({
    "JakeKnowsTemplate.pdf",
    "doc/JakeKnowsTemplate.pdf",
    "JakeKnowsTemplate.dotx",
})
DOC_EXTS = {".doc", ".docx"}
CONVERT_EXTS = {".doc", ".docx", ".rtf", ".dotx", ".odt"}
PDF_EXT = {".pdf"}


def normalize_pdf_title(title: str) -> str:
    if title.lower().endswith(",pdf"):
        return title[:-4] + ".pdf"
    path = Path(title)
    if path.suffix.lower() in PDF_EXT | CONVERT_EXTS | DOC_EXTS:
        return path.with_suffix(".pdf").name
    return f"{path.stem}.pdf"


def is_pdf_source(src: Path) -> bool:
    if src.suffix.lower() in PDF_EXT or src.name.lower().endswith(",pdf"):
        return True
    try:
        return src.read_bytes()[:4] == b"%PDF"
    except OSError:
        return False


def is_portfolio_document(title: str, rel: str, src: Path | None) -> bool:
    for name in (title, rel, src.name if src else ""):
        if not name:
            continue
        lower = name.lower()
        if lower.endswith(",pdf"):
            return True
        if Path(name).suffix.lower() in PDF_EXT | CONVERT_EXTS | DOC_EXTS:
            return True
    return bool(src and is_pdf_source(src))


def slug_folder_map(nnn_root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not nnn_root.is_dir():
        return mapping
    for child in sorted(nnn_root.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            mapping[child.name.lower()] = child.name
    return mapping


def resolve_source(
    nnn_root: Path,
    slug: str,
    rel: str,
    folders: dict[str, str],
    employer_name: str = "",
) -> Path | None:
    if not rel:
        return None
    folder_candidates = [
        folders.get(slug.lower()),
        employer_name,
        folders.get(employer_name.lower()) if employer_name else None,
        slug,
    ]
    seen: set[str] = set()
    for folder in folder_candidates:
        if not folder or folder in seen:
            continue
        seen.add(folder)
        candidate = nnn_root / folder / rel
        if candidate.is_file():
            return candidate
    candidate = nnn_root / rel
    if candidate.is_file():
        return candidate
    return None


def pdf_asset_name(title: str) -> str:
    normalized = normalize_pdf_title(title)
    stem = Path(normalized).stem
    safe = re.sub(r"[^\w\-+. ]+", "_", stem).strip().replace(" ", "_")
    return f"{safe or 'document'}.pdf"


def pdf_asset_rel(slug: str, title: str) -> str:
    return f"assets/archive/{slug}/pdf/{pdf_asset_name(title)}"


def convert_with_libreoffice(src: Path, out_dir: Path) -> Path | None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "soffice",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(src),
    ]
    subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    produced = out_dir / f"{src.stem}.pdf"
    return produced if produced.is_file() else None


def copy_or_convert(src: Path, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if is_pdf_source(src):
        dest.write_bytes(src.read_bytes())
        return True
    if src.suffix.lower() not in CONVERT_EXTS:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        produced = convert_with_libreoffice(src, Path(tmp))
        if not produced:
            return False
        dest.write_bytes(produced.read_bytes())
        return True


def strip_pdf_documents(data: dict) -> tuple[int, int]:
    """Remove extracted text from blocks that use pdf_src."""
    stripped = 0
    removed_files = 0
    for entry in data.get("employers", {}).values():
        for block in entry.get("blocks") or []:
            for rel in _strip_pdf_document_block(block):
                path = ROOT / rel
                if path.is_file():
                    path.unlink()
                    removed_files += 1
                    for parent in path.parents:
                        if parent == ROOT or not str(parent).startswith(str(ROOT / "assets")):
                            break
                        try:
                            parent.rmdir()
                        except OSError:
                            break
            if block.get("type") == "document" and block.get("pdf_src"):
                stripped += 1
        entry["stats"] = _archive_block_stats(entry.get("blocks") or [])
    return stripped, removed_files


def _archive_block_stats(blocks: list[dict]) -> dict:
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


def _strip_pdf_document_block(block: dict) -> list[str]:
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
        block["title"] = normalize_pdf_title(title)
    rel = block.get("rel") or ""
    if rel:
        rel_path = Path(rel)
        if rel_path.name.lower().endswith(",pdf"):
            block["rel"] = str(rel_path.with_name(normalize_pdf_title(rel_path.name)))
        else:
            block["rel"] = str(rel_path.with_suffix(".pdf"))
    for key in ("content", "segments", "figure_count", "truncated"):
        block.pop(key, None)
    return assets


def audit_documents(data: dict) -> list[str]:
    problems: list[str] = []
    for slug, entry in data.get("employers", {}).items():
        for block in entry.get("blocks") or []:
            if block.get("type") != "document":
                continue
            title = block.get("title") or block.get("rel") or "?"
            if not block.get("pdf_src"):
                problems.append(f"{slug}: missing pdf_src for {title}")
            if block.get("content") or block.get("segments"):
                problems.append(f"{slug}: leftover extracted text for {title}")
    return problems


def main() -> int:
    data = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    nnn_root = Path(data.get("source", ""))
    if not nnn_root.is_dir():
        print(f"Archive source missing: {nnn_root}", file=sys.stderr)
        return 1

    folders = slug_folder_map(nnn_root)
    converted = 0
    copied = 0
    missing: list[str] = []

    for slug, entry in data.get("employers", {}).items():
        employer_name = entry.get("name") or ""
        for block in entry.get("blocks", []):
            if block.get("type") != "document":
                continue
            if block.get("pdf_src") and not block.get("content") and not block.get("segments"):
                continue
            title = block.get("title") or ""
            rel = block.get("rel") or title
            if title in SKIP_DOCUMENTS or rel in SKIP_DOCUMENTS:
                continue
            src = resolve_source(nnn_root, slug, rel, folders, employer_name)
            if not is_portfolio_document(title, rel, src):
                continue
            asset_rel = pdf_asset_rel(slug, title)
            dest = ROOT / asset_rel
            if not src:
                missing.append(f"{slug}: {rel}")
                continue

            ext = Path(title).suffix.lower()
            if copy_or_convert(src, dest):
                block["pdf_src"] = asset_rel
                if is_pdf_source(src):
                    copied += 1
                else:
                    converted += 1
                print(f"OK {slug}: {title} -> {asset_rel}")
            else:
                missing.append(f"{slug}: convert failed for {src}")

    stripped, removed = strip_pdf_documents(data)
    problems = audit_documents(data)
    ARCHIVE_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Done: {converted} converted, {copied} PDFs copied, {len(missing)} missing/failed")
    print(f"Stripped {stripped} PDF blocks, removed {removed} extracted assets")
    for item in missing:
        print(f"  missing: {item}")
    for item in problems:
        print(f"  audit: {item}")
    return 0 if not missing and not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
