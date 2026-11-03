# adrianbanulsa.github.io

Source for my personal website, <https://adrianbanulsa.github.io/>, built with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and deployed
with GitHub Actions on every push to `main`.

It also hosts the QR codes I put on conference posters. Each code points to
`/qr/<slug>/`, which logs the scan in [GoatCounter](https://www.goatcounter.com/)
and then redirects to the paper.

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

## Local preview

```bash
pip install -r requirements.txt
python scripts/build_qr.py
mkdocs serve
```
