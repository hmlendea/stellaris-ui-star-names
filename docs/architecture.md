# Architecture (Complement)

This document complements the root [ARCHITECTURE.md](../ARCHITECTURE.md) by providing additional implementation detail, component-level views, and operational context for maintainers and contributors.

## Relationship to Root ARCHITECTURE.md

The root `ARCHITECTURE.md` provides the authoritative system-level architecture. This document:
- Elaborates on implementation details not covered at system level
- Provides component-level responsibility boundaries
- Documents operational procedures for maintainers
- Records design rationale for key decisions

## Component Responsibility Boundaries

### Name List Data Component

**Paths**: `ui-star-names/common/random_names/base/`

**Responsibilities**:
- Provide name lists for four celestial body categories: stars, nebulas, asteroids (prefixes/suffixes), black holes
- Organise names by source universe or category using naming convention `ui_<category>_<source>.txt`
- Conform to Stellaris `name_list` format with valid Clausewitz script syntax

**Boundary Rules**:
- Files must use `.txt` extension
- No subdirectories under `base/` (engine expects flat structure)
- Each file contains one or more `name_list` blocks
- Star/nebula/black hole files use `name = "..."` entries
- Asteroid files use `prefix = "..."` and `suffix = "..."` entries
- Category field in each `name_list` block must match expected values: `star`, `nebula`, `asteroid`, `black_hole`

**Ownership**: Mod maintainers and contributors

### Mod Metadata Component

**Paths**: `ui-star-names.mod`, `ui-star-names/descriptor.mod`

**Responsibilities**:
- Define mod identity (`name`), installation path (`path`), categorisation (`tags`), and game version compatibility (`supported_version`)
- `ui-star-names.mod`: Consumed by Steam Workshop upload workflow
- `ui-star-names/descriptor.mod`: Consumed by Stellaris game launcher

**Boundary Rules**:
- Both files must have identical `name` and `path` values
- `supported_version` must match target Stellaris version (currently `4.5.*`)
- `tags` must include `Galaxy Generation`
- Path must be `mod/ui-star-names` (relative to Stellaris mod directory)

**Ownership**: Mod maintainers

### Release Automation Component

**Paths**: `.github/workflows/steam-workshop.yml`, `.github/workflows/nexus-mods.yml`, `.github/workflows/github-release.yml`

**Responsibilities**:
- Automate packaging and publishing on version tag push (`v*.*.*`) and release publication
- Steam workflow: Builds the release archive, extracts it, uploads to Steam Workshop
- Nexus workflow: Builds the release archive, uploads to Nexus Mods via API
- GitHub Release workflow: Builds `ui-star-names_<version>.zip`, attaches it to the published release, and appends its SHA1 checksum to the release notes

**Boundary Rules**:
- Tag-triggered workflows match `v*.*.*`; the GitHub Release workflow triggers on the `published` release event
- Each workflow builds the release archive itself from the checked-out repository
- Release archive contents: the `ui-star-names/` directory and `ui-star-names.mod`
- GitHub release asset naming convention: `ui-star-names_<version>.zip`
- Steam workflow requires secrets: `STEAM_USERNAME`, `STEAM_PASSWORD`, `STEAM_2FA_SEED`
- Nexus workflow requires secret: `NEXUSMODS_API_KEY`
- Paradox Mods requires manual upload (no automation)

**Ownership**: Mod maintainers

### Utility Scripts Component

**Paths**: `count-additions.sh`

**Responsibilities**:
- Count unique names across all list files by category
- Output used for release notes and verification

**Boundary Rules**:
- Must be executable bash script
- Reads from `ui-star-names/common/random_names/base/`
- Uses `sed`/`sort`/`uniq`/`wc` pipeline to filter and count

**Ownership**: Mod maintainers

## Data Flow Detail

### Name List Parsing (Game Engine)

```
Source .txt Files (Clausewitz script)
         │
         ▼
Stellaris Engine Scanner (scans common/random_names/base/)
         │
         ▼
Parser (validates name_list blocks, extracts name/prefix/suffix entries)
         │
         ▼
Loaded Name Lists (in-memory, categorised by category field)
         │
         ▼
Galaxy Generator (randomly selects from loaded lists during generation)
         │
         ▼
Generated Celestial Bodies (receive names from mod lists)
```

### Release Flow

```
Git Tag Push (vX.Y.Z)
         │
         ▼
GitHub Release Published
         │
         ▼
GitHub Actions: Build Release Archive
         │
         ├──────────────────┬──────────────────┬──────────────────┐
         ▼                  ▼                  ▼                  ▼
   Steam Workshop      Nexus Mods         GitHub Releases
   (automated)         (automated)        (asset storage)
         │                  │                  │
         ▼                  ▼                  ▼
   Steam Users         Nexus Users        Manual Download
```

## Configuration Contracts

### Stellaris Version Compatibility

| Setting | Location | Current Value | Update Policy |
|---------|----------|---------------|---------------|
| `supported_version` | `descriptor.mod`, `ui-star-names.mod` | `4.5.*` | Update on each major/minor Stellaris release |

### Mod Identity

| Setting | Location | Current Value | Change Policy |
|---------|----------|---------------|---------------|
| `name` | Both descriptor files | `Universum Infinitum: Star Names` | Change only if mod identity changes |
| `path` | Both descriptor files | `mod/ui-star-names` | Must match mod directory name |
| `tags` | Both descriptor files | `["Galaxy Generation"]` | Preserve for correct categorisation |

## Operational Procedures

### Adding a New Name List

