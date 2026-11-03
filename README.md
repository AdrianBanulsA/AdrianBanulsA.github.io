# adrianbanulsa.github.io

Source for my personal website, <https://adrianbanulsa.github.io/>, built with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and deployed
with GitHub Actions on every push to `main`.

It also hosts the QR codes I put on conference posters. Each code points to
`/qr/<slug>/`, which logs the scan in [GoatCounter](https://www.goatcounter.com/)
and then redirects to the paper.

## Poster scans

<!-- scans:start -->
| Paper | Scans |
|---|---:|
| [Asynchronous deployment of RL software on physical systems (JA 2026)](https://doi.org/10.17979/ja-cea.2026.47.13751) | 1 |
| [Analysis of the timestep in RL for mobile robots (JA 2026)](https://doi.org/10.17979/ja-cea.2026.47.13780) | 0 |
| [Time-aware mobile robot navigation with Subjective Time Maps (CMES 2026)](https://doi.org/10.32604/cmes.2026.085976) | 2 |
<!-- scans:end -->

Unique visitors according to GoatCounter, updated every 6 hours by
`scripts/update_scans.py`.

## Adding a poster QR

1. Add an entry with a `slug` and a `doi` (or `url`) to `posters.yml`.
2. Push. The site rebuilds in a couple of minutes.
3. Download the SVG from <https://adrianbanulsa.github.io/qr/>.

Don't rename or remove a slug once the poster has been printed.

## Layout

- `posters.yml` – poster QR codes
- `mkdocs.yml` – site config, navigation, links and GoatCounter code
- `docs/` – page content (Markdown)
- `assets/logo.png` – optional logo placed in the centre of the QR codes
- `scripts/build_qr.py` – generates `docs/qr/` at build time (not tracked)
- `scripts/update_scans.py` – fills in the scans table above

## Local preview

```bash
pip install -r requirements.txt
python scripts/build_qr.py
mkdocs serve
```
