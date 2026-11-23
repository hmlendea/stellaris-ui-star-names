# Component: Release Automation

## Overview

The release automation component consists of four GitHub Actions workflows: a continuous integration workflow that builds all three game variants on every change to `master`, and three release workflows that automate publishing the mod to Steam Workshop, Nexus Mods, and GitHub Releases when a version tag is pushed or a release is published. Every workflow generates the mod from source with `scripts/generate-mod.py`, so publishing never depends on committed build output or a pre-existing release asset.

## Workflows

### Build (`.github/workflows/build.yml`)

**Trigger**: Push or pull request targeting `master`

**Jobs**:
1. `galciv2` ("Build for Galactic Civilizations II"): checks out the repository and generates the Galactic Civilizations II star name data with `scripts/generate-mod.py --version <version> --game galciv2`
2. `galciv3` ("Build for Galactic Civilizations III"): checks out the repository and generates the Galactic Civilizations III star name data with `scripts/generate-mod.py --version <version> --game galciv3`
3. `stellaris` ("Build for Stellaris"): checks out the repository and generates the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris`

The three jobs run independently, so a failure in one game does not mask the status of the others.

### Steam Workshop (`.github/workflows/steam-workshop-release.yml`)

**Trigger**: Push of Git tag matching `v*.*.*` OR manual workflow dispatch with tag input

**Steps**:
1. Checkout the requested tag
2. `galciv3` job: generate the Galactic Civilizations III mod with `scripts/generate-mod.py --version <version> --game galciv3` and upload the generated mod directory `out/galciv3/ui-star-names/` to Steam Workshop using `hmlendea/steam-workshop-update@latest`
3. `stellaris` job: generate the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris` and upload the generated mod directory `out/stellaris/ui-star-names/` to Steam Workshop using `hmlendea/steam-workshop-update@latest`

**Required Secrets**:
- `STEAM_USERNAME`
- `STEAM_PASSWORD`
- `STEAM_2FA_SEED`

**Configuration**:
- Galactic Civilizations III: `appid` 226860, `itemid` 3844651637, `path` `out/galciv3/ui-star-names/`
- Stellaris: `appid` 281990, `itemid` 2040215185, `path` `out/stellaris/ui-star-names/`
- `changenote`: Links to GitHub release page

### Nexus Mods (`.github/workflows/nexus-mods-release.yml`)

**Trigger**: Push of Git tag matching `v*.*.*` OR manual workflow dispatch with tag input

**Steps**:
1. Check out the requested tag
2. Generate the Stellaris mod with `scripts/generate-mod.py --version <version> --game stellaris` using the release version
3. Build the Stellaris `release.zip` from the generated `out/stellaris/` output
4. Generate the Galactic Civilizations II star name data with `scripts/generate-mod.py --version <version> --game galciv2`
5. Build the Galactic Civilizations II `release-galciv2.zip` from the generated `Data` and `Twilight` directories in `out/galciv2/`
6. Generate the Galactic Civilizations III mod with `scripts/generate-mod.py --version <version> --game galciv3`
7. Build the Galactic Civilizations III `release-galciv3.zip` from the generated `ui-star-names` directory in `out/galciv3/`
8. Upload all three archives to Nexus Mods using `Nexus-Mods/upload-action@v1.0.0-beta.11`

**Required Secrets**:
- `NEXUSMODS_API_KEY`

**Configuration**:
- `file_id`: 920143 (Stellaris), 8432274 (Galactic Civilizations II), and 8444367 (Galactic Civilizations III) Nexus Mods file IDs
- `filename`: `release.zip` (Stellaris), `release-galciv2.zip` (Galactic Civilizations II), and `release-galciv3.zip` (Galactic Civilizations III)
- `display_name`: `ui-star-names.zip` (Stellaris), `ui-star-names-galciv2.zip` (Galactic Civilizations II), and `ui-star-names-galciv3.zip` (Galactic Civilizations III)
- `version`: Tag name (with `v` prefix stripped)
- `description`: Links to GitHub release page
- `category`: `main`
- `archive_existing_version`: `true`
- `update_mod_version`: `true`

### GitHub Release (`.github/workflows/github-release.yml`)

