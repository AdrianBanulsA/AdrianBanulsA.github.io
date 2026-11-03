# Web personal y QR de pósteres

Web hecha con [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), publicada en
https://adrianbanulsa.github.io/ con GitHub Actions.

## Añadir el QR de un póster

1. Edita `posters.yml` y añade una entrada con `slug` y `doi` (o `url`).
2. Guarda los cambios (commit). En un par de minutos la web se actualiza sola.
3. Descarga el QR desde https://adrianbanulsa.github.io/qr/

Cada QR abre `https://adrianbanulsa.github.io/qr/<slug>/`, que cuenta el escaneo
en GoatCounter y redirige al paper. **No cambies ni borres un slug ya impreso.**

## Archivos importantes

- `posters.yml`: los QR de los pósteres.
- `mkdocs.yml`: nombre de la web, menú, enlaces y código de GoatCounter.
- `docs/`: el contenido de la web en Markdown (`index.md`, `publications.md`).
- `assets/logo.png`: logo opcional para el centro de los QR.
- `docs/qr/`: se genera automáticamente; no pongas nada ahí a mano.
