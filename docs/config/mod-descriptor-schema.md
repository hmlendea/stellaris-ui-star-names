# Config: Mod Descriptor Schema

## Overview

This document specifies the schema for Stellaris mod descriptor files (`descriptor.mod` and `ui-star-names.mod`).

## File Locations

| File | Path | Purpose |
|------|------|---------|
| Launcher descriptor | `ui-star-names/descriptor.mod` | Read by Stellaris launcher |
| Steam descriptor | `ui-star-names.mod` | Read by Steam Workshop upload workflow |

## Schema

```clausewitz
# Required fields
name = "string"           # Display name (max 100 chars)
path = "string"           # Relative path from mod directory
supported_version = "string"  # Version pattern (e.g., "4.5.*")

# Optional fields
tags = { "string", ... }  # Categorisation tags
version = "string"        # Mod version (not used by launcher)
description = "string"    # Mod description (not used by launcher)
picture = "string"        # Preview image path (not used)
remote_file_id = "string" # Steam Workshop item ID (auto-set)
```

## Field Specifications

### `name` (Required)

- **Type**: Quoted string
- **Max length**: 100 characters
- **Pattern**: `^[^"]+$` (no embedded quotes)
- **Example**: `name="Universum Infinitum: Star Names"`
- **Used by**: Launcher display, Steam Workshop, Nexus Mods, Paradox Mods

### `path` (Required)

- **Type**: Quoted string
- **Pattern**: `^mod/[a-z0-9_-]+$`
- **Example**: `path="mod/ui-star-names"`
- **Used by**: Launcher to locate mod files
- **Must match**: Actual directory name under mod directory

### `supported_version` (Required)

- **Type**: Quoted string
- **Pattern**: `^\d+\.\d+\.\*$` (major.minor.*)
- **Example**: `supported_version="4.5.*"`
- **Used by**: Launcher compatibility check
- **Wildcard**: `*` matches any patch version
- **Update**: Required on each Stellaris major/minor release

### `tags` (Required)

- **Type**: Array of quoted strings
- **Required tag**: `"Galaxy Generation"`
- **Example**: `tags={ "Galaxy Generation" }`
- **Used by**: Launcher categorisation and filtering
- **Valid tags**: See Stellaris launcher tag list

### `version` (Optional)

- **Type**: Quoted string
- **Pattern**: `^\d+\.\d+\.\d+$` (semantic versioning)
- **Example**: `version="1.2.3"`
- **Used by**: Not used by launcher; informational only
- **Recommendation**: Include for clarity

### `description` (Optional)

- **Type**: Quoted string (multi-line supported)
- **Example**:
  ```clausewitz
  description="Adds thousands of new star, nebula, asteroid, and black hole names from sci-fi and fantasy universes."
  ```
- **Used by**: Not used by launcher; shown on workshop pages

### `picture` (Optional)

- **Type**: Quoted string (relative path)
- **Example**: `picture="thumbnail.png"`
- **Used by**: Launcher preview image (if present)
- **Requirements**: 300x200 PNG, max 500 KB

### `remote_file_id` (Auto-generated)

- **Type**: Quoted string (numeric)
- **Example**: `remote_file_id="2040215185"`
- **Used by**: Steam Workshop to identify existing item
- **Set by**: Steam upload workflow after first upload
- **Do not edit manually**

## Validation Rules

1. Both descriptor files must have identical `name`, `path`, `supported_version`, and `tags`
2. `path` must match the mod directory name exactly
3. `supported_version` must use wildcard pattern for patch versions
4. `tags` must include `"Galaxy Generation"`
5. No trailing commas in arrays
6. All strings must be double-quoted
7. File encoding: UTF-8
8. Line endings: LF

## Example: Complete Descriptor

```clausewitz
name="Universum Infinitum: Star Names"
path="mod/ui-star-names"
tags={
    "Galaxy Generation"
}
supported_version="4.5.*"
version="1.2.3"
description="Adds thousands of new star, nebula, asteroid, and black hole names from sci-fi and fantasy universes including Star Wars, Star Trek, Warhammer 40K, Dune, Elite Dangerous, and many more."
picture="thumbnail.png"
remote_file_id="2040215185"
```

## Version Compatibility Matrix

| Stellaris Version | supported_value | Status |
|-------------------|-----------------|--------|
| 4.5.x | `4.5.*` | Current |
| 4.4.x | `4.4.*` | Previous |
| 4.3.x | `4.3.*` | Legacy |
| 4.2.x | `4.2.*` | Legacy |
| 4.1.x | `4.1.*` | Legacy |
| 4.0.x | `4.0.*` | Legacy |
| 3.14.x | `3.14.*` | Legacy |
| 3.13.x | `3.13.*` | Legacy |

## Updating Procedure

1. Edit `supported_version` in **both** files simultaneously
2. Optionally update `version` to match release
3. Test with target Stellaris version
4. Commit and push
5. Create release tag to trigger publishing

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Mod not in launcher | `descriptor.mod` missing or misplaced | Verify file at `ui-star-names/descriptor.mod` |
| Incompatible version | `supported_version` mismatch | Update to match Stellaris version |
| Wrong category | Missing `Galaxy Generation` tag | Add to `tags` array |
| Path not found | `path` doesn't match directory | Fix `path` or rename directory |
| Steam upload fails | `remote_file_id` incorrect | Remove field; let workflow set it |