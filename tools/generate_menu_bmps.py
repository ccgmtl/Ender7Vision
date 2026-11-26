#!/usr/bin/env python3
"""
Ender7Vision Menu BMP Generator
Generates pixel-perfect 480x272 BMPs for Ender 7 DWIN DGUS-Reloaded
with a unified, modern dark glassmorphic visual signature across ALL screens:
- Page 1: Main Menu (001_home.bmp)
- Page 5: Temperature Menu (005_temp_menu.bmp)
- Page 8: Move & Axes Jog Menu (008_move.bmp)
- Page 9: Settings Menu 1 (009_settings_menu.bmp)
- Page 10: Bed Leveling Menu (010_leveling_menu.bmp)
- Page 18: Settings Menu 2 (018_settings_menu2.bmp)
- Page 21: Klipper Macros Menu (021_macros_menu.bmp)

Coordinates carefully align with DWIN DGUS II text displays (14ShowFile.bin)
and touch bounding boxes (13TouchFile.bin).
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/home/cedric/ender7vision/tools/raw_480x272_bmps"
os.makedirs(OUT_DIR, exist_ok=True)

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# Theme Colors
BG_COLOR = (18, 22, 28)          # #12161c
HEADER_BG = (22, 26, 34)         # #161a22
HEADER_LINE = (38, 48, 64)       # #263040
CARD_BG = (24, 30, 40)           # #181e28
CARD_BORDER = (44, 54, 72)       # #2c3648
TEXT_PRIMARY = (255, 255, 255)
TEXT_MUTED = (148, 163, 184)     # #94a3b8
TEXT_HINT = (100, 116, 139)      # #64748b

def draw_header(draw, title, back_target=None):
    """
    Draws a sleek header bar.
    Crucial: The right side from X=170 to 476 is kept strictly CLEAR of static text
    or badges so Klipper's live status string (VP 0x3000 in 14ShowFile.bin)
    renders crisply without text collisions or visual artifacts.
    """
    draw.rectangle([0, 0, 480, 40], fill=HEADER_BG)
    draw.line([(0, 40), (480, 40)], fill=HEADER_LINE, width=1)
    
    if back_target:
        # Back button pill at (14, 7, 76, 33)
        draw.rounded_rectangle([14, 7, 76, 33], radius=6, fill=(30, 38, 52), outline=(50, 68, 92), width=1)
        font_btn = get_font(FONT_BOLD, 11)
        draw.text((22, 13), f"← {back_target}", fill=(200, 220, 245), font=font_btn)
        title_x = 88
    else:
        # Home title logo badge
        draw.rounded_rectangle([14, 8, 32, 32], radius=4, fill=(0, 210, 255), outline=(0, 180, 220), width=1)
        draw.polygon([(18, 25), (28, 15), (28, 25)], fill=(18, 22, 28))
        title_x = 42

    font_title = get_font(FONT_BOLD, 13)
    draw.text((title_x, 12), title, fill=TEXT_PRIMARY, font=font_title)

def draw_card(draw, box, border_color, fill_color, radius=8, width=2):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill_color, outline=border_color, width=width)

def draw_temp_status_bar(draw):
    """
    Draws dual status pills for Extruder & Bed at Y=208..248
    matching 14ShowFile.bin coordinates:
    Extruder actual at (76, 227), target at (120, 227)
    Bed actual at (328, 227), target at (372, 227)
    """
    # Extruder pill: X=26..236, Y=208..248
    draw.rounded_rectangle([26, 208, 236, 248], radius=8, fill=(24, 30, 40), outline=(0, 180, 220), width=1)
    font_lbl = get_font(FONT_BOLD, 10)
    font_sub = get_font(FONT_REG, 9)
    draw.text((34, 215), "EXTRUDER", fill=(0, 210, 255), font=font_lbl)
    draw.text((34, 231), "ACT / TGT °C", fill=TEXT_MUTED, font=font_sub)
    draw.text((106, 227), "/", fill=(100, 120, 140), font=get_font(FONT_BOLD, 11))
    
    # Bed pill: X=250..460, Y=208..248
    draw.rounded_rectangle([250, 208, 460, 248], radius=8, fill=(24, 30, 40), outline=(245, 158, 11), width=1)
    draw.text((258, 215), "HEATED BED", fill=(245, 158, 11), font=font_lbl)
    draw.text((258, 231), "ACT / TGT °C", fill=TEXT_MUTED, font=font_sub)
    draw.text((358, 227), "/", fill=(100, 120, 140), font=get_font(FONT_BOLD, 11))

# ==============================================================================
# SCREEN 1: 001_home.bmp (Main Menu)
# ==============================================================================
def generate_home_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "CREALITY ENDER-7 COREXY", back_target=None)
    
    # 4 Main Menu Cards: Symmetrical 4-Card Deck (Y=56..194, W=98, H=138)
    cards = [
        {
            "box": (26, 56, 124, 194),
            "title": "TEMP",
            "subtitle": "PREHEAT",
            "border": (0, 210, 255),
            "fill": (22, 32, 42),
            "accent": (0, 210, 255),
            "icon": "temp"
        },
        {
            "box": (138, 56, 236, 194),
            "title": "MOVE",
            "subtitle": "AXES JOG",
            "border": (16, 185, 129),
            "fill": (20, 36, 32),
            "accent": (52, 211, 153),
            "icon": "move"
        },
        {
            "box": (250, 56, 348, 194),
            "title": "SETTINGS",
            "subtitle": "CONFIG",
            "border": (245, 158, 11),
            "fill": (36, 32, 22),
            "accent": (251, 191, 36),
            "icon": "settings"
        },
        {
            "box": (362, 56, 460, 194),
            "title": "MACROS",
            "subtitle": "ROUTINES",
            "border": (168, 85, 247),
            "fill": (34, 24, 44),
            "accent": (192, 132, 252),
            "icon": "macros"
        }
    ]
    
    for c in cards:
        draw_card(draw, c["box"], c["border"], c["fill"], radius=10, width=2)
        cx = (c["box"][0] + c["box"][2]) // 2
        cy = c["box"][1] + 46
        
        # Badge circle
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(30, 40, 55), outline=c["accent"], width=2)
        
        # Vector icons
        if c["icon"] == "temp":
            draw.polygon([(cx, cy - 14), (cx + 8, cy + 4), (cx + 4, cy + 12), (cx - 4, cy + 12), (cx - 8, cy + 4)], fill=c["accent"])
            draw.ellipse([cx - 4, cy + 2, cx + 4, cy + 10], fill=(255, 255, 255))
        elif c["icon"] == "move":
            draw.polygon([(cx, cy - 15), (cx - 6, cy - 8), (cx + 6, cy - 8)], fill=c["accent"])
            draw.polygon([(cx, cy + 15), (cx - 6, cy + 8), (cx + 6, cy + 8)], fill=c["accent"])
            draw.polygon([(cx - 15, cy), (cx - 8, cy - 6), (cx - 8, cy + 6)], fill=c["accent"])
            draw.polygon([(cx + 15, cy), (cx + 8, cy - 6), (cx + 8, cy + 6)], fill=c["accent"])
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
        elif c["icon"] == "settings":
            for deg in [0, 45, 90, 135]:
                draw.rectangle([cx - 14, cy - 3, cx + 14, cy + 3], fill=c["accent"])
                draw.rectangle([cx - 3, cy - 14, cx + 3, cy + 14], fill=c["accent"])
            draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(30, 40, 55))
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        elif c["icon"] == "macros":
            draw.polygon([(cx + 2, cy - 16), (cx - 10, cy), (cx, cy), (cx - 2, cy + 16), (cx + 10, cy), (cx, cy)], fill=c["accent"])
            
        font_title = get_font(FONT_BOLD, 12)
        draw.text((cx, c["box"][1] + 94), c["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 9)
        draw.text((cx, c["box"][1] + 114), c["subtitle"], fill=TEXT_MUTED, font=font_sub, anchor="mt")
        
    draw_temp_status_bar(draw)
    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 5: 005_temp_menu.bmp (Temperature & Preheat Submenu)
# ==============================================================================
def generate_temp_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "TEMPERATURE & PREHEAT", back_target="HOME")
    
    # 4 Cards across Y=79..181 (W=102, H=102)
    cards = [
        {
            "box": (15, 79, 117, 181),
            "title": "PRESETS",
            "subtitle": "PLA / PETG",
            "border": (0, 210, 255),
            "fill": (22, 32, 42),
            "accent": (0, 210, 255),
            "icon": "presets"
        },
        {
            "box": (131, 79, 233, 181),
            "title": "MANUAL",
            "subtitle": "CUSTOM TEMP",
            "border": (16, 185, 129),
            "fill": (20, 36, 32),
            "accent": (52, 211, 153),
            "icon": "manual"
        },
        {
            "box": (247, 79, 349, 181),
            "title": "COOLDOWN",
            "subtitle": "OFF (0°C)",
            "border": (56, 189, 248),
            "fill": (20, 32, 46),
            "accent": (56, 189, 248),
            "icon": "cooldown"
        },
        {
            "box": (363, 79, 465, 181),
            "title": "FAN SPEED",
            "subtitle": "COOLING",
            "border": (245, 158, 11),
            "fill": (36, 32, 22),
            "accent": (251, 191, 36),
            "icon": "fan"
        }
    ]
    
    for c in cards:
        draw_card(draw, c["box"], c["border"], c["fill"], radius=10, width=2)
        cx = (c["box"][0] + c["box"][2]) // 2
        cy = c["box"][1] + 36
        
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(30, 40, 55), outline=c["accent"], width=2)
        
        if c["icon"] == "presets":
            draw.polygon([(cx, cy - 11), (cx + 6, cy + 2), (cx + 3, cy + 8), (cx - 3, cy + 8), (cx - 6, cy + 2)], fill=c["accent"])
        elif c["icon"] == "manual":
            draw.line([(cx - 9, cy - 6), (cx + 9, cy - 6)], fill=c["accent"], width=2)
            draw.ellipse([cx - 4, cy - 9, cx + 2, cy - 3], fill=(255, 255, 255))
            draw.line([(cx - 9, cy + 6), (cx + 9, cy + 6)], fill=c["accent"], width=2)
            draw.ellipse([cx, cy + 3, cx + 6, cy + 9], fill=(255, 255, 255))
        elif c["icon"] == "cooldown":
            draw.line([(cx, cy - 10), (cx, cy + 10)], fill=c["accent"], width=2)
            draw.line([(cx - 10, cy), (cx + 10, cy)], fill=c["accent"], width=2)
            draw.line([(cx - 7, cy - 7), (cx + 7, cy + 7)], fill=c["accent"], width=2)
            draw.line([(cx - 7, cy + 7), (cx + 7, cy - 7)], fill=c["accent"], width=2)
        elif c["icon"] == "fan":
            draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=c["accent"], width=2)
            draw.polygon([(cx, cy), (cx + 7, cy - 6), (cx + 5, cy - 8)], fill=c["accent"])
            draw.polygon([(cx, cy), (cx - 7, cy + 6), (cx - 5, cy + 8)], fill=c["accent"])
            
        font_title = get_font(FONT_BOLD, 11)
        draw.text((cx, c["box"][1] + 66), c["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 8)
        draw.text((cx, c["box"][1] + 82), c["subtitle"], fill=TEXT_MUTED, font=font_sub, anchor="mt")
        
    draw_temp_status_bar(draw)
    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 8: 008_move.bmp (Axes Jog & Control Menu)
# ==============================================================================
def generate_move_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "AXES CONTROL & MOVE", back_target="HOME")
    
    # Left Side: Coordinates Panel
    draw_card(draw, (16, 50, 166, 258), CARD_BORDER, (22, 28, 38), radius=8, width=1)
    font_sec = get_font(FONT_BOLD, 10)
    draw.text((24, 58), "LIVE POSITION", fill=(0, 210, 255), font=font_sec)
    
    axis_rows = [
        {"axis": "X", "y": 76, "accent": (0, 210, 255)},
        {"axis": "Y", "y": 133, "accent": (16, 185, 129)},
        {"axis": "Z", "y": 190, "accent": (245, 158, 11)}
    ]
    font_ax = get_font(FONT_BOLD, 13)
    font_unit = get_font(FONT_REG, 10)
    for r in axis_rows:
        ay = r["y"]
        draw.rounded_rectangle([24, ay, 46, ay + 31], radius=5, fill=(30, 40, 54), outline=r["accent"], width=1)
        draw.text((35, ay + 15), r["axis"], fill=r["accent"], font=font_ax, anchor="mm")
        
        # Coordinate box (DGUS renders live number at 65, ay+7)
        draw.rounded_rectangle([54, ay, 121, ay + 31], radius=5, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
        draw.text((130, ay + 15), "mm", fill=TEXT_MUTED, font=font_unit, anchor="lm")

    draw.text((91, 238), "Tap value to set", fill=TEXT_HINT, font=get_font(FONT_REG, 8), anchor="mm")

    # Center/Right: Jog Direction Controls
    font_btn_lbl = get_font(FONT_BOLD, 10)
    font_chev = get_font(FONT_BOLD, 15)

    def draw_jog_btn(box, border, fill, chevron, label):
        draw_card(draw, box, border, fill, radius=8, width=1)
        bx = (box[0] + box[2]) // 2
        by = (box[1] + box[3]) // 2
        draw.text((bx, by - 5), chevron, fill=(255, 255, 255), font=font_chev, anchor="mm")
        draw.text((bx, by + 13), label, fill=border, font=font_btn_lbl, anchor="mm")

    # Y+ & Y-
    draw_jog_btn((250, 50, 298, 98), (56, 189, 248), (24, 34, 48), "▲", "Y+")
    draw_jog_btn((250, 151, 298, 199), (56, 189, 248), (24, 34, 48), "▼", "Y-")

    # X- & X+
    draw_jog_btn((200, 100, 248, 148), (0, 210, 255), (20, 34, 46), "◀", "X-")
    draw_jog_btn((301, 100, 349, 148), (0, 210, 255), (20, 34, 46), "▶", "X+")

    # Center Home Button (Home All)
    draw_card(draw, (250, 100, 298, 148), (16, 185, 129), (20, 44, 36), radius=8, width=2)
    draw.polygon([(274, 114), (262, 124), (286, 124)], fill=(16, 185, 129))
    draw.rectangle([266, 124, 282, 134], fill=(16, 185, 129))
    draw.text((274, 141), "ALL", fill=(255, 255, 255), font=font_btn_lbl, anchor="mm")

    # Z+ & Z-
    draw_jog_btn((380, 50, 428, 98), (168, 85, 247), (36, 26, 48), "▲", "Z+")
    draw_jog_btn((380, 151, 428, 199), (168, 85, 247), (36, 26, 48), "▼", "Z-")
    draw.text((404, 124), "Z AXIS", fill=(168, 85, 247), font=get_font(FONT_BOLD, 9), anchor="mm")

    # Step Distance Selector (Y=218..256)
    steps = [
        {"box": (237, 218, 295, 256), "text": "0.1 mm"},
        {"box": (297, 218, 355, 256), "text": "1.0 mm"},
        {"box": (357, 218, 415, 256), "text": "10 mm"}
    ]
    font_step = get_font(FONT_BOLD, 9)
    for s in steps:
        draw_card(draw, s["box"], CARD_BORDER, (26, 32, 44), radius=6, width=1)
        sx = (s["box"][0] + s["box"][2]) // 2 + 6
        sy = (s["box"][1] + s["box"][3]) // 2
        draw.text((sx, sy), s["text"], fill=TEXT_PRIMARY, font=font_step, anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 10: 010_leveling_menu.bmp (Bed Leveling & Tramming Submenu)
# ==============================================================================
def generate_leveling_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "BED LEVELING & CALIBRATION", back_target="SETTINGS")
    
    # 3 Cards across Y=93..202 (W=109, H=109)
    cards = [
        {
            "box": (50, 93, 159, 202),
            "title": "MANUAL",
            "subtitle": "4 CORNERS TRAM",
            "border": (16, 185, 129),
            "fill": (20, 36, 32),
            "accent": (52, 211, 153),
            "icon": "manual"
        },
        {
            "box": (184, 93, 293, 202),
            "title": "AUTO MESH",
            "subtitle": "PROBE BED",
            "border": (0, 210, 255),
            "fill": (22, 32, 42),
            "accent": (0, 210, 255),
            "icon": "auto"
        },
        {
            "box": (319, 93, 428, 202),
            "title": "Z-OFFSET",
            "subtitle": "BABYSTEPPING",
            "border": (245, 158, 11),
            "fill": (36, 32, 22),
            "accent": (251, 191, 36),
            "icon": "zoffset"
        }
    ]
    
    for c in cards:
        draw_card(draw, c["box"], c["border"], c["fill"], radius=10, width=2)
        cx = (c["box"][0] + c["box"][2]) // 2
        cy = c["box"][1] + 38
        
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(30, 40, 55), outline=c["accent"], width=2)
        
        if c["icon"] == "manual":
            draw.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], outline=c["accent"], width=1)
            draw.ellipse([cx - 9, cy - 7, cx - 5, cy - 3], fill=c["accent"])
            draw.ellipse([cx + 5, cy - 7, cx + 9, cy - 3], fill=c["accent"])
            draw.ellipse([cx - 9, cy + 3, cx - 5, cy + 7], fill=c["accent"])
            draw.ellipse([cx + 5, cy + 3, cx + 9, cy + 7], fill=c["accent"])
        elif c["icon"] == "auto":
            draw.line([(cx - 10, cy - 5), (cx + 10, cy - 5)], fill=c["accent"], width=1)
            draw.line([(cx - 10, cy + 3), (cx + 10, cy + 3)], fill=c["accent"], width=1)
            draw.line([(cx - 5, cy - 10), (cx - 5, cy + 8)], fill=c["accent"], width=1)
            draw.line([(cx + 5, cy - 10), (cx + 5, cy + 8)], fill=c["accent"], width=1)
            draw.polygon([(cx, cy - 12), (cx - 3, cy - 6), (cx + 3, cy - 6)], fill=(255, 255, 255))
        elif c["icon"] == "zoffset":
            draw.line([(cx, cy - 12), (cx, cy + 12)], fill=c["accent"], width=2)
            draw.polygon([(cx, cy - 14), (cx - 5, cy - 8), (cx + 5, cy - 8)], fill=c["accent"])
            draw.polygon([(cx, cy + 14), (cx - 5, cy + 8), (cx + 5, cy + 8)], fill=c["accent"])
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
            
        font_title = get_font(FONT_BOLD, 12)
        draw.text((cx, c["box"][1] + 70), c["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 8)
        draw.text((cx, c["box"][1] + 88), c["subtitle"], fill=TEXT_MUTED, font=font_sub, anchor="mt")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 9: 009_settings_menu.bmp (Settings Menu 1)
# ==============================================================================
def generate_settings_menu_1(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SYSTEM SETTINGS (1/2)", back_target="HOME")
    
    slots = [
        {"box": (56, 45, 158, 147), "title": "LEVELING", "sub": "CALIBRATE", "border": (0, 210, 255), "accent": (0, 210, 255), "icon": "level"},
        {"box": (189, 45, 291, 147), "title": "FILAMENT", "sub": "LOAD / UNLOAD", "border": (16, 185, 129), "accent": (52, 211, 153), "icon": "filament"},
        {"box": (56, 158, 158, 260), "title": "AUDIO", "sub": "BUZZER", "border": (245, 158, 11), "accent": (251, 191, 36), "icon": "volume"},
        {"box": (189, 158, 291, 260), "title": "DISPLAY", "sub": "BRIGHTNESS", "border": (168, 85, 247), "accent": (192, 132, 252), "icon": "screen"}
    ]
    
    for s in slots:
        draw_card(draw, s["box"], s["border"], CARD_BG, radius=10, width=1)
        cx = (s["box"][0] + s["box"][2]) // 2
        cy = s["box"][1] + 36
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(30, 40, 55), outline=s["accent"], width=2)
        
        font_title = get_font(FONT_BOLD, 10)
        draw.text((cx, s["box"][1] + 66), s["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 8)
        draw.text((cx, s["box"][1] + 82), s["sub"], fill=TEXT_MUTED, font=font_sub, anchor="mt")
        
    # Next Page Button at (321, 45, 423, 147)
    draw_card(draw, (321, 45, 423, 147), (0, 210, 255), (20, 32, 44), radius=10, width=2)
    cx = (321 + 423) // 2
    draw.polygon([(cx - 8, 86), (cx + 8, 96), (cx - 8, 106)], fill=(0, 210, 255))
    draw.text((cx, 116), "NEXT PAGE", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 10), anchor="mt")
    
    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 18: 018_settings_menu2.bmp (Settings Menu 2)
# ==============================================================================
def generate_settings_menu_2(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SYSTEM SETTINGS (2/2)", back_target="PREV")
    
    slots = [
        {"box": (56, 45, 158, 147), "title": "PID TUNE", "sub": "HEATER CAL", "border": CARD_BORDER, "accent": (200, 215, 235)},
        {"box": (189, 45, 291, 147), "title": "ABOUT", "sub": "FIRMWARE INFO", "border": CARD_BORDER, "accent": (200, 215, 235)},
        {"box": (321, 45, 423, 147), "title": "DEBUG 2", "sub": "TERMINAL", "border": CARD_BORDER, "accent": (200, 215, 235)},
        {"box": (56, 158, 158, 260), "title": "DEBUG 1", "sub": "SYSTEM", "border": CARD_BORDER, "accent": (200, 215, 235)},
        {"box": (189, 158, 291, 260), "title": "MACROS", "sub": "QUICK ACTIONS", "border": (168, 85, 247), "accent": (192, 132, 252)},
        {"box": (321, 158, 423, 260), "title": "THEME", "sub": "CYCLE COLOR", "border": (0, 210, 255), "accent": (0, 210, 255)}
    ]
    
    for s in slots:
        draw_card(draw, s["box"], s["border"], CARD_BG, radius=10, width=1)
        cx = (s["box"][0] + s["box"][2]) // 2
        cy = s["box"][1] + 36
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(30, 40, 55), outline=s["accent"], width=2)
        
        font_title = get_font(FONT_BOLD, 10)
        draw.text((cx, s["box"][1] + 66), s["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 8)
        draw.text((cx, s["box"][1] + 82), s["sub"], fill=TEXT_MUTED, font=font_sub, anchor="mt")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 21: 021_macros_menu.bmp (Klipper Macros Menu)
# ==============================================================================
def generate_macros_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "KLIPPER MACROS & ROUTINES", back_target="HOME")
    
    macro_cards = [
        {"box": (15, 46, 235, 92), "title": "NOZZLE CLEAN", "sub": "PURGE & SCRUB", "border": (16, 185, 129), "fill": (20, 36, 32), "accent": (52, 211, 153), "icon": "⚡"},
        {"box": (245, 46, 465, 92), "title": "LOAD FILAMENT", "sub": "EXTRUDE 50MM", "border": (0, 210, 255), "fill": (20, 34, 46), "accent": (0, 210, 255), "icon": "⬇"},
        {"box": (15, 100, 235, 146), "title": "UNLOAD FILAMENT", "sub": "RETRACT 60MM", "border": (168, 85, 247), "fill": (34, 24, 46), "accent": (192, 132, 252), "icon": "⬆"},
        {"box": (245, 100, 465, 146), "title": "PARK & COOLDOWN", "sub": "HOME & OFF", "border": (244, 63, 94), "fill": (44, 22, 30), "accent": (251, 113, 133), "icon": "❄"},
        {"box": (15, 154, 235, 200), "title": "SCREWS TILT ADJ", "sub": "BED LEVEL CHECK", "border": (245, 158, 11), "fill": (38, 30, 20), "accent": (251, 191, 36), "icon": "⚙"},
        {"box": (245, 154, 465, 200), "title": "PROFILE: QUIET", "sub": "STEALTH / 80MM/S", "border": (59, 130, 246), "fill": (20, 28, 44), "accent": (96, 165, 250), "icon": "☾"},
        {"box": (15, 208, 235, 254), "title": "PROFILE: SPORT", "sub": "HIGH SPEED / 250MM/S", "border": (249, 115, 22), "fill": (44, 28, 20), "accent": (251, 146, 60), "icon": "🔥"},
        {"box": (245, 208, 465, 254), "title": "CYCLE THEME", "sub": "TEXT & ACCENT COLOR", "border": (236, 72, 153), "fill": (42, 22, 36), "accent": (244, 114, 182), "icon": "🎨"}
    ]
    
    font_mtitle = get_font(FONT_BOLD, 11)
    font_msub = get_font(FONT_REG, 8)
    font_icon = get_font(FONT_BOLD, 12)
    
    for m in macro_cards:
        draw_card(draw, m["box"], m["border"], m["fill"], radius=8, width=1)
        bx1, by1, bx2, by2 = m["box"]
        
        draw.rounded_rectangle([bx1 + 8, by1 + 7, bx1 + 38, by1 + 39], radius=6, fill=(30, 40, 55), outline=m["accent"], width=1)
        draw.text((bx1 + 23, by1 + 23), m["icon"], fill=m["accent"], font=font_icon, anchor="mm")
        
        draw.text((bx1 + 46, by1 + 12), m["title"], fill=TEXT_PRIMARY, font=font_mtitle)
        draw.text((bx1 + 46, by1 + 28), m["sub"], fill=TEXT_MUTED, font=font_msub)

    img.save(out_path)
    print(f"Generated {out_path}")

def main():
    print("Rendering updated Ender7Vision menus with unified visual signature...")
    generate_home_menu(os.path.join(OUT_DIR, "001_home.bmp"))
    generate_temp_menu(os.path.join(OUT_DIR, "005_temp_menu.bmp"))
    generate_move_menu(os.path.join(OUT_DIR, "008_move.bmp"))
    generate_settings_menu_1(os.path.join(OUT_DIR, "009_settings_menu.bmp"))
    generate_leveling_menu(os.path.join(OUT_DIR, "010_leveling_menu.bmp"))
    generate_settings_menu_2(os.path.join(OUT_DIR, "018_settings_menu2.bmp"))
    generate_macros_menu(os.path.join(OUT_DIR, "021_macros_menu.bmp"))
    print("All menus generated successfully!")

if __name__ == "__main__":
    main()
