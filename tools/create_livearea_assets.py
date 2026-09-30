#!/usr/bin/env python3
"""
Generate official retail-style Sony PlayStation Vita LiveArea visual assets
for Test Drive II: The Duel (1989).

Produces:
  vpk/bg.png       (840x500) - Full-bleed authentic 1989 Accolade cover art (Porsche 959 & Ferrari F40)
  vpk/startup.png  (280x158) - Polished start gate with official The Duel: Test Drive II logo
  vpk/icon0.png    (128x128) - Home Screen bubble icon with official logo & badge
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
BOXART_PATH = os.path.join(SCRIPT_DIR, "boxart_front.jpg")
OUTPUT_DIR = os.path.join(ROOT_DIR, "vpk")

FONT_DIR = "/System/Library/Fonts/Supplemental"
try:
    FONT_BADGE = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 8)
    FONT_SUB = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 8)
except Exception:
    default = ImageFont.load_default()
    FONT_BADGE = default
    FONT_SUB = default

def load_and_prep_boxart():
    if not os.path.exists(BOXART_PATH):
        raise FileNotFoundError(f"Box art source not found at {BOXART_PATH}")

    box = Image.open(BOXART_PATH).convert("RGB")
    return box

def extract_logo(box):
    # 'The Duel / TEST DRIVE II' logo is at x: [380, 1450], y: [400, 750]
    logo_crop = box.crop((380, 400, 1450, 750))
    logo_rgba = logo_crop.convert("RGBA")
    data = logo_rgba.getdata()
    clean_data = []
    for p in data:
        # Dark asphalt road background is R, G, B < 48
        if p[0] < 48 and p[1] < 48 and p[2] < 48:
            clean_data.append((0, 0, 0, 0))
        else:
            clean_data.append(p)
    logo_rgba.putdata(clean_data)
    return logo_rgba

def create_bg(box):
    # Crop to 840x500 ratio (1.68)
    # Include Porsche 959 (x: 700..1700, y: 800..1450) and cursive Accolade logo (y: 1450..1750)
    # Bounding box width = 1760 (skip outer worn paper tears)
    clean_box = box.crop((40, 720, 1800, 1807))
    bg = clean_box.resize((840, 500), Image.Resampling.LANCZOS)

    # Soft edge vignette for Vita system UI and top status bar
    vignette = Image.new("RGBA", (840, 500), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for y in range(75):
        alpha = int(120 * ((75 - y) / 75.0) ** 1.5)
        v_draw.line([(0, y), (839, y)], fill=(8, 10, 16, alpha))
    for x in range(45):
        alpha = int(110 * ((45 - x) / 45.0) ** 1.5)
        v_draw.line([(x, 0), (x, 499)], fill=(8, 10, 16, alpha))
    for x in range(45):
        alpha = int(110 * (x / 45.0) ** 1.5)
        v_draw.line([(839 - x, 0), (839 - x, 499)], fill=(8, 10, 16, alpha))

    bg_final = Image.alpha_composite(bg.convert("RGBA"), vignette).convert("RGB")
    out_path = os.path.join(OUTPUT_DIR, "bg.png")
    bg_final.save(out_path)
    print(f"Created {out_path} (840x500)")

def create_startup(logo_rgba):
    im = Image.new("RGB", (280, 158), (14, 16, 26))
    draw = ImageDraw.Draw(im)

    # Subtle dark asphalt gradient
    for y in range(158):
        ratio = y / 158.0
        r = int(12 + ratio * 14)
        g = int(14 + ratio * 12)
        b = int(22 + ratio * 18)
        draw.line([(0, y), (279, y)], fill=(r, g, b))

    # Ferrari Red & Porsche Amber dual border
    draw.rectangle([0, 0, 279, 157], outline=(255, 40, 40), width=2)
    draw.rectangle([3, 3, 276, 154], outline=(255, 180, 0), width=1)

    # Scale logo into upper half (leaves bottom y: 95..145 clear for blue Start button)
    target_w = 230
    target_h = int(logo_rgba.height * (target_w / logo_rgba.width))
    scaled_logo = logo_rgba.resize((target_w, target_h), Image.Resampling.LANCZOS)
    im.paste(scaled_logo, ((280 - target_w) // 2, 20), scaled_logo)

    out_path = os.path.join(OUTPUT_DIR, "startup.png")
    im.save(out_path)
    print(f"Created {out_path} (280x158)")

def create_icon(logo_rgba):
    im = Image.new("RGB", (128, 128), (14, 16, 24))
    draw = ImageDraw.Draw(im)

    # Gradient background
    for y in range(128):
        ratio = y / 128.0
        r = int(12 + ratio * 16)
        g = int(14 + ratio * 12)
        b = int(22 + ratio * 14)
        draw.line([(0, y), (127, y)], fill=(r, g, b))

    # Rounded borders (Ferrari Red & Porsche Amber)
    draw.rounded_rectangle([2, 2, 125, 125], radius=14, outline=(255, 40, 40), width=2)
    draw.rounded_rectangle([5, 5, 122, 122], radius=11, outline=(255, 180, 0), width=1)

    # Racing stripes
    draw.line([(12, 18), (115, 18)], fill=(255, 40, 40), width=2)
    draw.line([(12, 22), (115, 22)], fill=(255, 180, 0), width=1)

    # Scaled logo
    target_w = 114
    target_h = int(logo_rgba.height * (target_w / logo_rgba.width))
    scaled_logo = logo_rgba.resize((target_w, target_h), Image.Resampling.LANCZOS)
    im.paste(scaled_logo, ((128 - target_w) // 2, 34), scaled_logo)

    # Badges
    draw.rounded_rectangle([14, 78, 114, 96], radius=3, fill=(220, 35, 35), outline=(255, 100, 100), width=1)
    draw.text((18, 83), "FERRARI vs PORSCHE", font=FONT_BADGE, fill=(255, 255, 255))

    draw.text((24, 105), "ACCOLADE 1989", font=FONT_SUB, fill=(160, 180, 210))

    out_path = os.path.join(OUTPUT_DIR, "icon0.png")
    im.save(out_path)
    print(f"Created {out_path} (128x128)")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    box = load_and_prep_boxart()
    logo = extract_logo(box)

    create_bg(box)
    create_startup(logo)
    create_icon(logo)

    # Convert to 8-bit palette-indexed for strict Sony TRC compliance
    converter = os.path.join(SCRIPT_DIR, "convert_to_8bit_png.py")
    if os.path.exists(converter):
        import subprocess
        subprocess.check_call([
            sys.executable, converter,
            os.path.join(OUTPUT_DIR, "icon0.png"),
            os.path.join(OUTPUT_DIR, "startup.png"),
            os.path.join(OUTPUT_DIR, "bg.png")
        ])

if __name__ == "__main__":
    main()