**Trigger**: Publication of a GitHub Release OR manual workflow dispatch with tag input

**Jobs**:
1. `galciv2` ("Build and publish for Galactic Civilizations II"):
   1. Check out the repository at the release tag
   2. Extract the version from the GitHub release tag
   3. Generate the star name data with `scripts/generate-mod.py --version <version> --game galciv2` using the release version
   4. Build `ui-star-names-galciv2_<version>.zip` from the generated `Data` directory in `out/galciv2/`
   5. Publish it with `softprops/action-gh-release@v2`
2. `galciv3` ("Build and publish for Galactic Civilizations III"):
   1. Check out the repository at the release tag
   2. Extract the version from the GitHub release tag
   3. Generate the star name data with `scripts/generate-mod.py --version <version> --game galciv3` using the release version
   4. Build `ui-star-names-galciv3_<version>.zip` from the generated `ui-star-names` directory in `out/galciv3/`
   5. Publish it with `softprops/action-gh-release@v2`
3. `stellaris` ("Build and publish for Stellaris"):
   1. Check out the repository at the release tag
   2. Extract the version from the GitHub release tag
   3. Generate the mod with `scripts/generate-mod.py --version <version> --game stellaris` using the release version
   4. Build `ui-star-names_<version>.zip` from the generated `out/stellaris/` output
   5. Publish it with `softprops/action-gh-release@v2`

**Required Permissions**:
- `contents: write`

**Configuration**:
- `files`: Generated archive name

The release body is left exactly as the maintainer wrote it; no checksum is computed or appended.

## Release Archive

Each workflow generates the mod with `scripts/generate-mod.py` and builds its archive locally from the generated output directory. No GitHub release asset is downloaded.

**Stellaris archive contents** (`ui-star-names_<version>.zip`):
```
ui-star-names_<version>.zip
├── ui-star-names/
│   ├── descriptor.mod
│   ├── thumbnail.png
│   └── common/
│       └── random_names/
│           └── base/
│               └── universum_infinitum.txt
└── ui-star-names.mod
```

**Galactic Civilizations II archive contents** (`ui-star-names-galciv2_<version>.zip`):
```
ui-star-names-galciv2_<version>.zip
├── Data/
│   └── English/
│       └── STARS.txt
└── Twilight/
    └── Data/
        └── English/
            └── STARS.txt
```

**Galactic Civilizations III archive contents** (`ui-star-names-galciv3_<version>.zip`):
```
ui-star-names-galciv3_<version>.zip
└── ui-star-names/
    ├── ParticleScriptDefs/
    ├── Text/
    │   └── StarNamesText.xml
    ├── Core/
    └── Game/
```

The Galactic Civilizations II archive is not a mod: the game reads star names only from its own data files before mods are loaded, so the archived files replace the game's shipped files. The `Twilight/Data/English/STARS.txt` file is an identical copy of `Data/English/STARS.txt`. The Galactic Civilizations III archive is a mod: its `ui-star-names/` folder replaces the game's `Text/StarNamesText.xml` and is placed in the game's `Mods` directory, and it also contains the mandatory `ParticleScriptDefs`, `Core`, and `Game` folders the game requires every mod to provide.

The GitHub Release workflow builds all three archives in separate jobs. The Nexus workflow generates all three games in its single `release` job and uploads one archive per game, with the display names `ui-star-names.zip` for Stellaris, `ui-star-names-galciv2.zip` for Galactic Civilizations II, and `ui-star-names-galciv3.zip` for Galactic Civilizations III, while the Steam workflow uploads the generated `out/stellaris/ui-star-names/` directory rather than an archive.

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
3. `./scripts/count-additions.sh` run and output recorded for release notes
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
   - Triggers Nexus workflow, which builds and uploads the release archives for the Stellaris, Galactic Civilizations II, and Galactic Civilizations III content

4. Monitor workflow runs for success/failure

5. Manually upload the release archive to Paradox Mods

6. Verify all four platforms show new version

### Post-Release Verification

1. Check GitHub Release page for the attached archives
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
| Galactic Civilizations II archive build fails | `Data/English/STARS.txt` or `Twilight/Data/English/STARS.txt` missing | Verify the GalCiv2 output of `scripts/generate-mod.py`; re-run the workflow |

