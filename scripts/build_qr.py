#!/usr/bin/env python3
"""
Build the poster QR codes from posters.yml.

For each poster it writes docs/qr/<slug>/ with:
  index.html  redirect page that logs the scan in GoatCounter
  qr.png      QR code for quick use
  qr.svg      QR code for printing

plus docs/qr/index.html listing all of them. docs/qr/ is wiped on every run.
"""

import base64
import html
import io
import json
import re
import shutil
import sys
from pathlib import Path

import qrcode
import qrcode.image.svg
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "qr"
LOGO = ROOT / "assets" / "logo.png"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOGO_FRACTION = 0.22  # logo width relative to the QR; keep below ~0.25
PNG_TARGET_PX = 1400


def fail(msg):
    print(f"posters.yml: {msg}", file=sys.stderr)
    sys.exit(1)


class _TolerantLoader(yaml.SafeLoader):
    """SafeLoader that ignores the !!python/ tags MkDocs allows in mkdocs.yml."""


_TolerantLoader.add_multi_constructor("tag:yaml.org,2002:python/", lambda *a: None)


def load_config():
    mk = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_TolerantLoader)
    site_url = (mk.get("site_url") or "").rstrip("/")
    if not site_url.startswith("http"):
        print("mkdocs.yml: site_url is missing", file=sys.stderr)
        sys.exit(1)
    goatcounter = ((mk.get("extra") or {}).get("goatcounter") or "").strip()
    return site_url, goatcounter


def load_posters():
    data = yaml.safe_load((ROOT / "posters.yml").read_text(encoding="utf-8")) or {}
    posters = data.get("posters") or []
    seen = set()
    result = []
    for i, p in enumerate(posters, start=1):
        if not isinstance(p, dict):
            fail(f"entry {i} is malformed")
        slug = str(p.get("slug", "")).strip()
        if not SLUG_RE.match(slug):
            fail(f"invalid slug '{slug}' (entry {i}): use lowercase letters, digits and hyphens")
        if slug in seen:
            fail(f"duplicate slug '{slug}'")
        seen.add(slug)

        doi, url = p.get("doi"), p.get("url")
        if bool(doi) == bool(url):
            fail(f"'{slug}' needs exactly one of doi or url")
        if doi:
            doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", str(doi).strip(), flags=re.I)
            target = f"https://doi.org/{doi}"
        else:
            target = str(url).strip()
            if not target.startswith(("https://", "http://")):
                fail(f"url for '{slug}' must start with https://")
        result.append({"slug": slug, "target": target, "title": str(p.get("title") or slug)})
    return result


def redirect_page(slug, target, goatcounter):
    t_attr = html.escape(target, quote=True)
    t_js = json.dumps(target)
    if goatcounter:
        counter = (
            f'<script data-goatcounter="https://{html.escape(goatcounter)}.goatcounter.com/count"\n'
            "        data-goatcounter-settings='{\"no_onload\": true}'\n"
            '        async src="https://gc.zgo.at/count.js"\n'
            '        onload="track()" onerror="go()"></script>'
        )
    else:
        counter = "<script>go();</script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Opening paper…</title>
