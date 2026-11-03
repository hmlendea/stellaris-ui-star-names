# Config: Name List Format

## Overview

This document specifies the format for name list files in `ui-star-names/common/random_names/base/`.

## File Types

| Category | File Prefix | Entry Type | Block Type |
|----------|-------------|------------|------------|
| Stars | `ui_stars_` | `name` | `name_list` |
| Nebulas | `ui_nebulas_` | `name` | `name_list` |
| Black Holes | `ui_black-holes_` | `name` | `name_list` |
| Asteroid Prefixes | `ui_asteroid-prefixes` | `prefix` | `asteroid_prefix` |
| Asteroid Suffixes | `ui_asteroid-postfixes` | `suffix` | `asteroid_postfix` |

## Name List Block (Stars, Nebulas, Black Holes)

### Syntax

```clausewitz
name_list = {
    category = "<category>"
    name = "Entry 1"
    name = "Entry 2"
    # ...
}
```

### Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `category` | Yes | String | Must be `star`, `nebula`, or `black_hole` |
| `name` | Yes* | String | Quoted name entry; repeatable |

*At least one `name` entry required for valid list.

### Category Values

| File Category | `category` Value |
|---------------|------------------|
| Stars | `star` |
| Nebulas | `nebula` |
| Black Holes | `black_hole` |

### Example: Star Name List

```clausewitz
name_list = {
    category = "star"
    name = "Alpha Centauri"
    name = "Barnard's Star"
    name = "Sirius"
    name = "Proxima Centauri"
    name = "Tau Ceti"
}
```

### Example: Nebula Name List

```clausewitz
name_list = {
    category = "nebula"
    name = "Orion Nebula"
    name = "Crab Nebula"
    name = "Eagle Nebula"
}
```

### Example: Black Hole Name List

```clausewitz
name_list = {
    category = "black_hole"
    name = "Sagittarius A*"
    name = "Cygnus X-1"
    name = "M87*"
}
```

## Asteroid Prefix Block

### Syntax

```clausewitz
asteroid_prefix = {
    Prefix1-
    Prefix2-
    Prefix3-
    # ...
}
```

### Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| (entries) | Yes | Identifier | Unquoted prefix ending with `-`; repeatable |

### Rules

- Each entry must end with hyphen (`-`)
- No quotes around entries
- No `category` field
- Entries are identifiers, not strings

### Example

```clausewitz
asteroid_prefix = {
    Astra-
    Nova-
    Void-
    Stellar-
    Cosmic-
    Solar-
    Lunar-
    Orbital-
}
```

## Asteroid Suffix Block

### Syntax

```clausewitz
asteroid_postfix = {
    -Suffix1
    -Suffix2
    -Suffix3
    # ...
}
```

### Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| (entries) | Yes | Identifier | Unquoted suffix starting with `-`; repeatable |

### Rules

- Each entry must start with hyphen (`-`)
- No quotes around entries
- No `category` field
- Entries are identifiers, not strings

### Example

```clausewitz
asteroid_postfix = {
    -Prime
    -Secundus
    -Tertius
    -Major
    -Minor
    -Alpha
    -Beta
    -Gamma
}
```

## Naming Convention

### File Name Pattern

```
ui_<category>_<source>.txt
```

| Category | Prefix |
|----------|--------|
| Stars | `ui_stars_` |
| Nebulas | `ui_nebulas_` |
| Black Holes | `ui_black-holes_` |
| Asteroid Prefixes | `ui_asteroid-prefixes` (exact) |
| Asteroid Suffixes | `ui_asteroid-postfixes` (exact) |

### Source Identifier

- Lowercase
- Hyphen-separated words
- Descriptive of source universe
- Examples: `star-wars`, `elite-dangerous`, `warhammer40k`, `dune`, `real`, `markov`, `zzz_made-up`

### Special Prefixes

| Prefix | Meaning |
|--------|---------|
| `zzz_` | Sorts last; miscellaneous/original content |
| (none) | Base/primary file for category |

## Syntax Rules

### General

- Encoding: UTF-8
- Line endings: LF
- Indentation: 4 spaces per level
- Comments: `#` to end of line
- No trailing commas
- Block braces on same line as block name

### Quoting

- `name` entries: **Always double-quoted**
- `category` value: **Always double-quoted**
- Asteroid prefix/suffix entries: **Never quoted**

### Whitespace

- One entry per line preferred
- Blank lines allowed
- Comments on own line or trailing

## Validation Checklist

- [ ] File extension `.txt`
- [ ] Correct block type for category
- [ ] `category` field present and correct (name_list only)
- [ ] All `name` entries double-quoted
- [ ] Asteroid prefixes end with `-`
- [ ] Asteroid suffixes start with `-`
- [ ] No syntax errors (braces balanced)
- [ ] File in `common/random_names/base/`
- [ ] Filename follows convention

## Common Errors

| Error | Example | Fix |
|-------|---------|-----|
| Missing quotes | `name = Sirius` | `name = "Sirius"` |
| Wrong category | `category = "stars"` | `category = "star"` |
| Missing category | (omitted) | Add `category = "star"` |
| Prefix missing hyphen | `Astra` | `Astra-` |
| Suffix missing hyphen | `Prime` | `-Prime` |
| Quoted asteroid entry | `"Astra-"` | `Astra-` |
| Trailing comma | `name = "X",` | `name = "X"` |
| Windows line endings | CRLF | Convert to LF |

## Engine Parsing Behaviour

1. Engine scans `common/random_names/base/*.txt`
2. Parses each file as Clausewitz script
3. For `name_list` blocks:
   - Reads `category` field
   - Collects all `name` entries into registry[category]
4. For `asteroid_prefix` block:
   - Collects all entries into registry[asteroid_prefix]
5. For `asteroid_postfix` block:
   - Collects all entries into registry[asteroid_suffix]
6. Parse errors: file skipped, error logged, other files unaffected

## Extensibility

- New source files: Add to `base/` with correct naming
- New categories: **Not supported** (hardcoded in engine)
- Localisation: **Not supported** for name lists
- Weights: **Not supported** (uniform only)