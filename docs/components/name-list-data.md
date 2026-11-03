# Component: Name List Data

## Overview

The name list data component comprises all `.txt` files in `ui-star-names/common/random_names/base/` that define name lists for stars, nebulas, asteroids, and black holes. This is the core content of the mod.

## Responsibilities

- Provide name entries for four celestial body categories
- Organise names by source universe/category via filename convention
- Conform to Stellaris `name_list` format (Clausewitz script)
- Ensure all entries are valid quoted strings
- Maintain flat directory structure (no subdirectories)

## File Inventory

### Star Name Lists (36 files)

| File | Source Universe/Category | Approx. Names |
|------|-------------------------|---------------|
| `ui_stars_ageofmythology.txt` | Age of Mythology | ~50 |
| `ui_stars_alien.txt` | Alien franchise | ~30 |
| `ui_stars_aowp.txt` | Age of Wonders: Planetfall | ~40 |
| `ui_stars_artix-entertainment.txt` | Artix Entertainment games | ~25 |
| `ui_stars_asimov.txt` | Isaac Asimov works | ~40 |
| `ui_stars_asoiaf.txt` | A Song of Ice and Fire | ~60 |
| `ui_stars_authors.txt` | Science fiction authors | ~35 |
| `ui_stars_codominium.txt` | CoDominium series | ~20 |
| `ui_stars_distant-worlds.txt` | Distant Worlds game | ~45 |
| `ui_stars_doctor-who.txt` | Doctor Who | ~55 |
| `ui_stars_dune.txt` | Dune universe | ~70 |
| `ui_stars_elder-scrolls.txt` | The Elder Scrolls | ~60 |
| `ui_stars_elite-dangerous.txt` | Elite Dangerous | ~80 |
| `ui_stars_eons-of-war.txt` | Eons of War | ~25 |
| `ui_stars_eve.txt` | EVE Online | ~50 |
| `ui_stars_fantasy-name-generator.txt` | Fantasy Name Generator | ~40 |
| `ui_stars_galciv.txt` | Galactic Civilizations | ~35 |
| `ui_stars_letsmakeagame-net.txt` | Let's Make a Game | ~20 |
| `ui_stars_markov.txt` | Markov chain generated | ~100 |
| `ui_stars_master-of-orion.txt` | Master of Orion | ~45 |
| `ui_stars_middleearth.txt` | Middle-earth | ~65 |
| `ui_stars_middleearth copy.txt` | Duplicate (artifact) | — |
| `ui_stars_nmsgen.txt` | No Man's Sky generated | ~80 |
| `ui_stars_no-mans-sky.txt` | No Man's Sky | ~70 |
| `ui_stars_pax-nova.txt` | Pax Nova | ~30 |
| `ui_stars_predestination.txt` | Predestination | ~25 |
| `ui_stars_real.txt` | Real astronomical names | ~200 |
| `ui_stars_rotp.txt` | Remnants of the Precursors | ~30 |
| `ui_stars_sins-of-a-solar-empire.txt` | Sins of a Solar Empire | ~40 |
| `ui_stars_star-trek.txt` | Star Trek | ~90 |
| `ui_stars_star-wars.txt` | Star Wars | ~120 |
| `ui_stars_starcraft.txt` | StarCraft | ~50 |
| `ui_stars_stargate.txt` | Stargate | ~55 |
| `ui_stars_starruler2.txt` | Star Ruler 2 | ~35 |
| `ui_stars_zzz_made-up.txt` | Original/invented names | ~60 |
| `ui_stars_zzz_media.txt` | Miscellaneous media | ~40 |
| `ui_stars_zzz_others.txt` | Other sources | ~35 |
| `ui_stars_zzz_places.txt` | Real/fictional places | ~45 |

### Nebula Name Lists (13 files)

| File | Source Universe/Category | Approx. Names |
|------|-------------------------|---------------|
| `ui_nebulas.txt` | Base/real nebulas | ~80 |
| `ui_nebulas_dark-pirates.txt` | Dark Pirates | ~25 |
| `ui_nebulas_distant-worlds.txt` | Distant Worlds | ~30 |
| `ui_nebulas_doctor-who.txt` | Doctor Who | ~20 |
| `ui_nebulas_elite-dangerous.txt` | Elite Dangerous | ~60 |
| `ui_nebulas_fantasy-name-generator.txt` | Fantasy Name Generator | ~35 |
| `ui_nebulas_no-mans-sky.txt` | No Man's Sky | ~40 |
| `ui_nebulas_scifiideas.txt` | SciFi Ideas | ~30 |
| `ui_nebulas_star-wars.txt` | Star Wars | ~25 |
| `ui_nebulas_void_bastards.txt` | Void Bastards | ~20 |
| `ui_nebulas_warhammer40k.txt` | Warhammer 40K | ~45 |

### Asteroid Name Lists (2 files)

| File | Entry Type | Approx. Entries |
|------|------------|-----------------|
| `ui_asteroid-prefixes.txt` | `prefix` | ~120 |
| `ui_asteroid-postfixes.txt` | `suffix` | ~120 |

### Black Hole Name Lists (3 files)

| File | Source Universe/Category | Approx. Names |
|------|-------------------------|---------------|
| `ui_black-holes.txt` | Base/mixed | ~30 |
| `ui_black-holes_elite-dangerous.txt` | Elite Dangerous | ~25 |
| `ui_black-holes_scifiideas.txt` | SciFi Ideas | ~20 |

## Format Specification

### Star / Nebula / Black Hole Files

```clausewitz
name_list = {
    category = "star"  # or "nebula", "black_hole"
    name = "Name 1"
    name = "Name 2"
    # ...
}
```

### Asteroid Prefix File

```clausewitz
asteroid_prefix = {
    PREFIX1-
    PREFIX2-
    # ...
}
```

### Asteroid Postfix File

```clausewitz
asteroid_postfix = {
    -SUFFIX1
    -SUFFIX2
    # ...
}
```

## Boundary Rules

1. **File extension**: Must be `.txt`
2. **Directory**: All files directly in `base/` (no subdirectories)
3. **Naming convention**: `ui_<category>_<source>.txt`
4. **Syntax**: Valid Clausewitz script
5. **Category field**: Required in each `name_list` block
6. **Entry type match**: `name` for star/nebula/black_hole; `prefix`/`suffix` for asteroid
7. **Quoting**: All entries must be quoted strings (except asteroid prefixes/suffixes which are unquoted identifiers)

## Dependencies

- **Upstream**: None (source of truth)
- **Downstream**: Stellaris game engine (consumer)
- **Adjacent**: Mod metadata (descriptor files reference mod root)

## Ownership

- **Maintainers**: Review and merge contributions
- **Contributors**: Add new files, fix typos, reorganise names
- **Game engine**: Parses and applies at runtime

## Verification

- Run `./count-additions.sh` to count unique entries per category
- Install mod and start new game to verify names appear
- Check launcher for load errors

## Known Issues

- `ui_stars_middleearth copy.txt` — Duplicate file, should be removed
- No automated syntax validation
- No automated duplicate detection across files
- No localisation support (English only)