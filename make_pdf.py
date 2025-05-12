#!/usr/bin/env python3
import os
import sys
import argparse
from PIL import Image

def parse_args():
    p = argparse.ArgumentParser(
        description="Combine all JPGs in a folder (named 0.jpg, 1.jpg, ...) into one PDF."
    )
    p.add_argument(
        "folder",
        help="Path to folder containing JPG images"
    )
    p.add_argument(
        "-o", "--output",
        help="Output PDF filename (default: <folder>.pdf)",
        default=None
    )
    return p.parse_args()

def main():
    args = parse_args()
    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # 1) discover and numerically sort
    indexed = []
    for fname in os.listdir(folder):
        base, ext = os.path.splitext(fname)
        if ext.lower() in (".jpg", ".jpeg"):
            try:
                idx = int(base)
            except ValueError:
                continue
            indexed.append((idx, fname))
    if not indexed:
        print("No appropriately named JPGs found (e.g. '0.jpg', '1.jpg', ...).", file=sys.stderr)
        sys.exit(1)

    indexed.sort(key=lambda x: x[0])
    paths = [os.path.join(folder, fname) for _, fname in indexed]

    # 2) load & convert *inside* a with‐block so the file closes immediately
    pil_images = []
    for path in paths:
        with Image.open(path) as img:
            # convert always to RGB; this produces a new, in‐memory image
            img_rgb = img.convert("RGB")
            pil_images.append(img_rgb)

    # 3) determine output name
    output_pdf = args.output or f"{os.path.basename(os.path.normpath(folder))}.pdf"

    # 4) save
    first, rest = pil_images[0], pil_images[1:]
    first.save(
        output_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=rest
    )
    print(f"Combined {len(pil_images)} images into '{output_pdf}'.")

if __name__ == "__main__":
    main()
