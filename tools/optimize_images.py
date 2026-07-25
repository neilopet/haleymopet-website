#!/usr/bin/env python3
"""Web-optimize oversized images in images/.

Book covers arrive as print-resolution exports (3165px wide) but never render
larger than ~400 CSS px, so they are resized to 1200px -- still 3x retina for
the hero, and large enough for search rich-result imagery.

Run manually after adding a new cover or logo. NOT a build step: JPEG is lossy,
so re-encoding on every deploy would slowly degrade the artwork. The width guard
below makes re-runs safe, but there is still no reason to run it automatically.

    python3 tools/optimize_images.py

Note: if you resize a cover here, update the matching schema.org ImageObject
width/height in index.html or the structured data will describe a file that no
longer exists at those dimensions.
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent.parent

COVER_WIDTH = 1200
COVER_QUALITY = 88
COVERS = [
    "images/ABloodveiledDescent-Ebook.jpg",
    "images/ASunwovenAscent-Ebook.jpg",
]

# Sized to 3x the largest box the badges render in (138x52 in the hero).
BADGE_BOX = (414, 156)
BADGES = sorted((REPO / "images/retailers").glob("*.png")) if (REPO / "images/retailers").exists() else []

FOOTER_LOGO = "images/velvet-tea-press-logo-transparent.png"
FOOTER_LOGO_SIZE = 360  # rendered at 120px


def optimize_cover(rel: str) -> int:
    path = REPO / rel
    if not path.exists():
        print(f"  {rel}: missing, skipped")
        return 0
    before = path.stat().st_size
    img = Image.open(path)
    w, h = img.size
    if w <= COVER_WIDTH:
        print(f"  {path.name}: already {w}px wide -- skipped (re-encoding would degrade it)")
        return 0
    img = img.convert("RGB").resize((COVER_WIDTH, round(h * COVER_WIDTH / w)), Image.LANCZOS)
    img.save(path, "JPEG", quality=COVER_QUALITY, optimize=True, progressive=True)
    after = path.stat().st_size
    print(f"  {path.name}: {before/1024/1024:.2f} MB -> {after/1024:.1f} KB  ({img.width}x{img.height})")
    return before - after


def optimize_png(path: Path, box) -> int:
    if not path.exists():
        print(f"  {path.name}: missing, skipped")
        return 0
    before = path.stat().st_size
    img = Image.open(path).convert("RGBA")
    if img.width <= box[0] and img.height <= box[1]:
        print(f"  {path.name}: already {img.width}x{img.height} -- skipped")
        return 0
    img.thumbnail(box, Image.LANCZOS)
    img.save(path, "PNG", optimize=True)
    after = path.stat().st_size
    print(f"  {path.name}: {before/1024:.1f} KB -> {after/1024:.1f} KB  ({img.width}x{img.height})")
    return before - after


def main() -> None:
    saved = 0

    print("covers")
    for rel in COVERS:
        saved += optimize_cover(rel)

    print("retailer badges")
    for path in BADGES:
        saved += optimize_png(path, BADGE_BOX)

    print("footer logo")
    saved += optimize_png(REPO / FOOTER_LOGO, (FOOTER_LOGO_SIZE, FOOTER_LOGO_SIZE))

    print(f"\ntotal saved: {saved/1024/1024:.2f} MB" if saved else "\nnothing to do -- all assets already optimized")


if __name__ == "__main__":
    main()
