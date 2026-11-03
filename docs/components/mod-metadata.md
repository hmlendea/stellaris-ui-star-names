# Component: Mod Metadata

## Overview

The mod metadata component consists of two descriptor files that define the mod's identity, version compatibility, and categorisation for the Stellaris launcher and distribution platforms.

## Files

| File | Path | Consumer |
|------|------|----------|
| Launcher descriptor | `ui-star-names/descriptor.mod` | Stellaris game launcher |
| Steam descriptor | `ui-star-names.mod` | Steam Workshop upload workflow |

## Content

Both files contain identical content:

```clausewitz
name="Universum Infinitum: Star Names"
path="mod/ui-star-names"
tags={
    "Galaxy Generation"
}
supported_version="4.5.*"
```

## Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Display name in launcher and workshops |
| `path` | String | Yes | Relative path from Stellaris mod directory to mod root |
| `tags` | Array | Yes | Categorisation tags; must include `Galaxy Generation` |
| `supported_version` | String | Yes | Stellaris version compatibility (wildcard supported) |

## Contracts

### Identity Consistency

Both descriptor files **must** have identical `name` and `path` values. The Steam workflow uses `ui-star-names.mod` at repository root; the launcher reads `ui-star-names/descriptor.mod` in the mod directory.

### Version Compatibility

- `supported_version` uses wildcard pattern: `4.5.*` matches all 4.5.x patches
- Must be updated on each major/minor Stellaris release
- Incorrect version causes mod to show as incompatible in launcher

### Categorisation

- `tags` must include `Galaxy Generation` for correct launcher categorisation
- Additional tags permitted but not required

## Path Resolution

```
Stellaris mod directory/
└── ui-star-names/           ← path="mod/ui-star-names"
    ├── descriptor.mod       ← Read by launcher
    └── common/
        └── random_names/
            └── base/        ← Scanned for name lists
```

The `path` value is relative to the Stellaris mod directory (typically `~/Paradox Interactive/Stellaris/mod/` on Linux, `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` on Windows).

## Dependencies

- **Upstream**: None (authoritative source)
- **Downstream**:
  - Stellaris launcher (reads `descriptor.mod`)
  - Steam Workshop workflow (reads `ui-star-names.mod`)
- **Adjacent**: Name list data (mod root contains both)

## Ownership

- **Maintainers**: Update version compatibility, manage identity
- **Contributors**: Should not modify (maintainer-only)
- **Automation**: Steam workflow reads `ui-star-names.mod`

## Verification

1. Both files exist
2. `name` and `path` are identical in both files
3. `supported_version` matches target Stellaris version
4. `tags` includes `Galaxy Generation`
5. Mod appears in launcher with correct name and version status

## Change Procedure

### Updating Game Version Compatibility

1. Edit `supported_version` in **both** files
2. Test with target Stellaris version
3. Commit and push to master
4. Create release tag to trigger automated publishing

### Changing Mod Identity

1. Edit `name` in **both** files
2. Edit `path` in **both** files (must match directory name)
3. Update Steam Workshop workflow if `path` changes
4. Test installation
5. Create release tag

## Known Issues

- Two descriptor files must be kept in sync manually
- No automated validation of consistency between the two files
- `supported_version` update is manual (no automated check against current Stellaris version)