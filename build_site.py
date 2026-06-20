#!/usr/bin/env python3
"""Generate static HTML pages for KG Portfolio."""

import html
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
PROJECTS_DIR = ROOT / "projects"
RESUME_SRC = Path("/home/kg/Jobs/Kevin Guerra.pdf")
RESUME_ASSET = "assets/Kevin-Guerra.pdf"

OWNER = "Kevin Alexander Guerra"
OWNER_SHORT = "Kevin"
SITE_NAME = "KG PORTFOLIO"
COPYRIGHT_YEAR = "2026"
CONTACT_EMAIL = "kevingnet1@gmail.com"
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://kevingnet.github.io/kg-portfolio").rstrip("/")
SITE_TAGLINE = (
    "Software developer portfolio — currently Sr. Software Engineer at MAF RODA Agrobotic; "
    "enterprise systems, computer vision, traceability, cloud, and performance optimization."
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

NAV = [
    ("Portfolio", "index.html"),
    ("Services", "services.html"),
    ("Samples", "samples.html"),
    ("About", "about.html"),
]

SOCIAL = {
    "linkedin": "https://www.linkedin.com/in/kevin-guerra-36151446/",
    "github": "https://github.com/kevingnet",
}

# name, image file, ext, slug, card description, skill chips (max ~5 shown on card)
PORTFOLIO = [
    ("MAF RODA", "mafroda", "png", "mafroda",
     "Americas traceability lead — fleet installer, OpenCV on sorters, sample apps.",
     ["Python", "OpenCV", "C#", ".NET", "Traceability"]),
    ("Leidos", "leidos", "png", "leidos",
     "Airport security scanning app (C++, Qt5, Python) and enterprise performance architecture.",
     ["C++", "Qt5", "Python", "Imaging", "Security"]),
    ("Google", "google", "jpeg", "google",
     "Localization, Maps, Hardware Analytics, Speech Ops, YouTube, HR.",
     ["Java", "Python", "GCP", "Postgres", "Dart"]),
    ("DirecTV", "directv", "jpeg", "directv",
     "OCR automation, image processing, and test infrastructure.",
     ["C++", "Python", "OCR", "Computer Vision"]),
    ("JakeKnows", "company", "png", "jakeknows",
     "Distributed identity engine and Sony mobile job-application backend.",
     ["C#", "Python", "MSSQL", "Web Services"]),
    ("Disney", "disney", "jpeg", "disney",
     "Enterprise web apps, deployers, and Novell networking tools.",
     ["C++", "ASP", "VB", "MSSQL"]),
    ("Electrosonic", "electrosonic", "jpeg", "electrosonic",
     "AV scheduling, robotics integration, and remote device control.",
     ["C++", "COM", "TCP/IP", "Embedded"]),
    ("VoltDelta", "voltdelta", "jpeg", "voltdelta",
     "Phone switch simulator and X.25 network connector.",
     ["C++", "X.25", "TCP/IP", "Win32"]),
    ("Vmware", "vmware", "jpeg", "vmware",
     "QA automation framework — 80k LOC legacy replaced with 8k LOC Python.",
     ["Python", "Perl", "Automation", "Virtualization"]),
    ("HMS", "hypermedia", "jpeg", "hms",
     "Input validation library, penetration testing, security audits.",
     ["C++", "Python", "Security", "Linux"]),
    ("Surfware", "surfware", "jpeg", "surfware",
     "CAD/CAM CNC software and SolidWorks / AutoCAD interfaces.",
     ["C++", "C#", "OpenGL", "CAD/CAM"]),
    ("Motorola", "motorola", "jpeg", "motorola",
     "Closed-captioning module for set-top boxes.",
     ["C++", "Embedded", "OCAP", "Linux"]),
    ("OpenTV", "opentv", "jpeg", "opentv",
     "Local advertisement scheduler for major cable operators.",
     ["C#", "C++", "Python", "Oracle"]),
    ("Spirent", "spirent", "jpeg", "spirent",
     "Tcl scripting interface for network test appliances.",
     ["C++", "Tcl", "SWIG", "Networking"]),
]

SERVICES = [
    ("Ideation", "Product concepts, architecture options, and rapid prototypes to validate direction before a full build."),
    ("Web & Cloud Development", "Full-stack apps, REST APIs, microservices, and deployment on AWS, GCP, or Docker."),
    ("Security & Privacy", "Threat modeling, code review, input validation libraries, and compliance-aware design."),
    ("Reverse Engineering", "Legacy system analysis, protocol decoding, and safe modernization paths."),
    ("Databases", "Schema design, query optimization, Postgres / SQL Server, and data pipelines."),
    ("Consulting", "Technical leadership, stalled-project recovery, and team mentoring."),
    ("Custom Applications", "Desktop, embedded, and internal tools tailored to your workflow."),
    ("Performance Optimization", "Profiling-driven speedups — from geospatial XML (11×) to zero-allocation embedded paths."),
    ("Embedded Systems", "Set-top boxes, device drivers, robotics interfaces, and resource-constrained C++."),
    ("Image Processing", "OCR, machine vision, FFT-based recognition, and video capture pipelines."),
]

CORE_SKILLS = [
    "C/C++", "Python", "Java", "C#", "TypeScript", "Go",
    "Postgres", "SQL Server", "REST", "Microservices",
    "AWS", "GCP", "Docker", "Linux", "Win32", "Embedded",
    "Security", "OAuth2", "RBAC", "Automation", "OCR",
    "OpenCV", "SIMD", "Traceability",
    "Angular", "Node.js", "Tcl", "CAD/CAM", "Virtualization",
]

TIMELINE = [
    ("MAF RODA Agrobotic", "2025–present",
     "Sr. Software Engineer — Americas traceability lead, fleet installers, OpenCV on production sorters."),
    ("Leidos · Independent · Google · Meta", "2018–2025",
     "Airport scanning (Leidos), AWS consulting, YouTube/Earth/HR at Google, privacy audits at Meta."),
    ("VMware · Veritas · HPE", "2015–2018",
     "QA framework rewrite (80k→8k LOC), OSCAP/OWASP hardening on appliances."),
    ("Electrosonic · Disney · DirecTV · …", "1990s–2010s",
     "Embedded AV, enterprise web, OCR automation, CAD/CAM, set-top boxes, network test gear."),
]

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

# title, description, github URL, optional code snippet HTML, optional live demo URL
SAMPLES = [
    ("Magazine — Angular + REST Demo",
     "Angular admin app with in-browser fake backend — live on GitHub Pages.",
     "https://github.com/kevingnet/magazine", None, "https://kevingnet.github.io/magazine/"),
    ("Game of Life — Java",
     "Conway's Game of Life — cellular automaton in Java.",
     "https://github.com/kevingnet/GameOfLife",
     """<pre class="code-snippet"><code><span class="kw">int</span> neighbors = 0;
<span class="kw">for</span> (<span class="kw">int</span> dy = -1; dy &lt;= 1; dy++)
  <span class="kw">for</span> (<span class="kw">int</span> dx = -1; dx &lt;= 1; dx++)
    <span class="kw">if</span> (dx != 0 || dy != 0) neighbors += grid.at(x+dx, y+dy);
next[x][y] = (neighbors == 3) || (grid.at(x,y) &amp;&amp; neighbors == 2);</code></pre>""", "https://kevingnet.github.io/GameOfLife/"),
    ("Virtual Coffee Machine",
     "Angular coffee simulator — brew, refill, and tank levels. Live on GitHub Pages; Node API for local dev.",
     "https://github.com/kevingnet/coffee.bitnami", None,
     "https://kevingnet.github.io/coffee.bitnami/"),
    ("Flux — Electric Vehicle",
     "30 / 60 / 90-day project plan with architecture diagrams.",
     "https://github.com/kevingnet/FluxElectricVehicle", None, "https://kevingnet.github.io/FluxElectricVehicle/"),
    ("Time Server — Angular + REST Demo",
     "Angular client with REST time API and in-browser demo backend on GitHub Pages.",
     "https://github.com/kevingnet/time_server", None, "https://kevingnet.github.io/time_server/"),
]


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


def sample_entry(title: str, desc: str, gh: str | None, snippet: str | None, demo: str | None) -> str:
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
        f'        <div class="sample-links">\n          {" ".join(links)}\n        </div>'
        if links else ""
    )
    return f"""      <article class="sample-entry fade-in">
        <h2>{title_html}</h2>
        <p>{html.escape(desc)}</p>
        {snippet or ""}
{links_block}
      </article>"""


