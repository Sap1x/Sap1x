# Saptarshi Mondal GitHub Profile — Setup

## 1. Create the profile repository
Create a **public** repository named exactly `Sap1x`. GitHub displays the repository README as the profile README when the repository name matches the username and contains a non-empty `README.md`.

## 2. Local regeneration
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/render_stats_svg.py
```

## 3. GitHub Actions
The included workflow refreshes `data/contributions.json`, `contrib-heatmap.svg`, and `stats.svg` daily, on pushes to `main`, and via manual dispatch.

GitHub contribution data is the source of truth; GitHub documents that qualifying contributions include activity such as commits, issues, pull requests, reviews, and discussions under its contribution rules.

## 4. Photo
Replace `assets/saptarshi-source.jpg` and rerun `prep_photo.py` + `make_ascii_svg.py` whenever the portrait changes.
