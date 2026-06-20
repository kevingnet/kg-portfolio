# KG Portfolio

Static portfolio site for **Kevin Alexander Guerra** — generated from `build_site.py`.

Live site (after GitHub Pages is enabled): **https://kevingnet.github.io/kg-portfolio/**

## Build

Edit content in `build_site.py`, then regenerate HTML:

```bash
cd ~/Jobs/kg-portfolio
python3 build_site.py
```

Resume PDF is copied from `~/Jobs/Kevin Guerra.pdf` into `assets/Kevin-Guerra.pdf` on each build.

Override the public URL (for Open Graph / canonical links):

```bash
SITE_BASE_URL=https://your-domain.com python3 build_site.py
```

## Preview locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080/

## Deploy to GitHub Pages

1. Create a repo on GitHub named `kg-portfolio` (user: `kevingnet`).
2. Push this directory:

```bash
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin git@github.com:kevingnet/kg-portfolio.git
git push -u origin main
```

3. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Pushes to `main` run `.github/workflows/pages.yml`, which runs `build_site.py` and publishes the site root.

## Project layout

| Path | Purpose |
|------|---------|
| `build_site.py` | Source of truth — nav, copy, project pages |
| `index.html`, `about.html`, … | Generated pages (commit after build) |
| `projects/` | Employer project detail pages |
| `css/style.css` | Styles |
| `js/carousel.js` | Logo carousel |
| `assets/` | Images, favicon, resume PDF |

The `site/` and `mirrored/` folders are legacy Wix mirrors and are not deployed.