def tech_to_chips(tech: str, limit: int = 16) -> str:
    parts = [t.strip() for t in tech.replace(";", ",").split(",") if t.strip()]
    return skill_chips(parts, limit)


def project_gallery(figures: list[tuple[str, str]], depth: int = 1) -> str:
    """figures: list of (filename under projects/mafroda/, caption)"""
    p = rel_prefix(depth)
    items = "\n".join(
        f"""      <figure class="project-figure">
        <img src="{p}assets/images/projects/mafroda/{fname}" alt="{html.escape(caption)}" loading="lazy">
        <figcaption>{html.escape(caption)}</figcaption>
      </figure>"""
        for fname, caption in figures
    )
    return f'      <div class="project-gallery">\n{items}\n      </div>'


def copy_maf_project_images() -> None:
    src_dir = Path("/home/kg/Jobs/Graphics/images")
    dest = ROOT / "assets/images/projects/mafroda"
    dest.mkdir(parents=True, exist_ok=True)
    mapping = [
        ("traceability-dashboard.png", "Screenshot 2026-06-02 144647.png"),
        ("traceability-detail.png", "Screenshot 2026-06-02 144820.png"),
        ("traceability-ui.png", "Screenshot 2026-06-02 141535.png"),
        ("installer-gui.png", "Screenshot 2025-08-01 131140.png"),
        ("installer-scripts.png", "ListOfScripts.png"),
    ]
    for dest_name, src_name in mapping:
        src = src_dir / src_name
        if src.is_file():
            shutil.copy2(src, dest / dest_name)


