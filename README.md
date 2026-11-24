# Ender7Vision

**Native DWIN DGUS II Touchscreen Support for the Creality Ender 7 on Mainline Klipper**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Klipper](https://img.shields.io/badge/Klipper-v0.12--v0.14-orange.svg)](https://www.klipper3d.org/)
[![Display](https://img.shields.io/badge/Screen-DWIN%20T5L1%20DGUS%20II%20(480x272)-brightgreen.svg)]()

> From my research, this has not been done by anyone else to this day, which might be due to the fact that there's probably about only 100 of us on the internet still running the Ender 7. Even Creality doesn't admit to having produced this device.
>
> **Full disclosure:** This is complete AI Slop. It works, but I've not written a single line of code, I'm simply a solid prompt whisperer, and all the credit should go to my local AI stack running off a pile of outdated GPUs and Qwen Coder. If this thing sets your house on fire, don't blame me and call the fire department.
>
> It works on my Ender 7, running the latest version of Klipper. I've tested all the functionality, and it does borrow from Desuu's DWIN port.

---

## ⚡ Overview & Architecture

**Ender7Vision** restores the factory color touchscreen on the **Creality Ender 7** using native, in-tree Klipper routines. It operates **100% daemon-less**—meaning no external background Python bridges, no pseudo-terminals (`/tmp/ttyDWIN`), and zero overhead. Klipper communicates directly with the DWIN display ASIC over the motherboard's dedicated serial bus.

---

## 🔍 Key Hardware Discoveries & Solutions

If you have tried using standard Ender 3 V2 or CR-6 SE DGUS configurations on the Ender 7, your display was likely stuck on the boot screen or caused printer errors. Here is why:

1. **Screen Serial Port (`USART2` vs `USART3`):**
   * Unlike the Ender 3 V2 (which wires the display to `USART3` `PB10/PB11`), the Ender 7 motherboard (**Creality `CR-FDM-v2.4.S1_v101`**) routes the screen to **`USART2` (`PA3` RX / `PA2` TX)** at **115,200 baud**.
2. **Heated Bed Safety Clamp (`PA15`):**
   * Creality moved the heated bed MOSFET gate from `PA2` to **`PA15`** (`JTDI`) to free up `USART2` for the touchscreen.
   * On reset, STM32F103 defaults `PA15` to JTAG with an internal pull-up, which turns the bed heater ON immediately until Klipper initializes.
   * **Fix:** The MCU firmware must be compiled with `CONFIG_INITIAL_PINS="!PA15"`, and `[heater_bed]` in `printer.cfg` must specify `heater_pin: PA15`.
3. **Landscape DWIN T5L1 DGUS II Asset Requirements (`480×272`):**
   * The Ender 7 uses a native **480×272 landscape panel** powered by the DWIN T5L1 ASIC.
   * Screen backgrounds must be packed in a `DGUS_3` JPEG container (`32_screens.icl`) with 2048-byte sector alignment.
   * Touch files (`13TouchFile.bin`) require `0x00` control prefixes, and variable display files (`14ShowFile.bin`) require T5L descriptor record lengths.

---

## 🚀 Quick Install Guide

### Step 1: Flash the DWIN Touchscreen
1. Take a microSD card (16GB or smaller recommended) and format it on your computer as **FAT32** with an **Allocation Unit Size of 4096 bytes** (4K).
2. Copy the entire **`DWIN_SET`** folder from this repository onto the root of the microSD card.
3. Power off the Ender 7.
4. Unscrew the rear cover of the touchscreen to access the display's dedicated microSD slot.
5. Insert the microSD card into the display slot and power on the printer.
6. The screen will turn blue and print flashing progress. Wait until it displays **`END !`** (or all files count down).
7. Power off the printer, remove the microSD card, and reassemble the screen housing.

---

### Step 2: Install the Klipper Extension
On the Raspberry Pi (or host device running Klipper):

```bash
cd ~
git clone https://github.com/ccgmtl/ender7vision.git
cd ender7vision
chmod +x install.sh
./install.sh
```

The installer will automatically:
* Deploy the updated Python 3.11/Klipper v0.14 compatible `t5uid1` host module into `~/klipper/klippy/extras/t5uid1/`.
* Deploy the `USART2` MCU interrupt routines into `~/klipper/src/generic/` and `~/klipper/src/stm32/`.
* Patch `src/stm32/Kconfig` and `src/stm32/Makefile`.
* Copy `DGUS-Reloaded.cfg` to `~/printer_data/config/`.

---

### Step 3: Flash the Ender 7 Mainboard MCU

You can either flash the precompiled binary or compile it yourself:

#### Option A: Use Precompiled Firmware (Recommended)
1. Copy `mcu_firmware/klipper_ender7_usart2.bin` to a FAT32 SD card.
2. Rename it to a unique name (e.g., `kfirmware_2026.bin`—Creality bootloaders ignore filenames identical to the last flash).
3. Insert the card into the **front SD slot** of the Ender 7 and power on. Wait 15 seconds.

#### Option B: Compile from Source
```bash
cd ~/klipper
cp ~/ender7vision/mcu_firmware/klipper_mcu.config .config
make olddefconfig
make clean
make -j4
```
Copy `out/klipper.bin` to the SD card, rename it, and flash the front mainboard slot.

---

### Step 4: Update `printer.cfg`

Open your `printer.cfg` (via Mainsail, Fluidd, or SSH) and add the following:

```ini
[include DGUS-Reloaded.cfg]

[t5uid1]
baud: 115200
firmware: dgus_reloaded
machine_name: Ender 7
brightness: 100
volume: 100
x_min: 0
x_max: 250
y_min: 0
y_max: 250
z_min: 0
z_max: 285

[heater_bed]
heater_pin: PA15      # <-- CRITICAL: Must be PA15 on Ender 7!
sensor_type: EPCOS 100K B57560G104F
sensor_pin: PC4
min_temp: 0
max_temp: 100
```

Restart Klipper. Your Ender 7 display will initialize into the full interactive control dashboard!

---

## 🛠️ Repository Contents

```
ender7vision/
├── DWIN_SET/                  # Compiled screen assets for rear microSD flash
├── mcu_firmware/              # Prebuilt Klipper MCU firmware + .config
├── klipper_extension/         # In-tree Python & C extensions
│   ├── klippy/extras/t5uid1/  # Python host driver (Python 3.11+ compatible)
│   └── src/                   # MCU C USART2 driver for STM32F103
├── config/                    # DGUS-Reloaded macros & example printer.cfg
├── tools/                     # ICL compilation script & raw BMP assets
├── install.sh                 # One-click installer
├── uninstall.sh               # Clean uninstaller
└── README.md
```

---

## 📜 Attributions & Acknowledgments

This project is built upon the foundational work of the 3D printing and open-source communities:

* **[Desuuuu](https://github.com/Desuuuu/klipper):** Author of the original `t5uid1` DGUS implementation for Klipper, providing the C MCU serial interrupt infrastructure and Klippy display state machine.
* **[Thinkersbluff & the DGUS-Reloaded Project](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component):** The creators of the DGUS-Reloaded layout engine, page variable mapping conventions, and macro routines.
* **[Kevin O'Connor & the Klipper Community](https://github.com/Klipper3d/klipper):** The bedrock 3D printer firmware ecosystem.
* **[Creality3D](https://www.creality.com/):** For the Ender 7 printer and hardware platform.
* **Ender7Vision Maintainers (@ccgmtl & Contributors):**
  * Hardware mapping and discovery for the Creality `CR-FDM-v2.4.S1_v101` (`USART2` `PA3/PA2` routing and `PA15` bed clamp).
  * Native 480×272 landscape DGUS II asset creation and `DGUS_3` sector-aligned container compilation (`32_screens.icl`).
  * Modern Python 3.11 / Debian 12 Bookworm / Klipper v0.14 compatibility shims.
  * Modular zero-daemon installer and deployment suite.

---

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)** in accordance with the licenses of Klipper and Desuuuu's upstream implementation. See [LICENSE](LICENSE) for details.
