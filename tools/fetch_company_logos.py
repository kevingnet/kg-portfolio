#!/usr/bin/env python3
"""Download company logos from LinkedIn og:image (and local assets) for portfolio."""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "images"
DEV = Path("/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development")
DEV_MNT = Path("/mnt/data/all/Development")

# slug -> (direct image URL, linkedin page URL, optional local source path)
# Direct CDN URLs captured from LinkedIn og:image when page fetch works.
COMPANIES: dict[str, tuple[str | None, str | None, Path | None]] = {
    "frys": (
        "https://media.licdn.com/dms/image/v2/C560BAQGx1nIFjZ1ixw/company-logo_200_200/company-logo_200_200/0/1631329936430?e=2147483647&v=beta&t=placeholder",
        "https://www.linkedin.com/company/fry's-electronics",
        None,
    ),
    "access": (
        "https://media.licdn.com/dms/image/v2/C4E0BAQEf2nYBam0FbQ/company-logo_200_200/company-logo_200_200/0/1631332403977?e=2147483647&v=beta&t=placeholder",
        "https://www.linkedin.com/company/access-corporation",
        None,
    ),
    "posdev": (None, None, None),
    "audiotelco": (None, None, DEV / "10 TelVista" / "Telvista.bmp"),
    "woodtech": (None, "https://www.linkedin.com/company/wood-technologies", None),
    "bumpershop": (None, "https://www.linkedin.com/company/bumper-shop", None),
    "labumpers": (None, None, DEV / "06 LaBumpers" / "logo la bumpers.jpg"),
    "fotografia": (None, None, DEV_MNT / "08 FotografiaBlancarte" / "TODO" / "pic" / "logoblancarte2.jpg"),
    "plastering": (None, None, None),
    "lcs": (None, None, None),
}

UA = {"User-Agent": "Mozilla/5.0 (compatible; KG-Portfolio/1.0)"}
GENERIC_LI = "https://static.licdn.com/aero-v1/sc/h/cs8pjfgyw96g44ln9r7tct85f"


