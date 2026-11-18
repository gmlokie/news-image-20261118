#!/usr/bin/env python3
"""news-image-20261118 entrypoint: copy the pre-rendered front page to the
output directory.

Stdlib only, no network, no randomness. The picture (entry.png, 1024x1024)
is rendered offline by render.py and shipped beside this file; this program
just validates it is a real 1024x1024 PNG and copies it to
$MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
import shutil
import struct

MAGIC = b"\x89PNG\r\n\x1a\n"
BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")


def read_dimensions(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    width, height = read_dimensions(SOURCE)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"unexpected size {width}x{height}")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        raise SystemExit("copy size mismatch")
    print(f"wrote {target} ({os.path.getsize(target)} bytes, {width}x{height} PNG)")


if __name__ == "__main__":
    main()
