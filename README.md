[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# Stellaris - Universum Infinitum - Star Names

Mod for Stellaris that adds [thousands of new names](https://github.com/hmlendea/stellaris-ui-star-names/wiki/Additions) for stars, nebulas, asteroids, and black holes, drawn from science fiction, fantasy, games, and real astronomical catalogues.

## 📑 Table of Contents

- [Capabilities](#-capabilities)
- [Usage](#-usage)
- [Installation](#-installation)
- [Development](#-development)
- [Contributing](#-contributing)
- [Related Projects](#-related-projects)
- [Supporting the Project](#-supporting-the-project)
- [License](#-license)

## ✨ Capabilities

- Star names from dozens of universes, including Star Wars, Star Trek, Dune, Elder Scrolls, Doctor Who, Stargate, StarCraft, and many more
- Nebula names from Elite Dangerous, No Man's Sky, Warhammer 40K, Star Wars, and other sources
- Asteroid name prefixes and postfixes
- Black hole names from Elite Dangerous and other sci-fi sources

## 🚀 Usage

Enable the mod in the Stellaris launcher and start a new game. The additional names are applied automatically when starting a new game.

## 📦 Installation

[![Get it from the Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)
[![Get it from the Nexus](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://nexusmods.com/stellaris/mods/74)
[![Get it from Paradox Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/paradox-mods.png)](https://mods.paradoxplaza.com/mods/25413/Any)
[![Get it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

### Manual Installation

1. Download the [latest release](https://github.com/hmlendea/stellaris-ui-star-names/releases).
2. Extract the contents into your game's mod directory.

## 🛠️ Development

### Requirements

- [Stellaris](https://store.steampowered.com/app/281990/Stellaris/)

### Setup

Copy or symlink `ui-star-names/` and `ui-star-names.mod` inside your Stellaris' `mod/` directory.

### Build

No build step is required. Edit the `.txt` name list files under `ui-star-names/common/random_names/base/` directly.

### Run

Enable the mod in the Stellaris launcher and start a new game.

## 🏗️ Architecture

Stellaris - Universum Infinitum - Star Names is a pure data mod consisting of static name list files in Clausewitz script format. The Stellaris game engine loads these files during galaxy generation and randomly selects names for stars, nebulas, asteroids, and black holes. There is no executable code, build step, or runtime.

See the [architecture documentation](./ARCHITECTURE.md) for the system context, data architecture, deployment model, compatibility contracts, and source map.

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility
- Maintain the pull requests as focused and consistent with the existing code style
- Maintain your branch up-to-date with `master`
- Revise the documentation when behaviour changes
- Properly test all changes

See the [contributing guidelines](./CONTRIBUTING.md) for details on how to report issues, suggest enhancements, and submit changes.

## 🔗 Related Projects

- [Character Traits](https://github.com/hmlendea/stellaris-ui-character-traits): Adds new character trait names for leaders and rulers
- [Deposit Blockers](https://github.com/hmlendea/stellaris-ui-deposit-blockers): Adds new deposit blocker names
- [Flags](https://github.com/hmlendea/stellaris-ui-flags): Adds new flag emblems and backgrounds
- [Galaxy Sizes](https://github.com/hmlendea/stellaris-ui-galaxy-sizes): Adds new galaxy size options for game setup
- [Name Lists](https://github.com/hmlendea/stellaris-ui-name-lists): Adds new species name lists
- [Planet Modifiers](https://github.com/hmlendea/stellaris-ui-planet-modifiers): Adds new planet modifier names
- [Prescripted Countries](https://github.com/hmlendea/stellaris-ui-prescripted-countries): Adds new prescripted empire definitions
- [Species Names](https://github.com/hmlendea/stellaris-ui-species-names): Adds new species name options
- [Species Traits](https://github.com/hmlendea/stellaris-ui-species-traits): Adds new species trait names

## 💝 Supporting the Project

Discovered a problem or have a suggestion? [Open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

## 🛡️ Privacy and Data

Stellaris - Universum Infinitum - Star Names does not collect, process, store, or transmit any personal data. The mod consists of static text files containing fictional and real astronomical names for use in Stellaris.

For the detailed description of how the application handles privacy and personal data, see [PRIVACY.md](./PRIVACY.md).

| Data | Purpose | Storage | Retention | Optional |
|------|---------|---------|-----------|----------|
| None | N/A | N/A | N/A | N/A |

## 🔒 Security

Stellaris - Universum Infinitum - Star Names consists solely of static text files and does not execute code, process user data, or communicate over networks. Security issues are limited to supply chain integrity of distribution packages.

For the security policy, supported versions, and vulnerability reporting process, see [SECURITY.md](./SECURITY.md).

## 📜 Code of Conduct

See the [Code of Conduct](./CODE_OF_CONDUCT.md) for the standards of conduct expected in all project spaces.

## 📄 License

This project is being distributed under the `GNU General Public Licence v3` or later.
See [LICENSE](./LICENSE) for further information.
