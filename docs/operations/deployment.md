# Operations: Deployment

## Overview

This document describes the deployment process for the Universum Infinitum: Star Names mod across all distribution platforms.

## Deployment Targets

| Platform | Method | Automation | Audience |
|----------|--------|------------|----------|
| Steam Workshop | GitHub Actions | Full | Steam users |
| Nexus Mods | GitHub Actions | Full | Nexus users (Vortex/MO2) |
| Paradox Mods | Manual upload | None | Paradox launcher users |
| GitHub Releases | Git tag push | Full | Direct download, mod managers |

## Deployment Triggers

### Automated (Steam, Nexus, GitHub)

**Trigger**: Push of Git tag matching `v*.*.*`

```bash
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

**Sequence**:
1. GitHub creates Release
2. Release asset must be attached (manual or separate workflow)
3. Steam workflow downloads asset → uploads to Workshop
4. Nexus workflow downloads asset → uploads to Nexus
5. GitHub Release page updated with asset

### Manual (Paradox Mods)

**Trigger**: Maintainer action after automated deployments succeed

**Procedure**:
1. Download release asset from GitHub
2. Log in to mods.paradoxplaza.com
3. Navigate to mod page
4. Upload new version
5. Submit for review/publish

## Pre-Deployment Checklist

- [ ] All changes merged to `master`
- [ ] `supported_version` updated in both descriptor files
- [ ] `./count-additions.sh` run, output recorded
- [ ] Local test install successful
- [ ] No uncommitted changes
- [ ] `master` branch up to date with origin

## Deployment Procedure

### 1. Create Release Tag

```bash
# Ensure on master
git checkout master
git pull origin master

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z - <brief summary>"

# Push tag (triggers everything)
git push origin vX.Y.Z
```

### 2. Verify GitHub Release

1. Go to `https://github.com/hmlendea/stellaris-ui-star-names/releases`
2. Confirm new release `vX.Y.Z` exists
3. Confirm asset `ui-star-names_X.Y.Z.zip` attached
4. If missing: create ZIP locally and attach manually

### 3. Monitor Automated Workflows

1. Go to Actions tab
2. Watch `Steam Workshop` workflow
3. Watch `Nexus Mods` workflow
4. Wait for both to complete (green checkmarks)

### 4. Manual Paradox Mods Upload

1. Download `ui-star-names_X.Y.Z.zip` from GitHub Release
2. Go to `https://mods.paradoxplaza.com/mods/`
3. Log in
4. Find "Universum Infinitum: Star Names"
5. Click "Add Version" or "Update"
6. Upload ZIP
7. Fill changelog (copy from GitHub Release notes)
8. Submit/Publish

### 5. Post-Deployment Verification

| Platform | Check |
|----------|-------|
| GitHub | Release visible, asset downloadable |
| Steam Workshop | Version updated, changenote visible |
| Nexus Mods | Version updated, file downloadable |
| Paradox Mods | Version updated, approved |

## Rollback Procedure

No automated rollback. To fix a bad release:

1. Fix issue in `master`
2. Create new patch tag: `vX.Y.Z+1`
3. Push new tag
4. Automated workflows deploy new version
5. Manual Paradox upload for new version

## Deployment Timing

| Step | Duration |
|------|----------|
| Tag push → GitHub Release | ~30s |
| GitHub Release → Steam | 2-5 min |
| GitHub Release → Nexus | 1-3 min |
| Manual Paradox | 5-10 min |
| **Total** | **~10-20 min** |

## Secrets Management

### Steam Workshop

| Secret | Purpose | Rotation |
|--------|---------|----------|
| `STEAM_USERNAME` | Steam account login | On credential change |
| `STEAM_PASSWORD` | Steam account password | On credential change |
| `STEAM_2FA_SEED` | 2FA TOTP seed | On 2FA reset |

### Nexus Mods

| Secret | Purpose | Rotation |
|--------|---------|----------|
| `NEXUSMODS_API_KEY` | Nexus Mods API authentication | On key regeneration |

### Configuration

Secrets stored in GitHub repository settings → Secrets and variables → Actions.

## Failure Response

### Steam Workflow Fails

1. Check Actions log for error
2. Common: expired 2FA seed, rate limit, invalid credentials
3. Fix secret or wait for rate limit
4. Re-run workflow from Actions UI

### Nexus Workflow Fails

1. Check Actions log
2. Common: invalid API key, file ID mismatch
2. Fix secret or verify file_id
3. Re-run workflow

### Paradox Mods Rejects

1. Check rejection email/reason
2. Common: missing metadata, wrong ZIP structure
3. Fix and re-upload manually

## Versioning Policy

- Semantic versioning: `MAJOR.MINOR.PATCH`
- Tag format: `vX.Y.Z` (lowercase v, no prefix)
- Major: Breaking changes (category changes, format changes)
- Minor: New name lists, significant additions
- Patch: Fixes, small additions, metadata updates

## Communication

- GitHub Release notes serve as changelog
- Steam changenote links to GitHub Release
- Nexus description links to GitHub Release
- Paradox changelog copied from GitHub