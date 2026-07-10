#!/usr/bin/env python3
"""Generate static HTML pages for KG Portfolio."""

import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PROJECTS_DIR = ROOT / "projects"
RESUME_SRC = Path("/home/kg/Jobs/Kevin Guerra.pdf")
RESUME_ASSET = "assets/Kevin-Guerra.pdf"

OWNER = "Kevin Alexander Guerra"
OWNER_SHORT = "Kevin"
PROFESSIONAL_TITLE = "Senior Solution Architect"
SITE_NAME = "KG PORTFOLIO"
COPYRIGHT_YEAR = "2026"
CONTACT_EMAIL = "kevingnet1@gmail.com"
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://kevingnet.github.io/kg-portfolio").rstrip("/")
DEV_ROOT = Path("/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development")
DEV_INVENTORY_FILE = ROOT / "data" / "development-inventory.json"
CATALOG_FILE = ROOT / "data" / "portfolio-catalog.json"
COMPILATION_JSON = ROOT / "data" / "portfolio-compilation.json"
NNN_ARCHIVE_JSON = ROOT / "data" / "nnn-archive.json"
CAROUSEL_CHRONOLOGY_FILE = ROOT / "data" / "carousel-chronology.json"
SKIP_COMPILATION_SLUGS = frozenset({"access"})
SKIP_INDEX_SLUGS = frozenset({
    "hivemapper", "chase", "greenleaf", "opentv", "audiotelco",
    "pleiades", "nokio", "enigma", "plastering",
    "bumpershop", "labumpers", "fotografia", "puntabanda",
})  # index grid + carousel (+ project pages via main())
ARCHIVE_SLUG_ALIASES = {"telvista": "audiotelco"}  # archive assets keep legacy folder name
DEV_FOLDER_PREFIX_RE = re.compile(r"^\d{1,2}\s+")
DEV_FOLDER_SORT_RE = re.compile(r"^(\d+)")
RESUME_HTML_SRC = Path("/home/kg/Jobs/Kevin Guerra - Resume.html")
SITE_TAGLINE = (
    f"{PROFESSIONAL_TITLE} portfolio — currently Sr. Software Engineer at MAF RODA Agrobotic; "
    "cloud, distributed systems, performance, security, computer vision, and traceability."
)
DEFAULT_OG_IMAGE = "assets/images/profile.jpeg"

# Applied to any scraped/mirrored HTML as well — longest phrases first
BRANDING_REPLACEMENTS = [
    ("Ismael Guerra Dominguez", OWNER),
    ("Portfolio of Ismael Guerra", f"Portfolio of {OWNER}"),
    ("Ismael Guerra", OWNER),
    ("Hello, my name is Ismael,", f"Hello, my name is {OWNER_SHORT},"),
    ("my name is Ismael", f"my name is {OWNER_SHORT}"),
    ("IGD PORTFOLIO", SITE_NAME),
    ("IGD Portfolio", f"{SITE_NAME}"),
    ("IGD", "KG"),
    ("Ismael", OWNER_SHORT),
]


def apply_branding(text: str) -> str:
    for old, new in BRANDING_REPLACEMENTS:
        text = text.replace(old, new)
    return text


# Legal / distribution boilerplate stripped from extracted archive text (not resume prose).
_LEGAL_INLINE_RE = re.compile(
    r"\s*(?:Google\s+Confidential\s+and\s+Proprietary|and\s+Proprietary\s+Information)\s*",
    re.IGNORECASE,
)
_LEGAL_LINE_RE = re.compile(
    r"^\s*(?:"
    r"Google\s+Confidential\s+and\s+Proprietary|"
    r"and\s+Proprietary\s+Information|"
    r"Copyright\s+Consumer\s+Electronics\s+Association.*|"
    r"Document\s+provided\s+by\s+IHS\s+Licensee=.*|"
    r"Reproduced\s+by\s+IHS\s+under\s+license.*|"
    r"Questions\s+or\s+comments\s+about\s+this\s+message.*|"
    r"This\s+document\s+is\s+copyrighted\s+by\s+CEA.*|"
    r".*\bAll\s+Rights\s+Reserved\b.*|"
    r"CONFIDENTIAL|"
    r"Proprietary\s+and\s+Confidential"
    r")\s*$",
    re.IGNORECASE,
)


def scrub_legal_boilerplate(text: str) -> str:
    if not text:
        return text
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append(line)
            continue
        if _LEGAL_LINE_RE.match(stripped):
            continue
        lines.append(_LEGAL_INLINE_RE.sub("", line))
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def scrub_archive_obj(obj):
    if isinstance(obj, dict):
        out = {}
        for key, val in obj.items():
            if key == "content" and isinstance(val, str):
                out[key] = scrub_legal_boilerplate(val)
            else:
                out[key] = scrub_archive_obj(val)
        return out
    if isinstance(obj, list):
        return [scrub_archive_obj(item) for item in obj]
    return obj


def archive_text(text: str) -> str:
    return scrub_legal_boilerplate(text or "")


HLJS_LANG_ALIASES = {
    "csharp": "csharp",
    "cpp": "cpp",
    "c": "c",
    "python": "python",
    "java": "java",
    "sql": "sql",
    "html": "html",
    "javascript": "javascript",
    "js": "javascript",
    "perl": "perl",
    "yaml": "yaml",
    "xml": "xml",
    "text": "plaintext",
}


def highlight_lang(lang: str | None) -> str:
    key = (lang or "text").strip().lower()
    return HLJS_LANG_ALIASES.get(key, key or "plaintext")


# Archive blocks omitted from portfolio display (junk/reference docs).
SKIP_ARCHIVE_BLOCKS = frozenset({
    "CEA-CEB-10-A.pdf",
    "CEA1.2.new.srt",
    "log.htm",
    "JakeKnowsTemplate.pdf",
    "doc/JakeKnowsTemplate.pdf",
    "JakeKnowsTemplate.dotx",
})

_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")
_ANSI_BASIC = {
    30: "#000000", 31: "#cd3131", 32: "#0dbc79", 33: "#e5e510",
    34: "#2472c8", 35: "#bc3fbc", 36: "#11a8cd", 37: "#e5e5e5",
    90: "#666666", 91: "#f14c4c", 92: "#23d18b", 93: "#f5f543",
    94: "#3b8eea", 95: "#d670d6", 96: "#29b8db", 97: "#ffffff",
}
_ANSI_BASIC_BG = {
    40: "#000000", 41: "#cd3131", 42: "#0dbc79", 43: "#e5e510",
    44: "#2472c8", 45: "#bc3fbc", 46: "#11a8cd", 47: "#e5e5e5",
    100: "#666666", 101: "#f14c4c", 102: "#23d18b", 103: "#f5f543",
    104: "#3b8eea", 105: "#d670d6", 106: "#29b8db", 107: "#ffffff",
}


def _xterm256_rgb(code: int) -> str:
    if code < 16:
        palette = [
            "#000000", "#800000", "#008000", "#808000", "#000080", "#800080",
            "#008080", "#c0c0c0", "#808080", "#ff0000", "#00ff00", "#ffff00",
            "#0000ff", "#ff00ff", "#00ffff", "#ffffff",
        ]
        return palette[code]
    if code < 232:
        code -= 16
        r = code // 36
        code %= 36
        g = code // 6
        b = code % 6
        levels = [0, 95, 135, 175, 215, 255]
        return f"#{levels[r]:02x}{levels[g]:02x}{levels[b]:02x}"
    grey = 8 + (code - 232) * 10
    return f"#{grey:02x}{grey:02x}{grey:02x}"


def _ansi_style(fg: str | None, bg: str | None, bold: bool) -> str:
    parts: list[str] = []
    if fg:
        parts.append(f"color:{fg}")
    if bg:
        parts.append(f"background-color:{bg}")
    if bold:
        parts.append("font-weight:700")
    return ";".join(parts)


def ansi_to_html(text: str) -> str:
    """Convert ANSI SGR escapes to inline HTML spans."""
    if not text or "\x1b[" not in text:
        return html.escape(text or "")

    out: list[str] = []
    fg = bg = None
    bold = False
    open_span = False
    pos = 0

    def close_span() -> None:
        nonlocal open_span
        if open_span:
            out.append("</span>")
            open_span = False

    def sync_span() -> None:
        nonlocal open_span
        close_span()
        style = _ansi_style(fg, bg, bold)
        if style:
            out.append(f'<span style="{style}">')
            open_span = True

    for match in _ANSI_ESCAPE_RE.finditer(text):
        out.append(html.escape(text[pos:match.start()]))
        pos = match.end()
        codes = [int(part) if part else 0 for part in match.group()[2:-1].split(";")]
        i = 0
        while i < len(codes):
            code = codes[i]
            if code == 0:
                fg = bg = None
                bold = False
            elif code == 1:
                bold = True
            elif code == 22:
                bold = False
            elif 30 <= code <= 37 or 90 <= code <= 97:
                fg = _ANSI_BASIC.get(code)
            elif 40 <= code <= 47 or 100 <= code <= 107:
                bg = _ANSI_BASIC_BG.get(code)
            elif code == 38 and i + 1 < len(codes):
                if codes[i + 1] == 5 and i + 2 < len(codes):
                    fg = _xterm256_rgb(codes[i + 2])
                    i += 2
                elif codes[i + 1] == 2 and i + 4 < len(codes):
                    fg = f"#{codes[i + 2]:02x}{codes[i + 3]:02x}{codes[i + 4]:02x}"
                    i += 4
            elif code == 48 and i + 1 < len(codes):
                if codes[i + 1] == 5 and i + 2 < len(codes):
                    bg = _xterm256_rgb(codes[i + 2])
                    i += 2
                elif codes[i + 1] == 2 and i + 4 < len(codes):
                    bg = f"#{codes[i + 2]:02x}{codes[i + 3]:02x}{codes[i + 4]:02x}"
                    i += 4
            elif code == 39:
                fg = None
            elif code == 49:
                bg = None
            i += 1
        sync_span()

    out.append(html.escape(text[pos:]))
    close_span()
    return "".join(out)


def render_archive_text(content: str) -> str:
    content = archive_text(content)
    if "\x1b[" in content:
        inner = ansi_to_html(content)
        return (
            '        <pre class="archive-text archive-ansi"><code>'
            f"{inner}</code></pre>\n"
        )
    return (
        f'        <pre class="archive-text"><code>{html.escape(content)}</code></pre>\n'
    )


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


def filter_archive_data(data: dict) -> dict:
    employers = data.get("employers") or {}
    for entry in employers.values():
        blocks = entry.get("blocks") or []
        filtered = [
            b for b in blocks
            if b.get("title") not in SKIP_ARCHIVE_BLOCKS
            and b.get("rel") not in SKIP_ARCHIVE_BLOCKS
        ]
        entry["blocks"] = filtered
        entry["stats"] = _archive_block_stats(filtered)
    return data


NAV = [
    ("Portfolio", "index.html"),
    ("Services", "services.html"),
    ("Samples", "samples.html"),
    ("About", "about.html"),
]

SOCIAL = {
    "linkedin": "https://www.linkedin.com/in/kevin-guerra-36151446/",
    "github": "https://github.com/kevingnet",
    "stackoverflow": "https://stackoverflow.com/users/3828838/kevin-guerra",
}

# Fallback if catalog not built yet — run tools/extract_development.py
PORTFOLIO_FALLBACK: list[tuple] = []

# (logo stem, extension, display name, slug) — rebuilt in build_carousel_logos()
CAROUSEL_LOGOS: list[tuple[str, str, str, str]] = []


SERVICES = [
    ("Ideation", "Product concepts, architecture options, and rapid prototypes to validate direction before a full build.", "ideation.jpg"),
    ("Web & Cloud Development", "Full-stack apps, REST APIs, microservices, and deployment on AWS, GCP, or Docker.", "web-cloud.jpg"),
    ("Security & Privacy", "Threat modeling, code review, input validation libraries, and compliance-aware design.", "security-privacy.jpg"),
    ("Reverse Engineering", "Legacy system analysis, protocol decoding, and safe modernization paths.", "reverse-engineering.jpg"),
    ("Databases", "Schema design, query optimization, Postgres / SQL Server, and data pipelines.", "databases.jpg"),
    ("Consulting", "Technical leadership, stalled-project recovery, and team mentoring.", "consulting.jpg"),
    ("Custom Applications", "Desktop, embedded, and internal tools tailored to your workflow.", "custom-applications.jpg"),
    ("Performance Optimization", "Profiling-driven speedups — from geospatial XML (11×) to zero-allocation embedded paths.", "performance.jpg"),
    ("Embedded Systems", "Set-top boxes, device drivers, robotics interfaces, and resource-constrained C++.", "embedded.jpg"),
    ("Image Processing", "OCR, machine vision, FFT-based recognition, and video capture pipelines.", "image-processing.jpg"),
]

