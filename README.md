[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/releases/latest)
[![Build Status](https://github.com/hmlendea/stellaris-ui-star-names/actions/workflows/build.yml/badge.svg)](https://github.com/hmlendea/stellaris-ui-star-names/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/LICENSE)

# Universum Infinitum - Star Names

Mods for Galactic Civilizations II, Galactic Civilizations III, and Stellaris that add [thousands of new star names](https://github.com/hmlendea/stellaris-ui-star-names/wiki/Additions), drawn from science fiction, fantasy, games, and real astronomical catalogues. The Stellaris mod additionally adds nebula, asteroid, and black hole names.

## 📑 Table of Contents

- [Capabilities](#-capabilities)
- [Usage](#-usage)
- [Known Limitations](#-known-limitations)
- [Installation](#-installation)
  - [Galactic Civilizations II](#galactic-civilizations-ii)
    - [Manual Instructions](#manual-instructions)
  - [Galactic Civilizations III](#galactic-civilizations-iii)
    - [Manual Instructions](#manual-instructions-1)
  - [Stellaris](#stellaris)
- [Compatibility](#-compatibility)
- [Privacy and Data](#-privacy-and-data)
- [Development](#-development)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Build](#build)
  - [Run](#run)
  - [Test](#test)
- [GitHub Actions](#-github-actions)
- [Project Structure](#-project-structure)
  - [Directories](#directories)
- [Architecture](#-architecture)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Code of Conduct](#-code-of-conduct)
- [Related Projects](#-related-projects)
- [Security](#security)
- [Support](#-support)
- [Project Engagement](#-project-engagement)
- [License](#-license)

## ✨ Capabilities

- Star names for Galactic Civilizations II, Galactic Civilizations III, and Stellaris, drawn from dozens of universes, including Star Wars, Star Trek, Dune, Elder Scrolls, Doctor Who, Stargate, StarCraft, and many more
- Nebula names for Stellaris, from Elite Dangerous, No Man's Sky, Warhammer 40K, Star Wars, and other sources
- Asteroid name prefixes and postfixes for Stellaris
- Black hole names for Stellaris, from Elite Dangerous and other sci-fi sources

## 🚀 Usage

For Galactic Civilizations II, replace the game's star name data files as described in the installation instructions and start a new game. For Galactic Civilizations III, enable the mod in the game and start a new galaxy. For Stellaris, enable the mod in the launcher and start a new game; the additional names are applied automatically during galaxy generation.

## ⚠️ Known Limitations

- Names are selected during galaxy generation, so they apply only to newly generated galaxies and do not rename celestial bodies in existing saved games.
- Galactic Civilizations II does not support overriding star names through a mod, so its archive is a drop-in replacement for the game's shipped `Data/English/STARS.txt` rather than a mod that can be enabled in the game.
- Galactic Civilizations III reads its random star names from the game's `Text/StarNamesText.xml`, which the mod replaces; fixed homeworld star systems keep their own names.

## 📦 Installation

### Galactic Civilizations II

[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://www.nexusmods.com/galacticcivilizations2/mods/2)
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

Galactic Civilizations II does not support overriding star names through a mod, so the archived star name files replace the game's shipped files.

#### Manual Instructions

**Linux**

1. Back up `Data/English/STARS.txt` and `Twilight/Data/English/STARS.txt` inside your game's installation directory (`~/.steam/steam/steamapps/common/Galactic Civilizations II - Ultimate Edition/`).
2. Copy the archived `Data/English/STARS.txt` and `Twilight/Data/English/STARS.txt` over them.

**Windows**

1. Back up `Data\English\STARS.txt` and `Twilight\Data\English\STARS.txt` inside your game's installation directory (`%ProgramFiles(x86)%\Steam\steamapps\common\Galactic Civilizations II - Ultimate Edition\`).
2. Copy the archived `Data\English\STARS.txt` and `Twilight\Data\English\STARS.txt` over them.

Because Dark Avatar ships its own star name list in `DarkAvatar/Data/English/STARS.txt`, replace that file as well when playing the Dark Avatar executable. New names apply only to newly generated galaxies.

### Galactic Civilizations III

[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://www.nexusmods.com/galacticcivilizations3/mods/173)
[![Obtain it from Steam Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=3844651637)
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

Galactic Civilizations III supports overriding its star name file through a mod, so the archived `ui-star-names/` folder is installed into the game's `Mods` directory.

#### Manual Instructions

**Linux**

1. Extract the `ui-star-names/` folder into `~/.steam/steam/steamapps/compatdata/226860/pfx/drive_c/users/steamuser/Documents/My Games/GalCiv3/Mods` (or the corresponding `GC3Crusade` directory for the Crusade and Intrigue expansions). The path is inside the game's Proton prefix, not the Steam installation directory.
2. Enable mods in the game options, or set `EnableMods=1` in `Prefs.ini`, then restart the game.
3. Start a new galaxy; the mod's star names replace the vanilla names.

**Windows**

1. Extract the `ui-star-names/` folder into `%USERPROFILE%\Documents\My Games\GalCiv3\Mods` (or `%USERPROFILE%\Documents\My Games\GC3Crusade\Mods` for the Crusade and Intrigue expansions). The folder contains `Text/StarNamesText.xml` plus the mandatory `ParticleScriptDefs`, `Core`, and `Game` folders the game requires every mod to provide.
2. Enable mods in the game options, or set `EnableMods=1` in `Prefs.ini`, then restart the game.
3. Start a new galaxy; the mod's star names replace the vanilla names.

The mod replaces the game's `Text/StarNamesText.xml`, which holds the random star names as `RANDOM_STAR_NAME_<index>` entries, while fixed homeworld star systems keep their own names. New names apply only to newly generated galaxies.

### Stellaris

[![Obtain it from Steam Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)
[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://nexusmods.com/stellaris/mods/74)
[![Obtain it from Paradox Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/paradox-mods.png)](https://mods.paradoxplaza.com/mods/25413/Any)
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

Download the [latest release](https://github.com/hmlendea/stellaris-ui-star-names/releases), extract `ui-star-names/` and `ui-star-names.mod` into your game's mod directory, and enable the mod in the launcher.

## 🧩 Compatibility

| Component | Supported Versions | Notes |
|-----------|--------------------|-------|
| Galactic Civilizations II | Ultimate Edition (`v2.21`, Twilight of the Arnor) | Star names are read from the game's own `Data/English/STARS.txt`, `DarkAvatar/Data/English/STARS.txt`, and `Twilight/Data/English/STARS.txt` files |
| Galactic Civilizations III | `v4.x` | Star names are read from the game's `Text/StarNamesText.xml` file, which the mod replaces |
| Stellaris | `4.5.x` | Declared through `supported_version` in both `ui-star-names.mod` and `ui-star-names/descriptor.mod` |

## 🛡️ Privacy and Data

Universum Infinitum - Star Names does not collect, process, store, or transmit any personal data.

For the detailed description of how the application handles privacy and personal data, see the [Privacy Statement](./PRIVACY.md).

## 🛠️ Development

### Requirements

- [Galactic Civilizations II - Ultimate Edition](https://store.steampowered.com/app/202200/Galactic_Civilizations_II_Ultimate_Edition/)
- [Galactic Civilizations III](https://store.steampowered.com/app/226860/Galactic_Civilizations_III/)
- [Stellaris](https://store.steampowered.com/app/281990/Stellaris/)
- [Bash](https://www.gnu.org/software/bash/), used by the name count script

### Setup

Clone the repository, then generate only the targets you need; the Stellaris output can be symlinked into your Stellaris `mod/` directory.

### Build

The distributable mod is generated from the name lists in `src/names/` by running the generation script with the desired version number and the target game:

```bash
python3 scripts/generate-mod.py --version 1.0.0 --game galciv2
python3 scripts/generate-mod.py --version 1.0.0 --game galciv3
python3 scripts/generate-mod.py --version 1.0.0 --game stellaris
```

The `--version` and `--game` arguments are mandatory, and `--game` accepts `galciv2`, `galciv3`, or `stellaris`, case-insensitively.

For `galciv2`, only the star name data files are written, to `out/galciv2/Data/English/STARS.txt` and `out/galciv2/Twilight/Data/English/STARS.txt` (a copy of the former), with one star name per line in the Windows-1252 encoding and CRLF line endings expected by the game; these files are meant to replace the game's shipped star name files rather than to be installed as a mod. For `galciv3`, the mod is written to `out/galciv3/ui-star-names/`, containing `Text/StarNamesText.xml` (a UTF-8 string table of `RANDOM_STAR_NAME_<index>` entries with CRLF line endings and the `StringTable.xsd` schema declaration expected by the game) together with the mandatory `ParticleScriptDefs`, `Core`, and `Game` folders; the `ui-star-names/` folder is meant to be placed in the game's `Mods` directory. For `stellaris`, the complete mod is written to `out/stellaris/`, containing `ui-star-names/` (with `descriptor.mod`, `thumbnail.png`, and the aggregated name list) and `ui-star-names.mod`.

### Run

For Galactic Civilizations II, replace the generated `Data/English/STARS.txt` and `Twilight/Data/English/STARS.txt` files in the game installation and start a new game. For Galactic Civilizations III, copy the generated `ui-star-names/` folder into the game's `Mods` directory, enable mods, and start a new galaxy. For Stellaris, enable the mod in the launcher and start a new game.

### Test

Run the name count script to detect accidental removals or additions of name entries:

```bash
./scripts/count-additions.sh
```

## ⚙️ GitHub Actions

| Workflow | Purpose | What it does |
|----------|---------|--------------|
| [ CI ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/build.yml) | Build the content | Triggers on pushes and pull requests to `master`, builds the Galactic Civilizations II and III star name data and the Stellaris mod in separate jobs from the source name lists in `src/names/`, and fails if any generation does not succeed |
| [ Steam Workshop ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/steam-workshop-release.yml) | Publish releases to the Steam Workshop | Triggers on version tags or manual dispatch, generates the Galactic Civilizations III mod with `scripts/generate-mod.py --version <version> --game galciv3` and the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris` in separate jobs using the release version, then uploads each with the `hmlendea/steam-workshop-update` action |
| [ Nexus Mods ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/nexus-mods-release.yml) | Publish releases to Nexus Mods | Triggers on version tags or manual dispatch, generates the Stellaris mod and the Galactic Civilizations II and III star name data using the release version, builds and uploads one release archive per game with the `Nexus-Mods/upload-action` action |
| [ GitHub Release ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/github-release.yml) | Publish the release archives to GitHub Releases | Triggers on release publication or manual dispatch, generates the Galactic Civilizations II and III star name data and the Stellaris mod in separate jobs using the release version, builds `ui-star-names-galciv2_<version>.zip`, `ui-star-names-galciv3_<version>.zip`, and `ui-star-names_<version>.zip`, and uploads them with `softprops/action-gh-release` |

## 🗂️ Project Structure

### Directories

| Directory | Purpose |
|-----------|---------|
| `src/names/` | Source name lists, aggregated into the distributable content |
| `ui-star-names/common/random_names/base/` | Generated Stellaris name list files for stars, nebulas, asteroids, and black holes |
| `ui-star-names/` | Generated Stellaris mod content, including `descriptor.mod` |
| `description/` | Steam Workshop page body (`steam-workshop.bbcode`); not shipped with the mod |
| `scripts/` | Content generation and name counting scripts |
| `docs/` | Repository documentation |
| `.github/workflows/` | Release automation workflows |

## 🏗️ Architecture

Universum Infinitum - Star Names is a data-only project that ships star name data files for Galactic Civilizations II and III and static name list files for Stellaris in Clausewitz script format. The Stellaris game engine loads these files during galaxy generation and randomly selects names for stars, nebulas, asteroids, and black holes, while Galactic Civilizations II reads its own star name file before mods are loaded and Galactic Civilizations III reads its star name file through a mod that replaces it. None of the games run custom code of the project's own; the repository contains the source name lists, the generation script that aggregates them into the distributable content, and the release automation that publishes it.

See the [Architecture Documentation](./ARCHITECTURE.md) for the system context, principal components, runtime flows, ownership boundaries, dependencies, constraints, and extension points.

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) directory:

| Resource | Description |
|----------|-------------|
| [Documentation Index](./docs/INDEX.md) | Master catalogue with navigation |
| [Architecture & Design](./docs/architecture.md) | Implementation detail |
| [Repository Structure](./docs/repository-structure.md) | Source tree layout |
| [Data Model](./docs/data-model.md) | Domain entities and relationships |
| [Components](./docs/components/) | Name lists, metadata, release automation |
| [Flows](./docs/flows/) | Mod loading, release distribution |
| [Behaviour](./docs/behaviour/) | Name selection, contribution workflow |
| [Configuration](./docs/config/) | Descriptor schema, name list format |
| [Testing](./docs/testing/test-strategy.md) | Test strategy |
| [Operations](./docs/operations/) | Deployment, troubleshooting |
| [API Reference](./docs/api-reference/) | Engine internal APIs |
| [Logging](./docs/logging.md) | Engine log patterns |

## 🩺 Troubleshooting

| Symptom | Probable Cause | Resolution |
|---------|----------------|------------|
| Mod absent from the launcher mod list | Descriptor not placed at `ui-star-names/descriptor.mod`, or the mod folder is outside the Stellaris `mod/` directory | Move the descriptor to the correct path and place the mod folder inside the Stellaris `mod/` directory |
| Launcher reports the mod as incompatible | `supported_version` does not match the installed Stellaris version | Update `supported_version` in both descriptor files, then restart the launcher |
| Only vanilla names appear in game | Stellaris mod disabled, incorrect category field, or a syntax error in a referenced file | Enable the mod in the launcher, verify the `category` value, and inspect `logs/error.log` |
| Galactic Civilizations II still uses vanilla names | The game's `Data/English/STARS.txt` was not replaced, or the galaxy was generated before the replacement | Replace the game's star name files as described in the installation instructions and start a new galaxy |
| Galactic Civilizations III still uses vanilla names | The `ui-star-names/` folder is outside the game's `Mods` directory, mods are disabled, or the galaxy was generated before the mod was enabled | Place the `ui-star-names/` folder in the `Mods` directory, enable mods, and start a new galaxy |

## 📜 Code of Conduct

See the [Code of Conduct](./CODE_OF_CONDUCT.md) for the standards of conduct expected in all project spaces.

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility
- Submit focused pull requests that conform to the existing code style
- Maintain your branch synchronised with `master`
- Revise the documentation when functionality changes
- Properly test all modifications, including edge cases and error conditions
- Include tests for additional or modified functionality
- Raise a new [issue](https://github.com/hmlendea/stellaris-ui-star-names/issues) for problems or suggestions

See the [Contributing Guidelines](./CONTRIBUTING.md) for details on how to report issues, suggest enhancements, and submit changes.

## 🔗 Related Projects

- [Character Traits](https://github.com/hmlendea/stellaris-ui-character-traits): Adds character traits for Stellaris.
- [Deposit Blockers](https://github.com/hmlendea/stellaris-ui-deposit-blockers): Adds deposit blockers for Stellaris.
- [Flags](https://github.com/hmlendea/stellaris-ui-flags): Supplies flag assets used by this mod.
- [Galaxy Sizes](https://github.com/hmlendea/stellaris-ui-galaxy-sizes): Adds galaxy size options for Stellaris.
- [Name Lists](https://github.com/hmlendea/stellaris-ui-name-lists): Supplies name lists used by this mod.
- [Planet Modifiers](https://github.com/hmlendea/stellaris-ui-planet-modifiers): Adds planet modifiers for Stellaris.
- [Species Names](https://github.com/hmlendea/stellaris-ui-species-names): Adds species names for Stellaris.
- [Species Traits](https://github.com/hmlendea/stellaris-ui-species-traits): Supplies species traits used by this mod.
- [Star Names](https://github.com/hmlendea/stellaris-ui-star-names): Adds star names for Stellaris.

## 🔒 Security

Universum Infinitum - Star Names consists solely of static text files and does not execute code, process user data, or communicate over networks.

For information on reporting security vulnerabilities, see the [Security Policy](./SECURITY.md).

## 💬 Support

For support, please [open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues).

## 💝 Project Engagement

Discovered a problem with Universum Infinitum - Star Names or have a suggestion for it? [Open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub, or giving it a thumbs up and adding it as a favourite on the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

## 📄 License

This project is being distributed under the `GNU General Public License v3` or later.
See [LICENSE](./LICENSE) for additional information.
