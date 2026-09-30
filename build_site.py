#!/usr/bin/env python3
"""Refresh the parts every page shares: header, nav, logo carousel and footer.

The HTML pages are the source of truth for their own content and are edited
directly. This script only rewrites the shared chrome, so a change to the nav,
the carousel or the footer is made once here instead of in 35 files:

    python3 build_site.py           # rewrite pages that are out of date
    python3 build_site.py --check   # list pages that would change; exit 1 if any

Carousel order comes from data/carousel-chronology.json (oldest first); the
carousel shows it newest first. To add an employer: add its logo to
assets/images/, an entry to LOGOS below, its slug to the chronology file, and
its page to projects/.

The previous full-site generator is in git history (before this rewrite).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CHRONOLOGY_FILE = ROOT / "data" / "carousel-chronology.json"
RESUME_SRC = Path("/home/kg/Jobs/Kevin Guerra.pdf")  # copied in when present

OWNER = "Kevin Alexander Guerra"
SITE_NAME = "Kevin Guerra Portfolio"
COPYRIGHT_YEAR = "2026"
CONTACT_EMAIL = "kevingnet1@gmail.com"

NAV = [
    ("Portfolio", "index.html"),
    ("Services", "services.html"),
    ("Samples", "samples.html"),
    ("Resume", "resume.html"),
    ("About", "about.html"),
]

# slug -> (image under assets/images/, label, accent border)
LOGOS = {
    "mafroda": ("mafroda.png", "MAF RODA", True),
    "leidos": ("leidos.png", "Leidos", False),
    "google": ("google.jpeg", "Google", True),
    "meta": ("facebook.jpeg", "Meta", False),
    "vmware": ("vmware.jpeg", "VMware", True),
    "veritas": ("veritas.jpeg", "Veritas", False),
    "thuuz": ("thuuz.png", "Thuuz", False),
    "knurld": ("knulrd.jpeg", "Knurld", False),
    "butterfleye": ("butterfleye.jpeg", "Butterfleye", False),
    "hpe": ("hpe.jpeg", "HPE", False),
    "opentv": ("opentv.jpeg", "OpenTV (Nagra)", False),
    "jakeknows": ("company.png", "JakeKnows", True),
    "yahoo": ("yahoo.jpeg", "Yahoo", False),
    "motorola": ("motorola.jpeg", "Motorola", True),
    "surfware": ("surfware.jpeg", "Surfware", True),
    "spirent": ("spirent.jpeg", "Spirent", True),
    "directv": ("directv.jpeg", "DirecTV", True),
    "guidance": ("guidance.jpeg", "Guidance Software", False),
    "hms": ("hypermedia.jpeg", "HMS", True),
    "telvista": ("telvista.jpeg", "TelVista", False),
    "voltdelta": ("voltdelta.jpeg", "VoltDelta", True),
    "posdev": ("posdev.svg", "Positive Developments", True),
    "woodtech": ("woodtech.svg", "Wood Technologies", False),
    "disney": ("disney.jpeg", "Disney", True),
    "electrosonic": ("electrosonic.jpeg", "Electrosonic", True),
    "access": ("access.svg", "ACCESS!", False),
    "frys": ("frys.svg", "Fry's Electronics", False),
    "lcs": ("lcs.svg", "Logical Computer Services", False),
}

# Pages whose footer also links the HTML resume and the experience history
EXTENDED_FOOTER = {"resume.html", "experience-history.html"}

HEADER_RE = re.compile(r'  <header class="site-header">.*?</header>', re.S)
FOOTER_RE = re.compile(r'  <footer class="site-footer">.*?</footer>', re.S)
ACTIVE_RE = re.compile(r'<li><a href="(?:\.\./)?([^"]+)" class="active">')


def esc(text: str) -> str:
    return html.escape(text, quote=True).replace("&#x27;", "&#39;")


def carousel_order() -> list[str]:
    order = json.loads(CHRONOLOGY_FILE.read_text(encoding="utf-8"))["order"]
    missing = [s for s in order if s not in LOGOS]
    if missing:
        sys.exit(f"carousel-chronology.json lists slugs with no entry in LOGOS: {missing}")
    for slug in order:
        if not (ROOT / "projects" / f"{slug}.html").is_file():
            print(f"warn: carousel links to projects/{slug}.html, which does not exist")
    return list(reversed(order))  # newest first


def header(prefix: str, active_href: str, order: list[str]) -> str:
    nav = "\n".join(
        f'        <li><a href="{prefix}{href}" class="{"active" if href == active_href else ""}">{label}</a></li>'
        for label, href in NAV
    )
    logos = "\n".join(
        f'      <a class="logo-carousel-link{" logo-carousel-link--" + slug if LOGOS[slug][2] else ""}"'
        f' href="{prefix}projects/{slug}.html" title="{esc(LOGOS[slug][1])}">'
        f'<img src="{prefix}assets/images/{LOGOS[slug][0]}" alt="{esc(LOGOS[slug][1])}" loading="eager" decoding="async"></a>'
        for slug in order
    )
    return f"""  <header class="site-header">
  <div class="top-bar">
    <a href="{prefix}about.html" aria-label="About {OWNER}">
      <img class="profile-thumb" src="{prefix}assets/images/profile-thumb.png" width="40" height="40" alt="{OWNER}">
    </a>
    <a href="{prefix}index.html" class="site-brand">{SITE_NAME}</a>
    <a href="https://www.recordholders.org/en/list/rubik.html" class="rubiks-link" target="_blank" rel="noopener noreferrer" title="Rubik's Cube">
      <img src="{prefix}assets/images/rubiks-cube.png" alt="" width="31" height="31" loading="lazy" decoding="async">
      <span>11.2s average  (80s)</span>
    </a>
    <nav class="nav-wrap" aria-label="Primary">
      <ul class="site-nav">
{nav}
      </ul>
    </nav>
  </div>
    <div class="logo-carousel" aria-label="Career timeline — newest to oldest">
    <div class="logo-carousel-track">
{logos}
    </div>
  </div>
  </header>"""


def footer(prefix: str, extended: bool) -> str:
    if extended:
        copy = f"""    <p class="footer-copy">&copy; {COPYRIGHT_YEAR} {OWNER}.
      <a href="{prefix}resume.html">Resume</a> ·
      <a href="{prefix}assets/Kevin-Guerra.pdf">Resume (PDF)</a> ·
      <a href="{prefix}experience-history.html">Experience History</a> ·
      <a href="{prefix}assets/Kevin-Guerra-Experience-History.pdf">History (PDF)</a>
    </p>"""
    else:
        copy = f'    <p class="footer-copy">&copy; {COPYRIGHT_YEAR} {OWNER}. <a href="{prefix}assets/Kevin-Guerra.pdf">Resume (PDF)</a></p>'
    return f"""  <footer class="site-footer">
    <div class="footer-social">
      <a href="https://www.linkedin.com/in/kevin-guerra-36151446/" target="_blank" rel="noopener" title="LinkedIn">
        <img src="{prefix}assets/images/linkedin.svg" alt="LinkedIn">
      </a>
      <a href="https://github.com/kevingnet" target="_blank" rel="noopener" title="GitHub">
        <img src="{prefix}assets/images/github.jpeg" alt="GitHub">
      </a>
      <a href="https://stackoverflow.com/users/3828838/kevin-guerra" target="_blank" rel="noopener" title="Stack Overflow">
        <img src="{prefix}assets/images/stackoverflow.svg" alt="Stack Overflow">
      </a>
      <a href="mailto:{CONTACT_EMAIL}" title="Email">{CONTACT_EMAIL}</a>
    </div>
{copy}
  </footer>"""


def refresh(path: Path, order: list[str]) -> str | None:
    """Return the page with fresh chrome, or None if it has no site header."""
    text = path.read_text(encoding="utf-8")
    old_header = HEADER_RE.search(text)
    if not old_header:
        return None
    rel = path.relative_to(ROOT)
    prefix = "../" * (len(rel.parts) - 1)
    active = ACTIVE_RE.search(old_header.group(0))
    active_href = active.group(1) if active else "index.html"  # project pages sit under Portfolio
    text = HEADER_RE.sub(lambda _: header(prefix, active_href, order), text, count=1)
    text = FOOTER_RE.sub(lambda _: footer(prefix, rel.as_posix() in EXTENDED_FOOTER), text, count=1)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="only report pages that would change")
    args = ap.parse_args()

    if not args.check and RESUME_SRC.is_file():
        shutil.copy2(RESUME_SRC, ROOT / "assets" / "Kevin-Guerra.pdf")

    order = carousel_order()
    changed = []
    for path in sorted([*ROOT.glob("*.html"), *ROOT.glob("projects/*.html")]):
        new = refresh(path, order)
        if new is None or new == path.read_text(encoding="utf-8"):
            continue
        changed.append(path.relative_to(ROOT).as_posix())
        if not args.check:
            path.write_text(new, encoding="utf-8")

    verb = "would change" if args.check else "updated"
    print(f"{len(changed)} page(s) {verb}" + (": " + ", ".join(changed) if changed else ""))
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
