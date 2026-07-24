#!/usr/bin/env python3
"""Mirror Wix portfolio site: download all pages + assets, apply KG branding."""

from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests
from playwright.sync_api import sync_playwright

BASE_URL = "https://iguerranet3.wixsite.com/portfolio-of-igd"
OUT = Path(__file__).parent
ASSETS = OUT / "assets" / "wix"
PAGES_DIR = OUT

# Wix slug -> local filename
PAGES = {
    "/": "index.html",
    "/blank-1": "about.html",
    "/blank-4": "services.html",
    "/s-projects-basic": "samples.html",
    "/general-9": "projects/google.html",
    "/copy-of-google": "projects/directv.html",
    "/copy-of-directv": "projects/jakeknows.html",
    "/copy-of-jakeknows": "projects/disney.html",
    "/copy-of-motorola": "projects/electrosonic.html",
    "/copy-of-opentv": "projects/voltdelta.html",
    "/copy-of-disney": "projects/vmware.html",
    "/copy-of-electrosonic": "projects/hms.html",
    "/copy-of-voltdelta": "projects/surfware.html",
    "/copy-of-vmware": "projects/motorola.html",
    "/copy-of-hms": "projects/opentv.html",
    "/copy-of-surfware": "projects/spirent.html",
}

BRANDING_REPLACEMENTS = [
    ("Ismael Guerra Dominguez", "Kevin Alexander Guerra"),
    ("Portfolio of Ismael Guerra", "Portfolio of Kevin Alexander Guerra"),
    ("Ismael Guerra", "Kevin Alexander Guerra"),
    ("Hello, my name is Ismael,", "Hello, my name is Kevin,"),
    ("my name is Ismael", "my name is Kevin"),
    ("IGD PORTFOLIO", "KG PORTFOLIO"),
    ("IGD Portfolio", "KG PORTFOLIO"),
    ("IGD", "KG"),
    ("Ismael", "Kevin"),
    ("Proudly created with Wix.com", ""),
    ("This site was designed with the .com website builder. Create your website today.Start Now", ""),
]

URL_PATTERN = re.compile(
    r"https://(?:static\.wixstatic\.com|[^\"'\s>]+\.wixsite\.com)[^\"'\s>)]+",
    re.I,
)


def asset_local_name(url: str) -> str:
    path = urlparse(url).path
    base = unquote(path.split("/")[-1] or "asset")
    if not base or base == "/":
        base = hashlib.md5(url.encode()).hexdigest()[:12]
    base = re.sub(r"[^\w.\-]", "_", base)
    if "." not in base:
        base += ".bin"
    return base


def download_asset(url: str, cache: dict[str, str]) -> str:
    if url in cache:
        return cache[url]
    name = asset_local_name(url)
    dest = ASSETS / name
    # dedupe by media id
    media_id = re.search(r"/media/([^/]+)", url)
    if media_id:
        for existing, local in cache.items():
            if media_id.group(1) in existing:
                cache[url] = local
                return local
    if not dest.exists():
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            dest.write_bytes(r.content)
        except Exception as e:
            print(f"  WARN download failed: {url[:80]}... ({e})")
            cache[url] = url
            return url
    rel = f"assets/wix/{name}"
    cache[url] = rel
    return rel


def rewrite_html(html: str, cache: dict[str, str], depth: int) -> str:
    prefix = "../" * depth

    def sub_url(m: re.Match) -> str:
        url = m.group(0).rstrip("\\")
        if "wixsite.com" in url and "/portfolio-of-igd" in url:
            slug = url.split("/portfolio-of-igd", 1)[-1].split("?")[0] or "/"
            local = PAGES.get(slug)
            if local:
                return prefix + local
        if "wixstatic.com" in url or "parastorage.com" in url:
            return prefix + download_asset(url, cache)
        return url

    html = URL_PATTERN.sub(sub_url, html)

    for old, new in BRANDING_REPLACEMENTS:
        html = html.replace(old, new)

    # Remove Wix freemium banner
    html = re.sub(
        r'<div[^>]*data-hook="freemium-banner"[^>]*>.*?</div>',
        "",
        html,
        flags=re.S | re.I,
    )
    html = re.sub(
        r'This website was built on Wix\.[^<]*</a>',
        "",
        html,
        flags=re.I,
    )

    # Strip Wix scripts that break offline viewing
    html = re.sub(r"<script[^>]*src=\"[^\"]*parastorage[^\"]*\"[^>]*></script>", "", html, flags=re.I)
    html = re.sub(r"<script[^>]*src=\"[^\"]*wixstatic[^\"]*\"[^>]*></script>", "", html, flags=re.I)

    return html


def collect_urls_from_page(page) -> set[str]:
    urls = page.evaluate(
        """() => {
        const out = new Set();
        document.querySelectorAll('img[src], source[srcset], link[href]').forEach(el => {
          const s = el.src || el.href || '';
          if (s) out.add(s);
          const ss = el.srcset || '';
          ss.split(',').forEach(p => { const u = p.trim().split(' ')[0]; if (u) out.add(u); });
        });
        document.querySelectorAll('*').forEach(el => {
          const bg = getComputedStyle(el).backgroundImage;
          if (bg && bg !== 'none') {
            const m = bg.match(/url\\(["']?([^"')]+)["']?\\)/);
            if (m) out.add(m[1]);
          }
        });
        return [...out];
    }"""
    )
    return {u for u in urls if "wixstatic" in u or "parastorage" in u}


def main():
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    ASSETS.mkdir(parents=True)
    (OUT / "projects").mkdir(exist_ok=True)

    cache: dict[str, str] = {}
    all_asset_urls: set[str] = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        for slug, local_name in PAGES.items():
            url = BASE_URL + ("" if slug == "/" else slug)
            print(f"Loading {url} -> {local_name}")
            page.goto(url, wait_until="networkidle", timeout=120000)
            page.wait_for_timeout(2000)
            all_asset_urls |= collect_urls_from_page(page)
            html = page.content()
            depth = local_name.count("/")
            html = rewrite_html(html, cache, depth)
            out_path = OUT / local_name
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding="utf-8")

        browser.close()

    # Second pass: download any URLs found in saved HTML
    for html_file in OUT.rglob("*.html"):
        for m in URL_PATTERN.finditer(html_file.read_text(encoding="utf-8", errors="ignore")):
            u = m.group(0)
            if "wixstatic" in u:
                all_asset_urls.add(u)

    print(f"Downloading {len(all_asset_urls)} asset URLs...")
    for u in sorted(all_asset_urls):
        download_asset(u, cache)

    print(f"Done. {len(cache)} assets, {len(PAGES)} pages -> {OUT}")


if __name__ == "__main__":
    main()
