#!/usr/bin/env python3
"""Generate WebP versions of the wallpaper images inside the source tree.

The generated *.webp files are committed next to the original PNG/JPEG images.
Run this script after adding or updating a wallpaper, then commit the results.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is required to convert images (e.g. 'pip install Pillow').")

SOURCE_SUFFIXES = {".png", ".jpg", ".jpeg"}
WEBP_QUALITY = 95


def wallpaper_directories(paths: list[Path]) -> list[Path]:
    if paths:
        return paths
    return sorted(p for p in Path.cwd().iterdir() if (p / "metadata.json").is_file())


def iter_source_images(directory: Path) -> list[Path]:
    return sorted(
        p
        for p in directory.rglob("*")
        if p.is_file()
        and not p.is_symlink()
        and p.suffix.lower() in SOURCE_SUFFIXES
    )


def webp_path(image: Path) -> Path:
    return image.with_suffix(".webp")


def is_up_to_date(image: Path, webp: Path) -> bool:
    return (
        webp.is_file()
        and not webp.is_symlink()
        and webp.stat().st_mtime >= image.stat().st_mtime
    )


def convert_image(image: Path, webp: Path) -> int:
    with Image.open(image) as source:
        source.load()
        if source.mode not in ("RGB", "RGBA"):
            has_alpha = "A" in source.getbands() or "transparency" in source.info
            converted = source.convert("RGBA" if has_alpha else "RGB")
        else:
            converted = source
        converted = ImageOps.exif_transpose(converted)

        options: dict[str, object] = {"quality": WEBP_QUALITY, "method": 6}
        icc_profile = source.info.get("icc_profile")
        if icc_profile:
            options["icc_profile"] = icc_profile

        temp = webp.with_name(webp.name + ".tmp")
        converted.save(temp, "WEBP", **options)
    os.replace(temp, webp)
    return webp.stat().st_size


def find_collisions(images: list[Path]) -> list[str]:
    seen: dict[Path, Path] = {}
    collisions = []
    for image in images:
        output = webp_path(image)
        if output in seen:
            collisions.append(f"{seen[output]} and {image} both map to {output}")
        else:
            seen[output] = image
    return collisions


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="wallpaper directories to process (default: all with metadata.json)",
    )
    parser.add_argument(
        "--force", action="store_true", help="regenerate files even if up to date"
    )
    args = parser.parse_args()

    directories = wallpaper_directories(args.paths)
    if not directories:
        sys.exit("No wallpaper directories found. Run from the repository root.")

    images: list[Path] = []
    for directory in directories:
        if not directory.is_dir():
            sys.exit(f"Not a directory: {directory}")
        images.extend(iter_source_images(directory))

    collisions = find_collisions(images)
    if collisions:
        for collision in collisions:
            print(f"error: {collision}", file=sys.stderr)
        return 1

    converted = 0
    skipped = 0
    source_bytes = 0
    webp_bytes = 0

    for image in images:
        webp = webp_path(image)
        if not args.force and is_up_to_date(image, webp):
            skipped += 1
            continue

        webp.parent.mkdir(parents=True, exist_ok=True)
        size = convert_image(image, webp)
        source_bytes += image.stat().st_size
        webp_bytes += size
        converted += 1
        print(f"converted {display_path(image)} ({size // 1024} KiB)")

    print(f"{converted} image(s) converted, {skipped} up to date")
    if converted:
        print(
            f"{source_bytes // 1024} KiB -> {webp_bytes // 1024} KiB "
            f"({webp_bytes * 100 // max(source_bytes, 1)}%)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
