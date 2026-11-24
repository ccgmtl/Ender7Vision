#!/usr/bin/env bash
# ==============================================================================
# Ender7Vision: Uninstaller / Rollback Script
# License: GNU General Public License v3.0 (GPL-3.0)
# ==============================================================================

set -euo pipefail

KLIPPER_DIR="${KLIPPER_DIR:-$HOME/klipper}"

echo "======================================================================"
echo "                     Ender7Vision Uninstaller                        "
echo "======================================================================"

if [ ! -d "$KLIPPER_DIR" ]; then
    echo "[-] Error: Klipper directory not found at $KLIPPER_DIR"
    exit 1
fi

echo "[*] Removing t5uid1 host and MCU extensions from $KLIPPER_DIR..."
rm -rf "$KLIPPER_DIR/klippy/extras/t5uid1"
rm -rf "$KLIPPER_DIR/src/generic/t5uid1"
rm -rf "$KLIPPER_DIR/src/stm32/t5uid1"

KCONFIG_FILE="$KLIPPER_DIR/src/stm32/Kconfig"
if [ -f "$KCONFIG_FILE" ]; then
    sed -i '/source "src\/stm32\/t5uid1\/Kconfig"/d' "$KCONFIG_FILE"
    echo "[+] Cleaned $KCONFIG_FILE"
fi

MAKEFILE_FILE="$KLIPPER_DIR/src/stm32/Makefile"
if [ -f "$MAKEFILE_FILE" ]; then
    sed -i '/include src\/stm32\/t5uid1\/Makefile/d' "$MAKEFILE_FILE"
    echo "[+] Cleaned $MAKEFILE_FILE"
fi

if systemctl is-active --quiet klipper; then
    echo "[*] Restarting Klipper..."
    if [ "$EUID" -ne 0 ]; then
        sudo systemctl restart klipper || true
    else
        systemctl restart klipper || true
    fi
fi

echo "[+] Ender7Vision uninstalled cleanly."
