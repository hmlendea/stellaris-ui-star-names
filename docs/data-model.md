# Data Model

## Overview

The mod's data model consists entirely of name list definitions in Clausewitz script format. There are no runtime objects, databases, or persistent state managed by the mod. The Stellaris game engine owns all parsing, storage, and selection logic.

## Domain Entities

### Name List

A `name_list` is the top-level container in each data file. It defines a collection of names for a specific celestial body category.

**Structure**:
```
name_list = {
    category = "<category>"
    name = "Name 1"
    name = "Name 2"
    ...
}
```

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | String | Yes | Target celestial body type: `star`, `nebula`, `asteroid`, `black_hole` |
| `name` | String | Yes* | A star/nebula/black hole name (repeatable) |
| `prefix` | String | Yes* | An asteroid prefix (repeatable) |
| `suffix` | String | Yes* | An asteroid postfix (repeatable) |

*Exactly one of `name`, `prefix`, or `suffix` must be used per `name_list` block, matching the `category`.

**Categories and Entry Types**:

| Category | Entry Type | Example |
|----------|------------|---------|
| `star` | `name` | `name = "Alderaan"` |
| `nebula` | `name` | `name = "Horsehead Nebula"` |
| `black_hole` | `name` | `name = "Gargantua"` |
| `asteroid` | `prefix` / `suffix` | `prefix = "SOL-"`, `suffix = "-01"` |

### Name Entry

A single name string within a `name_list` block.

**Constraints**:
- Must be quoted: `name = "Alpha Centauri"`
- No escaping needed for standard characters
- Comments allowed with `#` (Clausewitz syntax)
- Duplicate names within a file are permitted but redundant

## File-Level Organisation

Each `.txt` file in `ui-star-names/common/random_names/base/` contains one or more `name_list` blocks.

**Typical File Structure**:
```
# ui_stars_star-wars.txt
name_list = {
    category = "star"
    name = "Alderaan"
    name = "Coruscant"
    name = "Tatooine"
    # ... more names
}

name_list = {
    category = "star"
    name = "Dagobah"
    name = "Endor"
    # ... more names
}
```

Multiple `name_list` blocks per file are permitted and treated identically by the engine.

## Relationships

### File to Category Mapping

| File Pattern | Category | Entry Type |
|--------------|----------|------------|
| `ui_stars_*.txt` | `star` | `name` |
| `ui_nebulas_*.txt` | `nebula` | `name` |
| `ui_black-holes_*.txt` | `black_hole` | `name` |
| `ui_asteroid-prefixes.txt` | `asteroid` | `prefix` |
| `ui_asteroid-postfixes.txt` | `asteroid` | `suffix` |

### Source Universe Grouping

Names are organised by source universe/category via filename:
- `ui_stars_star-wars.txt` → Star Wars universe
- `ui_stars_dune.txt` → Dune universe
- `ui_nebulas_elite-dangerous.txt` → Elite Dangerous game
- `ui_stars_real.txt` → Real astronomical names
- `ui_stars_zzz_made-up.txt` → Original/invented names

This is an organisational convention only; the engine treats all loaded names equally regardless of source file.

## Data Flow

```
Repository (.txt files)
        │
        ▼
GitHub Release (ZIP archive)
        │
        ▼
User Installation (Steam/Nexus/Paradox/Manual)
        │
        ▼
Stellaris Launcher (reads descriptor.mod)
        │
        ▼
Game Engine Startup
        │
        ▼
Scanner: common/random_names/base/*.txt
        │
        ▼
Parser: Clausewitz script → name_list objects
        │
        ▼
In-Memory Name Lists (categorised by category field)
        │
        ▼
Galaxy Generation (random selection from lists)
        │
        ▼
Generated Celestial Bodies (assigned names)
```

## Persistence

- **Repository**: Source of truth (Git)
- **Distribution**: ZIP archives on Steam/Nexus/Paradox/GitHub
- **Runtime**: In-memory only during game session
- **Save Games**: Names become part of save game data (engine-managed)

The mod itself has no persistence mechanism.

## Validation Rules

### Syntax Validation (Engine-Enforced)

1. File must be valid Clausewitz script
2. Each `name_list` must have `category` field
3. `category` must be one of: `star`, `nebula`, `asteroid`, `black_hole`
4. Entry type must match category (`name`/`prefix`/`suffix`)
5. All entries must be quoted strings

### Content Validation (Maintainer-Enforced)

1. No duplicate names within a single `name_list` block (redundant)
2. Names should be appropriate for the source universe
3. Filenames follow convention: `ui_<category>_<source>.txt`
4. No empty `name_list` blocks
5. Special characters handled per Clausewitz rules

## Statistics (Approximate)

Run `./count-additions.sh` for current counts.

| Category | File Count | Unique Names (approx) |
|----------|------------|----------------------|
| Stars | 36 | ~3,000+ |
| Nebulas | 13 | ~500+ |
| Asteroid Prefixes | 1 | ~100+ |
| Asteroid Postfixes | 1 | ~100+ |
| Black Holes | 3 | ~50+ |

## Schema Evolution

### Adding Names

- Append new `name = "..."` entries to existing `name_list` blocks
- Or create new `name_list` block in same or new file
- No format versioning needed

### Adding Source Universes

- Create new file following naming convention
- No engine changes required

### Changing Categories

- Not possible: categories are hardcoded in Stellaris engine
- Would require game update

### Localisation (Future)

If localisation support is added:
1. Move literal strings to `.yml` files in `localisation/`
2. Reference localisation keys in name lists: `name = "KEY_NAME"`
3. Engine must support localised name lists (unverified)

## Invariants

| Invariant | Description |
|-----------|-------------|
| Category validity | Every `name_list` has valid `category` |
| Entry-type match | `name`/`prefix`/`suffix` matches `category` |
| Quote requirement | All entries are quoted strings |
| Flat structure | No subdirectories under `base/` |
| File extension | All name list files use `.txt` |
| Descriptor consistency | Both `.mod` files have identical `name` and `path` |

## Example Records

### Star Name List (Star Wars)

```clausewitz
name_list = {
    category = "star"
    name = "Alderaan"
    name = "Coruscant"
    name = "Tatooine"
    name = "Naboo"
    name = "Mustafar"
    name = "Geonosis"
    name = "Kamino"
    name = "Utapau"
    name = "Kashyyyk"
    name = "Endor"
}
```

### Nebula Name List (Elite Dangerous)

```clausewitz
name_list = {
    category = "nebula"
    name = "Horsehead Nebula"
    name = "Eagle Nebula"
    name = "Crab Nebula"
    name = "Orion Nebula"
    name = "California Nebula"
}
```

### Asteroid Prefixes

```clausewitz
asteroid_prefix = {
    SOL-
    TER-
    LUN-
    MAR-
    VEN-
    JUP-
    SAT-
    URA-
    NEP-
    PLU-
}
```

### Asteroid Postfixes

```clausewitz
asteroid_postfix = {
    -01
    -02
    -03
    -04
    -05
    -A
    -B
    -C
    -D
    -E
}
```

### Black Hole Name List

```clausewitz
name_list = {
    category = "black_hole"
    name = "Gargantua"
    name = "Cygnus X-1"
    name = "Sagittarius A*"
    name = "M87*"
    name = "TON 618"
}
```