# API Reference: Mod Descriptor API

## Overview

This document describes the interface for Stellaris mod descriptor files as consumed by the launcher and Steam Workshop upload workflow.

## Descriptor File Interface

### File Locations

| Consumer | File Path | Purpose |
|----------|-----------|---------|
| Stellaris Launcher | `ui-star-names/descriptor.mod` | Mod discovery and loading |
| Steam Workshop Workflow | `ui-star-names.mod` | Workshop item identification |

### Schema

```clausewitz
name = "string"
path = "string"
tags = { "string", ... }
supported_version = "string"
version = "string"           // Optional
description = "string"       // Optional
picture = "string"           // Optional
remote_file_id = "string"    // Auto-set by Steam
```

## Field Specifications

### `name` — Mod Display Name

- **Type**: `string` (quoted)
- **Required**: Yes
- **Max Length**: 100 characters
- **Consumers**: Launcher, Steam, Nexus, Paradox
- **Validation**: Non-empty, no embedded quotes

### `path` — Mod Directory Path

- **Type**: `string` (quoted)
- **Required**: Yes
- **Pattern**: `^mod/[a-z0-9_-]+$`
- **Consumers**: Launcher (file system resolution)
- **Validation**: Directory must exist at `StellarisModDir/path`

### `tags` — Categorisation Tags

- **Type**: `array<string>` (quoted)
- **Required**: Yes
- **Required Element**: `"Galaxy Generation"`
- **Consumers**: Launcher (filtering), Steam (categorisation)
- **Valid Tags**: Defined by Stellaris launcher

### `supported_version` — Game Version Compatibility

- **Type**: `string` (quoted)
- **Required**: Yes
- **Pattern**: `^\d+\.\d+\.\*$`
- **Consumers**: Launcher (compatibility check)
- **Semantics**: Major.Minor.* matches all patches

### `version` — Mod Version

- **Type**: `string` (quoted)
- **Required**: No
- **Pattern**: `^\d+\.\d+\.\d+$` (semver)
- **Consumers**: Informational only

### `description` — Mod Description

- **Type**: `string` (quoted, multi-line)
- **Required**: No
- **Consumers**: Workshop pages (display)

### `picture` — Preview Image

- **Type**: `string` (quoted, relative path)
- **Required**: No
- **Consumers**: Launcher (preview)
- **Requirements**: 300x200 PNG, <500 KB

### `remote_file_id` — Steam Workshop Item ID

- **Type**: `string` (quoted, numeric)
- **Required**: No (auto-set)
- **Consumers**: Steam upload workflow
- **Set By**: Steam after first upload
- **Do Not Edit Manually**

## Launcher Integration

### Mod Discovery Flow

```
1. Launcher scans StellarisModDir/ for directories
2. For each dir, reads descriptor.mod
3. Parses fields
4. Validates supported_version against current game version
5. Adds to mod list with compatibility status
6. User enables/disables via checkbox
7. Enabled mods written to dlc_load.json
```

### Compatibility Check

```cpp
bool IsCompatible(const Descriptor& desc, const std::string& gameVersion) {
    // Parse "4.5.*" -> major=4, minor=5
    // Parse gameVersion "4.5.3" -> major=4, minor=5, patch=3
    return desc.major == gameMajor && desc.minor == gameMinor;
}
```

## Steam Workshop Integration

### Upload Workflow Interface

```yaml
# .github/workflows/steam-workshop.yml
uses: hmlendea/steam-workshop-update@v1.3.0
with:
  appid: 281990              # Stellaris App ID
  itemid: 2040215185         # Workshop item ID (from remote_file_id)
  path: "release/ui-star-names/"  # Mod content directory
  changenote: "..."          # BBCode changelog
env:
  STEAM_USERNAME: ${{secrets.STEAM_USERNAME}}
  STEAM_PASSWORD: ${{secrets.STEAM_PASSWORD}}
  STEAM_2FASEED: ${{secrets.STEAM_2FA_SEED}}
```

### Item ID Management

- First upload: Steam returns item ID
- Store in `remote_file_id` field
- Subsequent uploads use same item ID
- Do not change item ID or upload creates duplicate

## Validation API

### DescriptorValidator

```cpp
struct ValidationResult {
    bool valid;
    std::vector<std::string> errors;
    std::vector<std::string> warnings;
};

ValidationResult ValidateDescriptor(const std::string& filePath) {
    // Checks:
    // - File exists
    // - Valid Clausewitz syntax
    // - Required fields present
    // - Field format valid
    // - path directory exists
    // - supported_version pattern valid
    // - tags includes "Galaxy Generation"
}
```

### Cross-File Consistency

```cpp
ValidationResult ValidateConsistency(
    const std::string& launcherDescriptor,
    const std::string& steamDescriptor
) {
    // Checks:
    // - name identical
    // - path identical
    // - supported_version identical
    // - tags identical
}
```

## Error Codes

| Code | Field | Description |
|------|-------|-------------|
| `MISSING_FIELD` | Any required | Required field not present |
| `INVALID_FORMAT` | Any | Value doesn't match pattern |
| `PATH_NOT_FOUND` | `path` | Directory doesn't exist |
| `VERSION_MISMATCH` | `supported_version` | Doesn't match game version |
| `MISSING_TAG` | `tags` | "Galaxy Generation" not present |
| `DUPLICATE_TAG` | `tags` | Duplicate tag in array |
| `INCONSISTENT_DESCRIPTORS` | Cross-file | Launcher vs Steam descriptor differ |

## Version History

| Stellaris Version | Descriptor Changes |
|-------------------|-------------------|
| 4.5 | No changes |
| 4.0 | Added `tags` requirement |
| 3.0 | Added `supported_version` wildcard |
| 2.0 | Initial descriptor format |

## Best Practices

1. Keep both descriptor files identical
2. Update `supported_version` on every Stellaris minor release
3. Include `version` field matching release tag
4. Add `description` for workshop visibility
5. Provide `picture` for launcher preview
6. Never edit `remote_file_id` manually