#!/usr/bin/env python3
"""
Ensure all PNG assets under vpk/ are strictly 8-bit indexed PNGs (Color Type 3, no alpha channel).
This is required to prevent error 0x8010113D (SCE_PROMOTER_UTIL_ERROR_INVALID_PNG)
when installing the VPK on a physical PlayStation Vita via VitaShell.
"""

import glob
import os
import struct
from PIL import Image

def convert_to_vita_png(path, expected_size=None):
    im = Image.open(path)
    if expected_size and im.size != expected_size:
        print(f"Resizing {path} from {im.size} to {expected_size}...")
        im = im.resize(expected_size, Image.Resampling.LANCZOS)

    # If image has an alpha channel, flatten it onto black background
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (0, 0, 0))
        bg.paste(im, mask=im.split()[3])
        im = bg
    else:
        im = im.convert("RGB")

    # Quantize to 8-bit indexed palette (Color Type 3, no tRNS)
    quantized = im.quantize(colors=256)
    quantized.save(path, format="PNG", optimize=True)

    # Verify PNG IHDR
    with open(path, "rb") as f:
        sig = f.read(8)
        assert sig == b"\x89PNG\r\n\x1a\n", f"Invalid PNG signature in {path}"
        chunk_len_b = f.read(4)
        chunk_len = struct.unpack(">I", chunk_len_b)[0]
        chunk_type = f.read(4)
        assert chunk_type == b"IHDR"
        data = f.read(chunk_len)
        w, h, bit_depth, color_type, comp, filt, inter = struct.unpack(">IIBBBBB", data)
        assert bit_depth == 8 and color_type == 3 and inter == 0, \
            f"Image {path} failed 8-bit indexing check: bit_depth={bit_depth}, color_type={color_type}, interlace={inter}"
        print(f"  [OK] {path}: {w}x{h}, 8-bit indexed (color_type={color_type}), non-interlaced")

def main():
    print("Converting LiveArea assets to PS Vita 8-bit indexed format...")
    convert_to_vita_png("vpk/icon0.png", (128, 128))
    convert_to_vita_png("vpk/bg.png", (840, 500))
    convert_to_vita_png("vpk/startup.png", (280, 158))

    manual_files = sorted(glob.glob("vpk/manual/*.png"))
    if manual_files:
        print("\nConverting Manual pages...")
        for p in manual_files:
            convert_to_vita_png(p, (960, 544))

    print("\nAll assets successfully converted and verified for Sony PS Vita compatibility!")

if __name__ == "__main__":
    main()