def linkedin_og_image(company_url: str) -> str | None:
    req = urllib.request.Request(company_url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read(120_000).decode("utf-8", "replace")
    m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    if not m:
        m = re.search(r'content="([^"]+)"\s+property="og:image"', html)
    if not m:
        return None
    url = m.group(1)
    if url == GENERIC_LI:
        return None
    return url


def download(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if len(data) < 200:
        return False
    dest.write_bytes(data)
    return True


def access_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="ACCESS! Corporation">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="118" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#CC0000">Access!</text>
</svg>
"""


def write_access_wordmark() -> Path:
    path = IMG / "access.svg"
    path.write_text(access_wordmark_svg(), encoding="utf-8")
    return path


def bumpershop_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="The Bumper Shop">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="88" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="24" font-weight="900" fill="#003399">THE</text>
  <text x="100" y="122" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="24" font-weight="900" fill="#003399">BUMPER SHOP</text>
</svg>
"""


def write_bumpershop_wordmark() -> Path:
    path = IMG / "bumpershop.svg"
    path.write_text(bumpershop_wordmark_svg(), encoding="utf-8")
    return path


def lcs_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="LCS Logical Computer">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="98" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#5533cc">LCS</text>
  <text x="100" y="128" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="#5533cc">LOGICAL COMPUTER</text>
</svg>
"""


def plastering_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="California Plastering">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="88" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="20" font-weight="900" fill="#c9a227">CALIFORNIA</text>
  <text x="100" y="122" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="22" font-weight="900" fill="#c9a227">PLASTERING</text>
</svg>
"""


def woodtech_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Wood Technologies">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="88" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="24" font-weight="900" fill="#6b4f2a">WOOD</text>
  <text x="100" y="122" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="18" font-weight="900" fill="#6b4f2a">TECHNOLOGIES</text>
</svg>
"""


def posdev_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Positive Developments">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="88" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="20" font-weight="900" fill="#2d8a4e">POSITIVE</text>
  <text x="100" y="122" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="18" font-weight="900" fill="#2d8a4e">DEVELOPMENTS</text>
</svg>
"""


def frys_wordmark_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Fry's Electronics">
  <rect width="200" height="200" rx="12" fill="#ffffff"/>
  <text x="100" y="108" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="44" font-weight="700" font-style="italic" fill="#cc0000">Fry's</text>
</svg>
"""


def write_wordmark(slug: str, svg_text: str) -> Path:
    path = IMG / f"{slug}.svg"
    path.write_text(svg_text, encoding="utf-8")
    return path


def write_frys_logo() -> Path | None:
    url = "https://upload.wikimedia.org/wikipedia/commons/9/9e/Fry_s_Electronics.svg"
    dest = IMG / "frys.svg"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) >= 200:
            dest.write_bytes(data)
            return dest
    except Exception:
        pass
    return None


def letter_svg(slug: str, label: str, color: str = "#3d7cff") -> str:
    letter = label.strip()[:1].upper() or "?"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="{label}">
  <rect width="200" height="200" rx="24" fill="#161a22"/>
  <rect x="8" y="8" width="184" height="184" rx="18" fill="none" stroke="{color}" stroke-width="4"/>
  <text x="100" y="128" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="96" font-weight="700" fill="{color}">{letter}</text>
</svg>
"""


def write_placeholder(slug: str, label: str) -> Path:
    path = IMG / f"{slug}.svg"
    colors = {
        "posdev": "#5ec27a",
        "plastering": "#c9a227",
        "lcs": "#9b7bff",
        "audiotelco": "#4ec5f7",
    }
    path.write_text(letter_svg(slug, label, colors.get(slug, "#3d7cff")), encoding="utf-8")
    return path


def fit_logo_to_jpeg(src: Path, dest: Path, square: int = 100) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False
    logo = Image.open(src).convert("RGB")
    src_w, src_h = logo.size
    scale = min(square / src_w, square / src_h)
    new_w = max(1, round(src_w * scale))
    new_h = max(1, round(src_h * scale))
    logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (square, square), (255, 255, 255))
    canvas.paste(logo, ((square - new_w) // 2, (square - new_h) // 2))
    canvas.save(dest, "JPEG", quality=90, optimize=True)
    return True


def convert_bmp_to_jpeg(src: Path, dest: Path, square: int = 100) -> bool:
    return fit_logo_to_jpeg(src, dest, square)


def write_labumpers_logo() -> Path | None:
    local = DEV / "06 LaBumpers" / "logo la bumpers.jpg"
    dest = IMG / "labumpers.jpg"
    if local.is_file() and fit_logo_to_jpeg(local, dest):
        return dest
    return None


def write_fotografia_logo() -> Path | None:
    for local in (
        DEV_MNT / "08 FotografiaBlancarte" / "TODO" / "pic" / "logoblancarte2.jpg",
        DEV / "08 FotografiaBlancarte" / "TODO" / "pic" / "logoblancarte2.jpg",
    ):
        dest = IMG / "fotografia.jpg"
        if local.is_file() and fit_logo_to_jpeg(local, dest):
            return dest
    return None


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    labels = {
        "frys": "Fry's Electronics",
        "access": "ACCESS!",
        "posdev": "Positive Developments",
        "audiotelco": "Audio Telco",
        "woodtech": "Wood Technologies",
        "bumpershop": "The Bumper Shop",
        "labumpers": "La Bumpers",
        "fotografia": "Fotografia Blancarte",
        "plastering": "California Plastering",
        "lcs": "LCS",
    }
    for slug, (direct_url, li_page, local) in COMPANIES.items():
        if slug == "access":
            write_access_wordmark()
            print("access: wordmark svg (red Access! on white)")
            continue
        if slug == "bumpershop":
            write_bumpershop_wordmark()
            print("bumpershop: wordmark svg (blue THE BUMPER SHOP on white)")
            continue
        if slug == "lcs":
            write_wordmark(slug, lcs_wordmark_svg())
            print("lcs: wordmark svg")
            continue
        if slug == "plastering":
            write_wordmark(slug, plastering_wordmark_svg())
            print("plastering: wordmark svg")
            continue
        if slug == "woodtech":
            write_wordmark(slug, woodtech_wordmark_svg())
            print("woodtech: wordmark svg")
            continue
        if slug == "posdev":
            write_wordmark(slug, posdev_wordmark_svg())
            print("posdev: wordmark svg")
            continue
        if slug == "frys":
            if write_frys_logo():
                print("frys: wikimedia svg")
            else:
                write_wordmark(slug, frys_wordmark_svg())
                print("frys: wordmark svg (Fry's on white)")
            continue
        if slug == "labumpers":
            if write_labumpers_logo():
                print("labumpers: resized archive logo -> labumpers.jpg (100x100)")
            else:
                write_placeholder(slug, labels.get(slug, slug))
                print("labumpers: placeholder svg")
            continue
        if slug == "fotografia":
            if write_fotografia_logo():
                print("fotografia: resized logoblancarte2.jpg -> fotografia.jpg (100x100)")
            else:
                write_placeholder(slug, labels.get(slug, slug))
                print("fotografia: placeholder svg")
            continue
        jpeg = IMG / f"{slug}.jpeg"
        png = IMG / f"{slug}.png"
        svg = IMG / f"{slug}.svg"
        ok = False
        if direct_url:
            try:
                if download(direct_url, jpeg):
                    print(f"{slug}: cdn -> {jpeg.name}")
                    ok = True
            except Exception as exc:
                print(f"{slug}: cdn failed ({exc})")
        if not ok and li_page:
            try:
                og = linkedin_og_image(li_page)
                if og and download(og, jpeg):
                    print(f"{slug}: linkedin -> {jpeg.name}")
                    ok = True
            except Exception as exc:
                print(f"{slug}: linkedin failed ({exc})")
        if not ok and local and local.is_file():
            if local.suffix.lower() == ".bmp" and convert_bmp_to_jpeg(local, jpeg):
                print(f"{slug}: converted {local.name} -> {jpeg.name}")
                ok = True
            elif local.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                dest = jpeg if local.suffix.lower() in {".jpg", ".jpeg"} else png
                if fit_logo_to_jpeg(local, dest):
                    print(f"{slug}: resized {local.name} -> {dest.name}")
                    ok = True
        if not ok:
            existing = next(
                (p for p in (jpeg, png, svg, IMG / f"{slug}.jpg")
                 if p.is_file() and p.stat().st_size > 200),
                None,
            )
            if existing:
                print(f"{slug}: kept existing {existing.name}")
            else:
                write_placeholder(slug, labels.get(slug, slug))
                print(f"{slug}: placeholder svg")
    print("done")


if __name__ == "__main__":
    main()
