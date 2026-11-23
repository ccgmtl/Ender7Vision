#!/usr/bin/env bash
# ==============================================================================
# Ender7Vision: Native DWIN DGUS II Touchscreen Installer for Klipper
# Repository: https://github.com/ccgmtl/ender7vision
# License: GNU General Public License v3.0 (GPL-3.0)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KLIPPER_DIR="${KLIPPER_DIR:-$HOME/klipper}"
PRINTER_DATA_DIR="${PRINTER_DATA_DIR:-$HOME/printer_data}"

echo "======================================================================"
echo "          Ender7Vision Installer: DWIN DGUS II for Klipper"
echo "======================================================================"

# 1. Validate target Klipper repository
if [ ! -d "$KLIPPER_DIR" ] || [ ! -f "$KLIPPER_DIR/klippy/klippy.py" ]; then
    echo "[-] Error: Klipper directory not found at $KLIPPER_DIR"
    echo "    Please specify the Klipper directory with: KLIPPER_DIR=/path/to/klipper $0"
    exit 1
fi
echo "[+] Detected Klipper installation at: $KLIPPER_DIR"

# 2. Install Python host extension (klippy/extras/t5uid1)
echo "[*] Installing Klippy t5uid1 host extension..."
mkdir -p "$KLIPPER_DIR/klippy/extras/t5uid1"
rsync -a --exclude="*.pyc" --exclude="__pycache__" \
    "$SCRIPT_DIR/klipper_extension/klippy/extras/t5uid1/" "$KLIPPER_DIR/klippy/extras/t5uid1/"
echo "[+] Klippy host extension installed to $KLIPPER_DIR/klippy/extras/t5uid1"

# 3. Install MCU C extensions (generic and stm32)
echo "[*] Installing MCU C source modules..."
mkdir -p "$KLIPPER_DIR/src/generic/t5uid1" "$KLIPPER_DIR/src/stm32/t5uid1"
rsync -a "$SCRIPT_DIR/klipper_extension/src/generic/t5uid1/" "$KLIPPER_DIR/src/generic/t5uid1/"
rsync -a "$SCRIPT_DIR/klipper_extension/src/stm32/t5uid1/" "$KLIPPER_DIR/src/stm32/t5uid1/"
echo "[+] MCU C modules installed to $KLIPPER_DIR/src/"

# 4. Patch src/stm32/Kconfig
KCONFIG_FILE="$KLIPPER_DIR/src/stm32/Kconfig"
KCONFIG_LINE='source "src/stm32/t5uid1/Kconfig"'
if grep -qF "$KCONFIG_LINE" "$KCONFIG_FILE"; then
    echo "[+] $KCONFIG_FILE already patched."
else
    echo "[*] Patching $KCONFIG_FILE..."
    echo -e "\n$KCONFIG_LINE" >> "$KCONFIG_FILE"
    echo "[+] Patched $KCONFIG_FILE"
fi

# 5. Patch src/stm32/Makefile
MAKEFILE_FILE="$KLIPPER_DIR/src/stm32/Makefile"
MAKEFILE_LINE='include src/stm32/t5uid1/Makefile'
if grep -qF "$MAKEFILE_LINE" "$MAKEFILE_FILE"; then
    echo "[+] $MAKEFILE_FILE already patched."
else
    echo "[*] Patching $MAKEFILE_FILE..."
    echo -e "\n$MAKEFILE_LINE" >> "$MAKEFILE_FILE"
    echo "[+] Patched $MAKEFILE_FILE"
fi

# 6. Copy DGUS-Reloaded helper macros to printer_data/config if available
if [ -d "$PRINTER_DATA_DIR/config" ]; then
    if [ ! -f "$PRINTER_DATA_DIR/config/DGUS-Reloaded.cfg" ]; then
        echo "[*] Copying DGUS-Reloaded.cfg to $PRINTER_DATA_DIR/config/..."
        cp "$SCRIPT_DIR/config/DGUS-Reloaded.cfg" "$PRINTER_DATA_DIR/config/DGUS-Reloaded.cfg"
        echo "[+] Copied DGUS-Reloaded.cfg"
    else
        echo "[i] $PRINTER_DATA_DIR/config/DGUS-Reloaded.cfg already exists (skipping overwrite)."
    fi
fi

# 7. Restart Klipper service if present
if systemctl is-active --quiet klipper; then
    echo "[*] Restarting Klipper service..."
    if [ "$EUID" -ne 0 ]; then
        sudo systemctl restart klipper || true
    else
        systemctl restart klipper || true
    fi
    echo "[+] Klipper service restarted."
fi

echo "======================================================================"
echo "                   Installation Completed Successfully!               "
echo "======================================================================"
echo ""
echo "NEXT STEPS:"
echo "1. FLASH SCREEN:"
echo "   Copy all files inside 'DWIN_SET/' to a FAT32-formatted microSD card"
echo "   (Allocation unit size: 4096 bytes). Power off the printer, insert the card"
echo "   into the rear display microSD slot, and power on until the blue screen displays 'END !'."
echo ""
echo "2. FLASH MCU FIRMWARE:"
echo "   Flash the motherboard with 'mcu_firmware/klipper_ender7_usart2.bin' via the"
echo "   front SD card slot, OR compile your own with:"
echo "     cp $SCRIPT_DIR/mcu_firmware/klipper_mcu.config $KLIPPER_DIR/.config"
echo "     make olddefconfig && make -j4"
echo ""
echo "3. CONFIGURE PRINTER.CFG:"
echo "   Ensure your printer.cfg contains:"
echo "     [include DGUS-Reloaded.cfg]"
echo "     [t5uid1]"
echo "     baud: 115200"
echo "     firmware: dgus_reloaded"
echo "     machine_name: Ender 7"
echo ""
echo "   CRITICAL HARDWARE PIN NOTICE:"
echo "   Ensure [heater_bed] heater_pin is set to PA15 (NOT PA2!)."
echo "======================================================================"