<link rel="canonical" href="{t_attr}">
<noscript><meta http-equiv="refresh" content="0; url={t_attr}"></noscript>
<style>
  body {{ font-family: system-ui, sans-serif; display: grid; place-items: center;
         min-height: 90vh; margin: 0; color: #1f4a5a; }}
  a {{ color: inherit; }}
</style>
</head>
<body>
<p>Opening the paper… If nothing happens, <a href="{t_attr}">click here</a>.</p>
<script>
  var TARGET = {t_js};
  var done = false;
  function go() {{ if (!done) {{ done = true; location.replace(TARGET); }} }}
  function track() {{
    try {{ window.goatcounter.count({{ path: "/qr/{slug}/", title: "QR {slug}" }}); }} catch (e) {{}}
    setTimeout(go, 500);
  }}
  setTimeout(go, 3000); // redirect anyway if analytics is slow or blocked
</script>
{counter}
</body>
</html>
"""


def make_qr(data, with_logo):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H if with_logo else qrcode.constants.ERROR_CORRECT_M,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def logo_with_padding(size_px):
    """Scaled logo on a white box, ready to paste in the centre of the QR."""
    pad = max(2, size_px // 10)
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((size_px - 2 * pad, size_px - 2 * pad), Image.LANCZOS)
    box = Image.new("RGBA", (logo.width + 2 * pad, logo.height + 2 * pad), "white")
    box.paste(logo, (pad, pad), logo)
    return box


def write_png(qr, path, with_logo):
    total_modules = qr.modules_count + 2 * qr.border
    qr.box_size = max(10, PNG_TARGET_PX // total_modules)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    if with_logo:
        box = logo_with_padding(int(img.width * LOGO_FRACTION))
        img.paste(box, ((img.width - box.width) // 2, (img.height - box.height) // 2), box)
    img.convert("RGB").save(path)


def write_svg(qr, path, with_logo):
    svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string(encoding="unicode")
    n = float(re.search(r'viewBox="0 0 ([\d.]+)', svg).group(1))
    head_end = svg.index(">") + 1
    background = f'<rect width="{n:g}" height="{n:g}" fill="#fff"/>'
    svg = svg[:head_end] + background + svg[head_end:]
    if with_logo:
        box = logo_with_padding(512)
        buf = io.BytesIO()
        box.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        w = n * LOGO_FRACTION * (box.width / max(box.width, box.height))
        h = n * LOGO_FRACTION * (box.height / max(box.width, box.height))
        x, y = (n - w) / 2, (n - h) / 2
        svg = svg.replace(
            "</svg>",
            f'<image x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" '
            f'href="data:image/png;base64,{b64}"/></svg>',
        )
    path.write_text(svg, encoding="utf-8")


def index_page(posters, site_url):
    rows = "\n".join(
        f"""  <li>
    <img src="{p['slug']}/qr.png" alt="QR code for {html.escape(p['title'])}" width="160" height="160">
    <div>
      <strong>{html.escape(p['title'])}</strong>
      <p>Opens <code>{html.escape(site_url)}/qr/{p['slug']}/</code><br>
         and redirects to <a href="{html.escape(p['target'], quote=True)}">{html.escape(p['target'])}</a></p>
      <p><a href="{p['slug']}/qr.svg" download="qr-{p['slug']}.svg">SVG (print)</a>
         <a href="{p['slug']}/qr.png" download="qr-{p['slug']}.png">PNG</a></p>
    </div>
  </li>"""
        for p in posters
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Poster QR codes</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem;
         color: #1a2a30; line-height: 1.5; }}
  h1 {{ color: #1f4a5a; font-weight: 600; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ display: flex; gap: 1.25rem; align-items: flex-start; padding: 1rem 0;
       border-bottom: 1px solid #d5dee1; flex-wrap: wrap; }}
  img {{ border: 1px solid #d5dee1; }}
  p {{ margin: .3rem 0; }}
  a {{ color: #1f5f75; margin-right: 1rem; }}
  code {{ background: #eef3f4; padding: 0 .3em; }}
</style>
</head>
<body>
<h1>Poster QR codes</h1>
<p>Scans show up in GoatCounter under <code>/qr/…/</code>.</p>
<ul>
{rows}
</ul>
</body>
</html>
"""


def main():
    site_url, goatcounter = load_config()
    posters = load_posters()
    with_logo = LOGO.exists()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for p in posters:
        d = OUT / p["slug"]
        d.mkdir()
        (d / "index.html").write_text(redirect_page(p["slug"], p["target"], goatcounter), encoding="utf-8")
        qr = make_qr(f"{site_url}/qr/{p['slug']}/", with_logo)
        write_png(qr, d / "qr.png", with_logo)
        write_svg(qr, d / "qr.svg", with_logo)
        print(f"/qr/{p['slug']}/ -> {p['target']}")

    (OUT / "index.html").write_text(index_page(posters, site_url), encoding="utf-8")
    print(f"{len(posters)} QR codes written" + (" (with logo)" if with_logo else ""))
    if not goatcounter:
        print("warning: extra.goatcounter is empty in mkdocs.yml, scans will not be counted")


if __name__ == "__main__":
    main()
