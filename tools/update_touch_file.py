#!/usr/bin/env python3
"""
Ender7Vision Touch File Updater
Parses pristine 13TouchFile.bin respecting variable-length DGUS II control records:
- Control 0x05 (Return Key Code) & 0x03 (Slider/Inc): 32 bytes
- Control 0x01 (Touch Button / Popup), 0x02, 0x04: 48 bytes
- Control 0x00 (Variable Data Input): 64 bytes

Preserves 100% of authentic controls on Move (Page 8), Temp (Page 5), Leveling (Page 10),
Settings (Page 9), and popups, while cleanly injecting:
- Page 1: 4 Symmetrical Home Cards (Temp, Move, Settings, Macros)
- Page 18: Slots 5 (Quick Macros) & 6 (Cycle Theme)
- Page 21: Back Button & 8 Tactile Macro Cards
"""
import os
import subprocess
import struct

TOUCH_FILE = "/home/cedric/ender7vision/DWIN_SET/13TouchFile.bin"

def make_touch_record(page, x1, y1, x2, y2, vp, val, ctrl_type=0x05):
    # Standard 32-byte DGUS II Return Key Code record
    rec = bytearray(32)
    struct.pack_into(">HHHHH", rec, 0, page, x1, y1, x2, y2)
    rec[10:14] = b"\xff\x00\xff\x00"
    rec[14] = 0xfe
    rec[15] = ctrl_type
    rec[16] = 0xfe
    struct.pack_into(">H", rec, 17, vp)
    rec[19] = 0x00
    struct.pack_into(">H", rec, 20, val)
    return bytes(rec)

def get_pristine_touch_data():
    # If /tmp/orig_touch.bin exists, use it; otherwise extract from git v1.1.0
    if os.path.exists("/tmp/orig_touch.bin"):
        with open("/tmp/orig_touch.bin", "rb") as f:
            return f.read()
    res = subprocess.run(["git", "show", "v1.1.0:DWIN_SET/13TouchFile.bin"], cwd="/home/cedric/ender7vision", capture_output=True, check=True)
    return res.stdout

def update_touch_file():
    data = get_pristine_touch_data()
    
    pos = 0
    records = []
    while pos < len(data):
        if pos + 2 > len(data) or data[pos:pos+2] == b"\xff\xff":
            break
        page = int.from_bytes(data[pos:pos+2], "big")
        ctrl_type = data[pos+15]
        
        # Determine true record length in DGUS II
        if ctrl_type in [0x05, 0x03]:
            rlen = 32
        elif ctrl_type in [0x01, 0x02, 0x04]:
            rlen = 48
        elif ctrl_type == 0x00:
            rlen = 64
        else:
            rlen = 32
            
        chunk = data[pos:pos+rlen]
        
        # Keep all pristine pages except Page 1, Page 21, and any existing custom slot 5/6 on Page 18
        if page not in [1, 21]:
            if page == 18:
                x1 = struct.unpack(">H", chunk[2:4])[0]
                if x1 >= 180: # Filter out slots 5 & 6 if already present
                    pos += rlen
                    continue
            records.append(chunk)
            
        pos += rlen

    print(f"Loaded {len(records)} pristine records from original touch table.")

    # New Page 1 Controls (4 Symmetrical Cards)
    # Card 1: Temp (26, 56) -> (124, 194) => Val 5 (Page 5)
    # Card 2: Move (138, 56) -> (236, 194) => Val 8 (Page 8)
    # Card 3: Settings (250, 56) -> (348, 194) => Val 9 (Page 9)
    # Card 4: Macros (362, 56) -> (460, 194) => Val 21 (Page 21)
    new_records = [
        make_touch_record(1, 26, 56, 124, 194, 0x2000, 5),
        make_touch_record(1, 138, 56, 236, 194, 0x2000, 8),
        make_touch_record(1, 250, 56, 348, 194, 0x2000, 9),
        make_touch_record(1, 362, 56, 460, 194, 0x2000, 21),
    ]

    # Page 18 Controls (Slot 5: Quick Macros, Slot 6: Theme Cycle)
    new_records.extend([
        make_touch_record(18, 189, 158, 291, 260, 0x2000, 21),
        make_touch_record(18, 321, 158, 423, 260, 0x3501, 1),
    ])

    # Page 21 Controls (Back button + 8 Macro Cards)
    new_records.extend([
        make_touch_record(21, 0, 0, 76, 42, 0x2000, 1),
        make_touch_record(21, 15, 46, 235, 92, 0x3300, 1),
        make_touch_record(21, 245, 46, 465, 92, 0x3301, 1),
        make_touch_record(21, 15, 100, 235, 146, 0x3302, 1),
        make_touch_record(21, 245, 100, 465, 146, 0x3303, 1),
        make_touch_record(21, 15, 154, 235, 200, 0x3304, 1),
        make_touch_record(21, 245, 154, 465, 200, 0x3305, 1),
        make_touch_record(21, 15, 208, 235, 254, 0x3306, 1),
        make_touch_record(21, 245, 208, 465, 254, 0x3307, 1),
    ])

    all_records = records + new_records
    out_data = b"".join(all_records) + b"\xff\xff"

    with open(TOUCH_FILE, "wb") as f:
        f.write(out_data)

    print(f"Updated {TOUCH_FILE}: {len(all_records)} touch controls ({len(out_data)} bytes)")

if __name__ == "__main__":
    update_touch_file()
