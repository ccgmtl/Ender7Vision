# Ender7Vision Agent Guide & Project Standards

## 1. Project Overview
**Ender7Vision** is an open-source, daemon-less integration providing native DWIN DGUS II touchscreen support on the **Creality Ender 7** (`CR-FDM-v2.4.S1_v101`) running mainline Klipper (v0.12–v0.14+).
- **GitHub Repository:** `https://github.com/ccgmtl/Ender7Vision.git`
- **Local Source Directory:** `/home/cedric/ender7vision`
- **Target Host:** `ender7` (`192.168.2.82`), user `cedric` / `pi`
- **License:** GNU General Public License v3.0 (GPL-3.0)

---

## 2. Hardware Architecture & Crucial Discoveries
| Subsystem | Detail | Critical Note |
| :--- | :--- | :--- |
| **Mainboard** | Creality `CR-FDM-v2.4.S1_v101` (STM32F103RET6) | 28KiB bootloader (`0x8007000`), 8MHz crystal |
| **Host Serial** | `USART1` (`PA10` RX / `PA9` TX) | CH340 USB @ `250000` baud |
| **Touchscreen Serial** | **`USART2` (`PA3` RX / `PA2` TX)** | Dedicated LCD port @ `115200` baud (NOT `USART3` `PB10/PB11`!) |
| **Bed Heater Safety** | **`PA15`** (`JTDI`) | Gate pulled HIGH on reset by JTAG default. Requires `CONFIG_INITIAL_PINS="!PA15"` in MCU build and `heater_pin: PA15` in `printer.cfg` |
| **Touchscreen Panel** | DWIN `DMT48270C043_06WT` (T5L1 ASIC) | Native **480×272 landscape**, `DGUS_3` sector-aligned container |

---

## 3. Repository Structure
```
ender7vision/
├── DWIN_SET/                  # Compiled screen assets for rear display microSD flash
├── mcu_firmware/              # Prebuilt Klipper MCU firmware + .config
├── klipper_extension/         # In-tree Python & C extensions
│   ├── klippy/extras/t5uid1/  # Python host driver (Python 3.11+ / Klipper v0.14 compatible)
│   └── src/                   # MCU C USART2 driver for STM32F103
├── config/                    # DGUS-Reloaded macros & example printer.cfg
├── tools/                     # ICL compilation script & raw BMP assets
├── install.sh                 # One-click installer
├── uninstall.sh               # Clean uninstaller
├── LICENSE                    # GPL-3.0
└── README.md
```

---

## 4. Verification & Deployment Commands
```bash
# Verify repo status
cd /home/cedric/ender7vision
git status

# Deploy to target host (ender7)
ssh cedric@192.168.2.82
# Installer execution:
./install.sh

# Klipper restart and log inspection:
sudo systemctl restart klipper
tail -f /home/pi/printer_data/logs/klippy.log
```
