#!/usr/bin/env python3
"""Mirror all Wix pages via single-file-cli, apply KG branding, deploy to site root."""

import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
MIRROR = ROOT / "mirrored"
SITE = ROOT / "site"
BACKUP = ROOT / "_handmade_backup"

PAGES = {
    "https://iguerranet3.wixsite.com/portfolio-of-igd": "index.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/blank-1": "about.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/blank-4": "services.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/s-projects-basic": "samples.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/general-9": "projects/google.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-google": "projects/directv.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-directv": "projects/jakeknows.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-jakeknows": "projects/disney.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-motorola": "projects/electrosonic.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-opentv": "projects/voltdelta.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-disney": "projects/vmware.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-electrosonic": "projects/hms.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-voltdelta": "projects/surfware.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-vmware": "projects/motorola.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-hms": "projects/opentv.html",
    "https://iguerranet3.wixsite.com/portfolio-of-igd/copy-of-surfware": "projects/spirent.html",
}

BRANDING = [
    ("Ismael Guerra Dominguez", "Kevin Alexander Guerra"),
    ("Portfolio of Ismael Guerra", "Portfolio of Kevin Alexander Guerra"),
    ("Ismael Guerra", "Kevin Alexander Guerra"),
    ("Hello, my name is Ismael,", "Hello, my name is Kevin,"),
    ("my name is Ismael", "my name is Kevin"),
    ("IGD PORTFOLIO", "KG PORTFOLIO"),
    ("IGD Portfolio", "KG Portfolio"),
    ("Ismael", "Kevin"),
    ("IGD", "KG"),
]

# Wix slug -> local path (for internal link rewriting)
SLUG_MAP = {
    "/portfolio-of-igd": "/index.html",
    "/portfolio-of-igd/": "/index.html",
    "/portfolio-of-igd/blank-1": "/about.html",
    "/portfolio-of-igd/blank-4": "/services.html",
    "/portfolio-of-igd/s-projects-basic": "/samples.html",
    "/portfolio-of-igd/general-9": "/projects/google.html",
    "/portfolio-of-igd/copy-of-google": "/projects/directv.html",
    "/portfolio-of-igd/copy-of-directv": "/projects/jakeknows.html",
    "/portfolio-of-igd/copy-of-jakeknows": "/projects/disney.html",
    "/portfolio-of-igd/copy-of-motorola": "/projects/electrosonic.html",
    "/portfolio-of-igd/copy-of-opentv": "/projects/voltdelta.html",
    "/portfolio-of-igd/copy-of-disney": "/projects/vmware.html",
    "/portfolio-of-igd/copy-of-electrosonic": "/projects/hms.html",
    "/portfolio-of-igd/copy-of-voltdelta": "/projects/surfware.html",
    "/portfolio-of-igd/copy-of-vmware": "/projects/motorola.html",
    "/portfolio-of-igd/copy-of-hms": "/projects/opentv.html",
    "/portfolio-of-igd/copy-of-surfware": "/projects/spirent.html",
}


def brand_and_fix_links(html: str, from_file: Path) -> str:
    for old, new in BRANDING:
        html = html.replace(old, new)
    html = re.sub(r"This website was built on Wix\.[^<]{0,200}</a>", "", html, flags=re.I)
    html = re.sub(r"Proudly created with Wix\.com", "", html, flags=re.I)
    html = re.sub(
        r"This site was designed with the \.com website builder\.[^<]*",
        "",
        html,
        flags=re.I,
    )
    # Longest slugs first so base URL isn't partially replaced
    for slug in sorted(SLUG_MAP, key=len, reverse=True):
        local = SLUG_MAP[slug]
        target = local.lstrip("/")
        good = os.path.relpath(SITE / target, from_file.parent).replace("\\", "/")
        html = html.replace(f"https://iguerranet3.wixsite.com{slug}", good)
    return html


SCROLL_SCRIPT = ROOT / "mirror_scroll.js"


def mirror_page(url: str, dest: Path) -> None:
    tmp = MIRROR / f"_tmp_{dest.name}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Capturing {url}")
    cmd = [
        "npx", "--yes", "single-file-cli",
        url, str(tmp),
        "--browser-wait-delay", "8000",
        "--browser-wait-end-delay", "3000",
        "--browser-height", "2400",
        "--browser-load-max-time", "180000",
        "--browser-capture-max-time", "180000",
        "--load-deferred-images-dispatch-scroll-event", "true",
        "--max-resource-size", "50",
        "--compress-content", "false",
    ]
    if SCROLL_SCRIPT.is_file():
        cmd.extend(["--browser-script", str(SCROLL_SCRIPT)])
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    html = brand_and_fix_links(tmp.read_text(encoding="utf-8", errors="replace"), dest)
    dest.write_text(html, encoding="utf-8")
    tmp.unlink(missing_ok=True)
    print(f"  -> {dest} ({dest.stat().st_size // 1024} KB)")


def run_post_steps():
  subprocess.run(["python3", str(SITE / "fix_images.py")], check=True)
  subprocess.run(["python3", str(SITE / "fix_links.py")], check=True)
  subprocess.run(["python3", str(SITE / "post_process.py")], check=True)


def main():
    MIRROR.mkdir(exist_ok=True)
    keep = {}
    if SITE.exists():
        for name in ("serve.py", "fix_links.py", "fix_images.py", "post_process.py"):
            p = SITE / name
            if p.is_file():
                keep[name] = p.read_text(encoding="utf-8")
        shutil.rmtree(SITE)
    SITE.mkdir()
    for name, content in keep.items():
        (SITE / name).write_text(content, encoding="utf-8")

    for url, rel in PAGES.items():
        mirror_page(url, SITE / rel)

    run_post_steps()
    print(f"\nDone: {len(PAGES)} pages in {SITE}")
    print("Serve with: cd site && python3 serve.py")


if __name__ == "__main__":
    main()
