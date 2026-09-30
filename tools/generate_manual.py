#!/usr/bin/env python3
"""
Generate Sony PS Vita TRC-compliant LiveArea User Manual pages (960x544 PNG).
Creates 5 comprehensive, pixel-perfect, highly readable pages for Test Drive II: The Duel:
  001.png - Cover & Introduction
  002.png - Game Data Setup & File Installation
  003.png - PlayStation Vita Controls & Handling
  004.png - Display Modes & Real-Time Aspect Switching
  005.png - The Duel Mechanics, Radar Detector & Hazards
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 960
HEIGHT = 544
TOTAL_PAGES = 5
OUTPUT_DIR = "vpk/manual"

# Color Palette
BG_DARK = (14, 18, 26)
BG_CARD = (22, 28, 42)
BG_CARD_ALT = (28, 36, 52)
BORDER_MUTED = (45, 58, 82)
CYAN_ACCENT = (0, 212, 255)
GOLD_ACCENT = (255, 183, 3)
RED_ACCENT = (255, 61, 87)
GREEN_ACCENT = (0, 230, 118)
TEXT_WHITE = (245, 248, 255)
TEXT_MUTED = (160, 175, 200)
TEXT_DIM = (110, 125, 145)

# PlayStation Button Colors
COLOR_CROSS = (41, 121, 255)
COLOR_CIRCLE = (255, 61, 0)
COLOR_SQUARE = (224, 64, 251)
COLOR_TRIANGLE = (0, 230, 118)
COLOR_TRIGGER = (80, 95, 120)

# Fonts
FONT_DIR = "/System/Library/Fonts/Supplemental"
try:
    FONT_TITLE_HERO = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 36)
    FONT_PAGE_TITLE = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 25)
    FONT_SECTION_HDR = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 16)
    FONT_SUBTITLE = ImageFont.truetype(f"{FONT_DIR}/Arial.ttf", 14)
    FONT_BODY_BOLD = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 14)
    FONT_BODY = ImageFont.truetype(f"{FONT_DIR}/Arial.ttf", 13)
    FONT_BODY_SM = ImageFont.truetype(f"{FONT_DIR}/Arial.ttf", 12)
    FONT_MONO = ImageFont.truetype(f"{FONT_DIR}/Courier New Bold.ttf", 13)
    FONT_MONO_SM = ImageFont.truetype(f"{FONT_DIR}/Courier New Bold.ttf", 11)
    FONT_BADGE = ImageFont.truetype(f"{FONT_DIR}/Arial Bold.ttf", 11)
except Exception:
    default = ImageFont.load_default()
    FONT_TITLE_HERO = default
    FONT_PAGE_TITLE = default
    FONT_SECTION_HDR = default
    FONT_SUBTITLE = default
    FONT_BODY_BOLD = default
    FONT_BODY = default
    FONT_BODY_SM = default
    FONT_MONO = default
    FONT_MONO_SM = default
    FONT_BADGE = default


def create_base(page_num, title, subtitle):
    """Create standard canvas with top header and bottom footer."""
    im = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(im)

    # Subtle background gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_DARK[0] * (1 - ratio * 0.4) + 20 * (ratio * 0.4))
        g = int(BG_DARK[1] * (1 - ratio * 0.4) + 25 * (ratio * 0.4))
        b = int(BG_DARK[2] * (1 - ratio * 0.4) + 38 * (ratio * 0.4))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Top Header Bar (0..40)
    draw.rectangle([0, 0, WIDTH, 40], fill=(20, 26, 38))
    draw.line([(0, 40), (WIDTH, 40)], fill=CYAN_ACCENT, width=2)

    # Header Badges
    draw_badge(draw, 24, 10, "PLAYSTATION®VITA", CYAN_ACCENT, (10, 20, 30), border=CYAN_ACCENT)
    draw.text((155, 12), "TEST DRIVE II: THE DUEL (1989)", font=FONT_BODY_BOLD, fill=TEXT_MUTED)

    page_str = f"PAGE {page_num} OF {TOTAL_PAGES}"
    draw_badge(draw, WIDTH - 130, 10, page_str, (35, 45, 65), TEXT_WHITE, border=BORDER_MUTED)

    # Title & Subtitle
    draw.text((28, 52), title, font=FONT_PAGE_TITLE, fill=TEXT_WHITE)
    draw.text((30, 83), subtitle, font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.line([(28, 102), (WIDTH - 28, 102)], fill=BORDER_MUTED, width=1)

    # Footer (512..544)
    draw.line([(28, 510), (WIDTH - 28, 510)], fill=BORDER_MUTED, width=1)
    footer_text = "Swipe screen or use D-Pad / L/R to turn pages  •  Press PS Button to return"
    draw.text((WIDTH // 2 - 210, 518), footer_text, font=FONT_BODY_SM, fill=TEXT_DIM)

    return im, draw


def draw_badge(draw, x, y, text, bg_color, text_color, border=None):
    bbox = FONT_BADGE.getbbox(text)
    w = bbox[2] - bbox[0] + 16
    h = 20
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg_color, outline=border, width=1 if border else 0)
    draw.text((x + 8, y + 3), text, font=FONT_BADGE, fill=text_color)
    return w


def draw_btn_glyph(draw, cx, cy, btn_type, size=11):
    """Draw PS Vita controller buttons."""
    r = size
    if btn_type == 'cross':
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_CROSS)
        d = int(r * 0.55)
        draw.line([cx - d, cy - d, cx + d, cy + d], fill=TEXT_WHITE, width=2)
        draw.line([cx - d, cy + d, cx + d, cy - d], fill=TEXT_WHITE, width=2)
    elif btn_type == 'circle':
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_CIRCLE)
        draw.ellipse([cx - int(r * 0.55), cy - int(r * 0.55), cx + int(r * 0.55), cy + int(r * 0.55)], outline=TEXT_WHITE, width=2)
    elif btn_type == 'square':
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_SQUARE)
        d = int(r * 0.5)
        draw.rectangle([cx - d, cy - d, cx + d, cy + d], outline=TEXT_WHITE, width=2)
    elif btn_type == 'triangle':
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_TRIANGLE)
        d = int(r * 0.58)
        pts = [(cx, cy - d), (cx - d, cy + d - 2), (cx + d, cy + d - 2)]
        draw.polygon(pts, outline=TEXT_WHITE, width=2)


def measure_key_pill(text):
    bbox = FONT_BADGE.getbbox(text)
    tw = bbox[2] - bbox[0]
    return max(tw + 14, 26)


def draw_key_pill(draw, x, y, text, width=None, bg=COLOR_TRIGGER, fg=TEXT_WHITE, border=None):
    bbox = FONT_BADGE.getbbox(text)
    tw = bbox[2] - bbox[0]
    w = width if width else max(tw + 14, 26)
    h = 20
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg, outline=border, width=1 if border else 0)
    draw.text((x + (w - tw) // 2, y + 3), text, font=FONT_BADGE, fill=fg)
    return w


def generate_page_1():
    """Page 1: Cover & Welcome."""
    im = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(im)

    # Synthwave gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(10 + ratio * 28)
        g = int(14 + ratio * 20)
        b = int(28 + ratio * 45)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Perspective grid at bottom
    horizon = 320
    for y in range(horizon, HEIGHT - 30, 18):
        y_scaled = horizon + int((y - horizon) ** 1.35 * 0.6)
        if y_scaled < HEIGHT - 30:
            draw.line([(0, y_scaled), (WIDTH, y_scaled)], fill=(40, 55, 90), width=1)
    for x in range(0, WIDTH + 1, 60):
        draw.line([(WIDTH // 2 + (x - WIDTH // 2) // 4, horizon), (x, HEIGHT - 30)], fill=(35, 50, 80), width=1)

    # Top Header Bar
    draw.rectangle([0, 0, WIDTH, 36], fill=(16, 22, 34))
    draw.line([(0, 36), (WIDTH, 36)], fill=CYAN_ACCENT, width=2)
    draw_badge(draw, 24, 8, "OFFICIAL DIGITAL USER MANUAL", CYAN_ACCENT, (10, 20, 30), border=CYAN_ACCENT)
    draw.text((WIDTH - 130, 10), "PAGE 1 OF 5", font=FONT_BODY_BOLD, fill=TEXT_MUTED)

    # Embed App Icon if available
    icon_path = "vpk/icon0.png"
    if os.path.exists(icon_path):
        try:
            icon_img = Image.open(icon_path).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
            draw.rounded_rectangle([135, 62, 135 + 82, 62 + 82], radius=10, fill=(30, 40, 60), outline=CYAN_ACCENT, width=2)
            im.paste(icon_img, (138, 65), icon_img)
        except Exception:
            pass

    # Main Hero Title
    draw.text((235, 65), "TEST DRIVE II", font=FONT_TITLE_HERO, fill=TEXT_WHITE)
    draw_badge(draw, 495, 72, "THE DUEL", RED_ACCENT, (255, 255, 255), border=RED_ACCENT)
    draw.text((237, 112), "COMMUNITY HOMEBREW RECOMPILATION", font=FONT_BODY_BOLD, fill=CYAN_ACCENT)
    draw.text((237, 130), "Ferrari F40 vs. Porsche 959 Head-to-Head Racing on PlayStation®Vita", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Feature Cards in Grid
    cards = [
        ("NATIVE VITA GXM", "Hardware texture presentation at 60 FPS utilizing the Vita SGX543MP4+ GPU."),
        ("AUTHENTIC DOS AUDIO", "Accurate PC-Speaker synthesizer and EGA sound effects engine."),
        ("TRI-MODE ASPECT RATIO", "4:3 Pillarbox (Default), 2× Integer Scale, or 16:9 Widescreen Stretch."),
        ("ANALOG & PHYSICAL CONTROLS", "Precision left-stick steering, trigger throttles, and sequential shifting.")
    ]

    card_w, card_h = 425, 60
    xs = [40, 495]
    ys = [165, 235]

    idx = 0
    for r in range(2):
        for c in range(2):
            cx, cy = xs[c], ys[r]
            title, desc = cards[idx]
            draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)
            draw.rounded_rectangle([cx, cy, cx + 5, cy + card_h], radius=2, fill=CYAN_ACCENT)
            draw.text((cx + 16, cy + 8), title, font=FONT_SECTION_HDR, fill=CYAN_ACCENT)
            draw.text((cx + 16, cy + 30), desc, font=FONT_BODY_SM, fill=TEXT_MUTED)
            idx += 1

    # CRITICAL LEGAL & DATA NOTICE CARD
    notice_y = 312
    draw.rounded_rectangle([40, notice_y, WIDTH - 40, notice_y + 168], radius=8, fill=(28, 22, 18), outline=GOLD_ACCENT, width=2)
    draw.rectangle([40, notice_y, WIDTH - 40, notice_y + 32], fill=(48, 36, 18))
    draw_badge(draw, 55, notice_y + 6, "IMPORTANT NOTICE", GOLD_ACCENT, (20, 20, 20), border=GOLD_ACCENT)
    draw.text((195, notice_y + 8), "COMMERCIAL DOS GAME DATA NOT INCLUDED", font=FONT_BODY_BOLD, fill=GOLD_ACCENT)

    notice_lines = [
        "• To comply with copyright laws, this homebrew VPK DOES NOT contain proprietary game data.",
        "• You must supply original game files from your legal copy of Accolade's Test Drive II: The Duel (1989).",
        "• Copy the files to:  ux0:data/TestDrive2/  using VitaShell (via USB or FTP mode).",
        "• Turn to PAGE 2 for the complete step-by-step setup guide and file verification checklist."
    ]
    for i, line in enumerate(notice_lines):
        color = TEXT_WHITE if i == 2 else TEXT_MUTED
        draw.text((58, notice_y + 44 + i * 27), line, font=FONT_BODY, fill=color)

    # Footer
    draw.line([(28, 510), (WIDTH - 28, 510)], fill=BORDER_MUTED, width=1)
    draw.text((WIDTH // 2 - 200, 518), "Press D-Pad Right or Swipe to proceed to Page 2 (Setup Guide)", font=FONT_BODY_SM, fill=CYAN_ACCENT)

    return im


def generate_page_2():
    """Page 2: Game Data Installation Guide."""
    im, draw = create_base(2, "GAME DATA SETUP GUIDE", "How to install your original 1989 DOS game files onto your PS Vita")

    # Left Column: Step-by-Step Instructions (width: 485)
    left_x = 28
    left_w = 485
    draw.rounded_rectangle([left_x, 115, left_x + left_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    steps = [
        ("STEP 1: OBTAIN ORIGINAL DOS ASSETS", [
            "You need the original files from Accolade's Test Drive II: The Duel (1989).",
            "Files can be extracted from original 3.5\"/5.25\" floppy diskettes,",
            "CD-ROM releases, or licensed DOS emulation archives."
        ]),
        ("STEP 2: CONNECT TO PS VITA WITH VITASHELL", [
            "Launch VitaShell on your PlayStation®Vita.",
            "Press SELECT to activate USB or FTP connection mode.",
            "Connect your Vita to your PC, Mac, or mobile device."
        ]),
        ("STEP 3: COPY FILES TO ux0:data/TestDrive2/", [
            "Navigate to partition: ux0: -> data -> TestDrive2",
            "(The TestDrive2 directory is automatically created on first boot).",
            "Copy all DOS files into:  ux0:data/TestDrive2/"
        ]),
        ("STEP 4: LAUNCH TEST DRIVE II FROM LIVEAREA", [
            "Disconnect VitaShell and launch the Test Drive II bubble.",
            "The engine detects your files automatically and boots into the game!"
        ])
    ]

    sy = 125
    for title, lines in steps:
        draw.rounded_rectangle([left_x + 12, sy, left_x + left_w - 12, sy + 24], radius=3, fill=(35, 46, 68))
        draw.text((left_x + 18, sy + 4), title, font=FONT_SECTION_HDR, fill=CYAN_ACCENT)
        sy += 28
        for line in lines:
            draw.text((left_x + 22, sy), line, font=FONT_BODY_SM, fill=TEXT_MUTED)
            sy += 16
        sy += 8

    # Right Column: Required Files Checklist (width: 405)
    right_x = 527
    right_w = 405
    draw.rounded_rectangle([right_x, 115, right_x + right_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    draw.rounded_rectangle([right_x + 12, 125, right_x + right_w - 12, 149], radius=3, fill=(35, 46, 68))
    draw.text((right_x + 18, 129), "REQUIRED FILES CHECKLIST", font=FONT_SECTION_HDR, fill=GOLD_ACCENT)

    file_items = [
        ("TD2EGA.EXE", "Primary EGA executable (Required to boot!)", True),
        ("CARS.DAT", "Car catalogue file", True),
        ("SCENES.DAT", "Scenery scenery catalogue file", True),
        ("*.PES / *.PCS", "Cockpits, road scenery & art assets", True),
        ("*.BIN / *.SS", "Vehicle simulation & opponent sprites", True),
        ("SONGS.BIN", "PC speaker music & theme melodies", True),
        ("SELECT.DAT", "Saved user configuration & vehicle picks", False),
        ("Add-on Disks", "Optional car & scenery expansion disks", False)
    ]

    fy = 160
    for fname, fdesc, req in file_items:
        draw.rounded_rectangle([right_x + 12, fy, right_x + right_w - 12, fy + 33], radius=4, fill=(28, 36, 52))
        badge_text = "REQUIRED" if req else "OPTIONAL"
        badge_bg = (180, 40, 40) if req else (50, 70, 95)
        draw.rounded_rectangle([right_x + 18, fy + 6, right_x + 94, fy + 26], radius=4, fill=badge_bg)
        draw.text((right_x + 24, fy + 9), badge_text, font=FONT_BADGE, fill=TEXT_WHITE)
        draw.text((right_x + 106, fy + 4), fname, font=FONT_MONO, fill=TEXT_WHITE)
        draw.text((right_x + 106, fy + 18), fdesc, font=FONT_BODY_SM, fill=TEXT_MUTED)
        fy += 37

    # Case Sensitivity Note Box
    draw.rounded_rectangle([right_x + 12, 458, right_x + right_w - 12, 488], radius=4, fill=(22, 38, 48), outline=CYAN_ACCENT, width=1)
    draw.text((right_x + 20, 464), "Tip: Expansion disks placed in ux0:data/TestDrive2 load automatically!", font=FONT_BODY_SM, fill=CYAN_ACCENT)

    return im


def generate_page_3():
    """Page 3: Controls & Driving Operation."""
    im, draw = create_base(3, "PLAYSTATION®VITA CONTROLS", "Complete physical button mapping and vehicle operation guide")

    # Left Column: In-Game Driving Controls (width: 515)
    left_x = 28
    left_w = 515
    draw.rounded_rectangle([left_x, 115, left_x + left_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    draw.rounded_rectangle([left_x + 12, 125, left_x + left_w - 12, 149], radius=3, fill=(35, 46, 68))
    draw.text((left_x + 18, 129), "DRIVING CONTROLS (ON THE ROAD)", font=FONT_SECTION_HDR, fill=CYAN_ACCENT)

    controls = [
        ("STEERING", [("stick", "Left Stick"), ("text", "or"), ("badge", "D-Pad ◄ / ►")], "Steer left and right with full analog response."),
        ("ACCELERATE (GAS)", [("cross", None), ("text", "or"), ("badge", "R TRIGGER"), ("text", "or"), ("badge", "▲")], "Depress gas pedal to accelerate engine."),
        ("BRAKE", [("badge", "L TRIGGER"), ("text", "or"), ("badge", "▼")], "Apply vehicle brakes to rapidly decelerate."),
        ("SHIFT UP", [("triangle", None), ("text", "Triangle")], "Shift transmission UP into next higher gear."),
        ("SHIFT DOWN", [("square", None), ("text", "/"), ("circle", None), ("text", "Square / Circle")], "Shift transmission DOWN into lower gear."),
        ("CYCLE DISPLAY", [("badge", "SELECT")], "Switch aspect ratio (4:3 -> 2× Integer -> 16:9)."),
        ("PAUSE / MENU", [("badge", "START")], "Open in-game pause menu or cancel run (Esc).")
    ]

    cy = 160
    for action, inputs, desc in controls:
        draw.rounded_rectangle([left_x + 14, cy, left_x + left_w - 14, cy + 40], radius=4, fill=(28, 36, 52))
        draw.text((left_x + 20, cy + 6), action, font=FONT_BODY_BOLD, fill=GOLD_ACCENT)
        draw.text((left_x + 20, cy + 22), desc, font=FONT_BODY_SM, fill=TEXT_MUTED)

        # Draw inputs from right to left
        rx = left_x + left_w - 24
        curr_x = rx
        for item in reversed(inputs):
            itype = item[0]
            if itype == 'text':
                bbox = FONT_BODY_SM.getbbox(item[1])
                w = bbox[2] - bbox[0] + 6
                curr_x -= w
                draw.text((curr_x + 3, cy + 12), item[1], font=FONT_BODY_SM, fill=TEXT_MUTED)
            elif itype == 'badge':
                bw = measure_key_pill(item[1])
                curr_x -= (bw + 4)
                draw_key_pill(draw, curr_x, cy + 10, item[1])
            elif itype == 'cross':
                curr_x -= 24
                draw_btn_glyph(draw, curr_x + 11, cy + 20, 'cross')
            elif itype == 'circle':
                curr_x -= 24
                draw_btn_glyph(draw, curr_x + 11, cy + 20, 'circle')
            elif itype == 'square':
                curr_x -= 24
                draw_btn_glyph(draw, curr_x + 11, cy + 20, 'square')
            elif itype == 'triangle':
                curr_x -= 24
                draw_btn_glyph(draw, curr_x + 11, cy + 20, 'triangle')
            elif itype == 'stick':
                bw = measure_key_pill(item[1])
                curr_x -= (bw + 4)
                draw_key_pill(draw, curr_x, cy + 10, item[1], bg=(60, 75, 105))

        cy += 46

    # Right Column: Menus & Transmission Tips (width: 370)
    right_x = 560
    right_w = 370
    draw.rounded_rectangle([right_x, 115, right_x + right_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    draw.rounded_rectangle([right_x + 12, 125, right_x + right_w - 12, 149], radius=3, fill=(35, 46, 68))
    draw.text((right_x + 18, 129), "MENU NAVIGATION", font=FONT_SECTION_HDR, fill=CYAN_ACCENT)

    # Menu items with actual graphical buttons
    my = 160
    draw.text((right_x + 20, my), "D-Pad Up / Down", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((right_x + 20, my + 16), "Highlight menu entries & car choices", font=FONT_BODY_SM, fill=TEXT_MUTED)

    my += 36
    draw_btn_glyph(draw, right_x + 30, my + 8, 'cross')
    draw.text((right_x + 50, my), "Cross Button", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((right_x + 50, my + 16), "Confirm selection / DOS Enter key", font=FONT_BODY_SM, fill=TEXT_MUTED)

    my += 36
    draw_btn_glyph(draw, right_x + 30, my + 8, 'circle')
    draw.text((right_x + 50, my), "Circle Button", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((right_x + 50, my + 16), "Toggle options / DOS Spacebar key", font=FONT_BODY_SM, fill=TEXT_MUTED)

    my += 36
    draw_key_pill(draw, right_x + 18, my, "START")
    draw.text((right_x + 80, my), "Start Button", font=FONT_BODY_BOLD, fill=TEXT_WHITE)
    draw.text((right_x + 80, my + 16), "Back / Cancel / DOS Escape key", font=FONT_BODY_SM, fill=TEXT_MUTED)

    # Transmission Tips Card
    draw.rounded_rectangle([right_x + 12, 316, right_x + right_w - 12, 485], radius=6, fill=(28, 36, 52), outline=GOLD_ACCENT, width=1)
    draw.text((right_x + 20, 326), "MANUAL TRANSMISSION GUIDE", font=FONT_BODY_BOLD, fill=GOLD_ACCENT)

    tips = [
        "• All vehicles feature realistic manual gearboxes.",
        "• Watch the Tachometer (RPM): Shift UP (Triangle)",
        "  before the needle reaches the red line.",
        "• Downshift (Square/Circle) on steep uphill",
        "  grades or sharp turns to maintain engine torque.",
        "• WARNING: Do not stay in the redline! Over-revving",
        "  will catastrophically blow your engine!"
    ]
    ty = 350
    for tip in tips:
        draw.text((right_x + 20, ty), tip, font=FONT_BODY_SM, fill=TEXT_MUTED)
        ty += 19

    return im


def generate_page_4():
    """Page 4: Display Modes & Aspect Ratio Engine."""
    im, draw = create_base(4, "DISPLAY MODES & SCALING", "Select from 3 optimized display modes with real-time switching")

    # Banner Explaining SELECT button
    draw.rounded_rectangle([28, 115, WIDTH - 28, 155], radius=6, fill=(24, 38, 56), outline=CYAN_ACCENT, width=1)
    draw_badge(draw, 40, 125, "HOW TO SWITCH", CYAN_ACCENT, (10, 20, 30), border=CYAN_ACCENT)
    draw.text((160, 126), "Press the SELECT button at any time during gameplay to cycle modes instantaneously.", font=FONT_BODY_BOLD, fill=TEXT_WHITE)

    # 3 Mode Cards side by side (Width: 288 each)
    cards = [
        ("MODE 1 (DEFAULT)", "4:3 Aspect-Correct", "725 × 544 Pillarbox", CYAN_ACCENT, [
            "• Authentic retro CRT proportion.",
            "• Zero vertical cropping — all instruments,",
            "  gauges, and radar detectors fully visible.",
            "• Clean black side pillarboxes.",
            "• Hardware bilinear texture smoothing.",
            "• Recommended for the best authentic",
            "  gameplay experience!"
        ]),
        ("MODE 2", "2× Integer Scale", "640 × 480 Centered", GOLD_ACCENT, [
            "• Exact 2× pixel-perfect integer scale.",
            "• No fractional pixel distortion or blur.",
            "• 1:1 match with original DOS EGA",
            "  monitor scanline proportions.",
            "• Crisp, razor-sharp retro pixel edges.",
            "• Ideal for purists who love original",
            "  chunky DOS aesthetics."
        ]),
        ("MODE 0", "16:9 Widescreen", "960 × 544 Full Screen", (180, 140, 255), [
            "• Edge-to-edge panoramic stretch.",
            "• Completely fills the 5-inch OLED/LCD",
            "  PlayStation®Vita display.",
            "• Maximizes windscreen driving view.",
            "• Note: Due to wide aspect scaling, small",
            "  lower portions of cockpit gauges",
            "  may be subtly trimmed."
        ])
    ]

    card_w = 288
    for i, (tag, name, res, col, points) in enumerate(cards):
        cx = 28 + i * (card_w + 20)
        cy = 170
        draw.rounded_rectangle([cx, cy, cx + card_w, 495], radius=6, fill=BG_CARD, outline=col if i == 0 else BORDER_MUTED, width=2 if i == 0 else 1)

        # Header Box
        draw.rounded_rectangle([cx + 10, cy + 10, cx + card_w - 10, cy + 34], radius=3, fill=(35, 46, 68))
        draw_badge(draw, cx + 16, cy + 12, tag, col, (10, 20, 30))
        draw.text((cx + 16, cy + 42), name, font=FONT_SECTION_HDR, fill=TEXT_WHITE)
        draw.text((cx + 16, cy + 64), res, font=FONT_MONO, fill=col)
        draw.line([(cx + 16, cy + 86), (cx + card_w - 16, cy + 86)], fill=BORDER_MUTED, width=1)

        py = cy + 96
        for pt in points:
            draw.text((cx + 16, py), pt, font=FONT_BODY_SM, fill=TEXT_MUTED)
            py += 21

    return im


def generate_page_5():
    """Page 5: The Duel Mechanics & Hazards."""
    im, draw = create_base(5, "THE DUEL MECHANICS & HAZARDS", "Opponent racing AI, radar detection, gas stops, and road survival")

    # Left Column: The Duel & Gas Stops (width: 440)
    left_x = 28
    left_w = 440
    draw.rounded_rectangle([left_x, 115, left_x + left_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    draw.rounded_rectangle([left_x + 12, 125, left_x + left_w - 12, 149], radius=3, fill=(35, 46, 68))
    draw.text((left_x + 18, 129), "THE DUEL HEAD-TO-HEAD RACING", font=FONT_SECTION_HDR, fill=CYAN_ACCENT)

    mechanics = [
        ("HEAD-TO-HEAD RACING", [
            "Compete against an aggressive computer-controlled opponent.",
            "You can choose matching cars (F40 vs. F40) or battle",
            "the ultimate showdown: Ferrari F40 vs. Porsche 959!"
        ]),
        ("STAGE GAS STOPS", [
            "At the end of each stage, pull cleanly into the gas station bay.",
            "Be careful! Approaching too fast will result in a disastrous crash",
            "into the refueling pumps."
        ]),
        ("RADAR DETECTOR", [
            "Mounted on your sun visor. Flashes and emits rapid audio beeps",
            "when highway patrol speed traps are active down the road!"
        ]),
        ("REARVIEW MIRROR", [
            "Check your mirror to track opponent positions, trailing traffic,",
            "and pursuing highway patrol squad cars."
        ])
    ]

    gy = 160
    for name, lines in mechanics:
        card_h = 24 + len(lines) * 16 + 8
        draw.rounded_rectangle([left_x + 14, gy, left_x + left_w - 14, gy + card_h], radius=4, fill=(28, 36, 52))
        draw.text((left_x + 22, gy + 6), name, font=FONT_BODY_BOLD, fill=GOLD_ACCENT)
        for j, l in enumerate(lines):
            draw.text((left_x + 22, gy + 24 + j * 16), l, font=FONT_BODY_SM, fill=TEXT_MUTED)
        gy += card_h + 10

    # Right Column: Police & Mountain Hazards (width: 442)
    right_x = 490
    right_w = 442
    draw.rounded_rectangle([right_x, 115, right_x + right_w, 495], radius=6, fill=BG_CARD, outline=BORDER_MUTED, width=1)

    draw.rounded_rectangle([right_x + 12, 125, right_x + right_w - 12, 149], radius=3, fill=(35, 46, 68))
    draw.text((right_x + 18, 129), "POLICE PURSUITS & ROAD HAZARDS", font=FONT_SECTION_HDR, fill=RED_ACCENT)

    hazards = [
        ("POLICE PATROL & SPEED TRAPS", (255, 100, 100), [
            "• Highway patrol cruisers lurk behind roadside billboards.",
            "• When your radar detector alerts, tap BRAKE immediately to",
            "  drop below the speed limit.",
            "• If pursued, outrun the squad car before they pull in front,",
            "  or you will be stopped and issued a speeding ticket!"
        ]),
        ("ONCOMING CIVILIAN TRAFFIC", (255, 180, 50), [
            "• Slow-moving civilian cars share the two-lane road.",
            "• Timing your passes is critical: head-on collisions will",
            "  destroy your exotic supercar."
        ]),
        ("CLIFF EDGE DROP-OFF & TUNNELS", (100, 200, 255), [
            "• Mountain switchbacks border sheer drops into deep canyons.",
            "• Tunnels feature tight walls with zero margin for steering errors."
        ])
    ]

    hy = 160
    for htitle, hcol, hlines in hazards:
        h_h = 18 + len(hlines) * 16 + 8
        draw.rounded_rectangle([right_x + 14, hy, right_x + right_w - 14, hy + h_h], radius=4, fill=(28, 36, 52))
        draw.text((right_x + 22, hy + 6), htitle, font=FONT_BODY_BOLD, fill=hcol)
        for k, line in enumerate(hlines):
            draw.text((right_x + 22, hy + 24 + k * 16), line, font=FONT_BODY_SM, fill=TEXT_MUTED)
        hy += h_h + 10

    return im


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages = [
        ("001.png", generate_page_1),
        ("002.png", generate_page_2),
        ("003.png", generate_page_3),
        ("004.png", generate_page_4),
        ("005.png", generate_page_5)
    ]

    for fname, gen_fn in pages:
        out_path = os.path.join(OUTPUT_DIR, fname)
        im = gen_fn()
        im_8bit = im.convert('RGB').quantize(colors=256)
        im_8bit.save(out_path, format="PNG", optimize=True)
        sz_kb = os.path.getsize(out_path) / 1024
        print(f"  -> Saved {out_path} ({sz_kb:.1f} KB, 8-bit indexed)")

    print("\nAll 5 manual pages generated successfully!")


if __name__ == "__main__":
    main()
