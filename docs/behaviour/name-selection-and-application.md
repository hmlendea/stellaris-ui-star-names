# Behaviour: Name Selection and Application

## Overview

This document describes how the Stellaris engine selects and applies names from the mod's name lists during galaxy generation.

## Name Selection Algorithm

### Uniform Random Selection

For each celestial body requiring a name, the engine performs:

```
function GetRandomName(category):
    entries = NameRegistry[category]
    if entries.empty():
        return VanillaFallback(category)
    index = RandomInteger(0, entries.length - 1)
    return entries[index]
```

**Properties**:
- Uniform distribution — every entry has equal probability
- No weighting, prioritisation, or conditional logic
- No persistence of selection state between calls
- Deterministic given same RNG seed

### Category Mapping

| Celestial Body | Registry Category | Entry Type |
|----------------|-------------------|------------|
| Star | `star` | `name` |
| Nebula | `nebula` | `name` |
| Black Hole | `black_hole` | `name` |
| Asteroid | `asteroid_prefix` + `asteroid_suffix` | `prefix` + `suffix` |

### Asteroid Name Composition

```
asteroid_name = GetRandom("asteroid_prefix") + GetRandom("asteroid_suffix")
```

Example: `"Astra-" + "-Prime" = "Astra-Prime"`

Prefixes end with `-`, suffixes start with `-` — concatenation produces single hyphen.

## Application Timing

### When Names Are Assigned

1. **Stars**: During star system creation (early galaxy generation)
2. **Nebulas**: During nebula placement (mid galaxy generation)
3. **Black Holes**: During black hole placement (mid galaxy generation)
4. **Asteroids**: During asteroid belt/field creation (late galaxy generation)

### Generation Order

```
1. Galaxy shape & hyperlane layout
2. Star system placement
   → Star names assigned HERE
3. Nebula placement
   → Nebula names assigned HERE
4. Black hole placement
   → Black hole names assigned HERE
5. Asteroid belt/field placement
   → Asteroid names assigned HERE
6. Empire spawn placement
7. Event/trigger placement
```

## Determinism

### Seed Dependency

- Galaxy generation uses a master seed
- Name selection uses the same RNG stream
- Same seed + same mod state = identical names
- Different mod state (added/removed name files) = different names even with same seed

### Save Game Persistence

- Names are **baked into the save file** as strings
- Mod not required to load existing save
- New games with same seed but different mod = different names
- Continuing save with mod disabled = names unchanged

## Fallback Behaviour

### Empty Category

If a category has zero entries (all mod files disabled or empty):

```
function GetRandomName(category):
    entries = NameRegistry[category]
    if entries.empty():
        return VanillaNameList[category].GetRandom()
    ...
```

Vanilla name lists are always present as fallback.

### Parse Errors

If a `.txt` file fails to parse:
- File is skipped entirely
- Error written to `error.log`
- Other files in same category still loaded
- No partial loading of broken file

## Mod Interaction

### Multiple Mods Adding Names

If multiple mods add name lists for same category:
- All entries merged into single registry array
- Selection probability proportional to entry count
- Mod load order does not affect selection (uniform across all)

### Mod Overriding Vanilla

- Mod entries **supplement** vanilla, not replace
- Vanilla entries remain in registry
- To "replace", mod would need to provide many more entries to dilute vanilla probability

## Performance Characteristics

### Memory

- All name entries loaded at engine startup
- ~2,000 star names × ~20 bytes = ~40 KB
- ~500 nebula names = ~10 KB
- ~240 asteroid prefixes + 240 suffixes = ~10 KB
- ~75 black hole names = ~2 KB
- **Total: ~62 KB** — negligible

### CPU

- Name selection: O(1) array index
- Called once per celestial body
- ~1,000 stars + ~100 nebulas + ~50 black holes + ~5,000 asteroids = ~6,150 calls per galaxy
- **Total time: <1 ms** — negligible

## Invariants

1. Every celestial body gets exactly one name
2. Names are strings from the registry (no generation)
3. Asteroid names always prefix+suffix concatenation
4. Selection is uniform random per call
5. Same seed + same registry = same names
6. Save games contain baked names (mod-independent)
7. Vanilla fallback always available

## Edge Cases

| Scenario | Behaviour |
|----------|-----------|
| Duplicate names in registry | Both kept; higher selection probability |
| Empty prefix or suffix file | Fallback to vanilla asteroid naming |
| Category missing entirely | Vanilla fallback |
| Mod disabled mid-save | No effect on existing save |
| Mod added mid-save | No effect on existing save |
| RNG seed exhausted | Impossible (64-bit seed space) |

## Testing Behaviour

### Manual Verification

1. Start new game with fixed seed
2. Record star/nebula/black hole/asteroid names
3. Restart with same seed → names identical
4. Add name file → restart same seed → names differ
5. Disable mod → restart same seed → vanilla names

### Automated Verification

No automated tests exist. Behaviour verified by:
- Visual inspection in-game
- Save file examination
- `count-additions.sh` for entry counts