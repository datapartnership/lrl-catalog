#!/usr/bin/env python3
"""
build.py — Reads providers.csv and collections.csv, then updates the
PROVIDERS and COLLECTIONS arrays inside index.html.

Usage:
    python build.py

Expects providers.csv, collections.csv, and index.html in the same directory.
"""

import csv
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROVIDERS_CSV = SCRIPT_DIR / "providers.csv"
COLLECTIONS_CSV = SCRIPT_DIR / "collections.csv"
INDEX_HTML = SCRIPT_DIR / "index.html"


def read_providers(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "id": row["id"].strip(),
                "name": row["name"].strip(),
                "type": row["type"].strip(),
                "description": row["description"].strip(),
            })
    return rows


def read_collections(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            hours_raw = row["hours"].strip()
            items_raw = row["items"].strip()
            rows.append({
                "id": row["id"].strip(),
                "name": row["name"].strip(),
                "provider": row["provider"].strip(),
                "language": row["language"].strip(),
                "type": row["type"].strip(),
                "format": row["format"].strip(),
                "hours": int(hours_raw) if hours_raw else None,
                "items": int(items_raw) if items_raw else None,
                "description": row["description"].strip(),
                "yearStart": int(row["year_start"].strip()),
                "yearEnd": int(row["year_end"].strip()),
                "themes": [t.strip() for t in row["themes"].strip().split(";") if t.strip()],
            })
    return rows


def to_js_array(name, data, indent=0):
    """Convert a Python list of dicts to a JS const declaration."""
    prefix = " " * indent
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    # Convert null to JS null (json.dumps already does this)
    return f"const {name} = {json_str};"


def inject_into_html(html, providers_js, collections_js):
    """Replace the PROVIDERS and COLLECTIONS arrays in the HTML."""
    # Match from "const PROVIDERS = [" through "];"
    html = re.sub(
        r"const PROVIDERS = \[.*?\];",
        providers_js,
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"const COLLECTIONS = \[.*?\];",
        collections_js,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def main():
    for path in (PROVIDERS_CSV, COLLECTIONS_CSV, INDEX_HTML):
        if not path.exists():
            print(f"Error: {path} not found.", file=sys.stderr)
            sys.exit(1)

    providers = read_providers(PROVIDERS_CSV)
    collections = read_collections(COLLECTIONS_CSV)

    print(f"Read {len(providers)} providers, {len(collections)} collections.")

    providers_js = to_js_array("PROVIDERS", providers)
    collections_js = to_js_array("COLLECTIONS", collections)

    html = INDEX_HTML.read_text(encoding="utf-8")
    updated = inject_into_html(html, providers_js, collections_js)

    INDEX_HTML.write_text(updated, encoding="utf-8")
    print(f"Updated {INDEX_HTML}")

    # Update hero stats
    languages = set(c["language"] for c in collections)
    types = set(c["type"] for c in collections)

    stats = {
        "providers": len(providers),
        "collections": len(collections),
        "media_types": len(types),
        "languages": len(languages),
    }

    for label, count in stats.items():
        html_label = {
            "providers": "Data Providers",
            "collections": "Collections",
            "media_types": "Media Types",
            "languages": "Languages",
        }[label]
        updated = re.sub(
            rf'(<div class="num">)\d+(</div>\s*<div class="label">{html_label})',
            rf"\g<1>{count}\2",
            updated,
        )

    INDEX_HTML.write_text(updated, encoding="utf-8")
    print(f"Hero stats updated: {stats}")


if __name__ == "__main__":
    main()
