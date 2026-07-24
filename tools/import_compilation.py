#!/usr/bin/env python3
"""Parse data/portfolio-compilation.md → data/portfolio-compilation.json (per slug)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "portfolio-compilation.md"
OUT = ROOT / "data" / "portfolio-compilation.json"

# Compilation section header → portfolio slug
SECTION_TO_SLUG: dict[str, str] = {
    "01 Access!": "access",
    "02 BumperShop": "bumpershop",
    "03 Disney": "disney",
    "04 Electrosonic": "electrosonic",
    "05 Volt": "voltdelta",
    "06 LaBumpers": "labumpers",
    "07 PosDev": "posdev",
    "08 FotografiaBlancarte": "fotografia",
    "09 Pleiades": "pleiades",
    "10 TelVista": "audiotelco",
    "11 Enigma": "enigma",
    "12 Nokio": "nokio",
    "13 PuntaBandaData": "puntabanda",
    "15 HMS": "hms",
    "16 Spirent": "spirent",
    "18 DirecTV": "directv",
    "19 Surfware": "surfware",
    "22 Motorola": "motorola",
    "23 Yahoo": "yahoo",
    "24 JakeKnows": "jakeknows",
    "25 OpenTV": "opentv",
    "26 Google": "google",
    "27 Vmware": "vmware",
    "28 Knurld": "knurld",
    "29 Butterfleye": "butterfleye",
    "30 Thuuz": "thuuz",
    "32 Chase": "chase",
    "33 HiveMapper": "hivemapper",
    "graphics": "electrosonic",
    "WEBSITE": "greenleaf",
    "work": "jakeknows",
}

FOLDER_PREFIX_RE = re.compile(r"^(\d{1,2})\s+")
PATH_PREFIX_RE = re.compile(r"(?<![/\w])(\d{1,2})\s+([A-Za-z!][^\n/`]*)")


def strip_numbered_folder(text: str) -> str:
    """Remove leading NN from folder names in prose and tree listings."""
    lines = []
    for line in text.splitlines():
        # Tree lines: "03 Disney/" or "├── 03 Disney"
        line = re.sub(
            r"^(\s*[├└│─\s]*)(\d{1,2})\s+",
            r"\1",
            line,
        )
        # Inline references: "folders **03 Disney**"
        line = re.sub(r"\*\*(\d{1,2})\s+([^*]+)\*\*", r"**\2**", line)
        line = re.sub(r"`(\d{1,2})\s+([^`]+)`", r"`\2`", line)
        # BumperShop (02) or (24 JakeKnows) in relationship text
        line = re.sub(r"\((\d{1,2})\s+([^)]+)\)", r"(\2)", line)
        # "Related to: 04 Electrosonic" / "See also: 24 JakeKnows"
        line = re.sub(
            r"(?i)((?:related to|see also|canonical|evolved into|fork|overlap)[:\s]+)(\d{1,2})\s+",
            r"\1",
            line,
        )
        # "shares domain with `26 Google`"
        line = re.sub(
            r"(with\s+`?)(\d{1,2})\s+",
            r"\1",
            line,
        )
        lines.append(line)
    return "\n".join(lines)


def parse_section_title(title_line: str) -> tuple[str, str]:
    """Return (folder_key, display_name) from '### 03 Disney — Walt Disney Studio IT'."""
    title = title_line.strip()
    if title.startswith("### "):
        title = title[4:].strip()
    if " — " in title:
        left, subtitle = title.split(" — ", 1)
        folder_key = left.strip()
        display = left.strip()
        if FOLDER_PREFIX_RE.match(folder_key):
            display = FOLDER_PREFIX_RE.sub("", folder_key).strip()
            return folder_key, f"{display} — {subtitle.strip()}"
        return folder_key, title
    folder_key = title
    display = FOLDER_PREFIX_RE.sub("", folder_key).strip() or folder_key
    return folder_key, display


def md_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def clean_compilation_line(stripped: str) -> str | None:
    """Drop archive inventory meta (Files, Author) from compilation prose."""
    if re.match(r"\*\*Files:\*\*", stripped):
        return None
    if re.match(r"\*\*Author(?: credit)?:\*\*", stripped):
        return None
    cleaned = re.sub(r"\s*\|\s*\*\*Author(?: credit)?:\*\*[^|]*", "", stripped).strip()
    cleaned = re.sub(r"^\*\*Author(?: credit)?:\*\*[^|]*\s*\|\s*", "", cleaned).strip()
    if re.match(r"\*\*Author(?: credit)?:\*\*", cleaned):
        return None
    return cleaned or None


def md_block_to_html(body: str) -> str:
    body = strip_numbered_folder(body)
    parts: list[str] = []
    in_code = False
    code_lines: list[str] = []
    in_ul = False
    table_rows: list[str] = []

    def flush_ul() -> None:
        nonlocal in_ul
        if in_ul:
            parts.append("</ul>")
            in_ul = False

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        html_rows = []
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            tag = "th" if i == 0 else "td"
            html_rows.append(
                "<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cells) + "</tr>"
            )
        parts.append('<table class="compilation-table">' + "".join(html_rows) + "</table>")
        table_rows = []

    for line in body.splitlines():
        if line.strip().startswith("```"):
            flush_ul()
            flush_table()
            if in_code:
                parts.append(
                    '<pre class="compilation-tree"><code>'
                    + "\n".join(code_lines)
                    + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if line.startswith("|") and "|" in line[1:]:
            flush_ul()
            if re.match(r"^\|[-:\s|]+\|$", line.strip()):
                continue
            table_rows.append(line)
            continue
        flush_table()
        stripped = line.strip()
        if not stripped or stripped == "---":
            flush_ul()
            continue
        if stripped.startswith("- "):
            if not in_ul:
                parts.append("<ul>")
                in_ul = True
            parts.append(f"<li>{md_inline(stripped[2:])}</li>")
            continue
        flush_ul()
        cleaned = clean_compilation_line(stripped)
        if cleaned is None:
            continue
        if cleaned.startswith("**") and cleaned.endswith("**") and cleaned.count("**") == 2:
            parts.append(f"<p><strong>{cleaned[2:-2]}</strong></p>")
        else:
            parts.append(f"<p>{md_inline(cleaned)}</p>")

    flush_ul()
    flush_table()
    if in_code and code_lines:
        parts.append(
            '<pre class="compilation-tree"><code>'
            + "\n".join(code_lines)
            + "</code></pre>"
        )
    return "\n".join(parts)


def extract_meta(body: str) -> dict:
    meta: dict = {}
    for key, pat in [
        ("files", r"\*\*Files:\*\*\s*([^|\n]+)"),
        ("era", r"\*\*Era:\*\*\s*([^\n|]+)"),
        ("domain", r"\*\*Domain:\*\*\s*([^\n]+)"),
        ("client", r"\*\*Client:\*\*\s*([^\n]+)"),
        ("business", r"\*\*Business:\*\*\s*([^\n]+)"),
        ("status", r"\*\*Status:\*\*\s*([^\n]+)"),
        ("date", r"\*\*Date:\*\*\s*([^\n]+)"),
    ]:
        m = re.search(pat, body)
        if m:
            meta[key] = m.group(1).strip()
    purpose = re.search(r"\*\*Purpose:\*\*\s*(.+)", body)
    if purpose:
        meta["purpose"] = purpose.group(1).strip()
    tech = re.search(r"\*\*Technologies:\*\*\s*(.+)", body)
    if tech:
        meta["technologies"] = [t.strip() for t in re.split(r",(?![^()]*\))", tech.group(1)) if t.strip()]
    return meta


def parse_compilation(text: str) -> dict[str, dict]:
    sections = re.split(r"\n(?=### )", text)
    by_slug: dict[str, dict] = {}

    for block in sections:
        if not block.strip().startswith("### "):
            continue
        first_line, _, body = block.partition("\n")
        folder_key, display_title = parse_section_title(first_line)
        slug = SECTION_TO_SLUG.get(folder_key)
        if not slug:
            # Try matching without number prefix
            bare = FOLDER_PREFIX_RE.sub("", folder_key).strip()
            slug = SECTION_TO_SLUG.get(bare)
        if not slug:
            continue

        meta = extract_meta(body)
        html = md_block_to_html(body)
        entry = {
            "folder": FOLDER_PREFIX_RE.sub("", folder_key).strip() or folder_key,
            "display_title": display_title,
            "meta": meta,
            "html": html,
        }
        if slug in by_slug:
            # Append (graphics → electrosonic, work → jakeknows)
            prev = by_slug[slug]
            prev["html"] += (
                f'\n<h3>{md_inline(display_title)}</h3>\n{html}'
            )
            prev["extra_sections"] = prev.get("extra_sections", []) + [display_title]
        else:
            by_slug[slug] = entry
    return by_slug


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing {SRC}")
    text = SRC.read_text(encoding="utf-8")
    data = parse_compilation(text)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(data)} slug entries → {OUT}")


if __name__ == "__main__":
    main()
