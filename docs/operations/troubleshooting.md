# Operations: Troubleshooting

## Overview

This document provides troubleshooting guidance for common issues encountered during development, installation, runtime, and deployment.

## Category Index

- [Installation & Loading Issues](#installation--loading-issues)
- [In-Game Issues](#in-game-issues)
- [Development & Verification Issues](#development--verification-issues)
- [Release & Deployment Issues](#release--deployment-issues)

---

## Installation & Loading Issues

### Mod Does Not Appear in Launcher

**Symptoms**: Mod missing from launcher mod list

**Causes & Solutions**:

| Cause | Verification | Solution |
|-------|--------------|----------|
| Misplaced descriptor | File not at `ui-star-names/descriptor.mod` | Move file to correct path |
| Wrong mod directory | Path not in Stellaris mod folder | Move mod folder to `~/Paradox Interactive/Stellaris/mod/` |
| Invalid descriptor format | Syntax error in `descriptor.mod` | Fix quotes, braces, required fields |
| Launcher cache outdated | Cache has stale data | Delete launcher cache (`~/.local/share/Paradox Interactive/Stellaris/`) |

### Mod Shows as Incompatible

**Symptoms**: Red warning in launcher: "Incompatible version"

**Cause**: `supported_version` in descriptor does not match Stellaris version

**Solution**:
1. Edit `supported_version` in **both** `descriptor.mod` and `ui-star-names.mod`
2. Update to match current version (e.g., `supported_version="4.5.*"`)
3. Restart launcher

### Mod Causes Launcher Crash

**Symptoms**: Launcher crashes when loading mod list

**Cause**: Corrupt descriptor file or binary characters

**Solution**:
1. Verify file encoding is UTF-8
2. Check for hidden non-printable characters
3. Re-create descriptor file from schema template

---

## In-Game Issues

### Mod Names Do Not Appear (Vanilla Names Only)

**Symptoms**: Galaxy generated with vanilla names only

**Causes & Solutions**:

| Cause | Verification | Solution |
|-------|--------------|----------|
| Mod disabled | Check launcher mod list | Enable mod checkbox |
| Category field wrong | Check `category` in `.txt` files | Must be `"star"`, `"nebula"`, `"black_hole"` |
| Parse error | Check `~/.local/share/Paradox Interactive/Stellaris/logs/error.log` | Fix syntax error in referenced file |
| File location wrong | Files not directly in `base/` | Move files to `common/random_names/base/` |

### Unquoted Entry Causing Mod Failure

**Symptoms**: Entry ignored, error in `error.log`: "Expected quoted string"

**Cause**: Name entry missing double quotes (e.g., `name = Alpha`)

**Solution**: Change to `name = "Alpha"`

### Asteroid Names Formed Incorrectly

**Symptoms**: Asteroids named `AstraPrime` instead of `Astra-Prime` or `--Prime`

**Cause**: Missing or extra hyphens in prefix/suffix files

**Solution**:
- Prefixes must **end** with `-` (e.g., `Astra-`)
- Suffixes must **start** with `-` (e.g., `-Prime`)
- No spaces around hyphen

### Syntax Error in Log

**Symptoms**: `error.log` contains: `[12:34:56][clausewitz]: Unexpected token at line X`

**Cause**: Unbalanced braces, missing quotes, or invalid character

**Solution**:
1. Open file referenced in log
2. Check line number indicated
3. Verify braces balanced and all strings quoted

---

## Development & Verification Issues

### `./count-additions.sh` Returns Wrong Count

**Symptoms**: Count script returns 0 or unexpected number

**Causes & Solutions**:

| Cause | Verification | Solution |
|-------|--------------|----------|
| Run from wrong directory | Working directory not repository root | `cd` to repository root before running |
| File encoding non-UTF8 | `file -i` shows non-utf8 | Convert encoding to UTF-8 |
| Line endings CRLF | `file` shows CRLF | Run `dos2unix ui-star-names/common/random_names/base/*.txt` |
| `grep`/`sed` binary difference | Script uses GNU-specific syntax on BSD/macOS | Install GNU coreutils or adjust script |

### Duplicate Names in File

**Symptoms**: Duplicate name entries in single file

**Solution**:
```bash
# Find duplicates within file
grep 'name =' ui-star-names/common/random_names/base/ui_stars_star-wars.txt | sort | uniq -d
```
Remove duplicates manually or with script.

---

## Release & Deployment Issues

### Steam Workshop Upload Fails

**Symptoms**: GitHub Actions `Steam Workshop` workflow fails

**Causes & Solutions**:

| Cause | Error Log | Solution |
|-------|-----------|----------|
| Invalid credentials | `Authentication failed` | Update `STEAM_USERNAME` / `STEAM_PASSWORD` secrets |
| 2FA seed expired | `2FA token invalid` | Update `STEAM_2FA_SEED` secret |
| Release asset missing | `404 Not Found` for ZIP | Ensure release asset attached to GitHub Release |
| Rate limited | `Too many requests` | Wait 1 hour and re-run workflow |

### Nexus Mods Upload Fails

**Symptoms**: GitHub Actions `Nexus Mods` workflow fails

**Causes & Solutions**:

| Cause | Error Log | Solution |
|-------|-----------|----------|
| Invalid API key | `401 Unauthorized` | Regenerate API key on Nexus Mods, update secret |
| File ID mismatch | `404 File not found` | Verify `file_id` (920143) matches Nexus page |
| Tag format wrong | `Version parse error` | Tag must be `vX.Y.Z` |

### Paradox Mods Upload Rejected

**Symptoms**: Paradox Mods rejects uploaded ZIP

**Cause**: Invalid directory structure in ZIP

**Solution**: ZIP must contain `ui-star-names/` folder at root, not contents directly:

```
ui-star-names_1.2.3.zip
└── ui-star-names/        ← Required wrapper folder
    ├── descriptor.mod
    └── common/
```

### Descriptor Files Out of Sync

**Symptoms**: Steam displays different name/version than launcher

**Cause**: `descriptor.mod` and `ui-star-names.mod` modified independently

**Solution**:
```bash
# Check if files differ
diff ui-star-names/descriptor.mod ui-star-names.mod

# If diff found, copy master to slave
cp ui-star-names/descriptor.mod ui-star-names.mod
```

---

## Diagnostic Logs

### Stellaris Log Locations

| OS | Path |
|----|------|
| Linux | `~/.local/share/Paradox Interactive/Stellaris/logs/` |
| Windows | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\logs\` |
| macOS | `~/Documents/Paradox Interactive/Stellaris/logs/` |

### Key Log Files

- `error.log`: Syntax errors, missing files, parse warnings
- `system.log`: Mod load sequence, registered data paths
- `game.log`: General game execution log

### Useful Terminal Commands

```bash
# Count total entries across all files
./count-additions.sh

# Find all parse errors in Stellaris log (Linux)
grep -i 'random_names' ~/.local/share/Paradox\ Interactive/Stellaris/logs/error.log

# Check file encodings
file ui-star-names/common/random_names/base/*.txt

# Find non-ASCII characters
pcregrep --color='auto' -n "[\x80-\xFF]" ui-star-names/common/random_names/base/*.txt
```

---

## Escalation Path

1. Check this troubleshooting guide
2. Check `docs/` for relevant topic
3. Check Stellaris `error.log`
4. Search existing GitHub Issues
5. Create new GitHub Issue with:
   - Stellaris version
   - Mod version
   - OS
   - Reproduction steps
   - `error.log` snippet (redacted)