CORE_SKILLS_FALLBACK = [
    "C/C++", "Python", "Java", "C#", "TypeScript", "Go",
    "Postgres", "SQL Server", "NoSQL", "REST", "Microservices",
    "AWS", "GCP", "Docker", "Linux", "Win32", "Embedded",
    "Security", "OAuth2", "RBAC", "Automation", "OCR",
    "OpenCV", "SIMD", "Traceability", "Machine Learning", "AI",
    "Angular", "Node.js", "Tcl", "CAD/CAM", "Virtualization",
]

LINKEDIN_SKILLS_FILE = ROOT / "data" / "linkedin-skills.json"
CORE_SKILLS_EXCLUDE = frozenset({"C++", "PMD", "Telemarketing"})
CORE_SKILLS_ENSURE = ("NoSQL", "Machine Learning", "AI", "TypeScript")


def load_core_skills() -> list[str]:
    """About-page skill chips — prefer LinkedIn sync (data/linkedin-skills.json)."""
    skills: list[str] | None = None
    if LINKEDIN_SKILLS_FILE.is_file():
        try:
            data = json.loads(LINKEDIN_SKILLS_FILE.read_text(encoding="utf-8"))
            raw = data.get("display_skills")
            if isinstance(raw, list) and raw:
                skills = [str(s) for s in raw]
        except (json.JSONDecodeError, OSError):
            pass
    if skills is None:
        skills = list(CORE_SKILLS_FALLBACK)
    skills = [s for s in skills if s not in CORE_SKILLS_EXCLUDE]
    for skill in CORE_SKILLS_ENSURE:
        if skill not in skills:
            skills.append(skill)
    return skills

# role, dates, note — org name comes from portfolio grid (portfolio_entries order)
TIMELINE_BY_SLUG = {
    "mafroda": (
        "Sr. Software Engineer — R&D Staff", "Apr 2025 – Present",
        "Americas traceability lead; Python fleet installer (WMI/WinRM), OpenCV SIMD on production sorters.",
    ),
    "leidos": (
        "Sr. Solution Architect", "Nov 2022 – Jun 2023",
        "Secure airport scanning app (C++, Qt5, Python); enterprise performance — profiling and caching.",
    ),
    "google": (
        "Sr. Software Engineer / Solution Architect", "2018 – 2022",
        "YouTube, Hardware, Devices (2018–2020); Earth Enterprise & L10n (2020–2022); HR microservices (2022).",
    ),
    "meta": (
        "Privacy Audit Engineer", "Oct 2020 – Mar 2021",
        "Privacy/security assessments for acquisitions; architecture review tooling across SQL/NoSQL estates.",
    ),
    "vmware": (
        "Sr. Member of Technical Staff (MTS)", "2015 – 2016",
        "QA framework rewrite (80k→8k LOC, ~8× faster); ESX/HBR test automation.",
    ),
    "veritas": (
        "Senior Software Developer", "2016 – 2017",
        "NetBackup appliance hardening — OSCAP, OAuth2/LDAP, Java/Python refactor.",
    ),
    "thuuz": (
        "Contract consulting", "",
        "Callsigns JSON API, S3 sync scripts for sports broadcast metadata.",
    ),
    "knurld": (
        "Contract consulting", "",
        "Voice biometric API integration, Apigee, Python ML/scoring pipeline prototypes.",
    ),
    "butterfleye": (
        "Contract consulting", "",
        "Camera cloud backend — Alembic migrations, timeline events, video segments, streaming.",
    ),
    "hpe": (
        "Senior Software Developer", "2017 – 2018",
        "Airwave wireless appliance hardening; Perl→Python port; OSCAP/OWASP compliance.",
    ),
    "jakeknows": (
        "Contract consulting", "",
        "Identity engine, code generators, Sony Taleo mobile job app, WCF engine services.",
    ),
    "yahoo": (
        "Contract consulting", "",
        "Yahoo-era web and infrastructure contract work — see portfolio archive.",
    ),
    "motorola": (
        "Contract consulting", "2009 – 2011",
        "Closed-captioning embedded module for set-top boxes — OCAP, zero post-init allocation.",
    ),
    "surfware": (
        "Contract consulting", "2006 – 2012",
        "Surfcam CAD/CAM features, SolidWorks/AutoCAD import-export, 4/5-axis subsystem.",
    ),
    "spirent": (
        "Senior Software Engineer", "Nov 2005 – Dec 2006",
        "Tcl→C++ network-testing UI; embedded appliance scripting and instrumentation.",
    ),
    "directv": (
        "Contract consulting", "2007 – 2012",
        "OCR client/server pipeline rebuilt in under two months — C++, FFT, ActiveX, Perl automation.",
    ),
    "guidance": (
        "Senior Software Engineer", "Nov 2005 – Dec 2006",
        "Digital forensics — Symantec Ghost format reverse engineering, Win32 disk imaging.",
    ),
    "hms": (
        "Application Security Specialist — Staff", "Mar – Nov 2005",
        "Input validation library, penetration-testing tools, security reviews for e-commerce apps.",
    ),
    "telvista": (
        "Programmer Analyst — Consultant", "Apr 2001 – Nov 2001",
        "~8-month contract — TELMEX/Mexicana MIS, order entry, and scheduling databases.",
    ),
    "voltdelta": (
        "Telecommunications / Network Support", "Nov 1998 – Oct 1999",
        "Phone switch simulator, X.25 relay, and network visualization tools in C++.",
    ),
    "posdev": (
        "Network and Programming Support", "Oct 1999 – Jan 2000",
        "Warehouse PalmOS apps, SendGTL Win32 loader, help desk and network support.",
    ),
    "woodtech": (
        "Senior Software Engineer", "Nov 1996 – Mar 1997",
        "NT/Exchange, BBS file utilities, Netscape server, and executive MIS apps.",
    ),
    "disney": (
        "Senior Software Engineer", "Jul 1997 – Nov 1998",
        "Novell/Windows connector, commissary menu system, ASP/COM web apps for studio MIS.",
    ),
    "electrosonic": (
        "Senior Programmer Analyst — Staff", "Jan 2000 – Apr 2001",
        "AV scheduling, remote monitoring, museum deployments — ESCAN and CommLib winsock stack.",
    ),
    "access": (
        "Programmer and Support Associate", "Mar 1995 – Sep 1996",
        "Predictive dialer installs, Clipper utilities, and mainframe data integration.",
    ),
    "frys": (
        "Software Sales Associate / PC Technician", "Jan 1993 – Feb 1994",
        "Demo systems, software sales floor support, and hardware conflict resolution.",
    ),
    "lcs": (
        "Network and Debugging Support Associate", "Sep 1992 – Jan 1993",
        "Novell NetWare 3.11 installs and VB/Access MIS debugging on LAN/WAN.",
    ),
}

# Non-portfolio-grid roles inserted immediately after the named slug (portfolio order)
TIMELINE_AFTER_SLUG = {
    "leidos": [
        (
            "Senior Solution Architect", "Independent Consultant", "Jul 2023 – Apr 2025",
            "AWS microservices (EC2, S3, Lambda, API Gateway, CloudFormation) for multiple clients.",
        ),
    ],
    "google": [
        (
            "Solution Architect", "Intelliswift · Contractor (Accenture)", "Mar 2021 – Jan 2022",
            "AWS serverless/hybrid cloud; Java static-analysis platform with VS Code/PMD integration.",
        ),
    ],
}


def build_timeline() -> list[tuple[str, str, str, str]]:
    """Career timeline in portfolio grid order; dates match project pages."""
    entries: list[tuple[str, str, str, str]] = []
    for name, _logo, _ext, slug, desc, _skills in portfolio_entries():
        if slug in TIMELINE_BY_SLUG:
            role, dates, note = TIMELINE_BY_SLUG[slug]
        else:
            role, dates, note = "Contract consulting", "", desc
        entries.append((role, name, dates, note))
        entries.extend(TIMELINE_AFTER_SLUG.get(slug, ()))
    return entries

# metric, title, blurb, optional project slug for "read more" link
HIGHLIGHTS = [
    ("2h → 11m", "Google Earth pipeline",
     "Geospatial XML processing — branch reordering, invariant caching, parallel Postgres import.",
     "google"),
    ("7 months", "Localization platform",
     "Unstalled a 2-year project; ~45k LOC legacy replaced with ~24k LOC greenfield + 2k LOC RBAC.",
     "google"),
    ("80k → 8k LOC", "VMware QA framework",
     "Python automation framework ~8× faster than legacy Perl — OOP, functional, and meta-programming.",
     "vmware"),
    ("<2 months", "DirecTV OCR system",
     "Rebuilt failed OCR pipeline after a prior 6-person, 4-year effort — C++, FFT, client/server.",
     "directv"),
]

# title, description, github URL, optional code snippet HTML, optional live demo URL, image filename
SAMPLES = [
    ("Hive Mapper - Drone Navigation, C++",
     "The goal is to navigate a drone through an airport in the shortest time possible. The airport is composed of several interconnected circular roads, and the drone's position is described by a road name and the degrees clockwise around the road's circumference. The drone can transfer between roads at points of intersection. One week for completion.",
     "https://github.com/kevingnet/HiveMapperDrone", None, None, "hive-mapper.jpg"),
    ("Magazine - Node.js REST EC2 App",
     "Magazine sample app using Angular, Node.js with REST API for EC2 deployment. One week for completion.",
     "https://github.com/kevingnet/magazine", None, "https://kevingnet.github.io/magazine/", "magazine.jpg"),
    ("Game of Life - Java",
     "Conway's Game of Life - Java implementation. One day to develop.",
     "https://github.com/kevingnet/GameOfLife", None, "https://kevingnet.github.io/GameOfLife/", "game-of-life.jpg"),
    ("Word Finder - C++",
     "Find Longest Word Made of Other Words. Program reads a file containing a sorted list of words (one word per line, no spaces, all lower case), then identifies the longest word in the file that can be constructed by concatenating copies of shorter words also found in the file.",
     "https://github.com/kevingnet/WordFinder", None, None, "word-finder.jpg"),
    ("Virtual Coffee Machine",
     "Cloud app on AWS using Docker containers. Server is a NodeJS app with a simple API (level(GET), brew, refill (POST). A Client in TypeScript accesses those APIs to operate. 6 days to complete.",
     "https://github.com/kevingnet/coffee.bitnami", None,
     "https://kevingnet.github.io/coffee.bitnami/", "coffee.jpg"),
    ("Flux - Electric Vehicle",
     "Project Plan - 30, 60 and 90 days. Developed plan in two days. Look at Diagram and Architecture Document.",
     "https://github.com/kevingnet/FluxElectricVehicle", None, "https://kevingnet.github.io/FluxElectricVehicle/", "flux.jpg"),
    ("Time Server - Client/Server, TypeScript, JavaScript, SQL, Python",
     "Time Server sample app using Angular, Node.js with REST API for EC2 deployment. One week to develop.",
     "https://github.com/kevingnet/time_server", None, "https://kevingnet.github.io/time_server/", "time-server.jpg"),
]


def timeline_block() -> str:
    items = []
    for role, org, era, note in build_timeline():
        dates_html = (
            f'\n              <span class="timeline-dates">{html.escape(era)}</span>'
            if era else ""
        )
        items.append(
            f"""          <div class="timeline-item">
            <div class="timeline-header">
              <strong class="timeline-role">{html.escape(role)}</strong>{dates_html}
            </div>
            <div class="timeline-org">{html.escape(org)}</div>
            <p>{html.escape(note)}</p>
          </div>"""
        )
    return "\n".join(items)


def skill_chips(skills: list[str], limit: int | None = None) -> str:
    items = skills[:limit] if limit else skills
    return '<div class="skill-row">' + "".join(
        f'<span class="skill-chip">{html.escape(s)}</span>' for s in items
    ) + "</div>"


