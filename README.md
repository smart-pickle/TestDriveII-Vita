# Test Drive II: The Duel (1989) — PlayStation®Vita Port

A native, hardware-accelerated PlayStation®Vita and PlayStation®TV port of **Test Drive II: The Duel (1989)**, based on the static recompilation and reverse-engineering work by **kylofon**.

This port brings Accolade and Distinctive Software's classic 1989 head-to-head racing sequel to the PS Vita with smooth 60 FPS presentation via VitaGL / GXM hardware acceleration, authentic DOS sound synthesis, responsive physical controls, dynamic multi-mode aspect scaling, expansion disk support, and a Sony TRC-compliant LiveArea digital user manual.

---

## Features

- **Hardware Acceleration**: Smooth 60 FPS presentation powered by VitaSDK's SDL2 with VitaGL / GXM GPU backend.
- **Tri-Mode Aspect Ratio Engine**: Toggle between 3 display modes in real time with the **`Select`** button:
  - **Mode 1 (Boot Default)**: 4:3 Aspect-Correct ($725 \times 544$ pillarboxed) — authentic retro CRT proportion with full dashboard gauge visibility.
  - **Mode 2**: 2× Integer Scale ($640 \times 480$ centered) — razor-sharp pixel doubling matching original DOS EGA scanlines.
  - **Mode 0**: 16:9 Widescreen Stretch ($960 \times 544$) — full edge-to-edge panoramic view filling the 5-inch OLED/LCD display.
- **Ergonomic Vita Controls**: Full support for the Left Analog Stick, D-Pad, face buttons, and shoulder trigger pedals (R Trigger for Gas, L Trigger for Brake, Triangle for Shift Up, Square/Circle for Shift Down).
- **Hybrid Filesystem & Persistent Saves**: High scores (`<scenery>hisc.dat`), user car/scenery picks, and options (`select.dat`) are written directly to `ux0:data/TestDrive2/`, avoiding Sony's read-only `app0:` restriction.
- **Add-on Expansion Disks**: Drop optional Car Disks (*The Supercars*, *Muscle Cars*) and Scenery Disks (*California Challenge*, *European Challenge*) into `ux0:data/TestDrive2/` and the game automatically recognizes them!
- **Built-in LiveArea User Manual**: A complete 5-page digital manual installed to `sce_sys/manual/`, accessible directly from the LiveArea book icon.
- **Sony TRC Compliant**: All LiveArea & manual PNGs strictly 8-bit indexed palette (`color_type=3`, non-interlaced, no alpha in `icon0.png`) preventing VitaShell error `0x8010113D`.

---

## Important Notice: Game Data Setup

> [!IMPORTANT]
> **Proprietary game assets are NOT bundled in the release VPK.**
> To comply with copyright laws, you must provide the original game data from your legally owned copy of the original 1989 DOS version of *Test Drive II: The Duel* by Accolade.

### How to Install Game Files

1. Install `TestDrive2Vita.vpk` on your PS Vita using **VitaShell**.
2. Launch **VitaShell** and press **`Select`** to start a **USB** or **FTP** connection.
3. On your PS Vita memory card, navigate to:
   ```
   ux0:data/TestDrive2/
   ```
   *(This directory is created automatically when the game first launches, or you can create it manually).*
4. Copy all files from your original DOS version into `ux0:data/TestDrive2/`.

### Required Files Checklist

| File | Type | Description |
| :--- | :--- | :--- |
| **`TD2EGA.EXE`** | **Required** | Primary EGA game executable (needed to boot) |
| **`CARS.DAT`** | **Required** | Car catalogue file |
| **`SCENES.DAT`** | **Required** | Scenery catalogue file |
| **`*.PES` / `*.PCS`** | **Required** | Cockpits, road scenery, and visual assets |
| **`*.BIN` / `*.SS`** | **Required** | Vehicle physics and opponent sprite sequences |
| **`SONGS.BIN`** | **Required** | Music and theme melodies |
| **`SELECT.DAT`** | Optional | Saved configuration (created automatically if missing) |
| **`Add-on Disks`** | Optional | Extra car and scenery files (placed in `ux0:data/TestDrive2/`) |