1. Create new `.txt` file in `ui-star-names/common/random_names/base/`
2. Follow naming convention: `ui_<category>_<source>.txt`
3. Use valid Clausewitz `name_list` syntax:
   ```
   name_list = {
       category = "<star|nebula|asteroid|black_hole>"
       name = "Name 1"
       name = "Name 2"
       ...
   }
   ```
4. For asteroids: use `prefix` and `suffix` instead of `name`
5. Run `./count-additions.sh` to verify counts
6. Test by installing mod and starting new game

### Updating Game Version Compatibility

1. Edit `supported_version` in both `ui-star-names.mod` and `ui-star-names/descriptor.mod`
2. Test with target Stellaris version
3. Create release tag to trigger automated publishing

### Creating a Release

1. Ensure all changes are on `master` branch
2. Create and push annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z`
3. GitHub Actions automatically:
   - Builds the release archive from the repository and attaches it to the GitHub Release
   - Publishes to Steam Workshop
   - Publishes to Nexus Mods
4. Manually upload the archive to Paradox Mods
5. Verify all four platforms show the new version

## Design Rationale

### Flat File Structure

The game engine's name list scanner expects a flat directory under `common/random_names/base/`. Subdirectories are not scanned. This limits organisational options but ensures compatibility.

### Separate Descriptor Files

Two descriptor files exist because:
- `ui-star-names/descriptor.mod`: Required by game launcher at mod root
- `ui-star-names.mod`: Required by Steam Workshop upload workflow at repository root

They must remain identical in `name` and `path` fields.

### No Build Step

The mod is pure data. The "build" is simply creating a ZIP archive containing the `ui-star-names/` directory and `ui-star-names.mod`. Each release workflow builds this archive itself from the checked-out repository, so publishing no longer depends on a pre-existing GitHub release asset.

### Category Field in Name Lists

Each `name_list` block must declare its `category` so the engine knows which celestial body type to apply names to. This is a Stellaris engine requirement.

## Invariants

| Invariant | Verification |
|-----------|--------------|
| All name list files parse as valid Clausewitz script | Game loads mod without errors |
| Both descriptor files have identical `name` and `path` | Manual review / diff |
| `supported_version` matches target game version | Manual verification on game update |
| Release archive contains `ui-star-names/` (with `descriptor.mod` and `common/`) and `ui-star-names.mod` | Workflow validation; manual test install |
| No executable code or binary assets in mod | Repository inspection |

## Extension Points

### Adding New Source Universes

Create new name list file following naming convention. No engine changes required.

### Adding New Celestial Body Categories

Not currently extensible — categories are hardcoded in Stellaris engine (`star`, `nebula`, `asteroid`, `black_hole`). Would require game update.

### Localisation Support

Not currently implemented. Would require:
1. Adding `.yml` localisation files in `localisation/` directory
2. Referencing localisation keys in name lists instead of literal strings
3. Engine support for localised name lists (unverified)

## Cross-Cutting Concerns

### Error Handling

- **Invalid name list syntax**: Engine skips file or mod fails to load; no graceful degradation
- **Missing descriptor**: Mod not listed in launcher
- **Version mismatch**: Mod shows as incompatible in launcher
- **Upload failures**: Workflow fails; manual upload required
- **Archive build failure**: Missing or renamed `ui-star-names/` directory or `ui-star-names.mod` causes the packaging step to fail

### Observability

- No application logging (mod is passive data)
- Workflow logs in GitHub Actions provide deployment observability
- Game launcher shows mod load status

### Security

- No secrets in repository (workflow secrets stored in GitHub)
- No user data processed
- Supply chain: Release archive built from repository source by each workflow; verify checksums if concerned

## Testing and Verification

### Manual Verification Checklist

1. **Installation**: Mod appears in Stellaris launcher after install
2. **Load**: No errors when enabling mod and starting game
3. **Content**: Custom names appear in generated galaxy for all four categories
4. **Counts**: `./count-additions.sh` output matches expectations

### Coverage Gaps

- No automated syntax validation for Clausewitz script
- No automated duplicate detection across files
- No automated `supported_version` verification
- No integration test for Steam/Nexus upload workflows (require secrets)

## Source Map (Extended)

| Area | Path | Description |
|------|------|-------------|
| Mod root | `ui-star-names/` | Top-level mod directory |
| Launcher descriptor | `ui-star-names/descriptor.mod` | Game launcher metadata |
| Steam descriptor | `ui-star-names.mod` | Steam Workshop metadata |
| Name list directory | `ui-star-names/common/random_names/base/` | All name list files |
| Star name lists | `ui-star-names/common/random_names/base/ui_stars_*.txt` | 36 files |
| Nebula name lists | `ui-star-names/common/random_names/base/ui_nebulas_*.txt` | 13 files |
| Asteroid prefixes | `ui-star-names/common/random_names/base/ui_asteroid-prefixes.txt` | 1 file |
| Asteroid postfixes | `ui-star-names/common/random_names/base/ui_asteroid-postfixes.txt` | 1 file |
| Black hole lists | `ui-star-names/common/random_names/base/ui_black-holes_*.txt` | 3 files |
| Steam workflow | `.github/workflows/steam-workshop.yml` | Steam publishing automation |
| Nexus workflow | `.github/workflows/nexus-mods.yml` | Nexus publishing automation |
| GitHub Release workflow | `.github/workflows/github-release.yml` | GitHub Release asset automation |
| Count script | `count-additions.sh` | Name counting utility |
| Release archive (generated) | `ui-star-names_<version>.zip` | Archive attached to the GitHub Release |