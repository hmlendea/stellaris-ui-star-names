# Repository Overview

## Purpose

This repository hosts the source files for the Stellaris - Universum Infinitum - Star Names mod, a pure data modification for the game Stellaris that adds thousands of new names for stars, nebulas, asteroids, and black holes. The mod is distributed via Steam Workshop, Nexus Mods, Paradox Mods, and GitHub Releases.

## Scope

The repository contains:

- **Mod data files**: Static text files in Clausewitz script format defining name lists for celestial bodies
- **Mod descriptors**: Metadata files (`descriptor.mod`, `ui-star-names.mod`) consumed by the game launcher and distribution platforms
- **Release automation**: GitHub Actions workflows for automated publishing to Steam Workshop and Nexus Mods
- **Utility scripts**: Shell script for counting unique names across all list files
- **Documentation**: Root-level policy documents (README, ARCHITECTURE, CONTRIBUTING, SECURITY, PRIVACY, CODE_OF_CONDUCT, LICENSE)

## Entry Points

| Entry Point | Path | Purpose |
|-------------|------|---------|
| Mod root (game launcher) | `ui-star-names/` | Top-level mod directory recognised by Stellaris launcher |
| Mod descriptor (launcher) | `ui-star-names/descriptor.mod` | Defines mod identity, version compatibility, and tags for the game launcher |
| Mod descriptor (Steam) | `ui-star-names.mod` | Used by Steam Workshop upload workflow; references the mod directory |
| Name list directory | `ui-star-names/common/random_names/base/` | Flat directory containing all name list files |
| Steam Workshop workflow | `.github/workflows/steam-workshop.yml` | Automates packaging and publishing to Steam Workshop on version tag push |
| Nexus Mods workflow | `.github/workflows/nexus-mods.yml` | Automates packaging and publishing to Nexus Mods on version tag push |
| Name counting script | `count-additions.sh` | Utility to count unique names across all list files for release notes |

## Repository Type

This is a **content-only repository** for a game mod. It contains no executable code, build system, test suite, or runtime. The "build" is a simple ZIP archive containing the `ui-star-names/` directory and `ui-star-names.mod`, produced by each release workflow.

## Target Audience

- **Mod maintainers**: Manage releases, review contributions, update game version compatibility
- **Contributors**: Add new name lists, fix typos, organise existing names
- **Users**: Install the mod via Steam Workshop, Nexus Mods, Paradox Mods, or manual ZIP extraction
- **Downstream modders**: Reference name list format and organisation for their own mods

## Value Proposition

The mod extends Stellaris galaxy generation by providing additional name lists drawn from science fiction, fantasy, games, and real astronomical catalogues. It requires no configuration, no dependencies beyond the base game, and works automatically when enabled in the launcher.