## Known Issues

- Paradox Mods requires manual upload (no API)
- Workflows depend on third-party actions (`hmlendea/steam-workshop-update`, `Nexus-Mods/upload-action`, `softprops/action-gh-release`)
- No automated verification of release archive contents
- The mod `version` field is written into the checked-out descriptor files at release time; the committed descriptors carry no `version` line
- Nexus Mods requires separate mod pages per game, so the Stellaris, Galactic Civilizations II, and Galactic Civilizations III releases use different file identifiers
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
  galciv3:
    runs-on: ubuntu-latest
    env:
      VERSION: ${{ inputs.tag || github.ref_name }}
    steps:
    - uses: actions/checkout@v7
      with:
        ref: ${{ env.VERSION }}
    - name: Generate the mod
      run: |
        python3 scripts/generate-mod.py --version "${VERSION#v}" --game galciv3
    - name: Upload to Steam Workshop
      uses: hmlendea/steam-workshop-update@latest
      with:
        appid: 226860
        itemid: 3844651637
        path: "out/galciv3/ui-star-names/"
        changenote: "[url=https://github.com/hmlendea/stellaris-ui-star-names/releases/tag/${{env.VERSION}}]Version ${{env.VERSION}}[/url]"
      env:
        STEAM_USERNAME: ${{secrets.STEAM_USERNAME}}
        STEAM_PASSWORD: ${{secrets.STEAM_PASSWORD}}
        STEAM_2FASEED: ${{secrets.STEAM_2FA_SEED}}

  stellaris:
    runs-on: ubuntu-latest
    env:
      VERSION: ${{ inputs.tag || github.ref_name }}
    steps:
    - uses: actions/checkout@v7
      with:
        ref: ${{ env.VERSION }}
    - name: Generate the mod
      run: |
        python3 scripts/generate-mod.py --version "${VERSION#v}" --game stellaris
    - name: Upload
      uses: hmlendea/steam-workshop-update@latest
      with:
        appid: 281990
        itemid: 2040215185
        path: "out/stellaris/ui-star-names/"
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
    name: Release
    runs-on: ubuntu-latest
    env:
      VERSION: ${{ inputs.tag || github.ref_name }}
    steps:
    - uses: actions/checkout@v7
      with:
        ref: ${{ env.VERSION }}
    - name: Generate the mod
      run: |
        python3 scripts/generate-mod.py --version "${VERSION#v}" --game stellaris
    - name: Build the release archive
      run: |
        cd out/stellaris
        zip -r "${GITHUB_WORKSPACE}/release.zip" "ui-star-names/" "ui-star-names.mod"
    - name: Generate the Galactic Civilizations II data
      run: |
        python3 scripts/generate-mod.py --version "${VERSION#v}" --game galciv2
    - name: Build the Galactic Civilizations II release archive
      run: |
        cd out/galciv2
        zip -r "${GITHUB_WORKSPACE}/release-galciv2.zip" "Data" "Twilight"
    - name: Generate the Galactic Civilizations III mod
      run: |
        python3 scripts/generate-mod.py --version "${VERSION#v}" --game galciv3
    - name: Build the Galactic Civilizations III release archive
      run: |
        cd out/galciv3
        zip -r "${GITHUB_WORKSPACE}/release-galciv3.zip" "ui-star-names"
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
    - name: Upload the Galactic Civilizations II release
      uses: Nexus-Mods/upload-action@v1.0.0-beta.11
      with:
        api_key: ${{ secrets.NEXUSMODS_API_KEY }}
        file_id: 8432274
        filename: release-galciv2.zip
        display_name: ui-star-names-galciv2.zip
        version: ${{env.VERSION}}
        description: "Changelog: https://github.com/hmlendea/stellaris-ui-star-names/releases/${{env.VERSION}}"
        category: main
        archive_existing_version: true
        update_mod_version: true
    - name: Upload the Galactic Civilizations III release
      uses: Nexus-Mods/upload-action@v1.0.0-beta.11
      with:
        api_key: ${{ secrets.NEXUSMODS_API_KEY }}
        file_id: 8444367
        filename: release-galciv3.zip
        display_name: ui-star-names-galciv3.zip
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