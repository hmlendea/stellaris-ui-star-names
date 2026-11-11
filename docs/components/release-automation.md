# Component: Release Automation

## Overview

The release automation component consists of three GitHub Actions workflows that automate publishing the mod to Steam Workshop, Nexus Mods, and GitHub Releases when a version tag is pushed or a release is published. Each workflow builds the release archive itself from the checked-out repository, so publishing never depends on a pre-existing release asset.

## Workflows

### Steam Workshop (`.github/workflows/steam-workshop.yml`)

**Trigger**: Push of Git tag matching `v*.*.*`

**Steps**:
1. Checkout repository
2. Build the release archive `release.zip` containing `ui-star-names/` and `ui-star-names.mod`
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
2. Build the release archive `release.zip` containing `ui-star-names/` and `ui-star-names.mod`
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

### GitHub Release (`.github/workflows/github-release.yml`)

**Trigger**: Publication of a GitHub Release

**Steps**:
1. Checkout repository
2. Build `ui-star-names_<version>.zip` containing `ui-star-names/` and `ui-star-names.mod`
3. Compute the archive SHA1 checksum and append it to the release notes
4. Upload the archive with `softprops/action-gh-release@v2`

**Required Permissions**:
- `contents: write`

**Configuration**:
- `files`: Generated archive name
- `body_path`: Generated release notes file with the SHA1 checksum

## Release Archive

Each workflow builds its archive locally from the repository contents. No GitHub release asset is downloaded.

**Archive Contents**:
```
ui-star-names_<version>.zip
├── ui-star-names/
│   ├── descriptor.mod
│   └── common/
│       └── random_names/
│           └── base/
│               └── *.txt
└── ui-star-names.mod
```

The Steam and Nexus workflows build the same contents as `release.zip`; the Nexus workflow uploads it under the display name `ui-star-names.zip`, while the GitHub Release workflow publishes it as `ui-star-names_<version>.zip` and appends a SHA1 checksum to the release notes.

## Dependencies

- **Upstream**: Repository contents (checked out by the workflow)
- **Downstream**:
  - Steam Workshop (consumer)
  - Nexus Mods (consumer)
  - GitHub Releases (asset host)
- **Adjacent**:
  - Mod metadata (descriptor files included in the archive)
  - Name list data (included in the archive)

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

2. Publish a GitHub Release for the tag

3. GitHub Actions automatically:
   - Attaches `ui-star-names_<version>.zip` to the GitHub Release with its SHA1 checksum appended to the notes
   - Triggers Steam workflow, which builds and uploads the release archive
   - Triggers Nexus workflow, which builds and uploads the release archive

4. Monitor workflow runs for success/failure

5. Manually upload the release archive to Paradox Mods

6. Verify all four platforms show new version

### Post-Release Verification

1. Check GitHub Release page for the attached archive and checksum
2. Check Steam Workshop page for update
3. Check Nexus Mods page for update
4. Check Paradox Mods page (manual)
5. Test install from each platform

## Failure Modes

| Failure | Cause | Recovery |
|---------|-------|----------|
| Steam upload fails | Invalid credentials, rate limit, API change | Check secrets; manual upload via Steam Workshop website |
| Nexus upload fails | Invalid API key, rate limit, API change | Check secret; manual upload via Nexus Mods website |
| GitHub Release upload fails | Missing `contents: write` permission, release unpublished | Verify workflow permissions; re-run after the release exists |
| Archive build fails | `ui-star-names/` or `ui-star-names.mod` missing or renamed | Restore the expected paths in the repository; re-run the workflow |
| Archive structure invalid | Mod directory renamed, files missing | Verify `ui-star-names/` structure in repository |

## Known Issues

- Paradox Mods requires manual upload (no API)
- Workflows depend on third-party actions (`hmlendea/steam-workshop-update`, `Nexus-Mods/upload-action`, `softprops/action-gh-release`)
- No automated verification of release archive contents
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
    - name: Build the release archive
      run: |
        zip -r "release.zip" "ui-star-names" "ui-star-names.mod"
    - name: Extract the release archive
      run: |
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
    - name: Build the release archive
      run: |
        zip -r "release.zip" "ui-star-names" "ui-star-names.mod"
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

### GitHub Release Workflow

```yaml
name: GitHub Release
on:
  release:
    types:
      - published
permissions:
  contents: write
jobs:
  build-and-upload:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repository
      uses: actions/checkout@v4
    - name: Build the release archive
      id: package
      shell: bash
      env:
        RELEASE_BODY: ${{ github.event.release.body }}
      run: |
        version="${{ github.event.release.tag_name }}"
        version="${version#v}"
        archive_name="ui-star-names_${version}.zip"
        release_notes_file="release_notes.md"

        zip -r "$archive_name" "ui-star-names" "ui-star-names.mod"
        archive_sha1="$(sha1sum "$archive_name" | awk '{print $1}')"

        printf '%s\n\n**SHA1 Checksum**: %s\n' "$RELEASE_BODY" "$archive_sha1" > "$release_notes_file"

        echo "archive_name=$archive_name" >> "$GITHUB_OUTPUT"
        echo "release_notes_file=$release_notes_file" >> "$GITHUB_OUTPUT"
    - name: Upload the release archive
      uses: softprops/action-gh-release@v2
      with:
        files: ${{ steps.package.outputs.archive_name }}
        body_path: ${{ steps.package.outputs.release_notes_file }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```