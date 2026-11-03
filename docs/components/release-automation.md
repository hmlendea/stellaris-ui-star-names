# Component: Release Automation

## Overview

The release automation component consists of two GitHub Actions workflows that automate publishing the mod to Steam Workshop and Nexus Mods when a version tag is pushed.

## Workflows

### Steam Workshop (`.github/workflows/steam-workshop.yml`)

**Trigger**: Push of Git tag matching `v*.*.*`

**Steps**:
1. Checkout repository
2. Download release asset from GitHub Releases: `ui-star-names_<version>.zip`
3. Unzip to `release/` directory
4. Upload to Steam Workshop using `hmlendea/steam-workshop-update@v1.0.0`

**Required Secrets**:
- `STEAM_USERNAME`
- `STEAM_PASSWORD`
- `STEAM_2FA_SEED`

**Configuration**:
- `appid`: 281990 (Stellaris)
- `itemid`: 2040215185 (Workshop item ID)
- `path`: `release/ui-star-names/`
- `changenote`: Links to GitHub release page

### Nexus Mods (`.github/workflows/nexus-mods.yml`)

**Trigger**: Push of Git tag matching `v*.*.*` OR manual workflow dispatch with tag input

**Steps**:
1. Checkout repository
2. Download release asset from GitHub Releases: `ui-star-names_<version>.zip`
3. Upload to Nexus Mods using `Nexus-Mods/upload-action@v1.0.0-beta.10`

**Required Secrets**:
- `NEXUSMODS_API_KEY`

**Configuration**:
- `file_id`: 920143 (Nexus Mods file ID)
- `filename`: `release.zip`
- `display_name`: `ui-star-names.zip`
- `version`: Tag name (with `v` prefix stripped)
- `description`: Links to GitHub release page
- `category`: `main`
- `archive_existing_version`: `true`
- `update_mod_version`: `true`

## Release Asset

The workflows expect a release asset named `ui-star-names_<version>.zip` attached to the GitHub Release. This asset is created by GitHub Actions when the release is published (the tag push triggers release creation).

**Asset Contents**:
```
ui-star-names_<version>.zip
└── ui-star-names/
    ├── descriptor.mod
    └── common/
        └── random_names/
            └── base/
                └── *.txt
```

## Dependencies

- **Upstream**: GitHub Releases (asset source)
- **Downstream**:
  - Steam Workshop (consumer)
  - Nexus Mods (consumer)
- **Adjacent**:
  - Mod metadata (descriptor files included in ZIP)
  - Name list data (included in ZIP)

## Ownership

- **Maintainers**: Manage workflow configuration, secrets, and release process
- **Automation**: GitHub Actions runs workflows on tag push

## Verification

### Pre-Release Checklist

1. All changes merged to `master`
2. `supported_version` updated in both descriptor files
3. `./count-additions.sh` run and output recorded for release notes
4. Local test install successful

### Release Process

1. Create and push annotated tag:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

2. GitHub Actions automatically:
   - Creates GitHub Release
   - Builds ZIP asset (via release creation)
   - Triggers Steam workflow
   - Triggers Nexus workflow

3. Monitor workflow runs for success/failure

4. Manually upload ZIP to Paradox Mods

5. Verify all three platforms show new version

### Post-Release Verification

1. Check GitHub Release page for asset
2. Check Steam Workshop page for update
3. Check Nexus Mods page for update
4. Check Paradox Mods page (manual)
5. Test install from each platform

## Failure Modes

| Failure | Cause | Recovery |
|---------|-------|----------|
| Steam upload fails | Invalid credentials, rate limit, API change | Check secrets; manual upload via Steam Workshop website |
| Nexus upload fails | Invalid API key, rate limit, API change | Check secret; manual upload via Nexus Mods website |
| Release asset not found | Release creation failed, naming mismatch | Check GitHub Release; rebuild asset manually |
| ZIP structure invalid | Mod directory renamed, files missing | Verify `ui-star-names/` structure in repository |

## Known Issues

- Paradox Mods requires manual upload (no API)
- Workflows depend on third-party actions (`hmlendea/steam-workshop-update`, `Nexus-Mods/upload-action`)
- No automated verification of release asset contents
- No rollback mechanism (must push new tag)
- Secrets management: Steam 2FA seed must be kept current
- Version tag format must be exactly `vX.Y.Z` (semantic versioning)

## Configuration Reference

### Steam Workshop Workflow

```yaml
name: Steam Workshop
on:
  push:
    tags:
    - 'v*.*.*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Download the release asset
      run: |
        wget "https://github.com/hmlendea/stellaris-ui-star-names/releases/download/${{github.ref_name}}/ui-star-names_${GITHUB_REF:11}.zip" -O "release.zip"
        unzip "release.zip" -d "release/"
    - name: Upload
      uses: hmlendea/steam-workshop-update@v1.0.0
      with:
        appid: 281990
        itemid: 2040215185
        path: "release/ui-star-names/"
        changenote: "[url=https://github.com/hmlendea/stellaris-ui-star-names/releases/tag/${{github.ref_name}}]Version ${{github.ref_name}}[/url]"
      env:
        STEAM_USERNAME: ${{secrets.STEAM_USERNAME}}
        STEAM_PASSWORD: ${{secrets.STEAM_PASSWORD}}
        STEAM_2FASEED: ${{secrets.STEAM_2FA_SEED}}
```

### Nexus Mods Workflow

```yaml
name: Nexus Mods
on:
  push:
    tags:
    - 'v*.*.*'
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to release'
        required: true
jobs:
  release:
    runs-on: ubuntu-latest
    env:
      VERSION: ${{ inputs.tag || github.ref_name }}
    steps:
    - uses: actions/checkout@v1
    - name: Download the release asset
      run: |
        RELEASE_ASSET_NAME="ui-star-names_${VERSION#v}.zip"
        wget "https://github.com/hmlendea/stellaris-ui-star-names/releases/download/${VERSION}/${RELEASE_ASSET_NAME}" -O "release.zip"
    - name: Upload
      uses: Nexus-Mods/upload-action@v1.0.0-beta.10
      with:
        api_key: ${{ secrets.NEXUSMODS_API_KEY }}
        file_id: 920143
        filename: release.zip
        display_name: ui-star-names.zip
        version: ${{env.VERSION}}
        description: "Changelog: https://github.com/hmlendea/stellaris-ui-star-names/releases/${{env.VERSION}}"
        category: main
        archive_existing_version: true
        update_mod_version: true
```