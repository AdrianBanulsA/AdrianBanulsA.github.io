#!/usr/bin/env python3
"""
Write the poster scan counts from GoatCounter into the table in README.md.

Needs "Allow adding visitor counts on your website" enabled in the GoatCounter
settings. Paths that have never been visited return 404 and are shown as 0.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

from build_qr import ROOT, load_config, load_posters

README = ROOT / "README.md"
START, END = "<!-- scans:start -->", "<!-- scans:end -->"


def scan_count(goatcounter, slug):
    url = f"https://{goatcounter}.goatcounter.com/counter/{quote(f'/qr/{slug}/', safe='')}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "adrianbanulsa.github.io"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)["count"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "0"
        raise


def main():
    _, goatcounter = load_config()
    if not goatcounter:
        sys.exit("mkdocs.yml: extra.goatcounter is empty")

    rows = ["| Paper | Scans |", "|---|---:|"]
    for p in load_posters():
        rows.append(f"| [{p['title']}]({p['target']}) | {scan_count(goatcounter, p['slug'])} |")
    table = "\n".join(rows)

    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        sys.exit(f"README.md: markers {START} / {END} not found")
    README.write_text(pattern.sub(lambda _: f"{START}\n{table}\n{END}", text), encoding="utf-8")
    print(table)


if __name__ == "__main__":
    main()