*Note: The game engine resolves filenames case-insensitively, so both lowercase (`td2ega.exe`) and uppercase (`TD2EGA.EXE`) work seamlessly.*

---

## Controls

### In-Game Driving

| Input | Action | Description |
| :--- | :--- | :--- |
| **Left Stick** or **D-Pad ◄ / ►** | **Steer** | Turn vehicle left and right with analog precision |
| **Cross ($\times$)** / **R Trigger** / **D-Pad ▲** | **Gas (Accelerate)** | Depress accelerator pedal |
| **L Trigger** / **D-Pad ▼** | **Brake** | Apply vehicle brakes |
| **Triangle ($\triangle$)** | **Shift Up** | Shift manual transmission to higher gear |
| **Square ($\square$)** or **Circle ($\bigcirc$)** | **Shift Down** | Shift manual transmission to lower gear |
| **Select** | **Cycle Display Mode** | Switch between 4:3, 2× Integer, and 16:9 |
| **Start** | **Pause / Menu** | Pause gameplay or exit current drive (`Esc`) |

### Menu Navigation

| Input | Action |
| :--- | :--- |
| **D-Pad ▲ / ▼** | Highlight menu options and vehicle selection |
| **Cross ($\times$)** | Confirm selection / DOS `Enter` key |
| **Circle ($\bigcirc$)** | Toggle options / DOS `Spacebar` key |
| **Start** | Cancel / Return / DOS `Esc` key |

### Driving & Survival Tips

- **Sequential Shifting**: Test Drive II features realistic manual gearboxes. Watch the tachometer and shift UP before reaching the redline. Over-revving the engine for too long will blow it!
- **Head-to-Head Racing**: Watch your rearview mirror! The computer AI opponent will aggressively try to overtake you and block passes.
- **Gas Station Refueling**: At the end of each stage, slow down and steer smoothly into the gas station. Coming in too fast will crash your supercar into the gas pumps!
- **Radar Detector**: When your visor radar detector flashes and beeps, tap the brake immediately to avoid getting pulled over by the highway patrol cruiser!

---

## Building from Source

### Prerequisites
- [Docker](https://www.docker.com/) (recommended) or a local installation of [VitaSDK](https://vitasdk.org/).

### Build using Docker (One-Liner)

```bash
# Clone repository
git clone https://github.com/gainusha/TestDrive2Vita.git
cd TestDrive2Vita

# Build clean release VPK (without bundled DOS files)
docker run --platform linux/amd64 --rm -v "$(pwd):/src" -w /src vitasdk/vitasdk bash -c "
  cmake -B build-vita -DCMAKE_TOOLCHAIN_FILE=/usr/local/vitasdk/share/vita.toolchain.cmake -DBUNDLE_GAME_DATA=OFF &&
  cmake --build build-vita
"
```

The output package `TestDrive2Vita.vpk` will be generated in the root directory.

### CMake Build Options

- `-DBUNDLE_GAME_DATA=OFF` *(Default for releases)*: Builds a clean, standalone VPK with zero copyrighted DOS assets bundled.
- `-DBUNDLE_GAME_DATA=ON` : Bundles local files from `Game/` into the VPK under `app0:Game/` for self-testing.

---

## Credits & Acknowledgments

- **[kylofon](https://github.com/kylofon)** — Creator of the exceptional [**test-drive-2-sdl3**](https://github.com/kylofon/test-drive-2-sdl3) static recompilation and reverse-engineering work. This port is built directly upon their incredible engineering efforts.
- **Accolade & Distinctive Software, Inc. (DSI)** — Creators of the legendary *Test Drive II: The Duel* (1989).
- **VitaSDK Team** — For the open-source cross-compiler toolchain and Sony PS Vita homebrew libraries.
- **Vita3K Team** — For the PlayStation Vita emulator facilitating development and testing.
