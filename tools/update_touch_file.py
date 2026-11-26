#!/usr/bin/env python3
"""
Ender7Vision Touch File Updater
Parses 13TouchFile.bin, removes outdated/misaligned Page 1, 9, 18, 21 controls,
and inserts geometrically synchronized controls for all menus.
"""
import struct

TOUCH_FILE = "/home/cedric/ender7vision/DWIN_SET/13TouchFile.bin"

def make_touch_record(page, x1, y1, x2, y2, vp, val, ctrl_type=0x05):
    # Standard 32-byte DGUS II Return Key Code / Control record
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

def update_touch_file():
    with open(TOUCH_FILE, "rb") as f:
        data = f.read()

    pos = 0
    records = []
    while pos + 32 <= len(data):
        chunk = data[pos:pos+32]
        if chunk[:2] == b"\xff\xff":
            break
        page = struct.unpack(">H", chunk[:2])[0]
        # Keep all pages except Page 1, Page 21, and the modified Page 18 buttons
        # We will re-insert Page 1, Page 18 (Slot 5 & 6), and Page 21 cleanly
        if page not in [1, 21]:
            # Also filter out the newly added slot 5 and 6 on page 18 to avoid duplicates
            if page == 18:
                vp = struct.unpack(">H", chunk[17:19])[0]
                if vp in [0x2000, 0x3501]:
                    x1 = struct.unpack(">H", chunk[2:4])[0]
                    if x1 >= 180: # Slots 5 & 6
                        pos += 32
                        continue
            records.append(chunk)
        pos += 32

    # New Page 1 Controls (4 Symmetrical Cards)
    # Card 1: Temp (26, 56) -> (124, 194) => Val 5
    # Card 2: Move (138, 56) -> (236, 194) => Val 8
    # Card 3: Settings (250, 56) -> (348, 194) => Val 9
    # Card 4: Macros (362, 56) -> (460, 194) => Val 21
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
        make_touch_record(21, 0, 0, 72, 42, 0x2000, 1),
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