def highlights_strip(depth: int = 0) -> str:
    p = rel_prefix(depth)
    cards = []
    for metric, title, blurb, slug in HIGHLIGHTS:
        link = f'{p}projects/{slug}.html' if slug else None
        title_html = (
            f'<a href="{link}">{html.escape(title)}</a>' if link
            else html.escape(title)
        )
        cards.append(
            f"""      <article class="highlight-card fade-in">
        <span class="highlight-metric">{html.escape(metric)}</span>
        <h2 class="highlight-title">{title_html}</h2>
        <p>{html.escape(blurb)}</p>
      </article>"""
        )
    return (
        '    <section class="highlights-strip fade-in" aria-label="Selected highlights">\n'
        '      <h2 class="highlights-heading">Selected highlights</h2>\n'
        '      <div class="highlights-grid">\n'
        + "\n".join(cards)
        + "\n      </div>\n    </section>"
    )


def sample_entry(
    title: str,
    desc: str,
    gh: str | None,
    snippet: str | None,
    demo: str | None,
    image: str,
    depth: int = 0,
) -> str:
    p = rel_prefix(depth)
    link = demo or gh
    title_html = (
        f'<a href="{link}" target="_blank" rel="noopener">{html.escape(title)}</a>'
        if link else html.escape(title)
    )
    links = []
    if gh:
        links.append(f'<a href="{gh}" target="_blank" rel="noopener">GitHub</a>')
    if demo:
        links.append(f'<a href="{demo}" target="_blank" rel="noopener">LiveDemo</a>')
    links_block = (
        f'          <div class="sample-links">\n            {" ".join(links)}\n          </div>'
        if links else ""
    )
    img_link = link or gh or "#"
    return f"""      <article class="sample-entry fade-in">
        <div class="sample-entry-img">
          <a href="{img_link}" target="_blank" rel="noopener">
            <img src="{p}assets/images/samples/{html.escape(image)}" alt="{html.escape(title)}" loading="lazy">
          </a>
        </div>
        <div class="sample-entry-body">
          <h2>{title_html}</h2>
          <p>{html.escape(desc)}</p>
          {snippet or ""}
{links_block}
        </div>
      </article>"""


def tech_to_chips(tech: str, limit: int = 16) -> str:
    parts = [t.strip() for t in tech.replace(";", ",").split(",") if t.strip()]
    return skill_chips(parts, limit)


def project_gallery(figures: list[tuple[str, str]], depth: int = 1, extra_class: str = "") -> str:
    """figures: list of (filename under projects/mafroda/, caption)"""
    p = rel_prefix(depth)
    gallery_cls = "project-gallery"
    if extra_class:
        gallery_cls += f" {extra_class}"
    items = "\n".join(
        f"""      <figure class="project-figure">
        <img src="{p}assets/images/projects/mafroda/{fname}" alt="{html.escape(caption)}" loading="lazy">
        <figcaption>{html.escape(caption)}</figcaption>
      </figure>"""
        for fname, caption in figures
    )
    return f'      <div class="{gallery_cls}">\n{items}\n      </div>'


def copy_maf_project_images() -> None:
    trace_src = Path("/home/kg/Jobs/Graphics/Screenshot 2026-06-30 081832")
    legacy_src = Path("/home/kg/Jobs/Graphics/images")
    dest = ROOT / "assets/images/projects/mafroda"
    dest.mkdir(parents=True, exist_ok=True)
    mapping = [
        ("traceability-overview.png", trace_src / "Screenshot 2026-06-25 150107.png"),
        ("traceability-dashboard.png", trace_src / "Screenshot 2026-06-30 081603.png"),
        ("traceability-detail.png", trace_src / "Screenshot 2026-06-30 081733.png"),
        ("traceability-ui.png", trace_src / "Screenshot 2026-06-30 081832.png"),
        ("installer-gui.png", legacy_src / "Screenshot 2025-08-01 131140.png"),
        ("installer-scripts.png", legacy_src / "ListOfScripts.png"),
    ]
    for dest_name, src in mapping:
        if src.is_file():
            shutil.copy2(src, dest / dest_name)


def rel_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def carousel(depth: int = 0) -> str:
    p = rel_prefix(depth)
    items = "\n".join(
        f'      <a class="logo-carousel-link" href="{p}projects/{html.escape(slug)}.html"'
        f' title="{html.escape(alt)}">'
        f'<img src="{p}assets/images/{logo}.{ext}" alt="{html.escape(alt)}" loading="eager" decoding="async"></a>'
        for logo, ext, alt, slug in CAROUSEL_LOGOS
    )
    return f"""  <div class="logo-carousel" aria-label="Career timeline — oldest to newest">
    <div class="logo-carousel-track">
{items}
    </div>
  </div>"""


def header(active: str, depth: int = 0) -> str:
    p = rel_prefix(depth)
    links = "\n".join(
        f'        <li><a href="{p}{href}" class="{"active" if label == active else ""}">{label}</a></li>'
        for label, href in NAV
    )
    return f"""  <header class="site-header">
  <div class="top-bar">
    <a href="{p}about.html" aria-label="About {OWNER}">
      <img class="profile-thumb" src="{p}assets/images/profile.jpeg" alt="{OWNER}">
    </a>
    <a href="{p}index.html" class="site-brand">{SITE_NAME}</a>
    <a href="https://www.recordholders.org/en/list/rubik.html" class="rubiks-link" target="_blank" rel="noopener noreferrer" title="Rubik's Cube">
      <img src="{p}assets/images/rubiks-cube.png" alt="" width="31" height="31" loading="lazy" decoding="async">
      <span>11.2s average  (80s)</span>
    </a>
    <nav class="nav-wrap" aria-label="Primary">
      <ul class="site-nav">
{links}
      </ul>
    </nav>
  </div>
{carousel(depth)}
  </header>"""


def load_catalog() -> dict:
    if CATALOG_FILE.is_file():
        try:
            return json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"portfolio": []}


def display_dev_folder(name: str) -> str:
    """Strip leading archive numbers (e.g. '03 Disney' → 'Disney')."""
    if not name:
        return name
    return DEV_FOLDER_PREFIX_RE.sub("", name).strip() or name


