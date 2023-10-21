<div align="center">

# `vanilla-tweaks-partition`

Download [Vanilla Tweaks][vanillatweaks] packs into separate Minecraft resource
packs.

</div>

### 📦 Installation

```sh
poetry install
```

### 🚀 Usage

```sh
$ vanilla-tweaks-partition --help

 Usage: vanilla-tweaks-partition [OPTIONS] 📦 PACKS...

 Download Vanilla Tweaks packs into separate Minecraft resource packs.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packs      📦 PACKS...  Vanilla Tweaks pack names in format 'Category/Pack Name'. [required]                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mc-version                TEXT  The Minecraft version. [default: 1.20]                                           │
│ --outdir                    PATH  The pack output directory. [default: packs]                                      │
│ --install-completion              Install completion for the current shell.                                        │
│ --show-completion                 Show completion for the current shell, to copy it or customize the installation. │
│ --help                            Show this message and exit.                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 🪄 Example

```sh
$ vanilla-tweaks-partition \
    'Aesthetic/Colorful Enchanting Table Particles' \
    'HUD/Ping Color Indicator' \
    'Unobtrusive/Lower Shield' \
    'Unobtrusive/Invisible Totem' \
    'Utility/Directional Dispensers & Droppers' \
    'Utility/Directional Observers' \
    'Utility/Fully Aged Amethyst Cluster Marker' \
    'Utility/Fully Aged Crop Marker' \
    'Utility/Ore Borders' \
    'Utility/Sticky Piston Sides' \
    'Utility/Suspicious Sand & Gravel Borders' \
    'Utility/Visual Honey Stages' \
    'Utility/Visual Note Block Pitch'

📦 Requested 13 Vanilla Tweaks pack/s

  Aesthetic » Colorful Enchanting Table Particles ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Fully Aged Amethyst Cluster Marker    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Fully Aged Crop Marker                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Visual Note Block Pitch               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Visual Honey Stages                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Directional Observers                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Directional Dispensers & Droppers     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Sticky Piston Sides                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Suspicious Sand & Gravel Borders      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Utility » Ore Borders                           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Unobtrusive » Lower Shield                      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Unobtrusive » Invisible Totem                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  HUD » Ping Color Indicator                      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

🎉 Success!
```

[vanillatweaks]: https://vanillatweaks.net/picker/resource-packs/
