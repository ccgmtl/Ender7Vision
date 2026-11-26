#!/usr/bin/env python3
"""
Ender7Vision Menu BMP Generator
Generates pixel-perfect 480x272 BMPs for Ender 7 DWIN DGUS-Reloaded
with a unified, modern dark glassmorphic visual signature across ALL screens:
- Page 1: Main Menu (001_home.bmp)
- Page 5: Temperature Menu (005_temp_menu.bmp)
- Page 6: Manual Temperature Control (006_temp_manual.bmp)
- Page 7: Fan Speed Control (007_fan.bmp)
- Page 8: Move & Axes Jog Menu (008_move.bmp)
- Page 9: Settings Menu 1 (009_settings_menu.bmp)
- Page 10: Bed Leveling Menu (010_leveling_menu.bmp)
- Page 11: Leveling Z-Offset (011_leveling_offset.bmp)
- Page 12: Manual Tramming / 4 Corners (012_leveling_manual.bmp)
- Page 13: Auto Mesh Bed Leveling (013_leveling_automatic.bmp)
- Page 14: Probing Status (014_leveling_probing.bmp)
- Page 15: Filament Load / Unload (015_filament.bmp)
- Page 16: Volume & Audio Settings (016_volume.bmp)
- Page 17: Screen Brightness Settings (017_brightness.bmp)
- Page 18: Settings Menu 2 (018_settings_menu2.bmp)
- Page 19: PID Tuning (019_pid.bmp)
- Page 20: System & Firmware Info (020_information.bmp)
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
    Strict Rule: The right side from X=140 to 476 is kept strictly CLEAR of static text
    or badges so Klipper's live status string (VP 0x3000 in 14ShowFile.bin at X=181..476)
    renders crisply without text collisions, dot artifacts, or overlaps.
    """
    draw.rectangle([0, 0, 480, 40], fill=HEADER_BG)
    draw.line([(0, 40), (480, 40)], fill=HEADER_LINE, width=1)
    
    if back_target:
        # Back button pill at (14, 7, 76, 33)
        draw.rounded_rectangle([14, 7, 76, 33], radius=6, fill=(30, 38, 52), outline=(50, 68, 92), width=1)
        font_btn = get_font(FONT_BOLD, 10)
        draw.text((22, 13), f"← {back_target}", fill=(200, 220, 245), font=font_btn)
        title_x = 86
    else:
        # Home title logo badge
        draw.rounded_rectangle([14, 8, 30, 32], radius=4, fill=(0, 210, 255), outline=(0, 180, 220), width=1)
        draw.polygon([(17, 24), (26, 15), (26, 24)], fill=(18, 22, 28))
        title_x = 38

    # Keep title strictly concise so it ends well before X=140
    font_title = get_font(FONT_BOLD, 12)
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
    
    # Concise title to keep X=120..480 completely clear for Klipper status VP 0x3000
    draw_header(draw, "ENDER-7", back_target=None)
    
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
        
        if c["icon"] == "temp":
            draw.line([(cx, cy - 14), (cx, cy + 8)], fill=c["accent"], width=3)
            draw.ellipse([cx - 7, cy + 5, cx + 7, cy + 17], fill=c["accent"])
        elif c["icon"] == "move":
            draw.polygon([(cx, cy - 14), (cx - 6, cy - 6), (cx + 6, cy - 6)], fill=c["accent"])
            draw.polygon([(cx, cy + 14), (cx - 6, cy + 6), (cx + 6, cy + 6)], fill=c["accent"])
            draw.polygon([(cx - 14, cy), (cx - 6, cy - 6), (cx - 6, cy + 6)], fill=c["accent"])
            draw.polygon([(cx + 14, cy), (cx + 6, cy - 6), (cx + 6, cy + 6)], fill=c["accent"])
        elif c["icon"] == "settings":
            draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=c["accent"], width=3)
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c["accent"])
        elif c["icon"] == "macros":
            draw.polygon([(cx + 1, cy - 14), (cx - 7, cy + 1), (cx, cy + 1), (cx - 2, cy + 14), (cx + 7, cy - 1), (cx, cy - 1)], fill=c["accent"])
            
        font_title = get_font(FONT_BOLD, 12)
        draw.text((cx, c["box"][1] + 82), c["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 9)
        draw.text((cx, c["box"][1] + 102), c["subtitle"], fill=TEXT_MUTED, font=font_sub, anchor="mt")
        
    draw_temp_status_bar(draw)
    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 5: 005_temp_menu.bmp (Temperature Preset & Fan Menu)
# ==============================================================================
def generate_temp_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "TEMPERATURE PRESETS", back_target="HOME")
    
    cards = [
        {
            "box": (15, 79, 117, 181),
            "title": "PRESETS",
            "subtitle": "PLA / ABS / PETG",
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
# SCREEN 6: 006_temp_manual.bmp (Manual Temperature Control)
# ==============================================================================
def generate_temp_manual(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "MANUAL TEMPERATURE", back_target="TEMP")
    
    # Dual Panels: Extruder (top) & Bed (bottom)
    # Extruder Panel: Y=54..148
    draw_card(draw, (20, 54, 460, 148), (0, 210, 255), CARD_BG, radius=10, width=1)
    font_sec = get_font(FONT_BOLD, 12)
    font_sub = get_font(FONT_REG, 9)
    draw.text((36, 68), "NOZZLE HEATER", fill=(0, 210, 255), font=font_sec)
    draw.text((36, 86), "ACTUAL / TARGET °C", fill=TEXT_MUTED, font=font_sub)
    
    # Numpad button at (239, 66, 302, 97)
    draw.rounded_rectangle([239, 66, 302, 97], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((270, 81), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Off button at (193, 105, 286, 141)
    draw.rounded_rectangle([193, 105, 286, 141], radius=6, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((239, 123), "TURN OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Bed Panel: Y=158..252
    draw_card(draw, (20, 158, 460, 252), (245, 158, 11), CARD_BG, radius=10, width=1)
    draw.text((36, 172), "HEATED BED", fill=(245, 158, 11), font=font_sec)
    draw.text((36, 190), "ACTUAL / TARGET °C", fill=TEXT_MUTED, font=font_sub)
    
    # Numpad button at (239, 163, 302, 194)
    draw.rounded_rectangle([239, 163, 302, 194], radius=6, fill=(40, 36, 30), outline=(245, 158, 11), width=1)
    draw.text((270, 178), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Off button at (193, 202, 286, 238)
    draw.rounded_rectangle([193, 202, 286, 238], radius=6, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((239, 220), "TURN OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 10), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 7: 007_fan.bmp (Fan Speed Control)
# ==============================================================================
def generate_fan_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "PART COOLING FAN", back_target="TEMP")
    
    # Main Fan Card
    draw_card(draw, (20, 54, 460, 252), (0, 210, 255), CARD_BG, radius=10, width=1)
    
    font_sec = get_font(FONT_BOLD, 13)
    draw.text((40, 72), "PART COOLING SPEED", fill=(0, 210, 255), font=font_sec)
    draw.text((40, 94), "Adjust PWM speed from 0% to 100%", fill=TEXT_MUTED, font=get_font(FONT_REG, 10))
    
    # Set Value Box at (259, 96, 322, 127)
    draw.rounded_rectangle([259, 96, 322, 127], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((330, 111), "%", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 11), anchor="lm")
    
    # Slider Track at Y=169..199, X=97..381
    draw.rounded_rectangle([97, 180, 381, 188], radius=4, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
    
    # 0% Button at (24, 167, 109, 203)
    draw.rounded_rectangle([24, 167, 85, 203], radius=6, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((54, 185), "OFF (0%)", fill=(251, 113, 133), font=get_font(FONT_BOLD, 9), anchor="mm")
    
    # 100% Button at (370, 167, 455, 203)
    draw.rounded_rectangle([393, 167, 455, 203], radius=6, fill=(20, 36, 32), outline=(16, 185, 129), width=1)
    draw.text((424, 185), "MAX (100%)", fill=(52, 211, 153), font=get_font(FONT_BOLD, 9), anchor="mm")

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
        if chevron:
            draw.text((bx, by - 4), chevron, fill=border, font=font_chev, anchor="mm")
            draw.text((bx, by + 10), label, fill=TEXT_MUTED, font=get_font(FONT_REG, 8), anchor="mm")
        else:
            draw.text((bx, by), label, fill=TEXT_PRIMARY, font=font_btn_lbl, anchor="mm")

    # Y+ at (234, 52, 296, 104)
    draw_jog_btn((234, 52, 296, 104), (16, 185, 129), (20, 36, 32), "▲", "Y+")
    # Y- at (234, 158, 296, 210)
    draw_jog_btn((234, 158, 296, 210), (16, 185, 129), (20, 36, 32), "▼", "Y-")
    # X- at (176, 105, 238, 157)
    draw_jog_btn((176, 105, 238, 157), (0, 210, 255), (22, 32, 42), "◀", "X-")
    # X+ at (292, 105, 354, 157)
    draw_jog_btn((292, 105, 354, 157), (0, 210, 255), (22, 32, 42), "▶", "X+")
    # Home All in center at (238, 105, 292, 157)
    draw_card(draw, (238, 105, 292, 157), (168, 85, 247), (34, 24, 44), radius=8, width=1)
    draw.text((265, 126), "HOME", fill=(192, 132, 252), font=get_font(FONT_BOLD, 9), anchor="mm")
    draw.text((265, 138), "ALL", fill=TEXT_MUTED, font=get_font(FONT_REG, 7), anchor="mm")

    # Z Controls: Z+ at (360, 52, 412, 104), Z- at (360, 158, 412, 210)
    draw_jog_btn((360, 52, 412, 104), (245, 158, 11), (36, 32, 22), "▲", "Z+")
    draw_jog_btn((360, 158, 412, 210), (245, 158, 11), (36, 32, 22), "▼", "Z-")

    # Step Distance Selector at Bottom (Y=218..254)
    steps = [
        {"box": (180, 218, 260, 254), "val": "0.1 mm"},
        {"box": (270, 218, 350, 254), "val": "1.0 mm"},
        {"box": (360, 218, 440, 254), "val": "10.0 mm"}
    ]
    for s in steps:
        draw_card(draw, s["box"], CARD_BORDER, (24, 30, 40), radius=6, width=1)
        draw.text(((s["box"][0] + s["box"][2])//2, (s["box"][1] + s["box"][3])//2), s["val"], fill=TEXT_PRIMARY, font=font_btn_lbl, anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 9: 009_settings_menu.bmp (Settings Menu 1)
# ==============================================================================
def generate_settings_menu_1(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SYSTEM SETTINGS (1/2)", back_target="HOME")
    
    # Exact 6 slots matching original Creality DGUS 13TouchFile layout:
    # Row 0:
    #   Col 0 (56, 45, 158, 147): Page 10 Leveling
    #   Col 1 (189, 45, 291, 147): Page 15 Filament
    #   Col 2 (321, 45, 423, 147): Motor Lock / Stepper Control (VP 0x2015, val 212)
    # Row 1:
    #   Col 0 (56, 158, 158, 260): Page 16 Audio / Buzzer
    #   Col 1 (189, 158, 291, 260): Page 17 Display Brightness
    #   Col 2 (321, 158, 423, 260): Page 18 Settings 2 (NEXT PAGE)
    slots = [
        {"box": (56, 45, 158, 147), "title": "LEVELING", "sub": "CALIBRATE", "border": (0, 210, 255), "accent": (0, 210, 255), "icon": "level"},
        {"box": (189, 45, 291, 147), "title": "FILAMENT", "sub": "LOAD / UNLOAD", "border": (16, 185, 129), "accent": (52, 211, 153), "icon": "filament"},
        {"box": (321, 45, 423, 147), "title": "STEPPERS", "sub": "UNLOCK / LOCK", "border": (239, 68, 68), "accent": (248, 113, 113), "icon": "motor"},
        {"box": (56, 158, 158, 260), "title": "AUDIO", "sub": "BUZZER", "border": (245, 158, 11), "accent": (251, 191, 36), "icon": "volume"},
        {"box": (189, 158, 291, 260), "title": "DISPLAY", "sub": "BRIGHTNESS", "border": (168, 85, 247), "accent": (192, 132, 252), "icon": "screen"},
        {"box": (321, 158, 423, 260), "title": "NEXT PAGE", "sub": "SETTINGS (2/2)", "border": (0, 210, 255), "accent": (0, 210, 255), "icon": "next"}
    ]
    
    for s in slots:
        draw_card(draw, s["box"], s["border"], CARD_BG, radius=10, width=1)
        cx = (s["box"][0] + s["box"][2]) // 2
        cy = s["box"][1] + 36
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(30, 40, 55), outline=s["accent"], width=2)
        
        if s["icon"] == "next":
            draw.polygon([(cx - 6, cy - 8), (cx + 6, cy), (cx - 6, cy + 8)], fill=s["accent"])
        elif s["icon"] == "motor":
            draw.rectangle([cx - 8, cy - 4, cx + 8, cy + 8], outline=s["accent"], width=2)
            draw.arc([cx - 5, cy - 10, cx + 5, cy - 2], 180, 0, fill=s["accent"], width=2)
        
        font_title = get_font(FONT_BOLD, 10)
        draw.text((cx, s["box"][1] + 66), s["title"], fill=TEXT_PRIMARY, font=font_title, anchor="mt")
        font_sub = get_font(FONT_REG, 8)
        draw.text((cx, s["box"][1] + 82), s["sub"], fill=TEXT_MUTED, font=font_sub, anchor="mt")
    
    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 10: 010_leveling_menu.bmp (Bed Leveling Hub)
# ==============================================================================
def generate_leveling_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "BED LEVELING CALIBRATION", back_target="CONFIG")
    
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
# SCREEN 11: 011_leveling_offset.bmp (Z-Offset Babystepping)
# ==============================================================================
def generate_leveling_offset(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "Z-OFFSET BABYSTEPPING", back_target="LEVEL")
    
    # Main Card
    draw_card(draw, (20, 50, 460, 255), (245, 158, 11), CARD_BG, radius=10, width=1)
    
    # Up Button at (213, 65, 262, 97)
    draw.rounded_rectangle([213, 65, 262, 97], radius=6, fill=(36, 32, 22), outline=(245, 158, 11), width=1)
    draw.polygon([(237, 72), (225, 88), (249, 88)], fill=(245, 158, 11))
    
    # Value Box at (206, 98, 269, 129)
    draw.rounded_rectangle([206, 98, 269, 129], radius=6, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
    draw.text((276, 113), "mm", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 10), anchor="lm")
    
    # Down Button at (213, 130, 262, 162)
    draw.rounded_rectangle([213, 130, 262, 162], radius=6, fill=(36, 32, 22), outline=(245, 158, 11), width=1)
    draw.polygon([(237, 155), (225, 139), (249, 139)], fill=(245, 158, 11))
    
    # Step Selectors: 0.01mm at (201, 179, 259, 217), 0.05mm at (261, 179, 319, 217)
    draw.rounded_rectangle([201, 179, 259, 217], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((230, 198), "0.01", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 10), anchor="mm")
    draw.rounded_rectangle([261, 179, 319, 217], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((290, 198), "0.05", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Save button at (307, 96, 394, 132)
    draw.rounded_rectangle([307, 96, 394, 132], radius=6, fill=(20, 36, 32), outline=(16, 185, 129), width=1)
    draw.text((350, 114), "SAVE", fill=(52, 211, 153), font=get_font(FONT_BOLD, 11), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 12: 012_leveling_manual.bmp (4 Corners Bed Tramming)
# ==============================================================================
def generate_leveling_manual(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "MANUAL BED TRAMMING", back_target="LEVEL")
    
    # Bed Graphic on Left: (20, 50, 220, 255)
    draw_card(draw, (20, 50, 220, 255), CARD_BORDER, (22, 28, 38), radius=8, width=1)
    draw.rectangle([34, 68, 206, 238], outline=(50, 68, 92), width=1)
    
    # 5 Touch Points on Bed:
    # 1: Center (88, 122, 150, 184)
    # 2: Front Left (24, 186, 86, 248)
    # 3: Front Right (152, 186, 214, 248)
    # 4: Back Right (152, 58, 214, 120)
    # 5: Back Left (24, 58, 86, 120)
    points = [
        {"box": (88, 122, 150, 184), "label": "CENTER", "col": (0, 210, 255)},
        {"box": (24, 186, 86, 248), "label": "FL (1)", "col": (16, 185, 129)},
        {"box": (152, 186, 214, 248), "label": "FR (2)", "col": (16, 185, 129)},
        {"box": (152, 58, 214, 120), "label": "BR (3)", "col": (16, 185, 129)},
        {"box": (24, 58, 86, 120), "label": "BL (4)", "col": (16, 185, 129)}
    ]
    font_pt = get_font(FONT_BOLD, 9)
    for p in points:
        draw.ellipse(p["box"], fill=(30, 40, 54), outline=p["col"], width=2)
        cx = (p["box"][0] + p["box"][2]) // 2
        cy = (p["box"][1] + p["box"][3]) // 2
        draw.text((cx, cy), p["label"], fill=p["col"], font=font_pt, anchor="mm")
        
    # Right Side: Temperature Status Panel (230, 50, 460, 255)
    draw_card(draw, (230, 50, 460, 255), CARD_BORDER, CARD_BG, radius=8, width=1)
    draw.text((245, 62), "TRAMMING PREHEAT", fill=(0, 210, 255), font=get_font(FONT_BOLD, 11))
    
    # Extruder target numpad at (352, 69, 415, 100), off at (305, 108, 398, 144)
    draw.rounded_rectangle([352, 69, 415, 100], radius=5, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((383, 84), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 9), anchor="mm")
    draw.rounded_rectangle([305, 108, 398, 144], radius=5, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((351, 126), "NOZZLE OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 9), anchor="mm")
    
    # Bed target numpad at (352, 166, 415, 197), off at (305, 205, 398, 241)
    draw.rounded_rectangle([352, 166, 415, 197], radius=5, fill=(40, 36, 30), outline=(245, 158, 11), width=1)
    draw.text((383, 181), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 9), anchor="mm")
    draw.rounded_rectangle([305, 205, 398, 241], radius=5, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((351, 223), "BED OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 9), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 13: 013_leveling_automatic.bmp (Auto Mesh Bed Leveling)
# ==============================================================================
def generate_leveling_automatic(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "AUTO BED MESH (5x5)", back_target="LEVEL")
    
    # Left Side: Action Buttons
    # Start Probing at (38, 65, 144, 103)
    draw.rounded_rectangle([38, 65, 144, 103], radius=8, fill=(20, 36, 32), outline=(16, 185, 129), width=2)
    draw.text((91, 84), "START MESH", fill=(52, 211, 153), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Stop / Abort at (38, 110, 144, 148)
    draw.rounded_rectangle([38, 110, 144, 148], radius=8, fill=(44, 24, 30), outline=(244, 63, 94), width=2)
    draw.text((91, 129), "ABORT", fill=(251, 113, 133), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # 5x5 Mesh Grid Visual Box at (176, 50, 460, 160)
    draw_card(draw, (176, 50, 460, 160), CARD_BORDER, (22, 28, 38), radius=8, width=1)
    draw.text((188, 56), "5x5 HEIGHTMAP MATRIX", fill=(0, 210, 255), font=get_font(FONT_BOLD, 9))
    
    # Bottom Temperature Panel (Y=170..260)
    draw_card(draw, (20, 170, 460, 260), CARD_BORDER, CARD_BG, radius=8, width=1)
    draw.text((36, 176), "PREHEAT FOR PROBING", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 9))
    
    # Extruder Set (135, 181, 198, 212), Off (86, 220, 179, 256)
    draw.rounded_rectangle([135, 181, 198, 212], radius=4, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((166, 196), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 8), anchor="mm")
    draw.rounded_rectangle([86, 220, 179, 256], radius=4, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((132, 238), "NOZZLE OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 8), anchor="mm")
    
    # Bed Set (345, 181, 408, 212), Off (296, 220, 389, 256)
    draw.rounded_rectangle([345, 181, 408, 212], radius=4, fill=(40, 36, 30), outline=(245, 158, 11), width=1)
    draw.text((376, 196), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 8), anchor="mm")
    draw.rounded_rectangle([296, 220, 389, 256], radius=4, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((342, 238), "BED OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 8), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 14: 014_leveling_probing.bmp (Auto Mesh Probing Animated Screen)
# ==============================================================================
def generate_leveling_probing(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "AUTO MESH PROBING...", back_target=None)
    
    # Progress Card in center
    draw_card(draw, (60, 60, 420, 230), (0, 210, 255), CARD_BG, radius=12, width=1)
    
    font_lg = get_font(FONT_BOLD, 14)
    font_md = get_font(FONT_REG, 11)
    draw.text((240, 95), "MEASURING BED SURFACE", fill=(0, 210, 255), font=font_lg, anchor="mm")
    draw.text((240, 125), "Please wait while BLTouch / CR Touch probes 25 points...", fill=TEXT_MUTED, font=font_md, anchor="mm")
    
    # Animated-style progress bar track
    draw.rounded_rectangle([100, 160, 380, 175], radius=6, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
    draw.rounded_rectangle([102, 162, 260, 173], radius=4, fill=(0, 210, 255))
    
    draw.text((240, 195), "DO NOT POWER OFF OR TOUCH BED", fill=(244, 63, 94), font=get_font(FONT_BOLD, 10), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 15: 015_filament.bmp (Filament Load / Unload)
# ==============================================================================
def generate_filament_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "FILAMENT LOAD & UNLOAD", back_target="CONFIG")
    
    # Load & Unload Buttons:
    # Retract / Unload at (127, 105, 231, 143)
    draw.rounded_rectangle([127, 105, 231, 143], radius=8, fill=(34, 24, 46), outline=(168, 85, 247), width=1)
    draw.text((179, 124), "RETRACT (UNLOAD)", fill=(192, 132, 252), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Extrude / Load at (248, 105, 352, 143)
    draw.rounded_rectangle([248, 105, 352, 143], radius=8, fill=(20, 36, 32), outline=(16, 185, 129), width=1)
    draw.text((300, 124), "EXTRUDE (LOAD)", fill=(52, 211, 153), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Length Selector at (240, 61, 303, 92)
    draw.rounded_rectangle([240, 61, 303, 92], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((140, 76), "FEED DISTANCE:", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 10))
    draw.text((310, 76), "mm", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 10))
    
    # Extruder Temp Panel at Y=160..252
    draw_card(draw, (20, 160, 460, 252), CARD_BORDER, CARD_BG, radius=8, width=1)
    draw.text((40, 174), "NOZZLE HEATER", fill=(0, 210, 255), font=get_font(FONT_BOLD, 11))
    
    # Set Temp at (240, 176, 303, 207)
    draw.rounded_rectangle([240, 176, 303, 207], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((271, 191), "SET", fill=TEXT_PRIMARY, font=get_font(FONT_BOLD, 9), anchor="mm")
    
    # Turn Off at (193, 215, 286, 251)
    draw.rounded_rectangle([193, 215, 286, 251], radius=6, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((239, 233), "HEATER OFF", fill=(251, 113, 133), font=get_font(FONT_BOLD, 9), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 16: 016_volume.bmp (Buzzer & Sound Settings)
# ==============================================================================
def generate_volume_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "AUDIO & BUZZER VOLUME", back_target="CONFIG")
    
    draw_card(draw, (20, 54, 460, 252), (245, 158, 11), CARD_BG, radius=10, width=1)
    
    font_sec = get_font(FONT_BOLD, 13)
    draw.text((40, 72), "TOUCH SOUND & BUZZER", fill=(245, 158, 11), font=font_sec)
    draw.text((40, 94), "Adjust system beep volume from 0% to 100%", fill=TEXT_MUTED, font=get_font(FONT_REG, 10))
    
    # Set Value Box at (251, 96, 314, 127)
    draw.rounded_rectangle([251, 96, 314, 127], radius=6, fill=(40, 36, 30), outline=(245, 158, 11), width=1)
    draw.text((322, 111), "%", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 11), anchor="lm")
    
    # Slider Track at Y=169..199, X=97..381
    draw.rounded_rectangle([97, 180, 381, 188], radius=4, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
    
    # MUTE Button at (24, 167, 109, 203)
    draw.rounded_rectangle([24, 167, 85, 203], radius=6, fill=(44, 24, 30), outline=(244, 63, 94), width=1)
    draw.text((54, 185), "MUTE (0%)", fill=(251, 113, 133), font=get_font(FONT_BOLD, 9), anchor="mm")
    
    # 100% Button at (370, 167, 455, 203)
    draw.rounded_rectangle([393, 167, 455, 203], radius=6, fill=(20, 36, 32), outline=(16, 185, 129), width=1)
    draw.text((424, 185), "MAX (100%)", fill=(52, 211, 153), font=get_font(FONT_BOLD, 9), anchor="mm")

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 17: 017_brightness.bmp (Screen Brightness Settings)
# ==============================================================================
def generate_brightness_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "DISPLAY BACKLIGHT", back_target="CONFIG")
    
    draw_card(draw, (20, 54, 460, 252), (168, 85, 247), CARD_BG, radius=10, width=1)
    
    font_sec = get_font(FONT_BOLD, 13)
    draw.text((40, 72), "SCREEN BRIGHTNESS", fill=(192, 132, 252), font=font_sec)
    draw.text((40, 94), "Adjust LCD backlight level from 10% to 100%", fill=TEXT_MUTED, font=get_font(FONT_REG, 10))
    
    # Set Value Box at (262, 96, 325, 127)
    draw.rounded_rectangle([262, 96, 325, 127], radius=6, fill=(34, 24, 46), outline=(168, 85, 247), width=1)
    draw.text((333, 111), "%", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 11), anchor="lm")
    
    # Slider Track at Y=169..199, X=97..381
    draw.rounded_rectangle([97, 180, 381, 188], radius=4, fill=(16, 20, 28), outline=(60, 75, 100), width=1)
    
    # Min Button at (24, 167, 109, 203)
    draw.rounded_rectangle([24, 167, 85, 203], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((54, 185), "DIM (10%)", fill=(0, 210, 255), font=get_font(FONT_BOLD, 9), anchor="mm")
    
    # Max Button at (370, 167, 455, 203)
    draw.rounded_rectangle([393, 167, 455, 203], radius=6, fill=(20, 36, 32), outline=(16, 185, 129), width=1)
    draw.text((424, 185), "MAX (100%)", fill=(52, 211, 153), font=get_font(FONT_BOLD, 9), anchor="mm")

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
        {"box": (56, 45, 158, 147), "title": "PID TUNE", "sub": "HEATER CAL", "border": (0, 210, 255), "accent": (0, 210, 255), "icon": "pid"},
        {"box": (189, 45, 291, 147), "title": "ABOUT", "sub": "FIRMWARE INFO", "border": (16, 185, 129), "accent": (52, 211, 153), "icon": "info"},
        {"box": (321, 45, 423, 147), "title": "DEBUG 2", "sub": "TERMINAL", "border": CARD_BORDER, "accent": (200, 215, 235), "icon": "term"},
        {"box": (56, 158, 158, 260), "title": "DEBUG 1", "sub": "SYSTEM", "border": CARD_BORDER, "accent": (200, 215, 235), "icon": "sys"},
        {"box": (189, 158, 291, 260), "title": "MACROS", "sub": "QUICK ACTIONS", "border": (168, 85, 247), "accent": (192, 132, 252), "icon": "macros"},
        {"box": (321, 158, 423, 260), "title": "THEME", "sub": "CYCLE COLOR", "border": (245, 158, 11), "accent": (251, 191, 36), "icon": "theme"}
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
# SCREEN 19: 019_pid.bmp (PID Calibration)
# ==============================================================================
def generate_pid_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "HEATER PID AUTOTUNE", back_target="CONFIG")
    
    # Left Card: Heater Select & Target
    draw_card(draw, (20, 50, 230, 255), (0, 210, 255), CARD_BG, radius=8, width=1)
    
    # Heater Selectors: Nozzle at (170, 49, 236, 85), Bed at (243, 49, 309, 85)
    draw.rounded_rectangle([35, 60, 115, 95], radius=6, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    draw.text((75, 77), "NOZZLE", fill=(0, 210, 255), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    draw.rounded_rectangle([125, 60, 205, 95], radius=6, fill=(40, 36, 30), outline=(245, 158, 11), width=1)
    draw.text((165, 77), "BED", fill=(245, 158, 11), font=get_font(FONT_BOLD, 10), anchor="mm")
    
    # Target Temperature Numpad at (168, 124, 231, 155)
    draw.text((35, 139), "TARGET TEMP:", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 10))
    draw.rounded_rectangle([168, 124, 231, 155], radius=5, fill=(30, 40, 54), outline=(0, 210, 255), width=1)
    
    # Start PID Button at (111, 182, 204, 220)
    draw.rounded_rectangle([111, 182, 204, 220], radius=8, fill=(20, 36, 32), outline=(16, 185, 129), width=2)
    draw.text((157, 201), "START PID", fill=(52, 211, 153), font=get_font(FONT_BOLD, 11), anchor="mm")
    
    # Right Card: PID Values Display (Kp, Ki, Kd)
    draw_card(draw, (245, 50, 460, 255), CARD_BORDER, (22, 28, 38), radius=8, width=1)
    draw.text((260, 62), "TUNED PID CONSTANTS", fill=(0, 210, 255), font=get_font(FONT_BOLD, 10))
    
    pid_rows = [("Kp", 100), ("Ki", 150), ("Kd", 200)]
    for name, y in pid_rows:
        draw.text((265, y), f"{name}:", fill=TEXT_MUTED, font=get_font(FONT_BOLD, 12))
        draw.rounded_rectangle([305, y - 5, 435, y + 25], radius=5, fill=(16, 20, 28), outline=(60, 75, 100), width=1)

    img.save(out_path)
    print(f"Generated {out_path}")

# ==============================================================================
# SCREEN 20: 020_information.bmp (System & Firmware Info)
# ==============================================================================
def generate_info_menu(out_path):
    img = Image.new("RGB", (480, 272), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, "SYSTEM INFORMATION", back_target="CONFIG")
    
    # Main Glassmorphic Card
    draw_card(draw, (20, 50, 460, 255), CARD_BORDER, CARD_BG, radius=10, width=1)
    
    font_lbl = get_font(FONT_BOLD, 11)
    
    rows = [
        ("FIRMWARE", "Klipper + DGUS-Reloaded", 75),
        ("UI ENGINE", "Ender7Vision Glassmorphic v1.1.4", 113),
        ("PRINTER", "Creality Ender-7 CoreXY (250x250x300)", 151)
    ]
    
    for lbl, desc, y in rows:
        draw.text((40, y), lbl, fill=(0, 210, 255), font=font_lbl)
        # 14ShowFile text control positions:
        # VP 0x3133 at (183, 78)
        # VP 0x314B at (183, 116)
        # VP 0x3163 at (183, 154)
        draw.line([(40, y + 22), (440, y + 22)], fill=(32, 42, 56), width=1)
        
    # Reset / Diagnostic Button at (49, 186, 240, 217)
    draw.rounded_rectangle([49, 186, 240, 217], radius=6, fill=(30, 38, 52), outline=(50, 68, 92), width=1)
    draw.text((144, 201), "SYSTEM DIAGNOSTICS", fill=(200, 220, 245), font=get_font(FONT_BOLD, 10), anchor="mm")

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
    generate_temp_manual(os.path.join(OUT_DIR, "006_temp_manual.bmp"))
    generate_fan_menu(os.path.join(OUT_DIR, "007_fan.bmp"))
    generate_move_menu(os.path.join(OUT_DIR, "008_move.bmp"))
    generate_settings_menu_1(os.path.join(OUT_DIR, "009_settings_menu.bmp"))
    generate_leveling_menu(os.path.join(OUT_DIR, "010_leveling_menu.bmp"))
    generate_leveling_offset(os.path.join(OUT_DIR, "011_leveling_offset.bmp"))
    generate_leveling_manual(os.path.join(OUT_DIR, "012_leveling_manual.bmp"))
    generate_leveling_automatic(os.path.join(OUT_DIR, "013_leveling_automatic.bmp"))
    generate_leveling_probing(os.path.join(OUT_DIR, "014_leveling_probing.bmp"))
    generate_filament_menu(os.path.join(OUT_DIR, "015_filament.bmp"))
    generate_volume_menu(os.path.join(OUT_DIR, "016_volume.bmp"))
    generate_brightness_menu(os.path.join(OUT_DIR, "017_brightness.bmp"))
    generate_settings_menu_2(os.path.join(OUT_DIR, "018_settings_menu2.bmp"))
    generate_pid_menu(os.path.join(OUT_DIR, "019_pid.bmp"))
    generate_info_menu(os.path.join(OUT_DIR, "020_information.bmp"))
    generate_macros_menu(os.path.join(OUT_DIR, "021_macros_menu.bmp"))
    print("All 18 menu screens generated successfully with unified visual signature!")

if __name__ == "__main__":
    main()
