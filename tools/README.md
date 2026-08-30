# Asset tools

One-off scripts for preparing images. **None of these run during deploy** — see
"Why not in CI" below. Their output is committed, so a normal deploy just serves
files that are already in the repo.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r tools/requirements.txt
python -m playwright install chromium   # only needed for make_og_card.py
```

## The scripts

| Script | Run it when | Output |
|---|---|---|
| `optimize_images.py` | After adding any cover or logo | Resizes/compresses in place |
| `make_og_card.py` | The featured book changes | `images/og-sunwoven-ascent.jpg` |
| `prep_retailer_logos.py` | A bookshop rebrands, or badges get resized | `images/retailers/*.png` |
| `prep_author_photo.py` | The author photo changes | `images/haley-headshot.jpg` |

### optimize_images.py

Covers arrive as print-resolution exports (3165px) but never render wider than
~400 CSS px. This resizes them to 1200px — 3x retina for the hero, still large
enough for search rich-result imagery — and strips metadata.

Safe to re-run: anything already at or below target width is skipped, because
JPEG is lossy and repeated re-encoding would degrade the artwork.

> If you change `COVER_WIDTH`, update the matching schema.org `ImageObject`
> width/height in `index.html`. Otherwise the structured data describes
> dimensions the file no longer has.

### make_og_card.py

Book covers are tall portraits; social platforms crop link previews to roughly
2:1 and would slice the middle out of one. This composes the cover into a proper
1200x630 landscape card. It also keeps the file under Twitter's 5 MB limit,
which a raw cover exceeds on its own.

Renders through headless Chromium so the card uses the site's own webfonts.
Needs network access for Google Fonts. Edit the constants near the top to
feature a different book; if you change the output filename, update `og:image`
and `twitter:image` in `index.html`.

### prep_retailer_logos.py

Trims each bookshop's wordmark, makes the background transparent, and normalizes
heights so the badges sit evenly in a row.

Originals are committed in `logo-sources/` rather than re-downloaded — they came
from Squarespace/Wix/Shopify CDNs whose hashed URLs will eventually rot. The
original source URLs are recorded in the script.

Run `optimize_images.py` afterwards to scale the badges to their final size.

### prep_author_photo.py

Crops and compresses the author headshot. The source is a landscape
environmental portrait, so a centre-crop lands on the subject's shoulder --
the crop boxes are chosen against the face position instead.

The About photo is styled `border-radius: 50%`, so the visible area is the
inscribed circle: a square crop renders a true circle, while a non-square one
renders an ellipse. Two variants are defined; `--all` writes both for
comparison without touching the live file.

This emits a final optimized JPEG, so `optimize_images.py` deliberately skips
it -- a second lossy pass would only degrade it.

## Why not in CI

These look like build steps but shouldn't be:

- **`optimize_images.py`** re-encodes lossy JPEGs. Running it every deploy would
  compound generation loss on the covers. The width guard makes re-runs safe,
  but there's still nothing to gain from running it automatically.
- **`make_og_card.py`** would add a ~130 MB Chromium download to every deploy,
  plus a Google Fonts dependency, to regenerate a card that changes maybe twice
  a year.
- **`prep_retailer_logos.py`** has no reason to run unless a shop rebrands.

The deploy workflow's job is to inject the GA4 ID and publish. Keeping asset
prep manual means a broken CDN or a font timeout can never block a release.
