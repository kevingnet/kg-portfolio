# Kevin Guerra Portfolio

Static portfolio site for **Kevin Alexander Guerra**, published with GitHub Pages at
<https://kevingnet.github.io/kg-portfolio/>. Every push to `main` redeploys it within a minute or two.

## Editing

The HTML pages are the source of truth: edit `index.html`, `case-studies.html`,
`projects/<employer>.html` and the rest directly. Styles are in `css/style.css`;
scripts in `js/`.

The header, nav, logo carousel and footer are the same on every page. Change them
in `build_site.py`, then run:

```bash
python3 build_site.py           # rewrite pages whose shared parts are out of date
python3 build_site.py --check   # list pages that would change (exit 1 if any)
```

It leaves page content alone. Run with `--check` before committing to confirm the
shared parts are in sync.

## Adding an employer to the carousel

1. Put the logo in `assets/images/`.
2. Add an entry to `LOGOS` in `build_site.py`.
3. Add its slug to `data/carousel-chronology.json` in date order (oldest first).
4. Create `projects/<slug>.html` (copy an existing project page).
5. Run `python3 build_site.py`.

## Layout

| Path | Purpose |
|------|---------|
| `index.html` | Home: hero, highlights, recommendations, experience grid |
| `case-studies.html` | Four case studies in depth |
| `projects/` | One page per employer |
| `resume.html`, `experience-history.html` | Resume and full pre-2015 history |
| `services.html`, `samples.html`, `about.html` | Other top-level pages |
| `assets/images/` | Logos, photos and screenshots (screenshots are WebP) |
| `assets/*.pdf` | Resume and experience-history PDFs |
| `data/` | Carousel order and archive data used by `tools/` |
| `tools/` | One-off scripts used to import archive material |
