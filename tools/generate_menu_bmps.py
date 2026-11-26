#!/usr/bin/env python3
"""
Ender7Vision Menu Generator
Generates visually cohesive, geometrically synchronized menu screens for DWIN DGUS II:
- 001_home.bmp (4 balanced cards + bottom temp status bar)
- 009_settings_menu.bmp (Page 1 settings with matching card styling)
- 018_settings_menu2.bmp (Page 2 settings with matching card styling)
- 021_macros_menu.bmp (8 Quick Action macro cards with matching visual signature)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_header(draw, title, subtitle=None, back_btn=True, back_target="HOME"):
    # Header bar background
    draw.rectangle([0, 0, 480, 42], fill=(22, 26, 34))
    draw.line([0, 42, 480, 42], fill=(45, 52, 64), width=1)
    
    if back_btn:
        # Back button pill
        draw.rounded_rectangle([10, 8, 72, 34], radius=6, fill=(35, 42, 54), outline=(70, 82, 102), width=1)
        font_btn = get_font(FONT_BOLD, 11)
        draw.text((18, 14), f"← {back_target}", fill=(200, 215, 235), font=font_btn)
        title_x = 84
    else:
        title_x = 20
        
    font_title = get_font(FONT_BOLD, 15)
    draw.text((title_x, 11), title, fill=(255, 255, 255), font=font_title)
    
    if subtitle:
        font_sub = get_font(FONT_REG, 10)
        draw.text((title_x + draw.textlength(title, font=font_title) + 12, 16), subtitle, fill=(140, 160, 185), font=font_sub)

def draw_card(draw, box, border_color, fill_color, radius=10):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill_color, outline=border_color, width=2)

def generate_home_menu(out_path):
    img = Image.new("RGB", (480, 272), (18, 22, 28))
    draw = ImageDraw.Draw(img)
    
    # Top Header
    draw_header(draw, "CREALITY ENDER-7", "DGUS-Reloaded CoreXY", back_btn=False)
    
    # 4 Main Menu Cards (Side by Side, perfectly symmetrical)
    # Width = 98, Height = 138, Y = 56..194
    # X margins = 26, Gaps = 14 (26 + 98 + 14 + 98 + 14 + 98 + 14 + 98 + 26 = 480)
    cards = [
        {
            "box": (26, 56, 124, 194),
            "title": "TEMP",
            "subtitle": "PREHEAT",
            "border": (0, 210, 255),     # Cyan
            "fill": (24, 30, 40),
            "accent": (0, 220, 255),
            "icon": "temp"
        },
        {
            "box": (138, 56, 236, 194),
            "title": "MOVE",
            "subtitle": "AXES JOG",
            "border": (16, 185, 129),    # Green
            "fill": (22, 34, 32),
            "accent": (52, 211, 153),
            "icon": "move"
        },
        {
            "box": (250, 56, 348, 194),
            "title": "SETTINGS",
            "subtitle": "CONFIG",
            "border": (245, 158, 11),    # Amber
            "fill": (36, 32, 24),
            "accent": (251, 191, 36),
            "icon": "settings"
        },
        {
            "box": (362, 56, 460, 194),
            "title": "MACROS",
            "subtitle": "ROUTINES",
            "border": (168, 85, 247),    # Purple
            "fill": (34, 24, 44),
            "accent": (192, 132, 252),
            "icon": "macros"
        }
    ]
    
    font_card_title = get_font(FONT_BOLD, 13)
    font_card_sub = get_font(FONT_BOLD, 9)
    
    for c in cards:
        draw_card(draw, c["box"], c["border"], c["fill"], radius=12)
        cx = (c["box"][0] + c["box"][2]) // 2
        
        # Icon badge (circle/square at upper center)
        badge_box = [cx - 24, c["box"][1] + 16, cx + 24, c["box"][1] + 64]
        draw.rounded_rectangle(badge_box, radius=10, fill=(30, 36, 48), outline=c["accent"], width=1)
        
        # Draw vector icon inside badge
        icx, icy = (badge_box[0] + badge_box[2]) // 2, (badge_box[1] + badge_box[3]) // 2
        acc = c["accent"]
        if c["icon"] == "temp":
            # Thermometer
            draw.rectangle([icx - 3, icy - 14, icx + 3, icy + 4], fill=acc)
            draw.ellipse([icx - 7, icy + 1, icx + 7, icy + 15], fill=acc)
            draw.ellipse([icx - 3, icy + 5, icx + 3, icy + 11], fill=(255, 255, 255))
        elif c["icon"] == "move":
            # 4-way arrow cross
            draw.polygon([(icx, icy - 14), (icx - 6, icy - 7), (icx + 6, icy - 7)], fill=acc)
            draw.polygon([(icx, icy + 14), (icx - 6, icy + 7), (icx + 6, icy + 7)], fill=acc)
            draw.polygon([(icx - 14, icy), (icx - 7, icy - 6), (icx - 7, icy + 6)], fill=acc)
            draw.polygon([(icx + 14, icy), (icx + 7, icy - 6), (icx + 7, icy + 6)], fill=acc)
            draw.rectangle([icx - 2, icy - 7, icx + 2, icy + 7], fill=acc)
            draw.rectangle([icx - 7, icy - 2, icx + 7, icy + 2], fill=acc)
        elif c["icon"] == "settings":
            # Cogwheel
            draw.ellipse([icx - 12, icy - 12, icx + 12, icy + 12], outline=acc, width=3)
            draw.ellipse([icx - 5, icy - 5, icx + 5, icy + 5], fill=acc)
            for angle in [0, 45, 90, 135]:
                # Teeth markers
                pass
            draw.rectangle([icx - 2, icy - 15, icx + 2, icy + 15], fill=acc)
            draw.rectangle([icx - 15, icy - 2, icx + 15, icy + 2], fill=acc)
        elif c["icon"] == "macros":
            # Lightning bolt
            bolt = [(icx + 2, icy - 14), (icx - 9, icy), (icx - 1, icy), (icx - 4, icy + 14), (icx + 9, icy - 1), (icx + 1, icy - 1)]
            draw.polygon(bolt, fill=acc)
            
        # Card Title
        tw = draw.textlength(c["title"], font=font_card_title)
        draw.text((cx - tw // 2, c["box"][1] + 80), c["title"], fill=(255, 255, 255), font=font_card_title)
        
        # Card Subtitle
        sw = draw.textlength(c["subtitle"], font=font_card_sub)
        draw.text((cx - sw // 2, c["box"][1] + 104), c["subtitle"], fill=c["accent"], font=font_card_sub)
        
    # Bottom Temperature Status Bar (Aligned with DWIN 14ShowFile.bin coordinates at y=227)
    # Left status pill: Extruder (26..236, matches Cards 1+2 width)
    draw.rounded_rectangle([26, 210, 236, 258], radius=10, fill=(24, 28, 36), outline=(50, 60, 75), width=1)
    # Extruder icon & labels
    draw.rectangle([38, 222, 48, 232], fill=(0, 210, 255))
    draw.polygon([(38, 232), (48, 232), (43, 238)], fill=(0, 210, 255))
    font_stat_lbl = get_font(FONT_BOLD, 9)
    draw.text((54, 215), "NOZZLE", fill=(140, 160, 185), font=font_stat_lbl)
    # Separator slash between current and target temp
    font_stat_val = get_font(FONT_BOLD, 12)
    draw.text((106, 225), "/", fill=(100, 115, 130), font=font_stat_val)
    draw.text((146, 225), "°C", fill=(100, 115, 130), font=font_stat_lbl)
    
    # Right status pill: Bed (250..460, matches Cards 3+4 width)
    draw.rounded_rectangle([250, 210, 460, 258], radius=10, fill=(24, 28, 36), outline=(50, 60, 75), width=1)
    # Bed icon & labels
    draw.rectangle([262, 230, 276, 236], fill=(245, 158, 11))
    draw.line([264, 223, 267, 227], fill=(245, 158, 11), width=1)
    draw.line([269, 223, 271, 227], fill=(245, 158, 11), width=1)
    draw.line([274, 223, 276, 227], fill=(245, 158, 11), width=1)
    draw.text((284, 215), "HEATED BED", fill=(140, 160, 185), font=font_stat_lbl)
    draw.text((358, 225), "/", fill=(100, 115, 130), font=font_stat_val)
    draw.text((398, 225), "°C", fill=(100, 115, 130), font=font_stat_lbl)
    
    img.save(out_path, format="BMP")
    print(f"Generated {out_path} (480x272)")

def generate_settings_menu2(out_path):
    img = Image.new("RGB", (480, 272), (18, 22, 28))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SETTINGS", "Page 2 of 2", back_btn=True, back_target="PREV")
    
    # 6 Slots in 3x2 grid:
    # Row 1: Y: 45 to 147 (w=102, h=102)
    # Row 2: Y: 158 to 260 (w=102, h=102)
    # Col 1: 56..158, Col 2: 189..291, Col 3: 321..423
    slots = [
        {
            "box": (56, 45, 158, 147),
            "title": "BLTOUCH",
            "desc": "Pin Up/Down",
            "border": (0, 210, 255),
            "accent": (0, 220, 255),
            "fill": (24, 30, 40),
            "icon": "probe"
        },
        {
            "box": (189, 45, 291, 147),
            "title": "PID TUNE",
            "desc": "Calibrate",
            "border": (245, 158, 11),
            "accent": (251, 191, 36),
            "fill": (36, 32, 24),
            "icon": "pid"
        },
        {
            "box": (321, 45, 423, 147),
            "title": "INFO",
            "desc": "Version & Sys",
            "border": (100, 116, 139),
            "accent": (148, 163, 184),
            "fill": (26, 30, 38),
            "icon": "info"
        },
        {
            "box": (56, 158, 158, 260),
            "title": "PAGE 1",
            "desc": "Level & Motor",
            "border": (71, 85, 105),
            "accent": (148, 163, 184),
            "fill": (24, 28, 36),
            "icon": "prev"
        },
        {
            "box": (189, 158, 291, 260),
            "title": "MACROS",
            "desc": "Quick Actions",
            "border": (168, 85, 247),
            "accent": (192, 132, 252),
            "fill": (34, 24, 44),
            "icon": "macros"
        },
        {
            "box": (321, 158, 423, 260),
            "title": "COLOR",
            "desc": "Cycle Theme",
            "border": (236, 72, 153),
            "accent": (244, 114, 182),
            "fill": (38, 24, 34),
            "icon": "color"
        }
    ]
    
    font_title = get_font(FONT_BOLD, 12)
    font_desc = get_font(FONT_REG, 9)
    
    for s in slots:
        draw_card(draw, s["box"], s["border"], s["fill"], radius=10)
        cx = (s["box"][0] + s["box"][2]) // 2
        cy = s["box"][1] + 36
        acc = s["accent"]
        
        # Draw icon
        if s["icon"] == "probe":
            draw.rectangle([cx - 4, cy - 14, cx + 4, cy + 6], fill=acc)
            draw.polygon([(cx - 2, cy + 6), (cx + 2, cy + 6), (cx, cy + 14)], fill=(255, 255, 255))
        elif s["icon"] == "pid":
            draw.arc([cx - 12, cy - 12, cx + 12, cy + 12], start=180, end=360, fill=acc, width=3)
            draw.line([cx, cy, cx + 8, cy - 8], fill=(255, 255, 255), width=2)
        elif s["icon"] == "info":
            draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=acc, width=2)
            draw.text((cx - 2, cy - 7), "i", fill=acc, font=font_title)
        elif s["icon"] == "prev":
            draw.polygon([(cx - 8, cy), (cx + 4, cy - 10), (cx + 4, cy + 10)], fill=acc)
        elif s["icon"] == "macros":
            bolt = [(cx + 2, cy - 12), (cx - 7, cy), (cx - 1, cy), (cx - 3, cy + 12), (cx + 7, cy - 1), (cx + 1, cy - 1)]
            draw.polygon(bolt, fill=acc)
        elif s["icon"] == "color":
            # Color palette
            draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=acc)
            draw.ellipse([cx - 7, cy - 6, cx - 3, cy - 2], fill=(255, 255, 255))
            draw.ellipse([cx + 3, cy - 6, cx + 7, cy - 2], fill=(0, 210, 255))
            draw.ellipse([cx - 2, cy + 3, cx + 2, cy + 7], fill=(245, 158, 11))
            
        tw = draw.textlength(s["title"], font=font_title)
        draw.text((cx - tw // 2, s["box"][1] + 62), s["title"], fill=(255, 255, 255), font=font_title)
        dw = draw.textlength(s["desc"], font=font_desc)
        draw.text((cx - dw // 2, s["box"][1] + 82), s["desc"], fill=s["accent"], font=font_desc)
        
    img.save(out_path, format="BMP")
    print(f"Generated {out_path} (480x272)")

def generate_settings_menu1(out_path):
    img = Image.new("RGB", (480, 272), (18, 22, 28))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SETTINGS", "Page 1 of 2", back_btn=True, back_target="HOME")
    
    slots = [
        {
            "box": (56, 45, 158, 147),
            "title": "LEVELING",
            "desc": "Bed Tram & Mesh",
            "border": (0, 210, 255),
            "accent": (0, 220, 255),
            "fill": (24, 30, 40),
            "icon": "level"
        },
        {
            "box": (189, 45, 291, 147),
            "title": "FILAMENT",
            "desc": "Load & Unload",
            "border": (16, 185, 129),
            "accent": (52, 211, 153),
            "fill": (22, 34, 32),
            "icon": "filament"
        },
        {
            "box": (321, 45, 423, 147),
            "title": "STEPPERS",
            "desc": "Lock / Unlock",
            "border": (245, 158, 11),
            "accent": (251, 191, 36),
            "fill": (36, 32, 24),
            "icon": "stepper"
        },
        {
            "box": (56, 158, 158, 260),
            "title": "BRIGHTNESS",
            "desc": "Screen Backlight",
            "border": (244, 63, 94),
            "accent": (251, 113, 133),
            "fill": (38, 24, 28),
            "icon": "bright"
        },
        {
            "box": (189, 158, 291, 260),
            "title": "BUZZER",
            "desc": "Audio Beep",
            "border": (59, 130, 246),
            "accent": (96, 165, 250),
            "fill": (24, 28, 42),
            "icon": "buzzer"
        },
        {
            "box": (321, 158, 423, 260),
            "title": "PAGE 2",
            "desc": "BLTouch & Macro",
            "border": (168, 85, 247),
            "accent": (192, 132, 252),
            "fill": (34, 24, 44),
            "icon": "next"
        }
    ]
    
    font_title = get_font(FONT_BOLD, 12)
    font_desc = get_font(FONT_REG, 9)
    
    for s in slots:
        draw_card(draw, s["box"], s["border"], s["fill"], radius=10)
        cx = (s["box"][0] + s["box"][2]) // 2
        cy = s["box"][1] + 36
        acc = s["accent"]
        
        if s["icon"] == "level":
            draw.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], outline=acc, width=2)
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=acc)
        elif s["icon"] == "filament":
            draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=acc, width=2)
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=acc)
        elif s["icon"] == "stepper":
            draw.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], outline=acc, width=2)
            draw.line([cx - 10, cy, cx + 10, cy], fill=acc, width=1)
            draw.line([cx, cy - 10, cx, cy + 10], fill=acc, width=1)
        elif s["icon"] == "bright":
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=acc)
            for dx, dy in [(0, -11), (0, 11), (-11, 0), (11, 0)]:
                draw.line([cx, cy, cx + dx, cy + dy], fill=acc, width=2)
        elif s["icon"] == "buzzer":
            draw.polygon([(cx - 8, cy - 5), (cx - 2, cy - 5), (cx + 6, cy - 11), (cx + 6, cy + 11), (cx - 2, cy + 5), (cx - 8, cy + 5)], fill=acc)
        elif s["icon"] == "next":
            draw.polygon([(cx + 8, cy), (cx - 4, cy - 10), (cx - 4, cy + 10)], fill=acc)
            
        tw = draw.textlength(s["title"], font=font_title)
        draw.text((cx - tw // 2, s["box"][1] + 62), s["title"], fill=(255, 255, 255), font=font_title)
        dw = draw.textlength(s["desc"], font=font_desc)
        draw.text((cx - dw // 2, s["box"][1] + 82), s["desc"], fill=s["accent"], font=font_desc)
        
    img.save(out_path, format="BMP")
    print(f"Generated {out_path} (480x272)")

def generate_macros_menu(out_path):
    img = Image.new("RGB", (480, 272), (18, 22, 28))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "⚡ QUICK ACTIONS & MACROS", "Direct CoreXY Routines", back_btn=True, back_target="HOME")
    
    # 8 Tactile Cards arranged in 2 columns of 4 cards
    # Col 1: X = 15 to 235 (w=220)
    # Col 2: X = 245 to 465 (w=220)
    # Row 1: Y = 46 to 92 (h=46)
    # Row 2: Y = 100 to 146 (h=46)
    # Row 3: Y = 154 to 200 (h=46)
    # Row 4: Y = 208 to 254 (h=46)
    cards = [
        {"box": (15, 46, 235, 92), "title": "CLEAN NOZZLE", "desc": "Heat 210°C & purge front edge", "border": (16, 185, 129), "fill": (22, 34, 30), "accent": (52, 211, 153), "icon": "PURGE"},
        {"box": (245, 46, 465, 92), "title": "BED TRAMMING", "desc": "Screws tilt calculate helper", "border": (0, 210, 255), "fill": (22, 32, 40), "accent": (0, 220, 255), "icon": "TRAM"},
        {"box": (15, 100, 235, 146), "title": "LOAD FILAMENT", "desc": "Heat 220°C & feed 60mm", "border": (168, 85, 247), "fill": (32, 24, 42), "accent": (192, 132, 252), "icon": "LOAD"},
        {"box": (245, 100, 465, 146), "title": "UNLOAD FILAMENT", "desc": "Heat 220°C & retract 80mm", "border": (236, 72, 153), "fill": (38, 24, 34), "accent": (244, 114, 182), "icon": "UNLOAD"},
        {"box": (15, 154, 235, 200), "title": "BED MESH AUTO", "desc": "Full 25-point probe calibration", "border": (245, 158, 11), "fill": (36, 32, 24), "accent": (251, 191, 36), "icon": "MESH"},
        {"box": (245, 154, 465, 200), "title": "PARK & COOLDOWN", "desc": "Heaters off & rear park toolhead", "border": (59, 130, 246), "fill": (24, 28, 42), "accent": (96, 165, 250), "icon": "PARK"},
        {"box": (15, 208, 235, 254), "title": "SPEED TEST", "desc": "Kinematic travel diagnostic", "border": (249, 115, 22), "fill": (38, 28, 22), "accent": (251, 146, 60), "icon": "SPEED"},
        {"box": (245, 208, 465, 254), "title": "FIRMWARE RESTART", "desc": "Reboot Klippy host software", "border": (239, 68, 68), "fill": (38, 22, 24), "accent": (248, 113, 113), "icon": "RESTART"}
    ]
    
    font_card_title = get_font(FONT_BOLD, 12)
    font_card_desc = get_font(FONT_REG, 9)
    font_badge = get_font(FONT_BOLD, 8)
    
    for c in cards:
        draw_card(draw, c["box"], c["border"], c["fill"], radius=8)
        x1, y1, x2, y2 = c["box"]
        # Left badge
        draw.rounded_rectangle([x1 + 6, y1 + 7, x1 + 44, y2 - 7], radius=6, fill=(30, 36, 48), outline=c["accent"], width=1)
        bw = draw.textlength(c["icon"], font=font_badge)
        draw.text((x1 + 25 - bw // 2, y1 + 17), c["icon"], fill=c["accent"], font=font_badge)
        # Texts
        draw.text((x1 + 52, y1 + 9), c["title"], fill=(255, 255, 255), font=font_card_title)
        draw.text((x1 + 52, y1 + 27), c["desc"], fill=(160, 175, 195), font=font_card_desc)
        
    img.save(out_path, format="BMP")
    print(f"Generated {out_path} (480x272)")

if __name__ == "__main__":
    bmp_dir = "/home/cedric/ender7vision/tools/raw_480x272_bmps"
    generate_home_menu(os.path.join(bmp_dir, "001_home.bmp"))
    generate_settings_menu1(os.path.join(bmp_dir, "009_settings_menu.bmp"))
    generate_settings_menu2(os.path.join(bmp_dir, "018_settings_menu2.bmp"))
    generate_macros_menu(os.path.join(bmp_dir, "021_macros_menu.bmp"))
    print("All menu screens regenerated with matching visual signature!")
