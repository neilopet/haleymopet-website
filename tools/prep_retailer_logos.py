#!/usr/bin/env python3
"""Turn indie bookshop logos into uniform badge assets for images/retailers/.

Each shop's wordmark is trimmed of whitespace, given a transparent background,
and normalized to a common height so the badges sit evenly in a row.

Originals live in tools/logo-sources/ rather than being re-downloaded: they came
from Squarespace/Wix/Shopify CDNs whose URLs are hashed and will eventually rot.
Source URLs are recorded below for reference if a shop rebrands.

    python3 tools/prep_retailer_logos.py

Run only when a shop changes its branding or the badges need resizing. NOT a
build step -- the output is committed.
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(__file__).resolve().parent / "logo-sources"
OUT_DIR = REPO / "images" / "retailers"

# Height before the final optimize pass; tools/optimize_images.py scales these
# down to the 414x156 box the badges actually render in.
TARGET_H = 220

SOURCES = {
    # slug: (source file, original URL it was captured from)
    "flight-of-fantasy": (
        "flight-of-fantasy-source.png",
        "https://www.flightoffantasybooks.com/ (Squarespace header logo)",
    ),
    "the-crafty-bookstore": (
        "the-crafty-bookstore-source.png",
        "https://www.thecraftybookstore.com/ (Wix header logo, 'TCB Final Files-17.png')",
    ),
    "the-fated-chapter": (
        "the-fated-chapter-source.png",
        "https://thefatedchapterbookstore.com/ (Shopify header banner)",
    ),
}

# Fraction of height to keep after trimming. The Crafty Bookstore's lockup has a
# tagline that is unreadable at badge size, so only the wordmark is kept.
KEEP_TOP = {"the-crafty-bookstore": 2062 / 2355}

WHITE_THRESHOLD = 238


def whiten_to_alpha(img: Image.Image) -> Image.Image:
    """Make near-white pixels transparent so logos sit on any background."""
    img = img.convert("RGBA")
    img.putdata([
        (r, g, b, 0) if (r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD)
        else (r, g, b, a)
        for r, g, b, a in img.getdata()
    ])
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for slug, (filename, origin) in SOURCES.items():
        src = SOURCE_DIR / filename
        if not src.exists():
            print(f"{slug}: source missing at {src} -- skipped (originally from {origin})")
            continue

        img = whiten_to_alpha(Image.open(src))

        bbox = img.getbbox()  # trim fully transparent margins
        if bbox:
            img = img.crop(bbox)

        if slug in KEEP_TOP:
            w, h = img.size
            img = img.crop((0, 0, w, round(h * KEEP_TOP[slug])))
            if img.getbbox():
                img = img.crop(img.getbbox())

        w, h = img.size
        img = img.resize((max(1, round(w * TARGET_H / h)), TARGET_H), Image.LANCZOS)

        dest = OUT_DIR / f"{slug}.png"
        img.save(dest, "PNG", optimize=True)
        print(f"{slug}: {w}x{h} -> {img.width}x{img.height}  ({dest.stat().st_size // 1024} KB)")

    print("\nNow run: python3 tools/optimize_images.py")


if __name__ == "__main__":
    main()
