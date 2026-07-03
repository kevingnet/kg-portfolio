#!/usr/bin/env python3
"""Index ALL Development archive folders → portfolio-catalog.json + development-inventory.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

DEV_ROOT = Path("/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development")
OUT_DIR = Path(__file__).resolve().parents[1] / "data"
INVENTORY = OUT_DIR / "development-inventory.json"
CATALOG = OUT_DIR / "portfolio-catalog.json"

PROJECT_EXTS = {".sln", ".dsp", ".dsw", ".vcxproj", ".vbproj"}
SKIP_DIRS = {".git", ".svn", "node_modules", "__pycache__", "bin", "obj", "Debug", "Release", "res", ".aws"}

# slug → extra Development paths (beyond primary folder)
EXTRA_PATHS: dict[str, list[str]] = {
    "jakeknows": ["work"],
}

# Resume correlation (NOT added to resume — portfolio tagging only)
IN_OLD_RESUME = {
    "access", "disney", "electrosonic", "voltdelta", "posdev",
    "audiotelco", "woodtech", "frys", "lcs",
}

EXCLUDED_SLUGS = frozenset({
    "pleiades", "nokio", "enigma", "plastering",
    "bumpershop", "labumpers", "fotografia", "puntabanda",
})
IN_CURRENT_RESUME = {
    "mafroda", "leidos", "google", "directv", "vmware", "jakeknows", "disney",
    "electrosonic", "voltdelta", "hms", "surfware", "motorola", "opentv", "spirent",
}

# Every numbered / named folder under Development
FOLDER_META: dict[str, dict] = {
    "01 Access!": {
        "slug": "access", "name": "ACCESS!", "logo": "access", "ext": "svg",
        "desc": "Predictive dialer installs, Clipper data manager, mainframe file-transfer integration.",
        "skills": ["Clipper", "Dialogic", "Databases", "Telemarketing", "Mainframe"],
    },
    "02 BumperShop": {
        "slug": "bumpershop", "name": "The Bumper Shop", "logo": "bumpershop", "ext": "svg",
        "desc": "MS Access MIS — billing, inventory, accounting databases and LAN/WAN rollout.",
        "skills": ["MS Access", "LAN/WAN", "MIS", "Inventory", "Accounting"],
    },
    "03 Disney": {
        "slug": "disney", "name": "Disney", "logo": "disney", "ext": "jpeg",
        "desc": "NWConnect deployer, SendMail ActiveX, IIS/ASP enterprise web apps, Commissary menu system.",
        "skills": ["C++", "ASP", "VB", "MSSQL", "ActiveX"],
    },
    "04 Electrosonic": {
        "slug": "electrosonic", "name": "Electrosonic", "logo": "electrosonic", "ext": "jpeg",
        "desc": "ESCAN scheduler, museum client apps (AMNH, CMHF), remote AV device control.",
        "skills": ["C++", "COM", "TCP/IP", "Embedded", "MPEG"],
    },
    "05 Volt": {
        "slug": "voltdelta", "name": "VoltDelta", "logo": "voltdelta", "ext": "jpeg",
        "desc": "X.25/TCP/IP relay, StarTreeList DB, phone switch simulator.",
        "skills": ["C++", "X.25", "TCP/IP", "Win32", "MSSQL"],
    },
    "06 LaBumpers": {
        "slug": "labumpers", "name": "La Bumpers", "logo": "labumpers", "ext": "jpg",
        "desc": "E-commerce bumper catalog, EC2/AWS deployment, vehicle-fit databases and web storefront.",
        "skills": ["Java", "AWS", "EC2", "Drupal", "E-commerce"],
        "portfolio_only": True,
    },
    "07 PosDev": {
        "slug": "posdev", "name": "Positive Developments", "logo": "posdev", "ext": "svg",
        "desc": "SendGTL Win32 loader, Allstate Floral PalmOS warehouse scanner.",
        "skills": ["C++", "PalmOS", "MFC", "Warehouse", "Serial I/O"],
    },
    "08 FotografiaBlancarte": {
        "slug": "fotografia", "name": "Fotografia Blancarte", "logo": "fotografia", "ext": "jpg",
        "desc": "Photography studio MIS database and branding assets.",
        "skills": ["MS Access", "MIS", "Branding"],
        "portfolio_only": True,
    },
    "09 Pleiades": {
        "slug": "pleiades", "name": "Pleiades", "logo": "pleiades", "ext": "svg",
        "desc": "Blind Factory production MIS — persiana/window-cover manufacturing databases.",
        "skills": ["MS Access", "MIS", "Manufacturing"],
        "portfolio_only": True,
    },
    "10 TelVista": {
        "slug": "audiotelco", "name": "Audio Telco", "logo": "audiotelco", "ext": "jpeg",
        "desc": "TelVista MIS, TELMEX/Mexicana scheduling, WorkFlowApp .NET solution.",
        "skills": ["MS Access", "Visual Basic", ".NET", "Telecom"],
    },
    "11 Enigma": {
        "slug": "enigma", "name": "Enigma Video", "logo": "enigma", "ext": "svg",
        "desc": "Premiere/3ds Max video production projects — logos, aurora exports, motion composites.",
        "skills": ["Video", "Premiere", "3ds Max", "Motion Graphics"],
        "portfolio_only": True,
    },
    "12 Nokio": {
        "slug": "nokio", "name": "Nokio Insurance", "logo": "nokio", "ext": "svg",
        "desc": "Multi-line insurance quote web forms — home, auto, business HTML workflows.",
        "skills": ["HTML", "Web Forms", "Insurance", "JavaScript"],
        "portfolio_only": True,
    },
    "13 PuntaBandaData": {
        "slug": "puntabanda", "name": "Punta Banda Data", "logo": "puntabanda", "ext": "svg",
        "desc": "SPA PuntaBanda POS, barcode label printers, SQL Server stored procedures.",
        "skills": ["C#", "ASP.NET", "SQL Server", "POS", "Barcode"],
        "portfolio_only": True,
    },
    "15 HMS": {
        "slug": "hms", "name": "HMS", "logo": "hypermedia", "ext": "jpeg",
        "desc": "Assembly-optimized input validation library, auth/netidb, penetration testing tools.",
        "skills": ["C++", "Python", "Security", "Linux", "Perl"],
    },
    "16 Spirent": {
        "slug": "spirent", "name": "Spirent", "logo": "spirent", "ext": "jpeg",
        "desc": "TestCenter Tcl/SWIG UI, mainline network-test appliance automation.",
        "skills": ["C++", "Tcl", "SWIG", "Networking", ".NET"],
    },
    "18 DirecTV": {
        "slug": "directv", "name": "DirecTV", "logo": "directv", "ext": "jpeg",
        "desc": "OCR client/server, RedRat IR automation, STB test scripts, screen capture pipeline.",
        "skills": ["C++", "OCR", "ACE", "Computer Vision", "Perl"],
    },
    "19 Surfware": {
        "slug": "surfware", "name": "Surfware", "logo": "surfware", "ext": "jpeg",
        "desc": "Surfcam Velocity4/5, INC2APT, SolidWorks translators, InstallManager.",
        "skills": ["C++", "C#", "OpenGL", "CAD/CAM", "Parasolid"],
    },
    "22 Motorola": {
        "slug": "motorola", "name": "Motorola", "logo": "motorola", "ext": "jpeg",
        "desc": "OCAP closed-captioning renderer for set-top boxes — zero post-init allocation.",
        "skills": ["C++", "Embedded", "OCAP", "Linux", "DTV"],
    },
    "23 Yahoo": {
        "slug": "yahoo", "name": "Yahoo", "logo": "yahoo", "ext": "jpeg",
        "desc": "Search infrastructure C++ modules — alf* networking, I/O, and server components.",
        "skills": ["C++", "Search", "Networking", "Linux"],
        "portfolio_only": True,
    },
    "24 JakeKnows": {
        "slug": "jakeknows", "name": "JakeKnows", "logo": "company", "ext": "png",
        "desc": "Identity engine, code generators, Sony Taleo mobile job app, WCF engine services.",
        "skills": ["C#", "Python", "MSSQL", "WCF", "Code Generation"],
    },
    "25 OpenTV": {
        "slug": "opentv", "name": "OpenTV", "logo": "opentv", "ext": "jpeg",
        "desc": "DynSchLib dynamic ad scheduler — Core2 scheduling engine for cable head-ends.",
        "skills": ["C#", "C++", "Scheduling", "Oracle", "Cable"],
    },
    "26 Google": {
        "slug": "google", "name": "Google", "logo": "google", "ext": "jpeg",
        "desc": "Earth Enterprise, Avik/Babel L10n, Antaeus, Android tooling — archived contractor trees.",
        "skills": ["Java", "Python", "Dart", "GCP", "Android"],
    },
    "27 Vmware": {
        "slug": "vmware", "name": "VMware", "logo": "vmware", "ext": "jpeg",
        "desc": "Gemini Python QA framework, gemini2 automation, CLIInfo test harness.",
        "skills": ["Python", "Perl", "Virtualization", "Automation", "ESX"],
    },
    "28 Knurld": {
        "slug": "knurld", "name": "Knurld", "logo": "knulrd", "ext": "jpeg",
        "desc": "Voice biometric API integration, Apigee, Python ML/scoring pipeline prototypes.",
        "skills": ["Python", "API", "ML", "Voice Biometrics", "Apigee"],
        "portfolio_only": True,
    },
    "29 Butterfleye": {
        "slug": "butterfleye", "name": "Butterfleye", "logo": "butterfleye", "ext": "jpeg",
        "desc": "Camera cloud backend — Alembic migrations, timeline events, video segments, streaming.",
        "skills": ["Python", "SQL", "AWS", "IoT", "Video"],
        "portfolio_only": True,
    },
    "30 Thuuz": {
        "slug": "thuuz", "name": "Thuuz", "logo": "thuuz", "ext": "png",
        "desc": "Callsigns JSON API, S3 sync scripts for sports broadcast metadata.",
        "skills": ["Python", "AWS", "S3", "JSON", "API"],
        "portfolio_only": True,
    },
    "32 Chase": {
        "slug": "chase", "name": "Chase (Game of Life)", "logo": "chase", "ext": "svg",
        "desc": "Conway Game of Life Java grid implementation — portfolio sample project.",
        "skills": ["Java", "Algorithms", "Grid", "Simulation"],
        "portfolio_only": True,
    },
    "33 HiveMapper": {
        "slug": "hivemapper", "name": "HiveMapper", "logo": "hivemapper", "ext": "svg",
        "desc": "Drone airport navigation — C++ geometry graph, shortest-path planner.",
        "skills": ["C++", "Graph", "Geometry", "Algorithms", "Drones"],
        "portfolio_only": True,
    },
    "WEBSITE": {
        "slug": "greenleaf", "name": "Green Leaf Website", "logo": "greenleaf", "ext": "svg",
        "desc": "Green Leaf branding site assets and category catalog.",
        "skills": ["Web", "Branding", "HTML"],
        "portfolio_only": True,
    },
}

# Resume employers with NO Development folder — portfolio cards only, no archive block
RESUME_ONLY: list[dict] = [
    {"slug": "mafroda", "name": "MAF RODA", "logo": "mafroda", "ext": "png", "current": True,
     "desc": "Americas traceability lead — fleet installer, OpenCV on sorters, sample apps.",
     "skills": ["Python", "OpenCV", "C#", ".NET", "Traceability"]},
    {"slug": "leidos", "name": "Leidos", "logo": "leidos", "ext": "png",
     "desc": "Airport security scanning app (C++, Qt5, Python) and enterprise performance architecture.",
     "skills": ["C++", "Qt5", "Python", "Imaging", "Security"]},
    {"slug": "meta", "name": "Meta", "logo": "facebook", "ext": "jpeg",
     "desc": "Privacy audit engineering for M&A — compliance tooling across SQL/NoSQL estates.",
     "skills": ["Privacy", "Security", "Compliance", "SQL", "NoSQL"]},
    {"slug": "veritas", "name": "Veritas", "logo": "veritas", "ext": "jpeg",
     "desc": "NetBackup appliance hardening — OSCAP, OAuth2/LDAP, Java/Python refactor.",
     "skills": ["Java", "Python", "OSCAP", "Security", "Backup"]},
    {"slug": "hpe", "name": "HPE", "logo": "hpe", "ext": "jpeg",
     "desc": "Airwave wireless appliance hardening and Perl→Python port.",
     "skills": ["Python", "Perl", "OSCAP", "Wireless", "Security"]},
    {"slug": "guidance", "name": "Guidance Software", "logo": "guidance", "ext": "jpeg",
     "desc": "Digital forensics — Symantec Ghost format reverse engineering, Win32 disk imaging.",
     "skills": ["C++", "Forensics", "IDA Pro", "Win32", "Reverse Engineering", "Image Processing", "Visual Studio", "WinDbg", "DDK", "SoftICE"]},
    {"slug": "woodtech", "name": "Wood Technologies", "logo": "woodtech", "ext": "svg",
     "desc": "NT/Exchange, BBS utilities, Netscape server, executive MIS databases.",
     "skills": ["NT", "Exchange", "BBS", "SQL", "Netscape"]},
    {"slug": "frys", "name": "Fry's Electronics", "logo": "frys", "ext": "svg",
     "desc": "Retail software sales, demo systems, PC technical support.",
     "skills": ["PC Support", "Retail", "Diagnostics", "Sales"]},
    {"slug": "lcs", "name": "LCS Logical Computer", "logo": "lcs", "ext": "svg",
     "desc": "Novell NetWare 3.11 installs, VB/Access MIS debugging on LAN/WAN.",
     "skills": ["Novell", "NetWare", "Visual Basic", "MS Access"]},
]

# Display order: recent/current first (portfolio grid); carousel = reversed
PRIORITY_SLUGS = [
    "mafroda", "leidos", "google", "meta", "vmware",
    "veritas", "thuuz", "knurld", "butterfleye", "hpe", "jakeknows", "yahoo", "motorola", "surfware", "spirent", "directv",
    "guidance", "hms", "audiotelco",
    "voltdelta", "posdev", "woodtech", "disney", "electrosonic",
    "access", "frys", "lcs",
    "hivemapper", "chase", "greenleaf",
]


def project_names(folder: Path) -> list[str]:
    names: set[str] = set()
    for ext in PROJECT_EXTS:
        for f in folder.rglob(f"*{ext}"):
            if any(p in SKIP_DIRS for p in f.parts):
                continue
            names.add(f.stem)
    return sorted(names)


def area_detail(area_path: Path) -> dict:
    projs = project_names(area_path)
    subdirs = sorted(x.name for x in area_path.iterdir() if x.is_dir() and x.name not in SKIP_DIRS)[:20]
    if not projs:
        for x in sorted(area_path.iterdir()):
            if x.is_dir() and x.name not in SKIP_DIRS:
                projs.append(x.name)
            elif x.suffix.lower() in {".mdb", ".accdb", ".cs", ".java", ".py", ".cpp", ".rb"}:
                projs.append(x.stem)
        projs = sorted(set(projs))[:40]
    if area_path.name in {"asp", "Clients", "ESCAN", "automation", "redrat", "search", "knurld", "butterfleye"}:
        deep: set[str] = set()
        for sub in area_path.iterdir():
            if sub.is_dir() and sub.name not in SKIP_DIRS:
                inner = project_names(sub)
                deep.update(inner if inner else [sub.name])
        if deep:
            projs = sorted(set(projs) | deep)[:40]
    if area_path.name == "WebApps":
        asp = area_path / "asp"
        if asp.is_dir():
            for sub in sorted(asp.iterdir()):
                if sub.is_dir() and sub.name not in SKIP_DIRS:
                    projs.append(sub.name)
            projs = sorted(set(projs))[:40]
    return {"name": area_path.name, "projects": projs, "subdirs": subdirs[:12]}


def scan_folder(folder: Path) -> dict:
    areas: list[dict] = []
    if not folder.is_dir():
        return {"root": str(folder), "exists": False, "areas": [], "all_projects": []}
    for child in sorted(folder.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        areas.append(area_detail(child))
    root_files = [
        f.name for f in sorted(folder.iterdir())
        if f.is_file() and f.suffix.lower() in {".mdb", ".accdb", ".txt", ".doc", ".docx", ".pdf", ".py", ".java"}
    ]
    if root_files:
        areas.insert(0, {"name": "(root files)", "projects": root_files, "subdirs": []})
    all_p: set[str] = set()
    for a in areas:
        all_p.update(a.get("projects") or [])
    return {"root": str(folder), "exists": True, "areas": areas, "all_projects": sorted(all_p)}


def scan_slug(slug: str, folder_names: list[str]) -> dict:
    entries = []
    all_projects: set[str] = set()
    for name in folder_names:
        summary = scan_folder(DEV_ROOT / name)
        entries.append({"folder": name, **summary})
        all_projects.update(summary.get("all_projects") or [])
    return {
        "slug": slug,
        "folders": folder_names,
        "archive_entries": entries,
        "all_projects": sorted(all_projects),
    }


def folder_sort_key(name: str) -> tuple:
    m = re.match(r"^(\d+)", name)
    return (int(m.group(1)) if m else 999, name)


def main() -> None:
    if not DEV_ROOT.is_dir():
        raise SystemExit(f"Development archive missing: {DEV_ROOT}")

    slug_to_folders: dict[str, list[str]] = {}
    dev_employers: dict[str, dict] = {}

    for folder_name, meta in sorted(FOLDER_META.items(), key=lambda x: folder_sort_key(x[0])):
        slug = meta["slug"]
        if slug in EXCLUDED_SLUGS:
            continue
        slug_to_folders.setdefault(slug, []).append(folder_name)

    for slug, folders in slug_to_folders.items():
        extra = EXTRA_PATHS.get(slug, [])
        all_folders = folders + [f for f in extra if f not in folders]
        dev_employers[slug] = scan_slug(slug, all_folders)

    # Portfolio cards from Development
    dev_cards: dict[str, dict] = {}
    for folder_name, meta in FOLDER_META.items():
        slug = meta["slug"]
        if slug in EXCLUDED_SLUGS or slug in dev_cards:
            continue
        card = {
            "slug": slug,
            "name": meta["name"],
            "logo": meta["logo"],
            "ext": meta["ext"],
            "desc": meta["desc"],
            "skills": meta["skills"],
            "dev_folder": folder_name,
            "has_archive": True,
            "portfolio_only": meta.get("portfolio_only", False),
            "in_old_resume": slug in IN_OLD_RESUME,
            "in_current_resume": slug in IN_CURRENT_RESUME,
        }
        dev_cards[slug] = card

    resume_cards = {e["slug"]: {**e, "has_archive": False, "portfolio_only": False,
                                 "in_old_resume": e["slug"] in IN_OLD_RESUME,
                                 "in_current_resume": e["slug"] in IN_CURRENT_RESUME}
                    for e in RESUME_ONLY if e["slug"] not in EXCLUDED_SLUGS}

    all_slugs = (set(dev_cards) | set(resume_cards)) - EXCLUDED_SLUGS
    ordered = [s for s in PRIORITY_SLUGS if s in all_slugs]
    ordered += sorted(all_slugs - set(ordered))

    portfolio = []
    for slug in ordered:
        card = resume_cards.get(slug) or dev_cards.get(slug)
        if not card:
            continue
        portfolio.append(card)

    inventory = {"dev_root": str(DEV_ROOT), "employers": dev_employers}
    catalog = {
        "dev_root": str(DEV_ROOT),
        "portfolio": portfolio,
        "dev_cards": dev_cards,
        "resume_only_cards": resume_cards,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(dev_employers)} archive slugs, {len(portfolio)} portfolio cards → {CATALOG}")


if __name__ == "__main__":
    main()
