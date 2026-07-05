#!/usr/bin/env python3
"""Parse LinkedIn skills from linkedin-profile export → portfolio data/linkedin-skills.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

LINKEDIN_RAW = Path("/home/kg/Jobs/linkedin-profile/raw-public-fetch.txt")
OUT = Path(__file__).resolve().parents[1] / "data" / "linkedin-skills.json"

# Tokens that are LinkedIn scrape noise, not real skills
NOISE = frozenset({
    "set", "get", "axis", "well", "adds", "produce", "fix", "track", "fast", "grasp",
    "board", "streams", "government", "expediting", "progress", "engineer", "developer",
    "consultant", "analysis", "processing", "designs", "development", "code", "data",
    "technology", "research", "process", "maintenance", "operations", "implementation",
    "teams", "core", "access", "storage", "management", "identity", "collection",
    "importing", "enhancements", "redesign", "efficiency", "facilitation", "replication",
    "querying", "scan", "interfaces", "optimizations", "produce", "lint", "regression",
    "backend", "architectures", "stack", "integration", "testing", "tests", "support",
    "programming", "engineering", "design", "architect", "software developer",
    "senior software engineer", "senior software developer", "application engineer",
    "maintenance engineer", "ui developer", "c++ python", "java c++", "c++, java",
    "c, c++", "java python", "java code", "python code", "developed design",
    "design code", "privacy security", "software engineering",
    "object oriented software development", "object-oriented software", "object oriented",
    "written communication", "abstract reasoning", "decision making", "impact production",
    "impact analysis", "software infrastructure", "back end development",
    "front-end development", "client/server architecture", "design architecture",
    "framework design", "architecture patterns", "design patterns", "design implementation",
    "configuration management", "operating system configuration", "system configuration",
    "linux environments", "agile environment", "remote work", "business applications",
    "enterprise solutions", "third-party management", "vendor management", "human resources",
    "project management", "large-scale scrum (less)", "microsoft office", "graphic design",
    "search engine optimization", "equipment management", "acquire gim suite",
    "international laws", "regulations", "ensure compliance", "security compliance",
    "security authorization", "tests automation", "provide support", "fix",
    "audio video", "adds", "well", "get", "metadata / meta-analysis",
})

TITLE_OVERRIDES = {
    "c++": "C++",
    "c": "C",
    "c#": "C#",
    "c, c++": "C/C++",
    "c++, java": "C++, Java",
    "java c++": "Java, C++",
    "c++ python": "C++, Python",
    "java python": "Java, Python",
    "amazon web services": "AWS",
    "rest web services": "REST",
    "restful web services": "REST",
    "restful": "REST",
    "postgresql": "Postgres",
    "optical character recognition (ocr)": "OCR",
    "optical character recognition": "OCR",
    "fast fourier transform": "FFT",
    "fourier transform": "FFT",
    "fourier analysis": "FFT",
    "google earth enterprise": "Google Earth Enterprise",
    "google earth": "Google Earth",
    "netbackup appliance": "NetBackup",
    "vmware cloud": "VMware",
    "cloud virtualization": "Cloud Virtualization",
    "cloud technologies": "Cloud",
    "cloud computing": "Cloud",
    "cloud development": "Cloud",
    "linux embedded": "Embedded Linux",
    "embedded systems": "Embedded",
    "embedded": "Embedded",
    "machine vision": "Machine Vision",
    "image processing": "Image Processing",
    "computer vision": "Computer Vision",
    "distributed systems": "Distributed Systems",
    "reverse engineering": "Reverse Engineering",
    "code analysis": "Code Analysis",
    "test automation": "Test Automation",
    "software maintenance": "Software Maintenance",
    "database schema": "Database Design",
    "schema design": "Database Design",
    "data pipelines": "Data Pipelines",
    "speech data collection": "Speech Data",
    "privacy audit": "Privacy Audit",
    "privacy": "Privacy",
    "security": "Security",
    "authorization": "Authorization",
    "authentication": "Authentication",
    "malware detection": "Malware Detection",
    "api development": "API Development",
    "plugin development": "Plugin Development",
    "infrastructure automation": "Infrastructure Automation",
    "object-oriented software": "OOP",
    "5-axis machining": "5-Axis CNC",
    "cad/cam": "CAD/CAM",
    "html5": "HTML5",
    "asp.net": "ASP.NET",
    ".net": ".NET",
    "app engine": "App Engine",
    "bigquery": "BigQuery",
    "opencv": "OpenCV",
    "qt": "Qt",
    "ios": "iOS",
    "android": "Android",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "bash scripts": "Bash",
    "bash": "Bash",
    "perl scripting": "Perl",
    "perl": "Perl",
    "mysql": "MySQL",
    "oracle": "Oracle",
    "docker": "Docker",
    "vmware": "VMware",
    "kubernetes": "Kubernetes",
    "esxi": "ESXi",
    "oscap": "OSCAP",
    "ldap": "LDAP",
    "rbac": "RBAC",
    "microservices": "Microservices",
    "angular": "Angular",
    "python": "Python",
    "java": "Java",
    "linux": "Linux",
    "windows": "Windows",
    "win32": "Win32",
    "windows 7": "Windows",
    "iot": "IoT",
    "sql": "SQL",
    "xml": "XML",
    "css": "CSS",
    "php": "PHP",
    "vba": "VBA",
    "tcl": "Tcl",
    "swig": "SWIG",
    "com": "COM",
    "activex": "ActiveX",
    "opengl": "OpenGL",
    "geospatial": "Geospatial",
    "virtualization": "Virtualization",
    "networking": "Networking",
    "wireless": "Wireless",
    "streaming": "Streaming",
    "telephony": "Telephony",
    "accessibility": "Accessibility",
    "mentoring": "Mentoring",
    "leadership": "Leadership",
    "agile": "Agile",
    "automation": "Automation",
    "consultancy": "Consulting",
    "databases": "Databases",
    "database": "Databases",
    "backup": "Backup",
    "open source": "Open Source",
    "visual studio": "Visual Studio",
    "mobile development": "Mobile",
    "mobile devices": "Mobile",
    "kernel": "Kernel",
    "kernel methods": "Kernel Methods",
    "decision trees": "Decision Trees",
    "libusb": "libusb",
    "infrared": "Infrared",
    "remote control": "Remote Control",
    "video capture": "Video Capture",
    "image data management": "Image Data",
    "captioning": "Closed Captioning",
    "closed captioning": "Closed Captioning",
    "solidworks": "SolidWorks",
    "parasolid": "Parasolid",
    "airwave": "Airwave",
    "netbackup": "NetBackup",
    "youtube": "YouTube",
    "localization": "Localization",
    "web development": "Web Development",
    "web applications": "Web Applications",
    "web services": "Web Services",
    "framework": "Frameworks",
    "pmd": "PMD",
    "crystal": "Crystal Reports",
    "atlassian": "Atlassian",
    "ansible": "Ansible",
    "transceiver": "Transceivers",
    "socket": "Sockets",
    "ace framework": "ACE",
    "ace": "ACE",
    "infrastructure": "Infrastructure",
    "production": "Production",
    "qa": "QA",
    "rest": "REST",
    "server": "Server",
    "workflow": "Workflow",
    "scripting": "Scripting",
    "scripts": "Scripting",
    "load testing": "Load Testing",
    "dataops": "DataOps",
    "analytics": "Analytics",
    "compliance": "Compliance",
    "auditing": "Auditing",
    "audit": "Auditing",
    "detection": "Detection",
    "hardware": "Hardware",
    "transceiver": "Transceivers",
    "resource allocation": "Resource Management",
    "build system": "Build Systems",
    "integration api": "API Integration",
    "operating system": "Operating Systems",
    "configuration": "Configuration",
    "algorithms": "Algorithms",
    "systems management": "Systems Management",
    "software architect": "Solution Architecture",
    "software architecture": "Solution Architecture",
    "architecture": "Architecture",
    "efficiency": "Performance",
    "optimizations": "Performance",
    "refactoring": "Refactoring",
    "bug fixes": "Debugging",
    "data collection tools": "Data Collection",
    "data collection": "Data Collection",
    "data comparison": "Data Analysis",
    "distributed teams": "Distributed Teams",
    "generator": "Code Generation",
    "code generator": "Code Generation",
    "meta programming": "Meta-programming",
    "memory allocation": "Memory Management",
    "client script": "Client Scripting",
    "ui": "UI/UX",
    "hardware solutions": "Hardware",
    "privacy security": "Privacy & Security",
}

NEVER_DISPLAY = frozenset({"C++", "PMD", "Telemarketing"})

DISPLAY_PRIORITY = [
    "C/C++", "Python", "Java", "C#", "JavaScript", "TypeScript", "Perl", "Dart", "Go",
    "Angular", "Node.js", ".NET", "HTML5", "REST", "Microservices", "Web Services",
    "Postgres", "SQL Server", "Oracle", "MySQL", "BigQuery", "NoSQL", "Database Design",
    "Machine Learning", "AI",
    "AWS", "GCP", "Docker", "Kubernetes", "Cloud", "VMware", "ESXi",
    "Linux", "Win32", "Embedded", "Embedded Linux", "Bash", "Kernel",
    "Security", "OAuth2", "RBAC", "Authorization", "Authentication",
    "OSCAP", "Privacy", "Privacy Audit", "LDAP", "Compliance", "Malware Detection",
    "OpenCV", "OCR", "Machine Vision", "Image Processing", "Computer Vision",
    "Geospatial", "Google Earth Enterprise", "FFT", "Video Capture", "SIMD", "Traceability",
    "Qt", "OpenGL", "COM", "ActiveX", "CAD/CAM", "SolidWorks", "IoT",
    "Automation", "Test Automation", "Distributed Systems", "Virtualization",
    "Reverse Engineering", "Code Analysis",
    "Networking", "Wireless", "Telephony", "Streaming", "Accessibility",
    "Tcl", "SWIG", "YAML", "Protobuf", "App Engine", "Data Pipelines",
    "Solution Architecture", "Mentoring", "Agile", "Consulting",
]

# Résumé / portfolio skills to keep even when LinkedIn tokens omit them
ALWAYS_INCLUDE = [
    "C/C++", "Go", "GCP", "Node.js", "OAuth2", "RBAC", "OpenCV", "SIMD",
    "Traceability", "Win32", "Tcl", "SQL Server", "LDAP", "YAML", "Protobuf",
    "Machine Vision", "Kubernetes", "NoSQL", "Machine Learning", "AI", "TypeScript",
]


def extract_skills_line(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("cloud computing •") or (
            "## Skills" in text and "cloud computing" in line and "•" in line
        ):
            return line.strip()
    in_skills = False
    buf: list[str] = []
    for line in text.splitlines():
        if line.strip() == "## Skills":
            in_skills = True
            continue
        if in_skills:
            if line.startswith("## "):
                break
            buf.append(line)
    return " ".join(buf).strip()


def normalize_token(raw: str) -> str | None:
    key = raw.strip().lower()
    if not key or len(key) < 2 or key in NOISE:
        return None
    if key in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[key]
    if key.isupper() or re.fullmatch(r"[a-z0-9.+#/-]+", key):
        return raw.strip() if raw.strip() != key else key.title()
    # Title-case short phrases
    parts = key.split()
    if len(parts) <= 4:
        titled = " ".join(p.upper() if p in ("api", "ocr", "fft", "sql", "xml", "css", "iot", "qa", "ui", "ux", "rbac", "ldap", "oscap", "esxi", "pmd", "com", "ace", "swig", "tcl", "php", "vba") else p.capitalize() for p in parts)
        return titled.replace("Ui/ux", "UI/UX")
    return None


def parse_skills(blob: str) -> list[str]:
    tokens = [t.strip() for t in blob.split("•")]
    seen: set[str] = set()
    out: list[str] = []
    for tok in tokens:
        norm = normalize_token(tok)
        if norm and norm not in seen:
            seen.add(norm)
            out.append(norm)
    return sorted(out, key=str.lower)


def pick_display(all_skills: list[str]) -> list[str]:
    skill_set = set(all_skills) | set(ALWAYS_INCLUDE)
    if "C++" in skill_set:
        skill_set.add("C/C++")
    display: list[str] = []
    for s in DISPLAY_PRIORITY + list(ALWAYS_INCLUDE):
        if s in skill_set and s not in display:
            display.append(s)
    # Fill with other strong skills up to 60
    extras = [
        s for s in all_skills
        if s not in display
        and len(s) >= 3
        and s not in {"Frameworks", "Production", "Scripting", "Configuration", "Detection", "Hardware", "Server", "Workflow", "Analytics", "Debugging", "Performance", "Architecture", "Consulting", "Cloud", "Mobile", "Backup", "Open Source", "Frameworks", "YouTube", "Localization", "Web Development", "Web Applications", "Data Collection", "Data Analysis", "Distributed Teams", "Code Generation", "Meta-programming", "Memory Management", "Client Scripting", "UI/UX", "Privacy & Security", "Crystal Reports", "Atlassian", "Transceivers", "Sockets", "ACE", "Infrastructure", "QA", "Resource Management", "Build Systems", "API Integration", "Operating Systems", "Algorithms", "Systems Management", "DataOps", "Auditing", "Remote Control", "Image Data", "Closed Captioning", "Parasolid", "5-Axis CNC", "Airwave", "NetBackup", "Software Maintenance", "Databases", "App Engine", "API Development", "Plugin Development", "Infrastructure Automation", "OOP", "ASP.NET", "PHP", "VBA", "libusb", "Infrared", "Kernel Methods", "Decision Trees", "Load Testing", "DataOps"}
    ]
    for s in extras:
        if len(display) >= 58:
            break
        if s not in display and s not in NEVER_DISPLAY:
            display.append(s)
    return [s for s in display if s not in NEVER_DISPLAY]


def main() -> None:
    if not LINKEDIN_RAW.is_file():
        raise SystemExit(f"Missing {LINKEDIN_RAW} — run LinkedIn profile fetch first.")
    text = LINKEDIN_RAW.read_text(encoding="utf-8")
    blob = extract_skills_line(text)
    if not blob:
        raise SystemExit("Could not find skills section in raw LinkedIn export.")
    all_skills = parse_skills(blob)
    display_skills = pick_display(all_skills)
    missing_from_old_portfolio = [
        s for s in display_skills
        if s not in {
            "C/C++", "Python", "Java", "C#", "TypeScript", "Go", "Postgres", "SQL Server",
            "REST", "Microservices", "AWS", "GCP", "Docker", "Linux", "Win32", "Embedded",
            "Security", "OAuth2", "RBAC", "Automation", "OCR", "OpenCV", "SIMD",
            "Traceability", "Angular", "Node.js", "Tcl", "CAD/CAM", "Virtualization",
        }
    ]
    payload = {
        "source_url": "https://www.linkedin.com/in/kevin-guerra-36151446/",
        "source_file": str(LINKEDIN_RAW),
        "parsed_count": len(all_skills),
        "display_skills": display_skills,
        "all_skills": all_skills,
        "added_to_portfolio_vs_previous": missing_from_old_portfolio,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_skills)} skills ({len(display_skills)} display) → {OUT}")
    print(f"New vs old CORE_SKILLS: {len(missing_from_old_portfolio)} added")


if __name__ == "__main__":
    main()