def rel_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def carousel(depth: int = 0) -> str:
    p = rel_prefix(depth)
    imgs = "\n".join(
        f'      <img src="{p}assets/images/{img}.{ext}" alt="{html.escape(display)}">'
        for display, img, ext, _slug, _desc, _skills in PORTFOLIO
    )
    return f"""  <div class="logo-carousel">
    <div class="logo-carousel-track">
{imgs}
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
  </div>
  <div class="nav-wrap">
    <ul class="site-nav">
{links}
    </ul>
  </div>
{carousel(depth)}
  </header>"""


def footer(depth: int = 0) -> str:
    p = rel_prefix(depth)
    return f"""  <footer class="site-footer">
    <div class="footer-social">
      <a href="{SOCIAL["linkedin"]}" target="_blank" rel="noopener" title="LinkedIn">
        <img src="{p}assets/images/linkedin.png" alt="LinkedIn">
      </a>
      <a href="{SOCIAL["github"]}" target="_blank" rel="noopener" title="GitHub">
        <img src="{p}assets/images/github.jpeg" alt="GitHub">
      </a>
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
            "About": "about.html",
        }.get(active, "index.html")
    canon = f"{SITE_BASE_URL}/{slug_path.replace('index.html', '').rstrip('/')}"
    if canon.endswith("/") and slug_path != "index.html":
        canon = canon.rstrip("/")
    if slug_path == "index.html":
        canon = f"{SITE_BASE_URL}/"
    img_rel = (og_image or DEFAULT_OG_IMAGE).removeprefix("../")
    og_img = f"{SITE_BASE_URL}/{img_rel}"
    full_title = f"{title} | {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{og_img}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_img}">
  <meta name="theme-color" content="#0e1014">
  <link rel="stylesheet" href="{p}css/style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header(active, depth)}
  <main id="main-content">
{body}
  </main>
{footer(depth)}
  <script src="{p}js/carousel.js"></script>
  <script src="{p}js/site.js"></script>
</body>
</html>
"""

