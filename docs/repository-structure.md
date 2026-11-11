# Repository Structure

## Source Tree Layout

```
stellaris-ui-star-names/
├── .github/
│   └── workflows/
│       ├── nexus-mods.yml          # Nexus Mods release automation
│       └── steam-workshop.yml      # Steam Workshop release automation
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
├── count-additions.sh              # Name counting utility script
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

### Release Automation (`.github/workflows/`)

- **`steam-workshop.yml`**: Triggers on version tags (`v*.*.*`). Builds the release archive (`ui-star-names/` and `ui-star-names.mod`), unzips it, and uploads to Steam Workshop using `hmlendea/steam-workshop-update` action.
- **`nexus-mods.yml`**: Triggers on version tags or manual dispatch. Builds the release archive and uploads it to Nexus Mods using `Nexus-Mods/upload-action`.
- **`github-release.yml`**: Triggers on release publication. Builds `ui-star-names_<version>.zip`, attaches it to the release using `softprops/action-gh-release`, and appends the SHA1 checksum to the release notes.

### Utility Scripts

- **`count-additions.sh`**: Bash script that counts unique names across all list files by category. Used for release notes.

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
| Workflow files | 2 |
| Descriptor files | 2 |
| Utility scripts | 1 |
| Root documentation | 8 |
| **Total repository files** | **~67** |