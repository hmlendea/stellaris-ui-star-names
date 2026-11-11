[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/releases/latest)
[![License](https://img.shields.io/github/license/hmlendea/stellaris-ui-star-names)](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/LICENSE)

# Stellaris - Universum Infinitum - Star Names

Mod for Stellaris that adds [thousands of new names](https://github.com/hmlendea/stellaris-ui-star-names/wiki/Additions) for stars, nebulas, asteroids, and black holes, drawn from science fiction, fantasy, games, and real astronomical catalogues.

## 📑 Table of Contents

- [Capabilities](#-capabilities)
- [Usage](#-usage)
- [Installation](#-installation)
- [Development](#-development)
- [GitHub Actions](#-github-actions)
- [Architecture](#-architecture)
- [Documentation](#-documentation)
- [Privacy and Data](#-privacy-and-data)
- [Security](#-security)
- [Code of Conduct](#-code-of-conduct)
- [Contributing](#-contributing)
- [Related Projects](#-related-projects)
- [Project Engagement](#-project-engagement)
- [License](#-license)

## ✨ Capabilities

- Star names from dozens of universes, including Star Wars, Star Trek, Dune, Elder Scrolls, Doctor Who, Stargate, StarCraft, and many more
- Nebula names from Elite Dangerous, No Man's Sky, Warhammer 40K, Star Wars, and other sources
- Asteroid name prefixes and postfixes
- Black hole names from Elite Dangerous and other sci-fi sources

## 🚀 Usage

Enable the mod in the Stellaris launcher and start a new game. The additional names are applied automatically when starting a new game.

## 📦 Installation

[![Obtain it from Steam Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)
[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://nexusmods.com/stellaris/mods/74)
[![Obtain it from Paradox Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/paradox-mods.png)](https://mods.paradoxplaza.com/mods/25413/Any)
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/hmlendea/stellaris-ui-star-names/releases)

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

## ⚙️ GitHub Actions

| Workflow | Purpose | What it does |
|----------|---------|--------------|
| [ Steam Workshop ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/steam-workshop.yml) | Publish releases to the Steam Workshop | Builds the release archive containing `ui-star-names/` and `ui-star-names.mod`, then uploads it with the `hmlendea/steam-workshop-update` action |
| [ Nexus Mods ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/nexus-mods.yml) | Publish releases to Nexus Mods | Builds the release archive containing `ui-star-names/` and `ui-star-names.mod`, then uploads it with the `Nexus-Mods/upload-action` action |
| [ GitHub Release ](https://github.com/hmlendea/stellaris-ui-star-names/blob/master/.github/workflows/github-release.yml) | Publish the release archive to GitHub Releases | Builds `ui-star-names_<version>.zip` containing `ui-star-names/` and `ui-star-names.mod`, uploads it with `softprops/action-gh-release`, and appends the SHA1 checksum to the release notes |

## 🏗️ Architecture

Stellaris - Universum Infinitum - Star Names is a pure data mod consisting of static name list files in Clausewitz script format. The Stellaris game engine loads these files during galaxy generation and randomly selects names for stars, nebulas, asteroids, and black holes. There is no executable code, build step, or runtime.

See the [architecture documentation](./ARCHITECTURE.md) for the system context, data architecture, deployment model, compatibility contracts, and source map.

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

## 🛡️ Privacy and Data

Stellaris - Universum Infinitum - Star Names does not collect, process, store, or transmit any personal data.

For the detailed description of how the application handles privacy and personal data, see [PRIVACY.md](./PRIVACY.md).

## 🔒 Security

Stellaris - Universum Infinitum - Star Names consists solely of static text files and does not execute code, process user data, or communicate over networks.

For information on reporting security vulnerabilities, see [SECURITY.md](./SECURITY.md).

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

See the [contributing guidelines](./CONTRIBUTING.md) for details on how to report issues, suggest enhancements, and submit changes.

## 🔗 Related Projects

- [Character Traits](https://github.com/hmlendea/stellaris-ui-character-traits): Adds new character trait names for leaders and rulers

## 💝 Project Engagement

Discovered a problem or have a suggestion? [Open an issue](https://github.com/hmlendea/stellaris-ui-star-names/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub, or giving it a thumbs up and adding it as a favourite on the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2040215185)!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

## 📄 License

This project is being distributed under the GNU General Public License v3 or later.
See [LICENSE](./LICENSE) for additional information.
