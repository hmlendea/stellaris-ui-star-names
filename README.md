[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/releases/latest)
[![Build Status](https://github.com/hmlendea/stellaris-ui-star-names/actions/workflows/build.yml/badge.svg)](https://github.com/hmlendea/stellaris-ui-star-names/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/LICENSE)

# Stellaris - Universum Infinitum - Star Names

Mod for Stellaris that adds [thousands of new names](https://github.com/hmlendea/stellaris-ui-star-names/wiki/Additions) for stars, nebulas, asteroids, and black holes, drawn from science fiction, fantasy, games, and real astronomical catalogues.

## 📑 Table of Contents

- [Capabilities](#-capabilities)
- [Usage](#-usage)
- [Known Limitations](#-known-limitations)
- [Installation](#-installation)
  - [Manual Installation](#manual-installation)
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

- Star names from dozens of universes, including Star Wars, Star Trek, Dune, Elder Scrolls, Doctor Who, Stargate, StarCraft, and many more
- Nebula names from Elite Dangerous, No Man's Sky, Warhammer 40K, Star Wars, and other sources
- Asteroid name prefixes and postfixes
- Black hole names from Elite Dangerous and other sci-fi sources

## 🚀 Usage

Enable the mod in the Stellaris launcher and start a new game. The additional names are applied automatically when starting a new game.

## ⚠️ Known Limitations

- Names are selected during galaxy generation, so they apply only to newly generated galaxies and do not rename celestial bodies in existing saved games.
- Galactic Civilizations II does not support overriding star names through a mod, so its archive is a drop-in replacement for the game's shipped `Data/English/STARS.txt` rather than a mod that can be enabled in the game.

## 📦 Installation

[![Obtain it from Steam Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)
[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://nexusmods.com/stellaris/mods/74)
[![Obtain it from Paradox Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/paradox-mods.png)](https://mods.paradoxplaza.com/mods/25413/Any)
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

### Manual Installation

For Stellaris, download the [latest release](https://github.com/hmlendea/stellaris-ui-star-names/releases), extract `ui-star-names/` and `ui-star-names.mod` into your game's mod directory, and enable the mod in the launcher.

For Galactic Civilizations II, download the [latest release](https://github.com/hmlendea/stellaris-ui-star-names/releases) and replace the game's shipped star name files with the archived ones. Galactic Civilizations II does not support overriding star names through a mod, so the game's own data files must be replaced:

1. Back up the existing `Data/English/STARS.txt` and `Twilight/Data/English/STARS.txt` files inside your game's installation directory.
2. Copy the archived `Data/English/STARS.txt` and `Twilight/Data/English/STARS.txt` over them.

Because Dark Avatar ships its own star name list in `DarkAvatar/Data/English/STARS.txt`, replace that file as well when playing the Dark Avatar executable. New names apply only to newly generated galaxies.

## 🧩 Compatibility

| Component | Supported Versions | Notes |
|-----------|--------------------|-------|
| Stellaris | `4.5.x` | Declared through `supported_version` in both `ui-star-names.mod` and `ui-star-names/descriptor.mod` |

## 🛡️ Privacy and Data

Stellaris - Universum Infinitum - Star Names does not collect, process, store, or transmit any personal data.

For the detailed description of how the application handles privacy and personal data, see the [Privacy Statement](./PRIVACY.md).

## 🛠️ Development

### Requirements

- [Stellaris](https://store.steampowered.com/app/281990/Stellaris/)
- [Bash](https://www.gnu.org/software/bash/), used by the name count script

### Setup

Copy or symlink `ui-star-names/` and `ui-star-names.mod` inside your Stellaris' `mod/` directory.

### Build

The distributable mod is generated from the name lists in `src/names/` by running the generation script with the desired version number and the target game:

```bash
python3 scripts/generate-mod.py --version 1.0.0 --game stellaris
python3 scripts/generate-mod.py --version 1.0.0 --game galciv2
```

The `--version` and `--game` arguments are mandatory, and `--game` accepts `stellaris` or `galciv2`, case-insensitively.

For `stellaris`, the complete mod is written to `out/stellaris/`, containing `ui-star-names/` (with `descriptor.mod`, `thumbnail.png`, and the aggregated name list) and `ui-star-names.mod`. For `galciv2`, only the star name data files are written, to `out/galciv2/Data/English/STARS.txt` and `out/galciv2/Twilight/Data/English/STARS.txt` (a copy of the former), with one star name per line in the Windows-1252 encoding and CRLF line endings expected by the game; these files are meant to replace the game's shipped star name files rather than to be installed as a mod.

### Run

Enable the mod in the Stellaris launcher and start a new game.

### Test

Run the name count script to detect accidental removals or additions of name entries:

```bash
./scripts/count-additions.sh
```

## ⚙️ GitHub Actions

| Workflow | Purpose | What it does |
|----------|---------|--------------|
| [ CI ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/build.yml) | Build the content | Triggers on pushes and pull requests to `master`, builds the Stellaris mod and the Galactic Civilizations II star name data in separate jobs from the source name lists in `src/names/`, and fails if either generation does not succeed |
| [ Steam Workshop ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/steam-workshop-release.yml) | Publish releases to the Steam Workshop | Triggers on version tags or manual dispatch, generates the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris` using the release version, then uploads it with the `hmlendea/steam-workshop-update` action |
| [ Nexus Mods ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/nexus-mods-release.yml) | Publish releases to Nexus Mods | Triggers on version tags or manual dispatch, generates the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris` using the release version, builds the release archive, then uploads it with the `Nexus-Mods/upload-action` action |
| [ GitHub Release ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/github-release.yml) | Publish the release archives to GitHub Releases | Triggers on release publication or manual dispatch, generates the Stellaris mod and the Galactic Civilizations II star name data in separate jobs using the release version, builds `ui-star-names_<version>.zip` and `ui-star-names-galciv2_<version>.zip`, and uploads them with `softprops/action-gh-release` |

## 🗂️ Project Structure

### Directories

| Directory | Purpose |
|-----------|---------|
| `ui-star-names/common/random_names/base/` | Name list files for stars, nebulas, asteroids, and black holes |
| `ui-star-names/` | Mod content, including `descriptor.mod` |
| `docs/` | Repository documentation |
| `.github/workflows/` | Release automation workflows |

## 🏗️ Architecture

Stellaris - Universum Infinitum - Star Names is a data mod that ships static name list files in Clausewitz script format. The Stellaris game engine loads these files during galaxy generation and randomly selects names for stars, nebulas, asteroids, and black holes. The mod has no runtime of its own; the repository contains only the source name lists, the generation script that aggregates them into the distributable mod, and the release automation that publishes it.

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
| Only vanilla names appear in game | Mod disabled, incorrect category field, or a syntax error in a referenced file | Enable the mod in the launcher, verify the `category` value, and inspect `logs/error.log` |

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

Stellaris - Universum Infinitum - Star Names consists solely of static text files and does not execute code, process user data, or communicate over networks.

For information on reporting security vulnerabilities, see the [Security Policy](./SECURITY.md).

## 💬 Support

For support, please [open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues).

## 💝 Project Engagement

Discovered a problem with Stellaris - Universum Infinitum - Star Names or have a suggestion for it? [Open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub, or giving it a thumbs up and adding it as a favourite on the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

## 📄 License

This project is being distributed under the `GNU General Public License v3` or later.
See [LICENSE](./LICENSE) for additional information.
