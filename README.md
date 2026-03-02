# Low-Resource Language Data Catalog

A static data catalog for Malawian low-resource language datasets, built for researchers fine-tuning LLMs and training ASR models. Part of the Gates Foundation–supported Development Data Partnership initiative to unlock proprietary content through ethical licensing.

**Live site:** Hosted on GitHub Pages.

## Repository structure

```
├── index.html          # Main catalog page (auto-updated by build.py)
├── main.css            # All styles
├── providers.csv       # Data provider registry (editable)
├── collections.csv     # Dataset collection registry (editable)
├── build.py            # Build script — reads CSVs, updates index.html
└── README.md
```

## How it works

The catalog is a single-page static site. All data lives in two CSV files. A Python build script reads the CSVs and injects them as JavaScript arrays into `index.html`, which handles filtering, rendering, and navigation entirely client-side. No server, no database, no build toolchain beyond Python 3.

## Updating the catalog

### 1. Edit the CSVs

**`providers.csv`** — one row per data provider:

| Column | Description |
|---|---|
| `id` | Unique slug (e.g., `radio_islam`, `mbc`) |
| `name` | Display name |
| `type` | Organization type (e.g., "Broadcaster — Radio") |
| `description` | One-paragraph description |

**`collections.csv`** — one row per dataset collection:

| Column | Description |
|---|---|
| `id` | Unique slug |
| `name` | Collection display name |
| `provider` | Must match a provider `id` |
| `language` | Language code: `chichewa`, `tumbuka`, `yao`, `lomwe`, `sena`, `english` |
| `type` | Media type: `radio`, `news`, `books`, `surveys` |
| `format` | MIME type (e.g., `audio/wav`, `text/html`, `text/pdf`) |
| `hours` | Total audio hours (leave blank for text collections) |
| `items` | Item count (leave blank for audio collections) |
| `description` | One-line description |
| `year_start` | Coverage start year |
| `year_end` | Coverage end year |
| `themes` | Semicolon-separated, up to 3 (e.g., `health;education;governance`) |

### 2. Run the build

```bash
python build.py
```

This replaces the `PROVIDERS` and `COLLECTIONS` JavaScript arrays inside `index.html` and updates the hero statistics (provider count, collection count, media types, languages). The build is idempotent — running it again with the same CSVs produces the same output.

### 3. Deploy

Commit and push. GitHub Pages serves the updated site automatically.

```bash
git add -A
git commit -m "Update catalog data"
git push
```

## Site sections

| Tab | Content |
|---|---|
| **Browse Collections** | Filterable card grid (language, media type, provider, theme, free-text search) |
| **Data Providers** | Each provider's description and collection table |
| **License** | Full text of the Development Data Partnership Clickthrough Sublicense Agreement |
| **API Reference** | Endpoint documentation, query parameters, example requests, Python SDK |
| **About** | Project overview, data types, access info, ethics, and application form |

## CSV editing tips

- Edit in any spreadsheet app (Excel, Google Sheets, LibreOffice) or a text editor.
- Description fields containing commas must be quoted — spreadsheet apps handle this automatically on export.
- The `provider` column in `collections.csv` must match an `id` in `providers.csv`, otherwise the card will show the raw slug instead of the provider name.
- The `themes` column uses semicolons as separators (not commas) to avoid CSV quoting issues.
- New languages or themes are automatically picked up by the filter dropdowns — no code changes needed.

## Requirements

- Python 3.6+ (standard library only — no pip dependencies)
- Any static hosting (GitHub Pages, Netlify, S3, etc.)

## License

All datasets are governed by the Development Data Partnership Clickthrough Sublicense Agreement. See the License tab on the site for full terms.
