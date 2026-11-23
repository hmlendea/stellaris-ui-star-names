# Repository Structure

## Source Tree Layout

```
stellaris-ui-star-names/
├── .github/
│   └── workflows/
│       ├── build.yml               # Continuous integration build
│       ├── github-release.yml      # GitHub Release asset automation
│       ├── nexus-mods-release.yml  # Nexus Mods release automation
│       └── steam-workshop-release.yml  # Steam Workshop release automation
├── ui-star-names/                  # Mod root (recognised by Stellaris launcher)
│   ├── descriptor.mod              # Mod metadata for game launcher
│   └── common/
│       └── random_names/
│           └── base/               # Flat directory of all name list files
│               ├── ui_asteroid-postfixes.txt
│               ├── ui_asteroid-prefixes.txt
│               ├── ui_black-holes.txt
│               ├── ui_black-holes_elite-dangerous.txt
│               ├── ui_black-holes_scifiideas.txt
│               ├── ui_nebulas.txt
│               ├── ui_nebulas_dark-pirates.txt
│               ├── ui_nebulas_distant-worlds.txt
│               ├── ui_nebulas_doctor-who.txt
│               ├── ui_nebulas_elite-dangerous.txt
│               ├── ui_nebulas_fantasy-name-generator.txt
│               ├── ui_nebulas_no-mans-sky.txt
│               ├── ui_nebulas_scifiideas.txt
│               ├── ui_nebulas_star-wars.txt
│               ├── ui_nebulas_void_bastards.txt
│               ├── ui_nebulas_warhammer40k.txt
│               ├── ui_stars_ageofmythology.txt
│               ├── ui_stars_alien.txt
│               ├── ui_stars_aowp.txt
│               ├── ui_stars_artix-entertainment.txt
│               ├── ui_stars_asimov.txt
│               ├── ui_stars_asoiaf.txt
│               ├── ui_stars_authors.txt
│               ├── ui_stars_codominium.txt
│               ├── ui_stars_distant-worlds.txt
│               ├── ui_stars_doctor-who.txt
│               ├── ui_stars_dune.txt
│               ├── ui_stars_elder-scrolls.txt
│               ├── ui_stars_elite-dangerous.txt
│               ├── ui_stars_eons-of-war.txt
│               ├── ui_stars_eve.txt
│               ├── ui_stars_fantasy-name-generator.txt
│               ├── ui_stars_galciv.txt
│               ├── ui_stars_letsmakeagame-net.txt
│               ├── ui_stars_markov.txt
│               ├── ui_stars_master-of-orion.txt
│               ├── ui_stars_middleearth.txt
│               ├── ui_stars_middleearth copy.txt
│               ├── ui_stars_nmsgen.txt
│               ├── ui_stars_no-mans-sky.txt
│               ├── ui_stars_pax-nova.txt
│               ├── ui_stars_predestination.txt
│               ├── ui_stars_real.txt
│               ├── ui_stars_rotp.txt
│               ├── ui_stars_sins-of-a-solar-empire.txt
│               ├── ui_stars_star-trek.txt
│               ├── ui_stars_star-wars.txt
│               ├── ui_stars_starcraft.txt
│               ├── ui_stars_stargate.txt
│               ├── ui_stars_starruler2.txt
│               ├── ui_stars_zzz_made-up.txt
│               ├── ui_stars_zzz_media.txt
│               ├── ui_stars_zzz_others.txt
│               └── ui_stars_zzz_places.txt
├── ui-star-names.mod               # Mod descriptor for Steam Workshop
├── description/
│   └── steam-workshop.bbcode       # Steam Workshop page body (BBCode)
├── scripts/                        # Build and utility scripts
│   ├── count-additions.sh          # Name counting utility script
│   └── generate-mod.py             # Mod generation script
├── ARCHITECTURE.md                 # System architecture documentation
├── CODE_OF_CONDUCT.md              # Community conduct standards
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # GNU GPL v3 license
├── PRIVACY.md                      # Privacy and data handling statement
├── README.md                       # Project overview and usage
├── ROADMAP.md                      # Project roadmap
└── SECURITY.md                     # Security policy
```

## Module Organisation

### Mod Data (`ui-star-names/`)

The mod directory follows Stellaris' expected structure:

- **`descriptor.mod`**: Required by the game launcher. Contains `name`, `path`, `tags`, and `supported_version`.
- **`common/random_names/base/`**: Flat directory containing all name list files. The game engine scans this directory recursively for `.txt` files containing `name_list` definitions.

### Name List Files