PROJECTS = {
    "mafroda": {
        "title": "MAF RODA Agrobotic",
        "intro": """<p><strong>Sr. Software Engineer — R&amp;D Staff</strong> · Apr 2025 – Present · Remote / Americas</p>
<p>MAF RODA Agrobotic — global leader in post-harvest fruit and vegetable automation (sorting, grading, packaging, palletizing). Current role (3rd at MAF RODA): <strong>Americas traceability lead</strong>.</p>
<ul>
<li><strong>Traceability — Americas:</strong> lead regional traceability systems; AI-assisted tooling and codebase modernization</li>
<li><strong>Python fleet installer (ORPHEA):</strong> YAML-driven operations framework — WMI/WinRM discovery, network config, remote provisioning of sorting clusters</li>
<li><strong>UiSettingsEditor:</strong> WinForms C# tool for production HMI skin / Figma palette settings (JSON appsettings)</li>
<li><strong>JsonWebApi:</strong> ASP.NET Core REST API backing traceability and packing web views</li>
<li><strong>OpenCV:</strong> SIMD + startup buffer pre-allocation on production sorters</li>
</ul>""",
        "tech": "Python, OpenCV, SIMD, C++, C#, ASP.NET Core, WinForms, WMI, WinRM, YAML, JSON, Windows, Image Processing, Traceability, Fleet Deployment, Network Provisioning, AI-Assisted Development",
        "sections": [
            ("Traceability — Americas", "Current · Regional traceability lead", """<p>Lead traceability systems across the Americas. Apply AI on the engineering side — developer tooling, codebase modernization, and AI-assisted improvements to traceability projects and delivery workflows.</p>
<p>Screenshots from traceability tooling and web views deployed in the MAF sorting environment.</p>"""
            + project_gallery([
                ("traceability-dashboard.png", "Traceability dashboard — production sorting overview"),
                ("traceability-detail.png", "Traceability detail view — lot and lane tracking"),
                ("traceability-ui.png", "Traceability UI — configuration and monitoring"),
            ])),
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
            ("JsonWebApi", "ASP.NET Core · REST · JSON", """<p>Sample web API supporting traceability and packing workflows — serves JSON to Angular / web front ends in the MAF ecosystem.</p>
<ul>
<li>ASP.NET Core minimal hosting with controllers and OpenAPI</li>
<li>JSON serialization with explicit property naming for legacy client compatibility</li>
<li>CORS-enabled development mode; integrates with ArticlesImg XML and web view projects</li>
</ul>
<p>Companion to web modules (WebPacking, WebViewBinFillers, LindaVista) in the Graphics tree.</p>"""),
            ("OpenCV Performance", "SIMD · Buffer pre-allocation · Production sorters", """<p>Optimized OpenCV image-processing paths on production fruit sorters using SIMD intrinsics and an allocation strategy that pre-allocates buffers at startup.</p>
<p>Result: reduced runtime memory footprint and buffer churn during high-throughput sorting operations on the line.</p>"""),
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
        "intro": """<p><strong>Software Engineer</strong> · 2018 – 2022 · Mountain View / Remote</p>
<p>Multiple teams across Google — localization, Maps / Earth Enterprise, hardware analytics, devices, YouTube, and HR / finance. Focus: stalled-project recovery, performance optimization, privacy-aware microservices, and greenfield rewrites at global scale.</p>
<ul>
<li><strong>Localization (Avik / Babel):</strong> unstalled a 2-year project; ~45k LOC legacy replaced with ~24k LOC greenfield + 2k LOC RBAC security module — delivered in 7 months</li>
<li><strong>Google Earth Enterprise:</strong> open-source migration, library upgrades, and geospatial XML pipeline — processing time <strong>2 hours → 11 minutes</strong> (~11×)</li>
<li><strong>Hardware Analytics &amp; YouTube:</strong> privacy-aware microservices, authN/authZ, BigQuery pipelines, Borg / GCP</li>
<li><strong>HR payroll (v2):</strong> Java microservices with Guice, Protobuf, and dependency-injection patterns</li>
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
        "intro": """<ul>
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
<p>Invented algorithms using kernel methods and decision trees for analysis of image data and comparison for recognition. This was done in an incredible short time working independently, this took about one month of research and implementation.</p>
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
    "disney": {
        "title": "Disney Projects",
        "intro": """<ul>
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
        "intro": """<ul>
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
        "intro": """<ul>
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
    "vmware": {
        "title": "VMware Projects",
        "intro": """<p><strong>Sr. Member of Technical Staff (MTS)</strong> · 2015 – 2018 · Palo Alto</p>
<p>VMware — virtualization and cloud infrastructure. QA automation for ESX, HBR, and related appliances.</p>
<ul>
<li><strong>Gemini framework:</strong> replaced ~80k LOC Perl legacy with ~8k LOC Python — ~8× faster execution</li>
<li><strong>Paradigms:</strong> object-oriented, functional, and meta-programming patterns in a cohesive test harness</li>
<li><strong>Veritas / HPE (adjacent):</strong> OSCAP and OWASP hardening on backup appliances (see timeline)</li>
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
        "intro": """<ul>
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
    "surfware": {
        "title": "Surfware Projects",
        "intro": """<ul>
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
        "intro": """<p><strong>Closed Captioning Embedded Module</strong></p>
<p>C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes</p>""",
        "tech": "C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes",
        "work": """<h2>Work Performed</h2>
<p>Developed, designed and coded software in a distributed team, agile environment for Linux and embedded systems. The system is embedded in a Set Top Box, it provides Closed Captioning capabilities. Redesign was done to provide exceptional performance eliminating memory allocation completely after initialization.</p>""",
    },
    "opentv": {
        "title": "OpenTV Projects",
        "intro": """<p><strong>Dynamic Scheduler:</strong> Resolved Issues and Enhanced Win32 C# App, used for Local Advertisement Scheduling</p>""",
        "tech": "C#, C/C++, Python, Perl, Oracle, Big Data Import, Win32, Scheduling, Web Services, SOAP, SQL, Stored Procedures, IIS, MVC, .NET, XML",
        "work": """<h2>Work Performed</h2>
<p>Developed software enhancements and bug fixes for application used by major cable companies worldwide. The application was very complex containing over a million lines of code.</p>""",
    },
    "spirent": {
        "title": "Spirent Projects",
        "intro": """<ul>
<li>Tlc Interface: replaced old Tcl code base and converted it to C++, resulting in only one line of tcl code from several thousands.</li>
<li>Mainline: Helped to create second version of embedded application that drives a network testing appliance and can be scripted and instrumented using tcl.</li>
</ul>""",
        "tech": "C/C++, Tcl, Network Testing, Automation, Script Instrumentation, Linux Embedded, ACE Framework, SWIG",
        "work": """<h2>Work Performed</h2>
<p>Developed new user interface for next generation system using SWIG for creation of tcl accessibility layer.</p>
<p>Developed new commands for the network testing system.</p>
<p>Re-factored code to later reuse for the new design. Network Programming, ACE Framework, OOD, Visual Studio.</p>""",
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
    parts.append("    </div>")
    return "\n".join(parts)


def main():
    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    copy_maf_project_images()
    if RESUME_SRC.is_file():
        shutil.copy2(RESUME_SRC, assets / "Kevin-Guerra.pdf")
    elif not (assets / "Kevin-Guerra.pdf").is_file():
        print(f"warn: resume not found at {RESUME_SRC}")

    cards = "\n".join(
        f"""      <article class="portfolio-item fade-in{" portfolio-item--current" if slug == "mafroda" else ""}">
        <a href="projects/{slug}.html">
          {'<span class="current-badge">Current</span>' if slug == "mafroda" else ""}
          <div class="logo-wrap"><img src="assets/images/{img}.{ext}" alt="{name}"></div>
          <span class="company-name">{name}</span>
          <span class="company-desc">{desc}</span>
          {skill_chips(skills, 5)}
        </a>
      </article>"""
        for name, img, ext, slug, desc, skills in PORTFOLIO
    )
    (ROOT / "index.html").write_text(
        page(
            "Portfolio",
            "Portfolio",
            f"""    <section class="hero fade-in">
      <p class="hero-eyebrow">Software Developer</p>
      <h1>{OWNER}</h1>
      <p class="hero-lead">Currently <strong>Sr. Software Engineer at MAF RODA Agrobotic</strong> (Americas traceability). Enterprise systems, computer vision, security, embedded software, and performance work across Google, Disney, VMware, DirecTV, and more.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{RESUME_ASSET}">Download Resume</a>
        <a class="btn btn-secondary" href="mailto:{CONTACT_EMAIL}">Get in Touch</a>
        <a class="btn btn-secondary" href="samples.html">View Samples</a>
      </div>
    </section>
{highlights_strip()}
    <h2 class="page-title">Experience</h2>
    <p class="page-intro">Selected employers and project highlights. Click a card for full detail.</p>
    <div class="portfolio-grid">
{cards}
    </div>""",
            description="Selected software projects at Google, Disney, VMware, DirecTV, and other companies.",
        )
    )

    services = "\n".join(
        f"""      <article class="service-card fade-in">
        <h2>{html.escape(title)}</h2>
        <p>{html.escape(blurb)}</p>
      </article>"""
        for title, blurb in SERVICES
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
    </section>""",
            slug_path="services.html",
            description="Consulting and development: web, cloud, security, embedded systems, and performance optimization.",
        )
    )

    samples_html = "\n".join(
        sample_entry(title, desc, gh, snippet, demo)
        for title, desc, gh, snippet, demo in SAMPLES
    )
    (ROOT / "samples.html").write_text(
        page(
            "Samples",
            "Samples",
            f'    <h1 class="page-title">Projects Samples</h1>\n    <div class="content-section">\n{samples_html}\n    </div>',
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
        <p>Hello, my name is Kevin. I'm a software developer — my career started as a hobby and I'm still passionate about building fast, reliable software across tools, web apps, embedded systems, robotics, networking, databases, security, and virtualization.</p>
        <p>I focus on quality code that stays maintainable: fewer lines, code generation where it helps, and patterns that scale. See my <a href="{RESUME_ASSET}">resume (PDF)</a> for the full technology list and employment history.</p>
        <h2>Core skills</h2>
        <div class="skills-cloud">{"".join(f'<span class="skill-chip">{html.escape(s)}</span>' for s in CORE_SKILLS)}</div>
        <h2>Career timeline</h2>
        <div class="timeline">
{"".join(f'''          <div class="timeline-item">
            <strong>{html.escape(label)}</strong>
            <span>{html.escape(era)}</span>
            <p>{html.escape(note)}</p>
          </div>''' for label, era, note in TIMELINE)}
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
            <a class="btn btn-secondary" href="{RESUME_ASSET}">Resume PDF</a>
          </div>
        </section>
      </div>
    </div>""",
            slug_path="about.html",
            description=f"About {OWNER} — software developer, autodidact, and portfolio author.",
            og_image="assets/images/hero.jpg",
        )
    )

    PROJECTS_DIR.mkdir(exist_ok=True)
    for slug in PROJECTS:
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

    print(f"Generated {len(PROJECTS) + 4} HTML pages in {ROOT}")


if __name__ == "__main__":
    main()
