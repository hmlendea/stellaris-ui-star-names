# Testing: Test Strategy

## Overview

This document describes the testing strategy for the Universum Infinitum: Star Names mod. As a pure data mod with no executable code, testing focuses on data validation, format correctness, and in-game verification.

## Testing Pyramid

```
        ┌─────────────┐
        │  In-Game    │  ← Manual, high confidence, slow
        │  Verification│
        ├─────────────┤
        │  Format     │  ← Automated, fast, catches syntax errors
        │  Validation │
        ├─────────────┤
        │  Count      │  ← Automated, fast, regression detection
        │  Script     │
        └─────────────┘
```

## Test Categories

### 1. Count Regression Testing (Automated)

**Tool**: `./count-additions.sh`

**Purpose**: Detect accidental deletions or massive additions

**Execution**:
- Run before commit
- Run in CI (if configured)
- Compare output to expected baseline

**Baseline** (approximate):
```
Stars: ~2800
Nebulas: ~480
Asteroid prefixes: ~240
Asteroid suffixes: ~240
Black holes: ~75
```

**Pass Criteria**: Counts within ±10% of baseline (allows organic growth)

**Failure Action**: Investigate unexpected changes

### 2. Format Validation (Automated)

**Purpose**: Ensure all `.txt` files parse as valid Clausewitz script

**Checks**:
- [ ] Balanced braces `{ }`
- [ ] Required fields present (`category` for name_list)
- [ ] Correct block type for file category
- [ ] All `name` entries double-quoted
- [ ] Asteroid prefixes end with `-`
- [ ] Asteroid suffixes start with `-`
- [ ] No trailing commas
- [ ] UTF-8 encoding
- [ ] LF line endings

**Implementation**: Custom script or Clausewitz parser (not yet implemented)

**Current State**: Manual verification only

### 3. In-Game Verification (Manual)

**Purpose**: Confirm names appear correctly in generated galaxies

**Procedure**:
1. Install mod in Stellaris
2. Enable in launcher
3. Start new game (any settings)
4. Observe star/nebula/black hole/asteroid names
5. Verify mod names appear (not just vanilla)

**Test Matrix**:

| Scenario | Expected |
|----------|----------|
| Fresh install, new game | Mod names visible |
| Existing save, mod enabled | Save names unchanged |
| Mod disabled, new game | Vanilla names only |
| Multiple mods enabled | Combined name pool |

**Frequency**: Before each release

### 4. Descriptor Validation (Manual)

**Purpose**: Ensure mod metadata is correct

**Checks**:
- [ ] Both descriptor files exist
- [ ] `name` identical in both
- [ ] `path` identical in both
- [ ] `path` matches directory name
- [ ] `supported_version` matches target Stellaris
- [ ] `tags` includes `Galaxy Generation`
- [ ] Mod appears in launcher
- [ ] Mod shows compatible (not outdated)

**Frequency**: Before each release, after Stellaris version updates

### 5. Release Asset Validation (Manual)

**Purpose**: Ensure ZIP asset has correct structure

**Checks**:
- [ ] Asset named `ui-star-names_<version>.zip`
- [ ] Contains `ui-star-names/` directory
- [ ] Contains `descriptor.mod`
- [ ] Contains `common/random_names/base/*.txt`
- [ ] No extra files (`.git`, `.github`, `docs/`, etc.)
- [ ] Extracts cleanly

**Frequency**: After GitHub Release creation

## Automation Opportunities

### Not Yet Implemented

| Test | Tool | Effort |
|------|------|--------|
| Clausewitz syntax validation | Custom Python script | Medium |
| Duplicate detection within files | grep/sort/uniq pipeline | Low |
| Cross-file duplicate detection | Custom script | Medium |
| Descriptor consistency check | diff/shell script | Low |
| Release asset structure check | shell script | Low |
| CI pipeline | GitHub Actions | Medium |

### Recommended CI Pipeline

```yaml
name: Validate
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Count entries
      run: ./count-additions.sh
    - name: Validate descriptors
      run: |
        diff ui-star-names/descriptor.mod ui-star-names.mod
    - name: Check file naming
      run: |
        # Verify all files follow naming convention
    - name: Validate Clausewitz syntax
      run: |
        # Parse each .txt file
```

## Test Data Management

### Test Seeds

For reproducible in-game testing:

| Seed | Purpose |
|------|---------|
| `123456789` | Baseline galaxy |
| `987654321` | Alternative layout |
| `42` | Minimal galaxy (tiny) |

### Baseline Counts

Record counts at each release for regression comparison:

| Release | Stars | Nebulas | Asteroid Prefixes | Asteroid Suffixes | Black Holes |
|---------|-------|---------|-------------------|-------------------|-------------|
| 1.0.0 | ~2800 | ~480 | ~240 | ~240 | ~75 |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Syntax error in new file | Medium | High (file ignored) | Format validation script |
| Accidental mass deletion | Low | High | Count regression test |
| Descriptor drift | Medium | Medium | Diff check in CI |
| Wrong category field | Low | Medium | Format validation |
| Duplicate file committed | Low | Low | Naming convention check |
| Release asset corrupt | Low | High | Asset validation |

## Test Execution Checklist (Pre-Release)

- [ ] Run `./count-additions.sh` — verify reasonable counts
- [ ] Diff descriptor files — verify identical
- [ ] Install mod locally — verify launcher shows compatible
- [ ] Start new game — verify mod names appear
- [ ] Create GitHub Release — verify asset structure
- [ ] Trigger workflows — verify Steam/Nexus upload
- [ ] Manual Paradox upload — verify success

## Future Improvements

1. Implement Clausewitz parser for automated syntax validation
2. Add GitHub Actions workflow for validation
3. Add duplicate detection (within and across files)
4. Create test seed gallery with screenshots
5. Automate release asset validation