def load_compilation() -> dict[str, dict]:
    if COMPILATION_JSON.is_file():
        try:
            return json.loads(COMPILATION_JSON.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def compilation_block(slug: str) -> str:
    """HTML from portfolio-compilation.json for this project slug."""
    return ""


def project_from_compilation(slug: str, card: dict) -> dict:
    """Build a project page primarily from compilation data."""
    entry = load_compilation().get(slug, {})
    name = card.get("name") or entry.get("folder") or slug
    title = f"{name} Projects"
    meta = entry.get("meta") or {}
    intro_parts = [f"<p><strong>{html.escape(name)}</strong></p>"]
    if meta.get("purpose"):
        intro_parts.append(f"<p>{html.escape(meta['purpose'])}</p>")
    elif card.get("desc"):
        intro_parts.append(f"<p>{html.escape(card['desc'])}</p>")
    bits = []
    if meta.get("era"):
        bits.append(f"Era: {meta['era']}")
    if meta.get("domain"):
        bits.append(meta["domain"])
    if bits:
        intro_parts.append(f"<p><em>{html.escape(' · '.join(bits))}</em></p>")
    tech = ", ".join(meta.get("technologies") or card.get("skills") or [])
    return {
        "title": title,
        "intro": "\n".join(intro_parts),
        "tech": tech or ", ".join(card.get("skills") or []),
    }


def portfolio_entries() -> list[tuple]:
    """(name, logo, ext, slug, desc, skills) from Development catalog."""
    cards = load_catalog().get("portfolio") or []
    if not cards:
        return PORTFOLIO_FALLBACK
    return [
        (c["name"], c["logo"], c["ext"], c["slug"], c["desc"], c["skills"])
        for c in cards
        if c["slug"] not in SKIP_INDEX_SLUGS
    ]


def dev_folder_sort_key(folder: str) -> tuple:
    m = DEV_FOLDER_SORT_RE.match(folder or "")
    return (int(m.group(1)) if m else 999, folder or "")


def load_carousel_chronology() -> list[str]:
    if CAROUSEL_CHRONOLOGY_FILE.is_file():
        try:
            data = json.loads(CAROUSEL_CHRONOLOGY_FILE.read_text(encoding="utf-8"))
            order = data.get("order")
            if isinstance(order, list) and order:
                return [str(s) for s in order]
        except (json.JSONDecodeError, OSError):
            pass
    return []


def report_carousel_discrepancies(cards_by_slug: dict[str, dict], resume_order: list[str]) -> None:
    """Log Development-folder vs resume-order inversions (resume wins in the carousel)."""
    dev_slugs = [
        c["slug"] for c in sorted(
            cards_by_slug.values(),
            key=lambda c: dev_folder_sort_key(c.get("dev_folder") or ""),
        )
        if c.get("dev_folder")
    ]
    resume_rank = {slug: i for i, slug in enumerate(resume_order)}
    dev_rank = {slug: i for i, slug in enumerate(dev_slugs)}
    shared = [s for s in resume_order if s in dev_rank]
    inversions: list[str] = []
    for i, a in enumerate(shared):
        for b in shared[i + 1:]:
            if dev_rank[a] > dev_rank[b] and resume_rank[a] < resume_rank[b]:
                fa = cards_by_slug[a].get("dev_folder", a)
                fb = cards_by_slug[b].get("dev_folder", b)
                inversions.append(f"{fa} after {fb} in Development, but resume places {a} before {b}")
    if inversions:
        print("Carousel order: resume overrides Development folder numbering for:")
        for line in inversions[:12]:
            print(f"  · {line}")
        if len(inversions) > 12:
            print(f"  · … +{len(inversions) - 12} more")


def build_carousel_logos() -> None:
    """Oldest → newest (left to right): reverse of portfolio grid order."""
    global CAROUSEL_LOGOS
    entries = portfolio_entries()
    CAROUSEL_LOGOS = [
        (logo, ext, name, slug)
        for name, logo, ext, slug, desc, skills in reversed(entries)
    ]
    sync_carousel_chronology_json([slug for _, _, _, slug in CAROUSEL_LOGOS])


def sync_carousel_chronology_json(slugs: list[str]) -> None:
    """Keep carousel-chronology.json aligned with portfolio-derived order."""
    data: dict = {}
    if CAROUSEL_CHRONOLOGY_FILE.is_file():
        try:
            data = json.loads(CAROUSEL_CHRONOLOGY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    data["description"] = (
        "Carousel logo order oldest → newest (left to right). "
        "Auto-synced from portfolio grid order on each build."
    )
    data["order"] = slugs
    CAROUSEL_CHRONOLOGY_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sync_static_page_carousels() -> None:
    """Keep manually maintained pages using the same carousel as generated headers."""
    block = carousel(0)
    pattern = re.compile(
        r'  <div class="logo-carousel"[^>]*>\s*<div class="logo-carousel-track">.*?</div>\s*</div>',
        re.DOTALL,
    )
    for rel in ("experience-history.html", "resume.html"):
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if not pattern.search(text):
            continue
        path.write_text(pattern.sub(block, text, count=1), encoding="utf-8")


def auto_project(slug: str, card: dict) -> dict:
    """Generate project page from catalog + Development inventory."""
    tags = []
    if card.get("in_current_resume"):
        tags.append("Current resume")
    elif card.get("in_old_resume"):
        tags.append("Generic Resume")
    tag_html = ""
    if tags:
        tag_html = f'<p class="portfolio-tag"><em>{html.escape(" · ".join(tags))}</em></p>'
    intro_parts = [
        f"<p><strong>{html.escape(card['name'])}</strong></p>",
        tag_html,
        f"<p>{html.escape(card['desc'])}</p>",
    ]
    return {
        "title": f"{card['name']} Projects",
        "intro": "\n".join(intro_parts),
        "tech": ", ".join(card.get("skills", [])),
    }


def ensure_all_projects() -> None:
    compilation = load_compilation()
    for card in load_catalog().get("portfolio", []):
        slug = card["slug"]
        if slug not in PROJECTS:
            if slug in compilation:
                PROJECTS[slug] = project_from_compilation(slug, card)
            else:
                PROJECTS[slug] = auto_project(slug, card)


def load_dev_inventory() -> dict:
    if DEV_INVENTORY_FILE.is_file():
        try:
            return json.loads(DEV_INVENTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"employers": {}}


def load_nnn_archive() -> dict:
    if NNN_ARCHIVE_JSON.is_file():
        try:
            return filter_archive_data(
                scrub_archive_obj(
                    json.loads(NNN_ARCHIVE_JSON.read_text(encoding="utf-8"))
                )
            )
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def render_doc_figures(images: list[dict]) -> str:
    if not images:
        return ""
    cells = []
    for img in images:
        src = html.escape(img.get("src") or "")
        alt = html.escape(img.get("alt") or "Figure")
        w = img.get("width")
        h = img.get("height")
        dim = ""
        try:
            if int(w) > 0 and int(h) > 0:
                dim = f' width="{int(w)}" height="{int(h)}"'
        except (TypeError, ValueError):
            dim = ""
        cap = html.escape(img.get("caption") or "")
        cap_html = f'<figcaption>{cap}</figcaption>' if cap else ""
        cells.append(
            '          <figure class="archive-doc-figure">\n'
            f'            <img src="../{src}" alt="{alt}" loading="eager" decoding="async"{dim}>\n'
            f"            {cap_html}\n"
            "          </figure>"
        )
    grid_class = "archive-doc-figures__grid"
    if len(images) == 1:
        grid_class += " archive-doc-figures__grid--solo"
    return (
        '        <div class="archive-doc-segment archive-doc-segment--figures">\n'
        f'          <div class="{grid_class}">\n'
        + "\n".join(cells)
        + "\n          </div>\n        </div>"
    )


def render_doc_segments(segments: list[dict]) -> str:
    parts = ['        <div class="archive-doc-body">']
    for seg in segments:
        kind = seg.get("kind")
        if kind == "text":
            content = html.escape(archive_text(seg.get("content") or ""))
            if not content.strip():
                continue
            parts.append(
                '        <div class="archive-doc-segment archive-doc-segment--text">'
                f"{content}</div>"
            )
        elif kind == "figures":
            fig_html = render_doc_figures(seg.get("images") or [])
            if fig_html:
                parts.append(fig_html)
    parts.append("        </div>")
    return "\n".join(parts)


def render_pdf_embed(pdf_src: str, title: str, depth: int = 1) -> str:
    url = html.escape(f"{rel_prefix(depth)}{pdf_src}")
    safe_title = html.escape(title)
    return (
        '        <div class="archive-pdf-embed">\n'
        f'        <object data="{url}" type="application/pdf" width="100%" height="600px">\n'
        f'            <iframe src="{url}" width="100%" height="100%" style="border: none;" title="{safe_title}">\n'
        "                <p>Your browser does not support embedded PDFs.\n"
        f'                   <a href="{url}">Download the PDF instead</a>.\n'
        "                </p>\n"
        "            </iframe>\n"
        "        </object>\n"
        "        </div>"
    )


def render_nnn_block(block: dict) -> str:
    """Render one showcase block from nnn-archive.json."""
    btype = block.get("type")
    if btype == "section":
        return f'      <div class="archive-section-label">{html.escape(block.get("title") or "")}</div>'
    title = html.escape(block.get("title") or "Untitled")
    rel = block.get("rel") or ""
    path_hint = html.escape(rel) if rel else ""

    if btype == "image":
        src = html.escape(block.get("src") or "")
        alt = html.escape(block.get("alt") or title)
        cap = f'<figcaption class="archive-figure__caption"><span class="archive-filename">{title}</span>'
        if path_hint:
            cap += f'<span class="archive-path">{path_hint}</span>'
        cap += "</figcaption>"
        return (
            '      <figure class="archive-figure">\n'
            f'        <div class="archive-figure__frame"><img src="../{src}" alt="{alt}" loading="lazy" decoding="async"></div>\n'
            f"        {cap}\n"
            "      </figure>"
        )

    badge = {
        "code": "CODE",
        "text": "TEXT",
        "document": "PDF" if block.get("pdf_src") else "DOC",
    }.get(btype, btype.upper() if btype else "")
    header = (
        f'        <div class="archive-panel__header">\n'
        f'          <span class="archive-badge-type">{badge}</span>\n'
        f'          <span class="archive-filename">{title}</span>\n'
    )
    if path_hint:
        header += f'          <span class="archive-path">{path_hint}</span>\n'
    header += "        </div>"

    content = archive_text(block.get("content") or "")
    truncated = block.get("truncated")
    meta = ""
    if truncated:
        if btype == "code" and block.get("line_count"):
            meta = f'        <p class="archive-truncated">Showing excerpt of {block["line_count"]} lines.</p>\n'
        else:
            meta = '        <p class="archive-truncated">Excerpt shown — full document in archive.</p>\n'

    if btype == "code":
        lang = html.escape(highlight_lang(block.get("lang")))
        body = (
            f'        <pre class="archive-code"><code class="language-{lang}">'
            f"{html.escape(content)}</code></pre>\n"
        )
        panel_class = "archive-panel archive-panel--code"
    elif btype == "document":
        pdf_src = block.get("pdf_src")
        if pdf_src:
            body = render_pdf_embed(pdf_src, block.get("title") or "Document") + "\n"
        else:
            segments = block.get("segments") or []
            if segments:
                body = render_doc_segments(segments) + "\n"
                if truncated and content:
                    body += (
                        '        <details class="archive-doc-fulltext">\n'
                        '          <summary>Full extracted text</summary>\n'
                        f'          <div class="archive-doc">{html.escape(content)}</div>\n'
                        "        </details>\n"
                    )
            else:
                body = f'        <div class="archive-doc">{html.escape(content)}</div>\n'
        panel_class = "archive-panel archive-panel--doc"
    elif btype == "text":
        body = render_archive_text(content)
        panel_class = "archive-panel archive-panel--text"
    else:
        return ""

    return (
        f'      <article class="{panel_class}">\n'
        f"{header}"
        f"{body}"
        f"{meta}"
        "      </article>"
    )


def nnn_archive_block(slug: str) -> str:
    """HTML showcase from nnn professional archive."""
    archive_slug = ARCHIVE_SLUG_ALIASES.get(slug, slug)
    entry = load_nnn_archive().get("employers", {}).get(archive_slug)
    if not entry:
        entry = load_nnn_archive().get("employers", {}).get(slug)
    if not entry or not entry.get("blocks"):
        return ""
    stats = entry.get("stats") or {}
    bits = []
    if stats.get("code"):
        bits.append(f"{stats['code']} source file{'s' if stats['code'] != 1 else ''}")
    if stats.get("document"):
        bits.append(f"{stats['document']} document{'s' if stats['document'] != 1 else ''}")
    if stats.get("text"):
        bits.append(f"{stats['text']} note{'s' if stats['text'] != 1 else ''}")
    if stats.get("image"):
        bits.append(f"{stats['image']} image{'s' if stats['image'] != 1 else ''}")
    if stats.get("figures"):
        bits.append(f"{stats['figures']} embedded figure{'s' if stats['figures'] != 1 else ''}")
    summary = ", ".join(bits) if bits else "archive materials"
    name = html.escape(entry.get("name") or slug)
    parts = [
        '      <section class="archive-showcase">',
        "      <h2>Archive showcase</h2>",
        f'      <p class="archive-lead"><em>{name}</em> — {html.escape(summary)} from the professional archive.</p>',
    ]
    for block in entry["blocks"]:
        parts.append(render_nnn_block(block))
    parts.append("      </section>")
    return "\n".join(parts)


def head_meta(
    full_title: str,
    desc: str,
    p: str,
    slug_path: str,
    og_image: str | None,
) -> str:
    """Local-first head tags — no absolute canonical/OG URLs unless SITE_BASE_URL is set."""
    lines = [
        f"  <title>{full_title}</title>",
        f'  <meta name="description" content="{desc}">',
        f'  <link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">',
        f'  <meta name="theme-color" content="#0e1014">',
        f'  <link rel="stylesheet" href="{p}css/style.css">',
        f'  <link rel="stylesheet" href="{p}assets/vendor/highlight/styles/github-dark.min.css">',
    ]
    if SITE_BASE_URL:
        canon = f"{SITE_BASE_URL}/{slug_path.replace('index.html', '').rstrip('/')}"
        if slug_path == "index.html":
            canon = f"{SITE_BASE_URL}/"
        img_rel = (og_image or DEFAULT_OG_IMAGE).removeprefix("../")
        og_img = f"{SITE_BASE_URL}/{img_rel}"
        lines[2:2] = [
            f'  <link rel="canonical" href="{canon}">',
            '  <meta property="og:type" content="website">',
            f'  <meta property="og:site_name" content="{SITE_NAME}">',
            f'  <meta property="og:title" content="{full_title}">',
            f'  <meta property="og:description" content="{desc}">',
            f'  <meta property="og:url" content="{canon}">',
            f'  <meta property="og:image" content="{og_img}">',
            '  <meta name="twitter:card" content="summary">',
            f'  <meta name="twitter:title" content="{full_title}">',
            f'  <meta name="twitter:description" content="{desc}">',
            f'  <meta name="twitter:image" content="{og_img}">',
        ]
    return "\n".join(lines)


def social_icon_links(depth: int = 0) -> str:
    """LinkedIn, GitHub, Stack Overflow — shared by footer and hero."""
    p = rel_prefix(depth)
    return f"""      <a href="{SOCIAL["linkedin"]}" target="_blank" rel="noopener" title="LinkedIn">
        <img src="{p}assets/images/linkedin.svg" alt="LinkedIn">
      </a>
      <a href="{SOCIAL["github"]}" target="_blank" rel="noopener" title="GitHub">
        <img src="{p}assets/images/github.jpeg" alt="GitHub">
      </a>
      <a href="{SOCIAL["stackoverflow"]}" target="_blank" rel="noopener" title="Stack Overflow">
        <img src="{p}assets/images/stackoverflow.svg" alt="Stack Overflow">
      </a>"""


def footer(depth: int = 0) -> str:
    p = rel_prefix(depth)
    return f"""  <footer class="site-footer">
    <div class="footer-social">
{social_icon_links(depth)}
      <a href="mailto:{CONTACT_EMAIL}" title="Email">{CONTACT_EMAIL}</a>
    </div>
    <p class="footer-copy">&copy; {COPYRIGHT_YEAR} {OWNER}. <a href="{p}{RESUME_ASSET}">Resume (PDF)</a></p>
  </footer>"""


def page(
    title: str,
    active: str,
    body: str,
    depth: int = 0,
    *,
    description: str | None = None,
    slug_path: str | None = None,
    og_image: str | None = None,
) -> str:
    p = rel_prefix(depth)
    desc = description or SITE_TAGLINE
    if slug_path is None:
        slug_path = {
            "Portfolio": "index.html",
            "Services": "services.html",
            "Samples": "samples.html",
            "History": "experience-history.html",
            "About": "about.html",
        }.get(active, "index.html")
    full_title = f"{title} | {SITE_NAME}"
    meta = head_meta(full_title, desc, p, slug_path, og_image)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
{meta}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header(active, depth)}
  <main id="main-content">
{body}
  </main>
{footer(depth)}
  <script src="{p}assets/vendor/highlight/highlight.min.js"></script>
  <script src="{p}js/carousel.js"></script>
  <script src="{p}js/site.js"></script>
</body>
</html>
"""

PROJECTS = {
    "mafroda": {
        "title": "MAF RODA Agrobotic",
        "intro": """<p><strong>Sr. Software Engineer — R&amp;D Staff</strong> · Apr 2025 – Present · Traver, CA</p>
<p>MAF RODA Agrobotic — global leader in post-harvest fruit and vegetable automation (sorting, grading, packaging, palletizing). Current role (3rd at MAF RODA): <strong>Americas traceability lead</strong>.</p>
<ul>
<li><strong>Traceability — Americas:</strong> lead regional traceability systems; AI-assisted tooling and codebase modernization</li>
<li><strong>OpenCV:</strong> SIMD + startup buffer pre-allocation on production sorters</li>
<li><strong>Python fleet installer (ORPHEA):</strong> YAML-driven operations framework — WMI/WinRM discovery, network config, remote provisioning of sorting clusters</li>
<li><strong>UiSettingsEditor:</strong> WinForms C# tool for production HMI skin / Figma palette settings (JSON appsettings)</li>
<li><strong>OrpheaSimulator:</strong> ASP.NET Core REST API backing traceability and packing web views</li>
</ul>""",
        "tech": "Python, OpenCV, SIMD, C++, C#, ASP.NET Core, WinForms, WMI, WinRM, YAML, JSON, Windows, Image Processing, Traceability, Fleet Deployment, Network Provisioning, AI-Assisted Development",
        "sections": [
            ("Traceability — Americas", "Current · Regional traceability lead", """<p>Lead traceability systems across the Americas. Apply AI on the engineering side — developer tooling, codebase modernization, and AI-assisted improvements to traceability projects and delivery workflows.</p>
<p>Screenshots from traceability tooling and web views deployed in the MAF sorting environment.</p>"""
            + project_gallery([
                ("traceability-overview.png", "Traceability — sorting line overview"),
                ("traceability-dashboard.png", "Traceability dashboard — production sorting"),
                ("traceability-detail.png", "Traceability detail — lot and lane tracking"),
                ("traceability-ui.png", "Traceability UI — monitoring and configuration"),
            ], extra_class="project-gallery--large")),
            ("OpenCV Performance", "SIMD · Buffer pre-allocation · Production sorters", """<p>Optimized OpenCV image-processing paths on production fruit sorters using SIMD intrinsics and an allocation strategy that pre-allocates buffers at startup.</p>
<p>Result: reduced runtime memory footprint and buffer churn during high-throughput sorting operations on the line.</p>"""),
            ("Python Fleet Installer", "ORPHEA Operations Framework · Python · YAML · WinRM", """<p>Designed and built the <strong>MAF Silent Install</strong> / ORPHEA operations framework: a layered Python system that provisions fruit-sorting clusters from YAML configuration.</p>
<ul>
<li>Multi-tier architecture: high-level modules, operation objects, and support layer (WinRM, PSRP, OpenSSH, PsExec, WMIC, netsh)</li>
<li>Remote handling of large installer payloads (~10 GB), decompression, and end-to-end software deployment on Orphea, Engine, and cluster hosts</li>
<li>GUI (<code>run_gui.py</code>) and batch runners for field engineers; script catalog and per-operation YAML configs</li>
<li>Documented in <em>Software Architecture Document</em>, <em>Functional Specifications</em>, and <em>Framework.md</em> (installer.doc)</li>
</ul>"""
            + project_gallery([
                ("installer-gui.png", "Installer GUI — fleet deployment control panel"),
                ("installer-scripts.png", "Operations script catalog — batch and individual runners"),
            ])),
            ("UiSettingsEditor", "C# · WinForms · JSON · Figma palettes", """<p>Desktop sample application for editing production UI settings used on sorting-line HMIs.</p>
<ul>
<li>Loads and saves JSON <code>appsettings</code> for skin, outlet, and message styling</li>
<li>Figma-integrated color palette editor with live swatches (container, label, font, border, clock, message stroke/shadow)</li>
<li>Validates combinations and syncs palette slots for article / outlet configurations</li>
</ul>
<p>Stack: .NET WinForms, System.Text.Json, custom color-swatch controls.</p>"""),
            ("OrpheaSimulator", "ASP.NET Core · REST · JSON", """<p>Sample web API supporting traceability and packing workflows — serves JSON to Angular / web front ends in the MAF ecosystem.</p>
<ul>
<li>ASP.NET Core minimal hosting with controllers and OpenAPI</li>
<li>JSON serialization with explicit property naming for legacy client compatibility</li>
<li>CORS-enabled development mode; integrates with ArticlesImg XML and web view projects</li>
</ul>
<p>Companion to web modules (WebPacking, WebViewBinFillers, LindaVista) in the Graphics tree.</p>"""),
        ],
    },
    "leidos": {
        "title": "Leidos Projects",
        "intro": """<p><strong>Sr. Solution Architect</strong> · Nov 2022 – Jun 2023 · Remote</p>
<p>Leidos — defense, aviation, and information-technology company building mission-critical systems for government and commercial customers. Contract via KForce.</p>
<ul>
<li><strong>Airport scanning application:</strong> C++ / Qt5 front end with Python imaging pipeline for high-assurance environments</li>
<li><strong>Enterprise architecture:</strong> performance profiling, caching, and throughput tuning on high-transaction systems</li>
<li><strong>Security-first design:</strong> reliability and accurate image processing where operational failure is not an option</li>
</ul>""",
        "tech": "C++, Qt5, Python, Image Processing, Security, Enterprise Architecture, Performance Profiling, Caching, High-Transaction Systems",
        "sections": [
            ("Airport Scanning Application", "C++, Qt5, Python · High-assurance imaging", """<p>Developed a secure airport scanning application combining a C++ and Qt5 operator UI with Python components for the imaging pipeline.</p>
<ul>
<li>Built for high-assurance environments — reliability, security, and accurate image processing are operational requirements</li>
<li>Integrated C++ UI with Python image-processing modules across a multi-language codebase</li>
<li>Qt5 desktop patterns for operator workflows in regulated airport security contexts</li>
</ul>"""),
            ("Enterprise Architecture", "Performance · Profiling · Caching", """<p>Solution architecture and performance engineering on high-transaction enterprise systems.</p>
<ul>
<li>Profiling-driven identification of bottlenecks under production-like load</li>
<li>Caching strategies to improve throughput and responsiveness</li>
<li>Architecture guidance for teams maintaining latency-sensitive services</li>
</ul>"""),
        ],
    },
    "google": {
        "title": "Google Projects",
        "intro": """<p><strong>Sr. Software Engineer / Solution Architect</strong> · 2018 – 2022 · Remote / Mountain View</p>
<p>Google — multiple teams · Contractors. Focus: stalled-project recovery, performance optimization, privacy-aware microservices, and greenfield rewrites at global scale.</p>
<ul>
<li><strong>YouTube, Hardware, Devices (2018–2020):</strong> Java/C++/Python microservices; Python/Angular/TypeScript on Borg; authN/authZ, audit tooling, BigQuery pipelines</li>
<li><strong>Earth Enterprise &amp; L10n (2020–2022):</strong> geospatial XML pipeline <strong>2 hours → 11 minutes</strong> (~11×); greenfield ~24k LOC replacement of ~45k LOC legacy platform + 2k LOC RBAC — delivered in 7 months after two years of stagnation</li>
<li><strong>HR (2022):</strong> Java microservices (Guice, Protobuf) for privacy-conscious internal payroll tooling</li>
</ul>""",
        "tech": "Java, Python, C++, Postgres, Dart, TypeScript, Angular, GCP, App Engine, BigQuery, Microservices, OAuth2, RBAC, Protobuf, Guice, Borg, HTML5, CSS, Memcache",
        "sections": [
            ("Localization Platform", "Avik / Babel · Java · Dart · RBAC · 7-month delivery", """<p>Led recovery and greenfield rewrite of a global localization platform that had been stalled for two years.</p>
<ul>
<li>Replaced ~45k LOC legacy web stack with ~16k LOC Java backend and ~6k LOC Dart front end (~24k LOC total)</li>
<li>Authored ~2k LOC RBAC module (MAC, DAC, authentication and authorization) — OAuth2-aware security layer</li>
<li>Onboarded to Google stack and a 60k+ LOC enterprise codebase in ~2 months; reverse-engineered legacy Java</li>
<li>Simplified operator workflow with highly performant operation; projected ~$500k first-year vendor savings plus user time savings</li>
<li>Unit, integration, and performance tests; Datastore / App Engine and internal APIs</li>
</ul>"""),
            ("Google Earth Enterprise", "C++, Python · Open source · 11× XML speedup", """<p>Maintained and optimized Google Earth Enterprise after open-source conversion — library upgrades and code optimization across C++, Python, and JavaScript.</p>
<ul>
<li><strong>Geospatial XML pipeline:</strong> reduced processing from ~2 hours to ~11 minutes via three-prong approach</li>
<li>Branch reordering — moved hot paths to the top of Python control flow</li>
<li>Parallel Postgres import using file-based bulk load</li>
<li>C++ / Python invariant caching for geospatial calculations — skip redundant point-invariant work</li>
<li>Modernized C++ dependencies; Postgres and image-processing integration</li>
</ul>"""),
            ("Hardware Analytics", "Python · Angular · BigQuery · Microservices", """<p>Architecture, design, and delivery for the Hardware Analytics team.</p>
<ul>
<li>Authentication and authorization mechanisms for security and privacy-policy compliance</li>
<li>Auditing solutions and automatic alerting pipelines</li>
<li>Cloud development on Borg and related internal platforms</li>
</ul>"""),
            ("Google Devices", "Python · Java · Speech data collection", """<p>Speech Data Collection Tools — automation and simplification of device data capture.</p>
<ul>
<li>Built testing framework for first- and third-party devices</li>
<li>Reduced manual steps in data-collection workflows for speech teams</li>
</ul>"""),
            ("YouTube", "Java · C++ · Python · Privacy-aware microservices", """<p>Architecture and development for internal YouTube team tooling.</p>
<ul>
<li>Secure, privacy-aware applications and data pipelines to proprietary graphical query tools</li>
<li>BigQuery-backed reporting; microservice decomposition</li>
<li>Mentored team members on design and delivery practices</li>
</ul>"""),
            ("HR Finance (Payroll v2)", "Java · Guice · Protobuf · Microservices", """<p>Designed, developed, and tested the second-generation HR payroll processing application.</p>
<ul>
<li>Microservice architecture with heavy dependency injection (Guice) and Protobuf messaging</li>
<li>Highly secure design addressing privacy and access-control requirements</li>
<li>Patterns and internal tooling aligned with Google best practices</li>
</ul>"""),
        ],
    },
    "directv": {
        "title": "DirecTV Projects",
        "intro": """<p><strong>Contract consulting</strong> · 2007 – 2012</p>
<ul>
<li>redrat_scripter: red rat code for infrared transceiver, usb, perl client that reads scripts and sends commands to server that uses sockets</li>
<li>redrat_blaster: used in server farm to blast with random IR messages to discover software errors</li>
<li>USB Device Driver: Modified to minimize memory usage and avoid excess of object recreation</li>
<li>ScreenCapture Control: ActiveX control to capture screens using various devices, creates images</li>
<li>Image Processing Code: binarize images, crop selected window</li>
<li>ScreenReader: Perform OCR on selected window</li>
<li>ScreenScraper: Perform OCR on a whole screen</li>
<li>AbbyReader OCR Instrumentation System, used by Server</li>
<li>OCR Server: Uses Abby Reader System, receives an image as input, performs OCR on it and returns text to the client, over TCP/IP Network.</li>
<li>OCR Server Tester: Performs various tests on the server.</li>
<li>OCR Client: Takes video screen shots with ScreenCapture, does some image processing, including adapted FFT algorithm, binarizes image, sends image to server, receives text, client is instrumented via javascript, usually from Test Director Web App.</li>
<li>OCR Client Blaster: Performance tester for OCR System.</li>
</ul>""",
        "tech": "C/C++, JavaScript, Perl, ACE Framework, ActiveX, COM, Win32, USB Device Driver Development, OCR, Machine Vision, Image Processing, FFT, Fast (Discrete) Fourier Transform, Heuristics Methods for Machine Vision, Image Database Retrieval System using above and FFT, Image Binarization, Image Capture, Embedded, Web Based Test: Test Director",
        "work": """<h2>Work Performed</h2>
<p>Envisioned, promoted, architected, designed and developed software infrastructure for Automation system in C++, ActiveX, COM and Win32. The Client/Server system uses ACE Framework design and architecture patterns and drives video capture devices to acquire and process images, perform OCR and recognition of other artifacts using the Fast Fourier Transform algorithm and other methods in Machine Vision.</p>
<p>Invented algorithms using kernel methods and decision trees for analysis of image data and comparison for recognition. This was done in an incredible short time working independently, this took one month of research and implementation.</p>
<p>Envisioned, promoted, designed and developed Linux Socket C++ Server and Perl Client script processing Automation application for driving libusb based RedRat infrared Transceiver concurrent multiple devices. A RedRat is a device that can read and replicate remote control signals. ANSI C, C++, OOP, Patterns, Image Processing, JavaScript, Test Director, Visual Studio, DirectX, USB Devices.</p>
<p>Applications and ActiveX controls were used from Test Directors and instrumented using javascript.</p>""",
    },
    "jakeknows": {
        "title": "JakeKnows Projects",
        "intro": """<p><strong>Web App and Engine:</strong> System Service that provides data to the Web App, a Web Bot collects information about users on the web, from various sites and calculates how trustworthy the user identity is based on the data found. Android and iPhone apps were developed by another team, and these apps interfaced with the backend. The backend was always ready with the data to be served, via caching and other mechanisms, so that a web call would be orders of magnitude faster as opposed to the usual web apps that get the data as needed, for each call.</p>
<p><strong>Sony App:</strong> Provide Job Applicants with Access to Sony Jobs Database and Apply for Jobs. This application was developed very fast in a matter of 3 or 4 weeks to deployment, sold to Sony. The application used the code generators and the code base from the app above so code reuse was at a maximum.</p>""",
        "tech": "C#, C/C++, Python, SQL, MSSQL, IIS, SOAP, WSDL, WCF, Web Services, Code Generation",
        "work": """<h2>Work Performed</h2>
<p>Web Applications Development. Assimilated legacy server application in order to develop new architecture and design. Developed back end server for job application system for mobile devices for iPhone and Android.</p>
<p>Developed architecture, design and code for the new Identity Engine. The engine is a business core application intended to provide positive identification of an individual via digital activity harvested in diverse ways using patented technologies.</p>""",
    },
    "yahoo": {
        "title": "Yahoo Projects",
        "intro": """<p><strong>Contract consulting</strong></p>
<p>Yahoo-era web and infrastructure contract work — see portfolio archive for project materials.</p>""",
        "tech": "Web, Infrastructure, Contract Consulting",
    },
    "disney": {
        "title": "Disney Projects",
        "intro": """<p><strong>Senior Software Engineer</strong> · Jul 1997 – Nov 1998 · Walt Disney Studios (CDI contract) · Burbank, CA</p>
<ul>
<li>CorpPurch: Request purchases</li>
<li>DialIn_OutRequest: Request dial in/out access</li>
<li>HRTS: Request hardware</li>
<li>IPAging: IP Accounting</li>
<li>IPListing: IP Listings</li>
<li>ISTechDBAccess: Request database access</li>
<li>PeopleSoftLoginRequest: Request PeopleSoft access</li>
<li>SuggestionToTechServices: Send a suggestion to Tech Services Team</li>
<li>UpdateStudioDirectory: self explanatory</li>
<li>Commissary: Used by all Disney Studios Personnel to view commissary menu.</li>
<li>NWConnect: Netware connector ActiveX control.</li>
<li>GenericUpdater: Update software from a remote location using Netware NWConnect</li>
<li>GenericDeployer: Update software to a remote location using Netware NWConnect, VB application.</li>
<li>SendMail: Send email control to be used from Visual Basic applications, ActiveX</li>
</ul>""",
        "tech": "C/C++, Assembly, Visual Basic, Microsoft Access, Visual Studio, ASP, Active Server Pages, Windows Development, DLL Development, Databases: MS Access, MSSQL, Email Delivery through MAPI API, Win32, Mac OS, IIS, Internet Information Server, Microsoft SQL Server",
        "work": """<h2>Work Performed</h2>
<p>Designed and developed multithreaded network connector in C++ for Novell and Windows networks. Developed Macintosh version later.</p>
<p>Developed software updater in C++ that used the network connector. User base of 10,000 worldwide. Developed Macintosh version.</p>
<p>Designed and developed software deployment application in Visual Basic which helped other development teams.</p>
<p>Completed and improved food menu system for Marriott food management at the Disney Commissary. Used Visual Basic and MS Access. It printed on paper and output to a web page.</p>
<p>Converted CGI and Visual Basic applications to internet applications.</p>
<p>Developed Management Information System, Projects Management System and numerous database driven internet applications. Using IIS, ASP, MS SQL, Stored Procedures, MS Access, Java and VB Scripts and COM. Applications had to run in PC, Macintosh and UNIX platforms with MS Internet Explorer and Netscape in several versions. Designed graphics.</p>
<p>Conceived and developed Mail ActiveX control in Visual C++ used by internet applications and other programming teams.</p>
<p>Conceived and developed ActiveX control that extended Visual Basic by intercepting Windows messages and providing Events for custom processing of those messages.</p>
<p>Maintained and added features to other applications and tools. Collaborated in Y2K project, analyzed software and promoted necessary changes. Designed and Administered databases in MS SQL and MS Access.</p>""",
    },
    "electrosonic": {
        "title": "Electrosonic Projects",
        "intro": """<p><strong>Senior Programmer Analyst — Staff</strong> · Jan 2000 – Apr 2001 · Burbank, CA</p>
<ul>
<li>CommLib: DLL, rewrote winsock to handle double buffering for better performance</li>
<li>MonitorDLL: DLL to monitor computers, servers or other devices through CommLib Winsock TCP/IP</li>
<li>LiquidAudio streaming control: Designed as an ActiveX control, used to stream audio</li>
<li>ESCAN Application and related tools</li>
<li>ESCAN: 2nd version of the Scheduler — visually script and schedule devices locally or remote</li>
<li>SiteLinx: connect two ESCAN servers through email</li>
<li>PC_Monitor: Win32 app to monitor a PC</li>
<li>PC_Server: Win32 app to monitor a Video Server</li>
<li>DeviceSimulator: Create devices for testing or simulation</li>
<li>XML ActiveX control: import data from a database and export to xml files</li>
<li>Email ActiveX control: used to send/read email</li>
<li>Custom Applications: Voting System for the SHOA Foundation, Event generation devices for AMNH, etc.</li>
</ul>""",
        "tech": "C/C++, TCP/IP, Win32, WinDbg, WinSock, DDK, Device Driver Development, COM+, ActiveX, Windows Applications, DLL Development, Multi-Threading, XML, MAPI, TAPI, RAS, MPEG encoding/decoding, TV Closed Captioning, GUI UX/UI Heavy Development, Printing, Embedded, Robotics, Video/Audio Streaming, Databases, Scheduling, Event Driven Programming, Remote Control through Email",
        "work": """<h2>Work Performed</h2>
<p>Designed, coded, tested, profiled and documented applications and tools and proposed changes and additions. Responsible for full development cycle. Worked in team environments. Served as mentor to other programmers and technicians.</p>
<p>Conceived, designed and developed application for remote control and monitoring using C++, COM+, MAPI, TAPI, RAS.</p>
<p>Improved serial port and internet connectivity DLL which provided support for most applications. Developed second version, maximized capacity and transfer speed using C++, raw sockets, multi-threading, network events and double buffering.</p>
<p>Took ownership of application that controls and interacts with network and embedded devices. Developed protocols, device interfaces, ActiveX and ATL controls; extended application's and device's capabilities. Developed second version with many enhancements: MDI GUI, scripting capabilities, XML format, device triggers, email reporting plus many others.</p>
<p>Developed applications, tools and controls to support projects: Database, printing, MPEG encoding, hardware programming, device driver interface for video hardware to output graphics and text to TV screens, magnetic cards scanning, touch panels, Real Audio streaming control and device.</p>
<p>Adapted and implemented systems and applications for: American Museum of Natural History in New York, Museum of Tolerance in Beverly Hills, The Country Music Hall of Fame in Nashville, The Shoa Foundation in Universal Studios and others.</p>""",
    },
    "voltdelta": {
        "title": "Volt Delta Projects",
        "intro": """<p><strong>Telecommunications / Network Support</strong> · Nov 1998 – Oct 1999 · Orange, CA</p>
<ul>
<li>Phone Switch Simulator: C++ app that was used to test other applications instead of using a real phone switch which cost $1,000/hr at AT&amp;T</li>
<li>X.25 Relay: C++ app, used special hardware in a computer/server to interface with X.25 networks, it connected TCP/IP networks to them</li>
<li>StarStationManager: Manage X.25 work stations</li>
<li>StarTreeList: Visualize X.25 networks</li>
</ul>""",
        "tech": "C/C++, X.25 Networking, TCP/IP Networking, Windows Development, DLL Development, Win32, MSSQL, Visual Studio",
        "work": """<h2>Work Performed</h2>
<p>Designed and developed X.25 and TCP/IP network connector in C++ used by Telephone Switch Simulator.</p>
<p>Led team developing Telephone Switch Simulator in C++ saving time and money by allowing testing of programs in-house.</p>
<p>Developed other tools using web technologies, MS SQL, Stored Procedures and Visual Studio.</p>""",
    },
    "veritas": {
        "title": "Veritas Projects",
        "intro": """<p><strong>Senior Software Developer</strong> · 2016 – 2017 · Contractor</p>
<p>NetBackup appliance hardening — OSCAP, OAuth2/LDAP, Java/Python refactor.</p>""",
        "tech": "Java, Python, C/C++, Perl, Bash, OSCAP, OWASP, OAuth2, LDAP, Active Directory, SELinux, REST, Microservices, CLI, Security, Backup",
        "work": """<h2>Work Performed</h2>
<ul>
<li>Developed solutions to enhance and harden NetBackup appliance. Secured compliance with OSCAP security recommendations.</li>
<li>Refactored Java and Python code for the new in-the-works architecture. Used Java, C/C++, Python, Perl, Bash, RESTful web services, microservices, and CLI.</li>
<li>Networking, LDAP, NIS/Kerberos, malware detection and elimination.</li>
<li>Used OWASP and OSCAP tools with XML lists of items for security compliance. OAuth2 authentication and authorization using SELinux, LDAP, and Active Directory.</li>
</ul>""",
    },
    "hpe": {
        "title": "HPE Projects",
        "intro": """<p><strong>Senior Software Developer</strong> · 2017 – 2018 · Contractor</p>
<p>Airwave wireless appliance hardening and Perl→Python port.</p>""",
        "tech": "Java, Python, Perl, Bash, RegEx, Flask, Celery, JavaScript, OSCAP, OWASP, REST, Microservices, CLI, LDAP, Docker, VMware, Cloud, Wireless, Security",
        "work": """<h2>Work Performed</h2>
<ul>
<li>Analysis and development of solutions to harden Airwave appliance for wireless management.</li>
<li>Developed solutions to enhance and harden wireless systems.</li>
<li>Secured compliance with OSCAP security recommendations. Ported Perl to Python code for the new in-the-works architecture.</li>
<li>Used Java, Python, RegEx, Flask, Celery, Perl, and Bash.</li>
<li>RESTful web services and microservices, JavaScript, and CLI. Networking, LDAP, NIS/Kerberos, malware detection and elimination. Docker, VMware, and cloud virtualization technologies. Used OWASP and OSCAP tools with XML lists of items for security compliance.</li>
</ul>""",
    },
    "meta": {
        "title": "Meta Projects",
        "intro": """<p><strong>Privacy Audit Engineer</strong> · Oct 2020 – Mar 2021 · Contractor (DISYS)</p>
<p>Privacy audit engineering for M&amp;A — compliance tooling across SQL/NoSQL estates.</p>""",
        "tech": "C/C++, Java, Perl, Python, SQL, NoSQL, Cassandra, MongoDB, AWS, Privacy, Security, Compliance, Virtual Reality, Graphics, Device Drivers, Camera Imaging, Windows, Linux",
        "work": """<h2>Work Performed</h2>
<ul>
<li>Auditing of systems for companies in the process of being acquired.</li>
<li>Reviewing systems and data to assess risks and ensure compliance with diverse government bodies and regulations, including international.</li>
<li>Analyzed databases and other information systems to ensure privacy and security compliance with US and international laws, working in conjunction with attorneys.</li>
<li>Created tools to aid the teams with analysis and keeping track of work, originally using spreadsheets.</li>
<li>Devised methods to abstract the analysis of architectures and designs, helping to better keep track of progress in a more standardized way.</li>
<li>C/C++, Java, Perl, Python, NoSQL, SQL, Cassandra, MongoDB, virtual reality, graphics and device drivers, camera imaging. AWS and other cloud systems, Windows and Linux.</li>
</ul>""",
    },
    "vmware": {
        "title": "VMware Projects",
        "intro": """<p><strong>Sr. Member of Technical Staff (MTS)</strong> · 2015 – 2016 · Palo Alto · Contractor</p>
<p>VMware — virtualization and cloud infrastructure. QA automation for ESX, HBR, and related appliances.</p>
<ul>
<li><strong>Gemini framework:</strong> replaced ~80k LOC Perl legacy with ~8k LOC Python — ~8× faster execution</li>
<li><strong>Paradigms:</strong> object-oriented, functional, and meta-programming patterns in a cohesive test harness</li>
</ul>""",
        "tech": "Python, Perl, Virtualization, ESX, HBR, SSH, Automation, QA, Framework Development, Test Instrumentation, Networking",
        "sections": [
            ("Gemini Automation Framework", "Python · QA · ~80k → ~8k LOC", """<p>Architected, designed, and implemented a new testing framework for the QA department — instrumenting virtual and physical servers, workstations, and appliances (ESX, HBR, and related targets).</p>
<ul>
<li>Replaced a ~80k LOC Perl-centric legacy framework with ~8k LOC Python — approximately <strong>8× faster</strong> test runs</li>
<li>Unified instrumentation across heterogeneous VMware product lines</li>
<li>OOP structure with functional helpers and meta-programming for extensible test definitions</li>
<li>Field engineers and QA could script complex scenarios without touching low-level Perl internals</li>
</ul>"""),
            ("SSH Connector &amp; Log Framework", "Secure remote execution · HTML / terminal logging", """<p>Supporting libraries used throughout Gemini.</p>
<ul>
<li><strong>SSH Connector:</strong> secure command dispatch to ESX hosts, appliances, and lab devices</li>
<li><strong>Log Framework:</strong> structured output to terminal or HTML reports for regression analysis</li>
<li>Composable building blocks — connectors and logging shared across test suites</li>
</ul>"""),
        ],
    },
    "hms": {
        "title": "Hypermedia Projects",
        "intro": """<p><strong>Application Security Specialist — Staff</strong> · Mar – Nov 2005 · Los Angeles, CA</p>
<ul>
<li>Input Validation Library: used by in-house web applications to provide security, prevent sql injection and other exploits</li>
<li>Tools: For penetration testing, web site accounting and monitoring</li>
</ul>""",
        "tech": "C/C++, Java, Python, Perl, Web Applications, Security, Library Development, Linux, Security, Privacy, ECommerce, Code Analysis, Code Security Reviews",
        "work": """<h2>Work Performed</h2>
<p>Developed in-house web applications making use of best user interface methodologies.</p>
<p>Analyzed applications to find security vulnerabilities, documented findings, proposed changes. Mostly in Linux. Malware detection and fixes.</p>
<p>Participated in the development process contributing security related advice and trained development groups on best practices.</p>
<p>Developed tools and scripts including an input validation library which uses regular expressions and is assembly optimized for speed, including several automatic features freeing developers from most of the responsibility of input validation.</p>
<p>Developed interfaces to this library for Java, C and Perl in a Linux environment.</p>""",
    },
    "guidance": {
        "title": "Guidance Software Projects",
        "intro": """<p><strong>Senior Software Engineer</strong> · Nov 2005 – Dec 2006 · Consultancy</p>
<p>Digital forensics — Symantec Ghost format reverse engineering, Win32 disk imaging.</p>""",
        "tech": "C++, Forensics, IDA Pro, Win32, Reverse Engineering, Image Processing, Visual Studio, WinDbg, DDK, SoftICE",
        "work": """<h2>Work Performed</h2>
<ul>
<li>Developed digital forensics tool using Win32. Utilized methods of data extraction for cellular phones and other devices.</li>
<li>Reverse engineered a commercial application for imaging hard drives to provide support for its file structure. Deciphered obfuscation techniques in the structures through the use of IDA Pro and hex viewers.</li>
<li>Developed the code to support the new file format using C++, all in approximately 2 months.</li>
</ul>""",
    },
    "surfware": {
        "title": "Surfware Projects",
        "intro": """<p><strong>Contract consulting</strong> · 2006 – 2012</p>
<ul>
<li>Surfcam: Added features and enhancements</li>
<li>SolidWorks/Autocad Import/Export App: windows app to export/import data from surfcam files to/from</li>
</ul>""",
        "tech": "C/C++, C#, CAD/CAM, CNC, milling machine codes, generated by surfcam from 3d models, Databases, Win32, COM, VBA, DirectX, OpenGL, Autocad, Solidworks, 3D",
        "work": """<h2>Work Performed</h2>
<p>Developed, designed and re-factored code for CAD/CAM systems in C++, C#, in a windows environment.</p>
<p>Implemented features for the 4 and 5 axis subsystem. Envisioned and Architected tools to improve the development process.</p>
<p>Updated and redesigned code and database business applications in MS SQL, VBA and MS Access.</p>
<p>Designed and coded Perl scripts to process text and expedite the development process. Developed plugins for applications such as Solid Works in C++, ActiveX and Parasolid CAD/CAM Kernel, used OpenGL and DirectX. Debugged and fixed application.</p>""",
    },
    "motorola": {
        "title": "Motorola Projects",
        "intro": """<p><strong>Contract consulting</strong> · 2009 – 2011</p>
<p><strong>Closed Captioning Embedded Module</strong></p>
<p>C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes</p>""",
        "tech": "C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes",
        "work": """<h2>Work Performed</h2>
<p>Developed, designed and coded software in a distributed team, agile environment for Linux and embedded systems. The system is embedded in a Set Top Box, it provides Closed Captioning capabilities. Redesign was done to provide exceptional performance eliminating memory allocation completely after initialization.</p>""",
    },
    "opentv": {
        "title": "OpenTV Projects",
        "intro": """<p><strong>Software Expert — Staff</strong> · Mar 2013 – Mar 2014 · Mountain View, CA</p>
<p><strong>Dynamic Scheduler:</strong> Resolved Issues and Enhanced Win32 C# App, used for Local Advertisement Scheduling</p>""",
        "tech": "C#, C/C++, Python, Perl, Oracle, Big Data Import, Win32, Scheduling, Web Services, SOAP, SQL, Stored Procedures, IIS, MVC, .NET, XML",
        "work": """<h2>Work Performed</h2>
<p>Developed software enhancements and bug fixes for application used by major cable companies worldwide. The application was very complex containing over a million lines of code.</p>""",
    },
    "spirent": {
        "title": "Spirent Projects",
        "intro": """<p><strong>Senior Software Engineer</strong> · Nov 2005 – Dec 2006 · Consultancy</p>
<ul>
<li>Tlc Interface: replaced old Tcl code base and converted it to C++, resulting in only one line of tcl code from several thousands.</li>
<li>Mainline: Helped to create second version of embedded application that drives a network testing appliance and can be scripted and instrumented using tcl.</li>
</ul>""",
        "tech": "C/C++, Tcl, Network Testing, Automation, Script Instrumentation, Linux Embedded, ACE Framework, SWIG",
        "work": """<h2>Work Performed</h2>
<p>Developed new user interface for next generation system using SWIG for creation of tcl accessibility layer.</p>
<p>Developed new commands for the network testing system.</p>
<p>Re-factored code to later reuse for the new design. Network Programming, ACE Framework, OOD, Visual Studio.</p>""",
    },
    "posdev": {
        "title": "Positive Developments",
        "intro": """<p><strong>Network and Programming Support</strong> · Oct 1999 – Jan 2000 · Anaheim, CA</p>
<p>Positive Developments — network support and warehouse-industry programming for PalmOS and handheld devices.</p>
<ul>
<li><strong>SendGTL:</strong> Win32 MFC utility that loads firmware and data files to warehouse handhelds over serial — parameterized via <code>SendGTL.txt</code> with manufacturer/model lists, comm settings, and custom bitmap dialogs</li>
<li><strong>Allstate Floral (PalmOS):</strong> order and item scanning on Palm/Symbol hardware — barcode scan screens, PDI file import, order index navigation (source tree: <code>Allstate Floral V2</code>)</li>
<li>Help desk and phone support for in-house staff and warehouse clients</li>
</ul>""",
        "tech": "C++, MFC, Win32, PalmOS, C, Serial Communications, Warehouse, Barcode Scanning, Help Desk, Networking",
        "work": """<h2>Work Performed</h2>
<p>Programmed warehouse applications for PalmOS and other handheld devices; maintained and extended the Allstate Floral order-entry scanner (v2.07 bug fixes and UI adjustments).</p>
<p>Built <strong>SendGTL</strong> — a configurable loader that reads pipe-delimited parameter rows, validates file paths, and drives serial transfer dialogs with registry persistence (<code>Positive Developments</code> registry key).</p>
<p>Provided network support and help desk coverage for employees and warehouse clients by phone.</p>""",
    },
    "telvista": {
        "title": "TelVista Projects",
        "intro": """<p><strong>Programmer Analyst — Consultant</strong> · Apr 2001 – Nov 2001 · ~8 month contract</p>
<p>TelVista — MIS databases, order entry, and telecom workflow for TELMEX and Mexicana Airlines.</p>
<ul>
<li><strong>MIS database:</strong> MS Access and Visual Basic with high-volume data entry forms, validation, and time-saving workflows</li>
<li><strong>Order entry database:</strong> customer and order tracking for telecommunications services</li>
<li><strong>TELMEX Account Processing:</strong> account workflow prototype (<code>Project 000 - Test</code>)</li>
<li><strong>Mexicana appointment scheduling:</strong> appointment database with feasibility analysis notes on routing and daily capacity (<code>Project 001 - Mexicana</code>)</li>
<li><strong>WorkFlowApp:</strong> reusable .NET workflow engine with full SDLC documentation in archive</li>
</ul>""",
        "tech": "MS Access, Visual Basic, .NET, C#, MIS, Order Entry, Telecommunications, Workflow, Database Design",
        "work": """<h2>Work Performed</h2>
<p>Designed and coded MIS and order-entry databases in MS Access and Visual Basic — forms optimized for large-volume entry with validation rules.</p>
<p>Documented requirements and QA processes for TELMEX and Mexicana airline scheduling projects.</p>
<p>Built workflow automation prototypes and reusable engine components for telecom business processes.</p>""",
    },
    "woodtech": {
        "title": "Wood Technologies International",
        "intro": """<p><strong>Senior Software Engineer</strong> · Nov 1996 – Mar 1997 · Long Beach, CA</p>
<ul>
<li>Network support and help desk for in-house employees and phone clients</li>
<li>Installation of NT, Windows 95, Exchange, BBS, and related software</li>
<li>Netscape Internet Server setup and maintenance</li>
<li>MIS database applications for executives</li>
<li>Programming support for SQL data-loading procedures</li>
<li>BBS upload utilities — file processing, archival, and database import</li>
</ul>""",
        "tech": "Windows NT, Exchange, Netscape Server, BBS, MS Access, SQL Server, Novell, Help Desk, MIS",
        "work": """<h2>Work Performed</h2>
<p>Network support and help desk for in-house employees and remote clients.</p>
<p>Installed and maintained NT, Windows 95, Exchange, and BBS systems; configured Netscape Internet Server.</p>
<p>Developed MIS database applications for executives and utilities to process files uploaded through the BBS into SQL databases.</p>""",
    },
    "access": {
        "title": "ACCESS! Corporation",
        "intro": """<p><strong>Programmer and Support Associate</strong> · Mar 1995 – Sep 1996 · Playa Del Rey, CA</p>
<p>ACCESS! — predictive dialer systems for collection and telemarketing agencies (PC/Dialogic).</p>
<ul>
<li>On-site installation and hardware/software support for administrators and clients nationwide</li>
<li>Trained system administrators at customer sites</li>
<li>Analyzed client databases to recommend integration paths with ACCESS! systems</li>
<li><strong>Data manager</strong> and utilities in Clipper/xBase</li>
<li>Mainframe data-sharing methods — communication scripts for file transfers across heterogeneous systems</li>
</ul>""",
        "tech": "Clipper, Dialogic, Predictive Dialer, PC/Dialogic, Databases, Mainframe Integration, Telemarketing, Tech Support",
        "work": """<h2>Work Performed</h2>
<p>Installed predictive dialer (PC/Dialogic) systems for collection and telemarketing agencies; heavy travel across multiple states.</p>
<p>Developed data manager software and Clipper utilities; coordinated data sharing between mainframes and ACCESS! systems.</p>
<p>Wrote communication scripts for file transfers between several types of mainframes and other computer systems.</p>
<p>Built strong customer relationships through on-site training and integration analysis.</p>""",
    },
    "bumpershop": {
        "title": "The Bumper Shop",
        "intro": """<p><strong>Computer Support Associate</strong> · Aug 1994 – Mar 1995 · Los Angeles, CA</p>
<p>The Bumper Shop — automotive body shop with Los Angeles and San Francisco branches.</p>
<ul>
<li>LAN/WAN network design, installation, and configuration</li>
<li>MS Access MIS: customers, billing, invoicing, inventory, statements, and custom reports</li>
<li>San Francisco branch network rollout</li>
</ul>
<p>Source archive: <code>BumperShop</code> (Access databases) and related accounting MDBs.</p>""",
        "tech": "MS Access, LAN/WAN, MIS, Billing, Inventory, Network Installation, Windows",
        "work": """<h2>Work Performed</h2>
<p>Installed and configured LAN/WAN network systems for the main location and San Francisco branch.</p>
<p>Designed and coded an MS Access database tracking customers, billing, invoicing, inventory, reports, statements, and management information.</p>""",
    },
    "plastering": {
        "title": "California Plastering",
        "intro": """<p><strong>Office Manager</strong> · Feb 1994 – Aug 1994 · Inglewood, CA</p>
<ul>
<li>Database system for customers, invoicing, payroll, billing, and general accounting</li>
<li>Bookkeeping and office management duties</li>
</ul>""",
        "tech": "MS Access, Accounting, Payroll, Invoicing, Bookkeeping, MIS",
        "work": """<h2>Work Performed</h2>
<p>Developed a database system to track customers, invoicing, payroll, billing, and general accounting for a plastering contractor.</p>
<p>Performed accounting and bookkeeping duties; helped customers with diverse business issues.</p>""",
    },
    "frys": {
        "title": "Fry's Electronics",
        "intro": """<p><strong>Software Sales Associate / PC Technician</strong> · Jan 1993 – Feb 1994 · Manhattan Beach, CA</p>
<ul>
<li>Demonstrated computer software and guided retail customers to appropriate products</li>
<li>Resolved hardware and software conflicts on demo and customer systems</li>
<li>Secured and maintained demo systems on the sales floor</li>
<li>Technical support for walk-in customers and phone inquiries</li>
</ul>""",
        "tech": "PC Diagnostics, Retail Software, Hardware Troubleshooting, Customer Support, Windows, DOS",
        "work": """<h2>Work Performed</h2>
<p>Combined software sales with hands-on PC technician work on the Fry's sales floor.</p>
<p>Diagnosed hardware and software conflicts; maintained demo machines for product showcases.</p>""",
    },
    "lcs": {
        "title": "Logical Computer Services",
        "intro": """<p><strong>Network and Debugging Support Associate</strong> · Sep 1992 – Jan 1993 · Burbank, CA</p>
<ul>
<li>Data processing duties for financial and MIS systems</li>
<li>Hardware installation and troubleshooting</li>
<li>Novell NetWare 3.11 and Windows for Workgroups network installs</li>
<li>Debugged Visual Basic and MS Access code for MIS and financial software on LAN/WAN</li>
</ul>""",
        "tech": "Novell NetWare, Windows for Workgroups, Visual Basic, MS Access, LAN/WAN, Data Processing",
        "work": """<h2>Work Performed</h2>
<p>Executed data processing duties; installed and troubleshot hardware.</p>
<p>Installed networks using Novell NetWare 3.11 and Windows for Workgroups.</p>
<p>Debugged Visual Basic and MS Access MIS and financial applications operating across LAN/WAN environments.</p>""",
    },
}


