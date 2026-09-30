#!/usr/bin/env python3
"""
Generate LiveArea visual assets for Test Drive II: The Duel on PS Vita.
Creates:
  vpk/icon0.png   (128x128)
  vpk/bg.png      (840x500)
  vpk/startup.png (280x158)
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/System/Library/Fonts/Supplemental"
try:
    FONT_TITLE_LG = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 38)
    FONT_TITLE_MD = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 22)
    FONT_TITLE_SM = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 15)
    FONT_SUB_MD = ImageFont.truetype(f"{FONT_DIR}/Arial.ttf", 14)
    FONT_SUB_SM = ImageFont.truetype(f"{FONT_DIR}/Arial.ttf", 10)
    FONT_BADGE = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 11)
except Exception:
    default = ImageFont.load_default()
    FONT_TITLE_LG = default
    FONT_TITLE_MD = default
    FONT_TITLE_SM = default
    FONT_SUB_MD = default
    FONT_SUB_SM = default
    FONT_BADGE = default

def create_icon():
    im = Image.new("RGB", (128, 128), (16, 20, 32))
    draw = ImageDraw.Draw(im)

    # Gradient background
    for y in range(128):
        ratio = y / 128.0
        r = int(14 + ratio * 20)
        g = int(18 + ratio * 16)
        b = int(32 + ratio * 40)
        draw.line([(0, y), (127, y)], fill=(r, g, b))

    # Outer border
    draw.rounded_rectangle([2, 2, 125, 125], radius=14, outline=(0, 212, 255), width=2)
    draw.rounded_rectangle([5, 5, 122, 122], radius=11, outline=(40, 55, 80), width=1)

    # Racing stripes (Ferrari Red & Porsche Amber)
    draw.line([(10, 22), (117, 22)], fill=(255, 40, 40), width=2)
    draw.line([(10, 26), (117, 26)], fill=(255, 180, 0), width=1)

    # "TEST DRIVE"
    draw.text((16, 32), "TEST", font=FONT_TITLE_SM, fill=(255, 255, 255))
    draw.text((64, 32), "DRIVE", font=FONT_TITLE_SM, fill=(0, 212, 255))

    # Big "II" roman numeral
    draw.text((54, 52), "II", font=FONT_TITLE_MD, fill=(255, 215, 0))

    # "THE DUEL" badge
    draw.rounded_rectangle([18, 86, 110, 106], radius=4, fill=(220, 35, 35), outline=(255, 100, 100), width=1)
    draw.text((28, 89), "THE DUEL", font=FONT_BADGE, fill=(255, 255, 255))

    # Bottom subtext
    draw.text((24, 110), "ACCOLADE 1989", font=FONT_SUB_SM, fill=(160, 180, 210))

    os.makedirs("vpk", exist_ok=True)
    im.save("vpk/icon0.png")
    print("Created vpk/icon0.png (128x128)")

def create_startup():
    im = Image.new("RGB", (280, 158), (14, 18, 28))
    draw = ImageDraw.Draw(im)

    # Gradient background
    for y in range(158):
        ratio = y / 158.0
        r = int(12 + ratio * 24)
        g = int(16 + ratio * 20)
        b = int(28 + ratio * 48)
        draw.line([(0, y), (279, y)], fill=(r, g, b))

    # Perspective road lines
    for y in range(95, 158, 12):
        draw.line([(0, y), (279, y)], fill=(35, 48, 75))
    draw.line([(140, 95), (30, 157)], fill=(0, 212, 255), width=2)
    draw.line([(140, 95), (250, 157)], fill=(0, 212, 255), width=2)
    draw.line([(140, 95), (140, 157)], fill=(255, 215, 0), width=2)

    # Frame border
    draw.rectangle([0, 0, 279, 157], outline=(0, 212, 255), width=2)

    # Title
    draw.text((26, 18), "TEST DRIVE II", font=FONT_TITLE_MD, fill=(255, 255, 255))
    draw.rounded_rectangle([26, 50, 130, 72], radius=4, fill=(220, 35, 35))
    draw.text((36, 54), "THE DUEL", font=FONT_BADGE, fill=(255, 255, 255))

    draw.text((140, 54), "FERRARI F40 vs. PORSCHE 959", font=FONT_SUB_SM, fill=(200, 220, 255))

    im.save("vpk/startup.png")
    print("Created vpk/startup.png (280x158)")

def create_bg():
    im = Image.new("RGB", (840, 500), (12, 16, 26))
    draw = ImageDraw.Draw(im)

    # Synthwave gradient
    for y in range(500):
        ratio = y / 500.0
        r = int(10 + ratio * 32)
        g = int(14 + ratio * 24)
        b = int(26 + ratio * 60)
        draw.line([(0, y), (839, y)], fill=(r, g, b))

    # Perspective highway grid at bottom
    horizon = 270
    for y in range(horizon, 500, 20):
        y_scaled = horizon + int((y - horizon) ** 1.3 * 0.7)
        if y_scaled < 500:
            draw.line([(0, y_scaled), (839, y_scaled)], fill=(35, 52, 85), width=1)
    for x in range(0, 841, 60):
        draw.line([(420 + (x - 420) // 5, horizon), (x, 499)], fill=(32, 46, 75), width=1)

    # Sun / Glow at horizon
    draw.ellipse([340, horizon - 80, 500, horizon + 80], fill=(45, 60, 100))

    # LiveArea Gate Title
    draw.text((60, 50), "TEST DRIVE II: THE DUEL", font=FONT_TITLE_LG, fill=(255, 255, 255))
    draw.rounded_rectangle([60, 105, 185, 132], radius=5, fill=(220, 35, 35), outline=(255, 100, 100), width=1)
    draw.text((72, 110), "EGA ENHANCED", font=FONT_BADGE, fill=(255, 255, 255))

    draw.text((200, 110), "PlayStation®Vita Community Edition", font=FONT_SUB_MD, fill=(0, 212, 255))
    draw.line([(60, 145), (780, 145)], fill=(45, 60, 90), width=1)

    # Info highlights
    draw.text((60, 165), "• Head-to-Head Exotic Supercar Racing (Ferrari F40 vs. Porsche 959)", font=FONT_SUB_MD, fill=(220, 230, 245))
    draw.text((60, 195), "• Native 960x544 Tri-Mode Display Engine (4:3 Pillarbox, 2x Integer, 16:9 Stretch)", font=FONT_SUB_MD, fill=(220, 230, 245))
    draw.text((60, 225), "• Full Analog Steering, Pedals & Manual Transmission Support", font=FONT_SUB_MD, fill=(220, 230, 245))

    im.save("vpk/bg.png")
    print("Created vpk/bg.png (840x500)")

if __name__ == "__main__":
    create_icon()
    create_startup()
    create_bg()
