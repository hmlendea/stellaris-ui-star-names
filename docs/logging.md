# Logging Documentation

## Overview

This document describes the logging behaviour of the Universum Infinitum: Star Names mod. As a pure data mod with no executable code, the mod itself produces no logs. All logging comes from the Stellaris engine when parsing and loading the mod's data files.

## Log Sources

| Source | Log File | Content |
|--------|----------|---------|
| Stellaris Engine | `error.log` | Parse errors, missing files, validation warnings |
| Stellaris Engine | `system.log` | Mod load sequence, data registration |
| Stellaris Engine | `game.log` | General game execution |

## Mod-Related Log Entries

### Successful Load (system.log)

```
[12:34:56][mod_manager]: Loading mod: Universum Infinitum: Star Names
[12:34:56][mod_manager]: Mod path: mod/ui-star-names
[12:34:56][data_loader]: Scanning common/random_names/base/
[12:34:56][data_loader]: Found 54 name list files
[12:34:56][name_registry]: Registered 2847 star names
[12:34:56][name_registry]: Registered 482 nebula names
[12:34:56][name_registry]: Registered 240 asteroid prefixes
[12:34:56][name_registry]: Registered 240 asteroid suffixes
[12:34:56][name_registry]: Registered 75 black hole names
```

### Parse Error (error.log)

```
[12:34:56][clausewitz]: [ui_stars_star-wars.txt:42] Expected quoted string, got: name = Death Star
[12:34:56][clausewitz]: [ui_stars_star-wars.txt] File skipped due to parse error
```

### Missing Category (error.log)

```
[12:34:56][clausewitz]: [ui_stars_newfile.txt] Missing required field: category
[12:34:56][clausewitz]: [ui_stars_newfile.txt] File skipped
```

### Invalid Category Value (error.log)

```
[12:34:56][clausewitz]: [ui_stars_newfile.txt:3] Invalid category: "stars" (expected: star, nebula, black_hole)
[12:34:56][clausewitz]: [ui_stars_newfile.txt] File skipped
```

### Empty Category Fallback (system.log)

```
[12:34:56][name_registry]: Category 'black_hole' empty, using vanilla fallback
```

## Log Locations

| OS | Path |
|----|------|
| Linux | `~/.local/share/Paradox Interactive/Stellaris/logs/` |
| Windows | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\logs\` |
| macOS | `~/Documents/Paradox Interactive/Stellaris/logs/` |

## Key Log Patterns for Mod Debugging

### Search for Mod-Related Errors

```bash
# Linux/macOS
grep -i "ui-star-names\|random_names" ~/.local/share/Paradox\ Interactive/Stellaris/logs/error.log

# Windows (PowerShell)
Select-String -Pattern "ui-star-names|random_names" "$env:USERPROFILE\Documents\Paradox Interactive\Stellaris\logs\error.log"
```

### Search for Name Registry Activity

```bash
grep -i "name_registry" ~/.local/share/Paradox\ Interactive/Stellaris/logs/system.log
```

## Log Levels

| Level | Description | Mod Relevance |
|-------|-------------|---------------|
| ERROR | Parse failures, missing required fields | High - mod content broken |
| WARNING | Empty categories, deprecated syntax | Medium - mod may not work fully |
| INFO | Mod load, file counts, registration | Low - normal operation |
| DEBUG | Detailed parsing steps | None - not available in release |

## What the Mod Does NOT Log

- No custom log entries (no executable code)
- No telemetry
- No analytics
- No user tracking
- No network requests

## Troubleshooting via Logs

### Mod Not Loading

1. Check `system.log` for "Loading mod: Universum Infinitum: Star Names"
2. If absent: mod not in mod directory or descriptor missing
3. If present but no name registry entries: check `error.log` for parse errors

### Names Not Appearing

1. Check `system.log` for registration counts
2. If counts are zero: check `error.log` for parse errors
3. If counts non-zero but names vanilla: mod disabled or wrong category

### Specific File Errors

1. `error.log` references file and line number
2. Open file, fix syntax at indicated line
3. Common: missing quotes, unbalanced braces, invalid category

## Log Retention

- Stellaris rotates logs on each launch
- Previous session logs suffixed with `.old`
- No persistent log accumulation from mod

## Privacy

- Logs contain no personal data
- Logs contain no mod-specific identifiers beyond file names
- Logs are local only, never transmitted