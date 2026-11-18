# Component: Release Automation

## Overview

The release automation component consists of three GitHub Actions workflows that automate publishing the mod to Steam Workshop, Nexus Mods, and GitHub Releases when a version tag is pushed or a release is published. Each workflow builds the release archive itself from the checked-out repository, so publishing never depends on a pre-existing release asset.

## Workflows

### Steam Workshop (`.github/workflows/steam-workshop-release.yml`)

**Trigger**: Push of Git tag matching `v*.*.*` OR manual workflow dispatch with tag input

**Steps**:
1. Checkout the requested tag
2. Update the `version` field in `ui-star-names.mod` and `ui-star-names/descriptor.mod`
3. Build the release archive `release.zip` containing `ui-star-names/` and `ui-star-names.mod`
4. Unzip to `release/` directory
5. Upload to Steam Workshop using `hmlendea/steam-workshop-update@latest`

**Required Secrets**:
- `STEAM_USERNAME`
- `STEAM_PASSWORD`
- `STEAM_2FA_SEED`

**Configuration**:
- `appid`: 281990 (Stellaris)
- `itemid`: 2040215185 (Workshop item ID)
- `path`: `release/ui-star-names/`
- `changenote`: Links to GitHub release page

### Nexus Mods (`.github/workflows/nexus-mods-release.yml`)

**Trigger**: Push of Git tag matching `v*.*.*` OR manual workflow dispatch with tag input

**Steps**:
1. Checkout the requested tag
2. Update the `version` field in `ui-star-names.mod` and `ui-star-names/descriptor.mod`
3. Build the release archive `release.zip` containing `ui-star-names/` and `ui-star-names.mod`
4. Upload to Nexus Mods using `Nexus-Mods/upload-action@v1.0.0-beta.11`

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
2. Extract the version from the GitHub release tag
3. Update the `version` field in `ui-star-names.mod` and `ui-star-names/descriptor.mod`
4. Build `ui-star-names_<version>.zip` containing `ui-star-names/` and `ui-star-names.mod`
5. Publish it with `softprops/action-gh-release@v2`

**Required Permissions**:
- `contents: write`

**Configuration**:
- `files`: Generated archive name

The release body is left exactly as the maintainer wrote it; no checksum is computed or appended.

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

The Steam and Nexus workflows build the same contents as `release.zip`; the Nexus workflow uploads it under the display name `ui-star-names.zip`, while the GitHub Release workflow publishes it as `ui-star-names_<version>.zip`.

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
   - Attaches `ui-star-names_<version>.zip` to the GitHub Release
   - Triggers Steam workflow, which builds and uploads the release archive
   - Triggers Nexus workflow, which builds and uploads the release archive

4. Monitor workflow runs for success/failure

5. Manually upload the release archive to Paradox Mods

6. Verify all four platforms show new version

### Post-Release Verification

1. Check GitHub Release page for the attached archive
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
- The mod `version` field is written into the checked-out descriptor files at release time; the committed descriptors carry no `version` line
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
    - uses: actions/checkout@v7
      with:
        ref: ${{ env.VERSION }}
    - name: Update the mod version
      run: |
        MOD_VERSION="${VERSION#v}"

        for DESCRIPTOR in "ui-star-names.mod" "ui-star-names/descriptor.mod"
        do
          if grep -q '^version=' "${DESCRIPTOR}"; then
            sed -i "s/^version=.*/version=\"${MOD_VERSION}\"/" "${DESCRIPTOR}"
          else
            printf 'version="%s"\n' "${MOD_VERSION}" | cat - "${DESCRIPTOR}" > "${DESCRIPTOR}.tmp"
            mv "${DESCRIPTOR}.tmp" "${DESCRIPTOR}"
          fi
        done
    - name: Build the release archive
      run: |
        zip -r "release.zip" "ui-star-names/" "ui-star-names.mod"
    - name: Extract the release archive
      run: |
        unzip "release.zip" -d "release/"
    - name: Upload
      uses: hmlendea/steam-workshop-update@latest
      with:
        appid: 281990
        itemid: 2040215185
        path: "release/ui-star-names/"
        changenote: "[url=https://github.com/hmlendea/stellaris-ui-star-names/releases/tag/${{env.VERSION}}]Version ${{env.VERSION}}[/url]"
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
    - uses: actions/checkout@v7
      with:
        ref: ${{ env.VERSION }}
    - name: Update the mod version
      run: |
        MOD_VERSION="${VERSION#v}"

        for DESCRIPTOR in "ui-star-names.mod" "ui-star-names/descriptor.mod"
        do
          if grep -q '^version=' "${DESCRIPTOR}"; then
            sed -i "s/^version=.*/version=\"${MOD_VERSION}\"/" "${DESCRIPTOR}"
          else
            printf 'version="%s"\n' "${MOD_VERSION}" | cat - "${DESCRIPTOR}" > "${DESCRIPTOR}.tmp"
            mv "${DESCRIPTOR}.tmp" "${DESCRIPTOR}"
          fi
        done
    - name: Build the release archive
      run: |
        zip -r "release.zip" "ui-star-names/" "ui-star-names.mod"
    - name: Upload
      uses: Nexus-Mods/upload-action@v1.0.0-beta.11
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
    types: [ published ]
permissions:
  contents: write
jobs:
  release:
    name: Build and publish
    runs-on: ubuntu-latest
    steps:
    - name: Check out the repository
      uses: actions/checkout@v7
    - name: Extract the version from the GitHub tag
      id: version
      run: |
        VERSION="${{ github.event.release.tag_name }}"
        VERSION="${VERSION#v}"
        echo "version=${VERSION}" >> "$GITHUB_OUTPUT"
    - name: Update the mod version
      shell: bash
      run: |
        MOD_VERSION="${{ steps.version.outputs.version }}"

        for DESCRIPTOR in "ui-star-names.mod" "ui-star-names/descriptor.mod"
        do
          if grep -q '^version=' "${DESCRIPTOR}"; then
            sed -i "s/^version=.*/version=\"${MOD_VERSION}\"/" "${DESCRIPTOR}"
          else
            printf 'version="%s"\n' "${MOD_VERSION}" | cat - "${DESCRIPTOR}" > "${DESCRIPTOR}.tmp"
            mv "${DESCRIPTOR}.tmp" "${DESCRIPTOR}"
          fi
        done
    - name: Build the release archive
      id: package
      shell: bash
      run: |
        ARCHIVE_NAME="ui-star-names_${{ steps.version.outputs.version }}.zip"

        zip -r "${ARCHIVE_NAME}" "ui-star-names/" "ui-star-names.mod"

        echo "archive_name=${ARCHIVE_NAME}" >> "$GITHUB_OUTPUT"
    - name: Publish the release asset
      uses: softprops/action-gh-release@v2
      with:
        files: ${{ steps.package.outputs.archive_name }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```