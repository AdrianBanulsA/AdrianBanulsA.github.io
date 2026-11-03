# adrianbanulsa.github.io

Source for my personal website, <https://adrianbanulsa.github.io/>, built with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and deployed
with GitHub Actions on every push to `main`.

It also hosts the QR codes I put on conference posters. Each code points to
`/qr/<slug>/`, which logs the scan in [GoatCounter](https://www.goatcounter.com/)
and then redirects to the paper.

## Poster scans

| Paper | Venue | Scans |
|---|---|---|
| [Time-aware navigation with Subjective Time Maps](https://doi.org/10.32604/cmes.2026.085976) | CMES 2026 | ![scans](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadrianbanuls.goatcounter.com%2Fcounter%2F%252Fqr%252Fstm-cmes26%252F.json&query=%24.count&label=scans&color=1f4a5a&cacheSeconds=3600) |
| [Asynchronous deployment of RL software on physical systems](https://doi.org/10.17979/ja-cea.2026.47.13751) | JA 2026 | ![scans](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadrianbanuls.goatcounter.com%2Fcounter%2F%252Fqr%252Fspindecoupler-ja26%252F.json&query=%24.count&label=scans&color=1f4a5a&cacheSeconds=3600) |
| [Timestep in RL for mobile robots](https://doi.org/10.17979/ja-cea.2026.47.13780) | JA 2026 | ![scans](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fadrianbanuls.goatcounter.com%2Fcounter%2F%252Fqr%252Ftimestep-ja26%252F.json&query=%24.count&label=scans&color=1f4a5a&cacheSeconds=3600) |

Unique visitors according to GoatCounter. Counts can lag a few hours.

## Adding a poster QR

1. Add an entry with a `slug` and a `doi` (or `url`) to `posters.yml`.
2. Push. The site rebuilds in a couple of minutes.
3. Download the SVG from <https://adrianbanulsa.github.io/qr/>.
4. Add a row to the scans table above (copy one and change the slug).

Don't rename or remove a slug once the poster has been printed.

## Layout

- `posters.yml` – poster QR codes
- `mkdocs.yml` – site config, navigation, links and GoatCounter code
- `docs/` – page content (Markdown)
- `assets/logo.png` – optional logo placed in the centre of the QR codes
- `scripts/build_qr.py` – generates `docs/qr/` at build time (not tracked)

## Local preview

```bash
pip install -r requirements.txt
python scripts/build_qr.py
mkdocs serve
```
