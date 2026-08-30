#!/usr/bin/env python3
"""Crop and compress the author headshot for the About section.

The source is a landscape environmental portrait (1620x1080) -- the subject is
off-centre with a house and lawn around her -- so a centre-crop lands on her
shoulder. The crop boxes below are chosen against the face position instead.

The About photo is styled `border-radius: 50%` at a 300px display width, so the
visible area is the inscribed circle: keep the face centred horizontally and a
little above centre, and expect the corners to be discarded.

    python3 tools/prep_author_photo.py            # writes the VARIANT below
    python3 tools/prep_author_photo.py --all      # both variants, for comparison

Run only when the author photo changes. NOT a build step -- the output is
committed, and this already emits a final optimized JPEG, so it deliberately is
not re-run by tools/optimize_images.py (a second lossy pass would only degrade
it).

Note: changing the output dimensions means updating the matching schema.org
ImageObject width/height in index.html, or the structured data will describe a
file that no longer exists at those dimensions.
"""
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / "photo-sources" / "haley-profile-aug2026.png"
OUT = REPO / "images" / "haley-headshot.jpg"

QUALITY = 88

# Crop boxes are (left, top, right, bottom) in source pixels, both centred on
# the face at x=880 and placing it ~35% down the frame. 800px wide is ~2.7x the
# 300px display slot; the 1080px-tall source cannot reach a true 3x without
# upscaling, which would only soften the result.
VARIANTS = {
    "square":   (480,  90, 1280,  890),   # 800x800  -- true circle
    "portrait": (480,  20, 1280, 1020),   # 800x1000 -- 4:5, matches the old file
}

# Which variant becomes images/haley-headshot.jpg
VARIANT = "square"


def render(name: str, dest: Path) -> tuple[int, int]:
    if not SOURCE.exists():
        raise SystemExit(f"source not found: {SOURCE}")
    img = Image.open(SOURCE).convert("RGB").crop(VARIANTS[name])
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    kb = dest.stat().st_size / 1024
    print(f"  {name:9} {img.width}x{img.height}  ->  {dest.name}  ({kb:.1f} KB)")
    return img.size


def main() -> None:
    if "--all" in sys.argv:
        for name in VARIANTS:
            render(name, OUT.with_name(f"haley-headshot-{name}.jpg"))
        print("\nboth variants written for comparison -- neither is the live file")
        return

    w, h = render(VARIANT, OUT)
    print(f"\nremember: schema.org ImageObject in index.html must read {w}x{h}")


if __name__ == "__main__":
    main()
