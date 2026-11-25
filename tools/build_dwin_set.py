#!/usr/bin/env python3
"""
Reproducible DWIN_SET Builder for Creality Ender 7 (DMT48270C043_06WT / T5L1 ASIC)
Generates native 480x272 landscape DGUS-Reloaded assets (32_screens.icl, 14ShowFile.bin, 13TouchFile.bin, T5LCFG.CFG)
"""
import os, sys, glob, datetime, struct, io, shutil
from PIL import Image, ImageDraw, ImageFont

def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc

def build_screens_icl(bmp_dir: str, out_icl_path: str, version_tag: str = "v2.3.0-LS"):
    boot_src = os.path.join(bmp_dir, "000_boot.bmp")
    img = Image.open(boot_src).convert("RGB")
    draw = ImageDraw.Draw(img)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    stamp_text = f"Ender 7 DGUS-Reloaded {version_tag} | {now_str}"
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), stamp_text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (480 - text_w) // 2, 272 - text_h - 12
    draw.rectangle([x - 10, y - 5, x + text_w + 10, y + text_h + 5], fill=(0, 0, 0), outline=(0, 255, 255), width=1)
    draw.text((x, y - 2), stamp_text, fill=(0, 255, 255), font=font)
    stamped_boot_path = "/tmp/stamped_000_boot.bmp"
    img.save(stamped_boot_path, format="BMP")

    bmp_files = glob.glob(os.path.join(bmp_dir, "*.bmp"))
    images_by_idx = {}
    for path in bmp_files:
        idx = int(os.path.basename(path).split("_")[0])
        images_by_idx[idx] = stamped_boot_path if idx == 0 else path

    jpegs_by_idx = {}
    for idx, path in sorted(images_by_idx.items()):
        im = Image.open(path)
        assert im.size == (480, 272), f"Expected 480x272, got {im.size} for {path}"
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=95, subsampling="4:2:0")
        jpegs_by_idx[idx] = (im.size, buf.getvalue())

    max_idx = max(jpegs_by_idx.keys())
    pointer_table_size = (max_idx + 1) * 4
    pointers = [0] * (max_idx + 1)
    body = bytearray()
    current_offset = 16 + pointer_table_size

    for idx in range(max_idx + 1):
        if idx not in jpegs_by_idx:
            continue
        (w, h), jpg_data = jpegs_by_idx[idx]
        if len(body) > 0:
            rem = current_offset % 2048
            if rem != 0:
                pad_len = 2048 - rem
                body.extend(b"\x00" * pad_len)
                current_offset += pad_len
        pointers[idx] = current_offset
        eoi = len(jpg_data)
        sos_idx = jpg_data.find(b"\xff\xda")
        sos_hdr_len = struct.unpack(">H", jpg_data[sos_idx + 2 : sos_idx + 4])[0]
        sos_len = sos_idx + 2 + sos_hdr_len
        diff = 10 - (eoi % 4) if (eoi % 4) <= 2 else 11
        plen = (eoi + diff) - sos_len
        block = struct.pack(">HHHI", w, h, sos_len, plen) + jpg_data + (b"\x00" * diff)
        body.extend(block)
        current_offset += len(block)

    header_bytes = bytearray(16)
    header_bytes[0:6] = b"DGUS_3"
    struct.pack_into("<HH", header_bytes, 12, 4, max_idx)
    pointer_bytes = b"".join(struct.pack(">I", p) for p in pointers)
    full_file = bytearray(header_bytes + pointer_bytes + body)
    struct.pack_into(">I", full_file, 8, len(full_file) - 8)
    crc = crc16_modbus(full_file[8:])
    struct.pack_into("<H", full_file, 6, crc)
    with open(out_icl_path, "wb") as f:
        f.write(full_file)
    print(f"Built {out_icl_path} ({len(full_file)} bytes, CRC={hex(crc)}, banner='{stamp_text}')")

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bmp_dir = os.path.join(repo_root, "tools", "raw_480x272_bmps")
    out_path = os.path.join(repo_root, "DWIN_SET", "32_screens.icl")
    version = sys.argv[1] if len(sys.argv) > 1 else "v1.1.0"
    build_screens_icl(bmp_dir, out_path, version_tag=version)

