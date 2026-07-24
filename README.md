# KG Portfolio — Full Career (local only)

Static HTML portfolio for **Kevin Alexander Guerra**. Generated from `build_site.py` and indexed from the Development archive on disk.

**This is a local site.** Open it directly in your browser — no web server, no GitHub Pages.

## Open the site

```bash
xdg-open ~/Jobs/kg-portfolio-full/index.html
```

Or in your file manager: navigate to `~/Jobs/kg-portfolio-full/` and double-click `index.html`.

All links, CSS, and assets use **relative paths** so `file://` works.

## Rebuild after edits

```bash
cd ~/Jobs/kg-portfolio-full
python3 build_site.py
```

This will:

1. Parse `data/portfolio-compilation.md` → `data/portfolio-compilation.json` (exhaustive archive analysis per employer)
2. Scan `/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development` → `data/development-inventory.json`
3. Regenerate HTML pages with **Development archive analysis** (from compilation) plus file index sections
4. Copy resume PDF from `~/Jobs/Kevin Guerra.pdf` if present
5. Build header carousel (oldest→newest from `data/carousel-chronology.json`; resume overrides Development folder order)

Archive folder names are shown **without** numeric prefixes (e.g. `Disney` not `03 Disney`).

**Carousel:** logos scroll left-to-right from earliest role (LCS, 1992) to current (MAF RODA). Each logo links to `projects/{slug}.html`. Order is defined in `data/carousel-chronology.json` from your resume + Experience History; Development folder numbers are tiebreakers only. `python3 build_site.py` prints any order conflicts where resume wins.

## Source archive

| Path | Role |
|------|------|
| `build_site.py` | Page copy, employer cards, project detail |
| `tools/import_compilation.py` | Parses `data/portfolio-compilation.md` into per-slug JSON |
| `data/portfolio-compilation.md` | Full Development archive compilation (source of truth for project analysis) |
| `data/portfolio-compilation.json` | Structured compilation content for site generation |
| `data/carousel-chronology.json` | Carousel logo order (resume-first) and documented Dev-folder discrepancies |
| `tools/extract_development.py` | Indexes `.sln`/`.dsp`/`.dsw`, web-app folders, `.mdb` from Development tree |
| `data/development-inventory.json` | Machine-readable index (regenerated each build) |
| `projects/` | Generated employer detail pages |
| `experience-history.html` | Full pre-2015 timeline supplement |

Development root (must be mounted/readable):

`/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development`

## Project layout

| Path | Purpose |
|------|---------|
| `index.html` | Portfolio grid (22 employers) |
| `about.html` | Bio, skills, timeline |
| `experience-history.html` | Detailed history from Generic Resume + later roles |
| `css/style.css` | Dark theme |
| `assets/images/` | Logos and photos |

Legacy folders `site/` and `mirrored/` are old Wix mirrors — not part of this site.