def project_body(slug: str) -> str:
    p = PROJECTS[slug]
    parts = [
        '    <a href="../index.html" class="back-link">&larr; Back to Portfolio</a>',
        f'    <h1 class="page-title">{p["title"]}</h1>',
        '    <div class="content-section">',
        p["intro"],
        f'      <div class="tech-tags"><strong>Technologies</strong>{tech_to_chips(p["tech"])}</div>',
    ]
    if "sections" in p:
        for h2, h3, content in p["sections"]:
            parts.append(f'      <h2>{h2}</h2>')
            parts.append(f'      <h3>{h3}</h3>')
            parts.append(content)
    if "work" in p:
        parts.append(p["work"])
    nnn = nnn_archive_block(slug)
    if nnn:
        parts.append(nnn)
    comp = compilation_block(slug)
    if comp:
        parts.append(comp)
    parts.append("    </div>")
    return "\n".join(parts)


def main():
    import_comp = ROOT / "tools" / "import_compilation.py"
    if import_comp.is_file():
        subprocess.run([sys.executable, str(import_comp)], check=False)

    extract = ROOT / "tools" / "extract_development.py"
    if extract.is_file() and DEV_ROOT.is_dir():
        subprocess.run([sys.executable, str(extract)], check=False)

    nnn_build = ROOT / "tools" / "build_nnn_archive.py"
    if nnn_build.is_file():
        subprocess.run([sys.executable, str(nnn_build)], check=False)

    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    copy_maf_project_images()
    if RESUME_SRC.is_file():
        shutil.copy2(RESUME_SRC, assets / "Kevin-Guerra.pdf")
    elif not (assets / "Kevin-Guerra.pdf").is_file():
        print(f"warn: resume not found at {RESUME_SRC}")

    build_carousel_logos()
    catalog_by_slug = {c["slug"]: c for c in load_catalog().get("portfolio", [])}

    def portfolio_card(entry: tuple) -> str:
        name, img, ext, slug, desc, skills = entry
        c = catalog_by_slug.get(slug, {})
        badge = ""
        if slug == "mafroda":
            badge = '<span class="current-badge">Current</span>'
        badge_line = f"          {badge}\n" if badge else ""
        current_cls = " portfolio-item--current" if slug == "mafroda" else ""
        return f"""      <article class="portfolio-item fade-in{current_cls}">
        <a href="projects/{slug}.html">
{badge_line}          <div class="logo-wrap"><img src="assets/images/{img}.{ext}" alt="{html.escape(name)}"></div>
          <span class="company-name">{html.escape(name)}</span>
          <span class="company-desc">{html.escape(desc)}</span>
          {skill_chips(skills, 5)}
        </a>
      </article>"""

    entries = portfolio_entries()
    cards = "\n".join(portfolio_card(e) for e in entries)
    (ROOT / "index.html").write_text(
        page(
            "Portfolio",
            "Portfolio",
            f"""    <section class="hero fade-in">
      <p class="hero-eyebrow">{PROFESSIONAL_TITLE}</p>
      <h1>{OWNER}</h1>
      <p class="hero-lead">Currently <strong>Sr. Software Engineer at MAF RODA Agrobotic</strong> (Americas traceability). Cloud, enterprise and solutions architecture, design and full development life cycle. AI &amp; ML. Virtualization, machine vision, reverse engineering, privacy &amp; security, digital forensics. Embedded systems, kernel, device and low-level programming. Databases and schema design.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{RESUME_ASSET}">Download Resume</a>
        <a class="btn btn-secondary" href="mailto:{CONTACT_EMAIL}">Get in Touch</a>
        <div class="hero-actions-samples">
          <a class="btn btn-secondary" href="samples.html">View Samples</a>
          <div class="hero-social" aria-label="Social profiles">
{social_icon_links()}
          </div>
        </div>
      </div>
    </section>
{highlights_strip()}
    <h2 class="page-title">Experience</h2>
    <div class="portfolio-grid">
{cards}
    </div>""",
            description=f"{PROFESSIONAL_TITLE} — portfolio spanning Google, Leidos, VMware, Disney, DirecTV, and current work at MAF RODA.",
        )
    )

    services = "\n".join(
        f"""      <article class="service-card fade-in">
        <div class="service-card-img">
          <img src="assets/images/services/{html.escape(img)}" alt="{html.escape(title)}" loading="lazy">
        </div>
        <h2>{html.escape(title)}</h2>
        <p>{html.escape(blurb)}</p>
      </article>"""
        for title, blurb, img in SERVICES
    )
    (ROOT / "services.html").write_text(
        page(
            "Services",
            "Services",
            f"""    <h1 class="page-title">Services</h1>
    <p class="page-intro text-center">What I bring to your team — from architecture through delivery.</p>
    <div class="services-grid">
{services}
    </div>
    <section class="contact-panel fade-in" style="margin-top:2rem">
      <h2>Start a project</h2>
      <p>Email me at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> or connect on <a href="{SOCIAL["linkedin"]}">LinkedIn</a>.</p>
      <div class="contact-actions">
        <a class="btn btn-primary" href="mailto:{CONTACT_EMAIL}">Email Kevin</a>
        <a class="btn btn-secondary" href="{RESUME_ASSET}">Download Resume</a>
      </div>
    </section>
    <img class="services-hero fade-in" src="assets/images/services/hero-banner.jpg" alt="" loading="lazy">""",
            slug_path="services.html",
            description="Consulting and development: web, cloud, security, embedded systems, and performance optimization.",
        )
    )

    samples_html = "\n".join(
        sample_entry(title, desc, gh, snippet, demo, image)
        for title, desc, gh, snippet, demo, image in SAMPLES
    )
    (ROOT / "samples.html").write_text(
        page(
            "Samples",
            "Samples",
            f"""    <img class="samples-hero fade-in" src="assets/images/samples/hero.jpeg" alt="" loading="lazy">
    <h1 class="page-title">Projects Samples</h1>
    <div class="samples-list">
{samples_html}
    </div>""",
            slug_path="samples.html",
            description="Open-source sample projects on GitHub — C++, Java, Angular, TypeScript, and Python demos.",
        )
    )

    (ROOT / "about.html").write_text(
        page(
            "About",
            "About",
            f"""    <div class="about-layout">
      <img class="about-hero-img fade-in" src="assets/images/hero.jpg" alt="{OWNER}">
      <div class="about-bio fade-in">
        <h1>About</h1>
        <p>Hello, my name is Kevin. I'm a {PROFESSIONAL_TITLE.lower()} — my career started as a hobby and I'm still passionate about building fast, reliable systems across cloud, web, embedded, robotics, networking, databases, security, and virtualization.</p>
        <p>I focus on quality code that stays maintainable: fewer lines, code generation where it helps, and patterns that scale. See my <a href="{RESUME_ASSET}">resume (PDF)</a> for the full technology list and employment history.</p>
        <h2>Core skills</h2>
        <p class="page-intro" style="margin-top:-0.5rem;margin-bottom:0.75rem">Synced from <a href="{SOCIAL["linkedin"]}">LinkedIn</a> profile skills.</p>
        <div class="skills-cloud">{"".join(f'<span class="skill-chip">{html.escape(s)}</span>' for s in load_core_skills())}</div>
        <h2>Career timeline</h2>
        <div class="timeline">
{timeline_block()}
        </div>
        <h2>Personal</h2>
        <ul>
          <li>Sports oriented — weight training, tennis, ping-pong; 1500+ push-ups in high school.</li>
          <li>Autodidact; continuous study across computer science and related fields.</li>
          <li>Rubik's cube: ~11.2s average in middle school (best 9.4s). <a href="https://www.recordholders.org/en/list/rubik.html" target="_blank" rel="noopener">World records</a></li>
        </ul>
        <section class="contact-panel">
          <h2>Contact</h2>
          <p>Open to consulting and senior development roles.</p>
          <div class="contact-actions">
            <a class="btn btn-primary" href="mailto:{CONTACT_EMAIL}">Email {CONTACT_EMAIL}</a>
            <button type="button" class="btn btn-secondary" data-copy-email="{CONTACT_EMAIL}">Copy email</button>
            <a class="btn btn-secondary" href="{SOCIAL["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a>
            <a class="btn btn-secondary" href="{SOCIAL["github"]}" target="_blank" rel="noopener">GitHub</a>
            <a class="btn btn-secondary" href="{SOCIAL["stackoverflow"]}" target="_blank" rel="noopener">Stack Overflow</a>
            <a class="btn btn-secondary" href="{RESUME_ASSET}">Resume PDF</a>
            <a class="btn btn-secondary" href="index.html">Portfolio</a>
          </div>
        </section>
      </div>
    </div>""",
            slug_path="about.html",
            description=f"About {OWNER} — {PROFESSIONAL_TITLE.lower()}, autodidact, and portfolio author.",
            og_image="assets/images/hero.jpg",
        )
    )

    ensure_all_projects()

    PROJECTS_DIR.mkdir(exist_ok=True)
    catalog_slugs = [c["slug"] for c in load_catalog().get("portfolio", [])]
    for slug in catalog_slugs:
        if slug in SKIP_INDEX_SLUGS:
            stale_page = PROJECTS_DIR / f"{slug}.html"
            if stale_page.exists():
                stale_page.unlink()
            continue
        if slug not in PROJECTS:
            card = catalog_by_slug.get(slug, {"slug": slug, "name": slug, "desc": "", "skills": []})
            PROJECTS[slug] = auto_project(slug, card)
        proj = PROJECTS[slug]
        (PROJECTS_DIR / f"{slug}.html").write_text(
            page(
                proj["title"],
                "Portfolio",
                project_body(slug),
                depth=1,
                slug_path=f"projects/{slug}.html",
                description=f"{proj['title']} — {OWNER}.",
            )
        )

    stale = PROJECTS_DIR / "hypermedia.html"
    if stale.exists():
        stale.unlink()

    redirect = PROJECTS_DIR / "audiotelco.html"
    redirect.write_text(
        page(
            "TelVista Projects",
            "Portfolio",
            '    <meta http-equiv="refresh" content="0; url=telvista.html">\n'
            '    <p>Moved to <a href="telvista.html">TelVista Projects</a>.</p>',
            depth=1,
            slug_path="projects/audiotelco.html",
            description="Redirect to TelVista project page.",
        ),
        encoding="utf-8",
    )

    sync_static_page_carousels()

    print(f"Generated {len(catalog_slugs) + 4} HTML pages ({len(catalog_slugs)} projects) in {ROOT}")


if __name__ == "__main__":
    main()
