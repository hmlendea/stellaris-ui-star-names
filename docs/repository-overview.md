# Repository Overview

## Purpose

This repository hosts the name sources for the Universum Infinitum - Star Names project, a set of data modifications for the games Stellaris, Galactic Civilizations II, and Galactic Civilizations III that add thousands of new star names, and, for Stellaris, additional nebula, asteroid, and black hole names. The content is distributed via Steam Workshop, Nexus Mods, Paradox Mods, and GitHub Releases.

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
| Build workflow | `.github/workflows/build.yml` | Generates the complete mod from the source name lists on every push and pull request to `master` |
| Steam Workshop workflow | `.github/workflows/steam-workshop-release.yml` | Automates packaging and publishing the Stellaris and Galactic Civilizations III mods to Steam Workshop on version tag push |
| Nexus Mods workflow | `.github/workflows/nexus-mods-release.yml` | Automates packaging and publishing to Nexus Mods on version tag push |
| GitHub Release workflow | `.github/workflows/github-release.yml` | Builds and attaches the release archive to a published GitHub Release |
| Name counting script | `scripts/count-additions.sh` | Utility to count unique names across all list files for release notes |
| Mod generation script | `scripts/generate-mod.py` | Generates the distributable Stellaris mod under `out/stellaris/`, the Galactic Civilizations II star name data file under `out/galciv2/Data/English/STARS.txt`, or the Galactic Civilizations III star name data file under `out/galciv3/ui-star-names/Text/StarNamesText.xml` from `src/names/`, taking the version number and the game through the mandatory `--version` and `--game` options (`stellaris`, `galciv2`, or `galciv3`, case-insensitive) |

## Repository Type

This is a **data-driven** repository for a game mod. The distributable Stellaris mod is generated from the source name lists in `src/names/` by `scripts/generate-mod.py`, which writes the complete Stellaris mod to `out/stellaris/`, the Galactic Civilizations II star name data file to `out/galciv2/Data/English/STARS.txt`, or the Galactic Civilizations III star name data file to `out/galciv3/ui-star-names/Text/StarNamesText.xml`, depending on the `--game` option. The packaged Stellaris release is a ZIP archive containing the `ui-star-names/` directory and `ui-star-names.mod`; the Galactic Civilizations II release is a ZIP archive containing only `Data/English/STARS.txt`, which replaces the game's shipped star name file because the game does not support overriding star names through a mod; the Galactic Civilizations III release is a ZIP archive containing the `ui-star-names/` mod folder, which replaces the game's star name file through a mod placed in the game's `Mods` directory.

## Target Audience

- **Mod maintainers**: Manage releases, review contributions, update game version compatibility
- **Contributors**: Add new name lists, fix typos, organise existing names
- **Users**: Install the mod via Steam Workshop, Nexus Mods, Paradox Mods, or manual ZIP extraction
- **Downstream modders**: Reference name list format and organisation for their own mods

## Value Proposition

The project extends galaxy generation in Galactic Civilizations II, Galactic Civilizations III, and Stellaris by providing additional star names drawn from science fiction, fantasy, games, and real astronomical catalogues. It requires no configuration, no dependencies beyond the respective games, and works automatically. For Stellaris it is enabled in the launcher, for Galactic Civilizations III as a mod in the game's `Mods` directory, and for Galactic Civilizations II by replacing the game's shipped star name files.