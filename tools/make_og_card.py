#!/usr/bin/env python3
"""Render the 1200x630 Open Graph share card used by og:image / twitter:image.

Book covers are tall portraits; social platforms crop link previews to roughly
2:1, which slices the middle out of a cover. This composes the cover into a
proper landscape card instead. It also keeps the file small -- the raw cover
exceeds Twitter's 5 MB limit on its own.

Rendered through headless Chromium so the card uses the same webfonts as the
site (Playfair Display + Lato), then downsampled from 2x for crisp text.

    python3 tools/make_og_card.py

Requires network access for Google Fonts. Run when the featured book changes,
then update og:image / twitter:image in index.html if the OUT filename changes.
NOT a build step -- the output is committed.
"""
import base64
import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent

# --- what the card features -------------------------------------------------
COVER = REPO / "images" / "ASunwovenAscent-Ebook.jpg"
OUT = REPO / "images" / "og-sunwoven-ascent.jpg"
EYEBROW = "The Solwyn Duology &mdash; Book Two"
TITLE = "A Sunwoven Ascent"
AUTHOR = "by Haley M. Opet"
CALLOUT = "Available Now"
SUBLINE = "Signed paperback &amp; Kindle editions"
# ---------------------------------------------------------------------------

WIDTH, HEIGHT = 1200, 630
QUALITY = 90


def build_html(cover_data_uri: str) -> str:
    return f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    width:{WIDTH}px; height:{HEIGHT}px; display:flex; align-items:center; gap:58px;
    padding:60px 70px;
    background:
      radial-gradient(circle at 78% 30%, rgba(201,162,39,0.20), transparent 58%),
      linear-gradient(135deg, #2b2320 0%, #17120f 60%, #100c0a 100%);
    font-family:'Lato',sans-serif; color:#f4efe8; overflow:hidden;
  }}
  .cover {{
    height:510px; width:auto; border-radius:6px; flex:0 0 auto;
    box-shadow:0 22px 55px rgba(0,0,0,0.65);
  }}
  .text {{ display:flex; flex-direction:column; justify-content:center; }}
  .eyebrow {{
    font-size:19px; letter-spacing:4.5px; text-transform:uppercase;
    color:rgba(244,239,232,0.55); margin-bottom:20px;
  }}
  h1 {{
    font-family:'Playfair Display',serif; font-size:76px; line-height:1.05;
    font-weight:600; margin-bottom:20px; color:#fbf7f1;
  }}
  .author {{
    font-family:'Playfair Display',serif; font-style:italic;
    font-size:30px; color:rgba(244,239,232,0.72); margin-bottom:34px;
  }}
  .rule {{ width:88px; height:2px; background:#c9a227; margin-bottom:30px; }}
  .callout {{
    font-size:22px; font-weight:700; letter-spacing:2.6px;
    text-transform:uppercase; color:#e0bb4f;
  }}
  .subline {{
    font-size:19px; letter-spacing:1.4px; color:rgba(244,239,232,0.62);
    margin-top:10px;
  }}
</style>
<img class="cover" src="{cover_data_uri}">
<div class="text">
  <div class="eyebrow">{EYEBROW}</div>
  <h1>{TITLE}</h1>
  <div class="author">{AUTHOR}</div>
  <div class="rule"></div>
  <div class="callout">{CALLOUT}</div>
  <div class="subline">{SUBLINE}</div>
</div>
"""


def main() -> None:
    if not COVER.exists():
        raise SystemExit(f"cover not found: {COVER}")

    # Inline the cover so the page needs no local web server.
    data_uri = "data:image/jpeg;base64," + base64.b64encode(COVER.read_bytes()).decode()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu"])
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT},
                                device_scale_factor=2)
        page.set_content(build_html(data_uri))
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1200)  # let webfonts settle
        shot = page.screenshot()
        browser.close()

    img = Image.open(io.BytesIO(shot)).convert("RGB").resize((WIDTH, HEIGHT), Image.LANCZOS)
    img.save(OUT, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"wrote {OUT.relative_to(REPO)}  {img.width}x{img.height}  {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