Naming convention: `ui_<category>_<source>.txt`

| Category | Prefix | Examples |
|----------|--------|----------|
| Stars | `ui_stars_` | `ui_stars_star-wars.txt`, `ui_stars_dune.txt`, `ui_stars_real.txt` |
| Nebulas | `ui_nebulas_` | `ui_nebulas_elite-dangerous.txt`, `ui_nebulas_warhammer40k.txt` |
| Asteroid prefixes | `ui_asteroid-prefixes` | `ui_asteroid-prefixes.txt` (single file) |
| Asteroid postfixes | `ui_asteroid-postfixes` | `ui_asteroid-postfixes.txt` (single file) |
| Black holes | `ui_black-holes_` | `ui_black-holes.txt`, `ui_black-holes_elite-dangerous.txt` |

Special naming:
- `ui_stars_zzz_*.txt`: Catch-all categories for miscellaneous names (made-up, media, others, places)
- `ui_stars_middleearth copy.txt`: Duplicate file (likely an artifact)

### Distribution Descriptors

- **`ui-star-names.mod`**: Used by Steam Workshop upload workflow. Identical content to `ui-star-names/descriptor.mod` but at repository root for the workflow to reference.
- **`ui-star-names/descriptor.mod`**: Read by the Stellaris game launcher.

### Steam Workshop Page Body (`description/`)

The `description/` directory sits outside the payload and is not delivered to any game. It holds `steam-workshop.bbcode`, the BBCode body pasted into the Steam Workshop item description. The publication workflows upload mod content only and do not manage that text.

### Release Automation (`.github/workflows/`)

- **`build.yml`**: Triggers on pushes and pull requests to `master`. Builds the Galactic Civilizations II and III star name data in the `galciv2` and `galciv3` jobs and the Stellaris mod in the `stellaris` job, failing the build when any generation fails.
- **`steam-workshop-release.yml`**: Triggers on version tags (`v*.*.*`) or manual dispatch. Generates the Galactic Civilizations III mod and the Stellaris mod in separate jobs with `scripts/generate-mod.py --version <version> --game galciv3` and `scripts/generate-mod.py --version <version> --game stellaris` using the release version, and uploads each generated mod directory to Steam Workshop using the `hmlendea/steam-workshop-update` action.
- **`nexus-mods-release.yml`**: Triggers on version tags or manual dispatch. Generates the Stellaris mod and the Galactic Civilizations II star name data with `scripts/generate-mod.py` in its single `release` job using the release version, builds one release archive per game from the generated output, and uploads both to Nexus Mods using `Nexus-Mods/upload-action`.
- **`github-release.yml`**: Triggers on release publication or manual dispatch. Generates the Galactic Civilizations II and III star name data in the `galciv2` and `galciv3` jobs and the Stellaris mod in the `stellaris` job using the release version, builds `ui-star-names_galciv2_<version>.zip`, `ui-star-names_galciv3_<version>.zip`, and `ui-star-names_stellaris_<version>.zip` from the generated output, and attaches all three to the release using `softprops/action-gh-release`.

### Utility Scripts

- **`scripts/count-additions.sh`**: Bash script that counts unique names across all source list files by category. Used for release notes.
- **`scripts/generate-mod.py`**: Python script that generates the complete distributable Stellaris mod under `out/stellaris/`, the Galactic Civilizations II star name data file under `out/galciv2/Data/English/STARS.txt`, or the Galactic Civilizations III star name data file under `out/galciv3/ui-star-names/Text/StarNamesText.xml` from the name lists in `src/names/`. Accepts the version number and the target game through the mandatory `--version` and `--game` options (`stellaris`, `galciv2`, or `galciv3`, case-insensitive).

### Root Documentation

All policy and overview documents reside at repository root per GitHub conventions:
- `README.md` — Project overview
- `ARCHITECTURE.md` — Technical architecture
- `CONTRIBUTING.md` — Contribution process
- `SECURITY.md` — Security policy
- `PRIVACY.md` — Data handling
- `CODE_OF_CONDUCT.md` — Community standards
- `LICENSE` — GPL v3
- `ROADMAP.md` — Future plans

## File Count Summary

| Category | File Count |
|----------|------------|
| Star name lists | 36 |
| Nebula name lists | 13 |
| Asteroid prefix lists | 1 |
| Asteroid postfix lists | 1 |
| Black hole name lists | 3 |
| **Total name list files** | **54** |
| Workflow files | 4 |
| Descriptor files | 2 |
| Utility scripts | 2 |
| Root documentation | 8 |
| **Total repository files** | **~70** |