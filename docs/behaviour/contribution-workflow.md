# Behaviour: Contribution Workflow

## Overview

This document describes the end-to-end workflow for contributing changes to the mod, from issue creation to merged pull request.

## Contribution Types

| Type | Description | Files Affected |
|------|-------------|----------------|
| New name list | Add new `.txt` file for a source universe | `ui-star-names/common/random_names/base/ui_<category>_<source>.txt` |
| Name additions | Add entries to existing file | Existing `.txt` file |
| Corrections | Fix typos, formatting, duplicates | Existing `.txt` file |
| Reorganisation | Split/merge/rename files | Multiple `.txt` files |
| Metadata update | Update game version compatibility | `descriptor.mod`, `ui-star-names.mod` |
| Documentation | Update docs/ files | `docs/**/*.md` |

## Workflow Steps

### 1. Issue Creation (Optional but Recommended)

1. Check existing issues for duplicates
2. Create issue with:
   - **Title**: `[Category] Brief description` (e.g., `[Stars] Add Warhammer 40K star names`)
   - **Description**: Source, approximate entry count, rationale
   - **Labels**: `enhancement`, `stars`/`nebulas`/`asteroids`/`black-holes`/`documentation`

### 2. Fork and Branch

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/<your-username>/stellaris-ui-star-names.git
cd stellaris-ui-star-names

# Create feature branch
git checkout -b feature/add-warhammer40k-stars
```

### 3. Development

#### Adding a New Name List File

1. Create new file in `ui-star-names/common/random_names/base/`:
   ```bash
   touch ui-star-names/common/random_names/base/ui_stars_warhammer40k.txt
   ```

2. Follow format:
   ```clausewitz
   name_list = {
       category = "star"
       name = "Terra"
       name = "Mars"
       name = "Holy Terra"
       # ... more names
   }
   ```

3. Naming convention: `ui_<category>_<source>.txt`
   - Categories: `stars`, `nebulas`, `asteroid-prefixes`, `asteroid-postfixes`, `black-holes`
   - Source: lowercase, hyphenated (e.g., `warhammer40k`, `star-wars`, `elite-dangerous`)

#### Editing Existing File

1. Open file in editor
2. Add/remove/modify `name = "..."` lines
3. Maintain alphabetical ordering (preferred but not required)
4. No trailing commas, each entry on own line

#### Asteroid Prefixes/Suffixes

```clausewitz
# Prefixes (end with -)
asteroid_prefix = {
    Astra-
    Nova-
    Void-
}

# Suffixes (start with -)
asteroid_postfix = {
    -Prime
    -Secundus
    -Major
}
```

### 4. Local Verification

```bash
# Count entries per category
./count-additions.sh

# Output example:
# Stars: 2847
# Nebulas: 482
# Asteroid prefixes: 240
# Asteroid suffixes: 240
# Black holes: 75
```

Verify your changes increased counts as expected.

#### Game Testing (Optional but Recommended)

1. Copy `ui-star-names/` to Stellaris mod directory
2. Enable mod in launcher
3. Start new game
4. Verify names appear in galaxy

### 5. Commit and Push

```bash
# Stage changes
git add ui-star-names/common/random_names/base/ui_stars_warhammer40k.txt

# Commit with conventional message
git commit -m "feat(stars): add Warhammer 40K star names (~60 entries)"

# Push to your fork
git push origin feature/add-warhammer40k-stars
```

#### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `chore`
Scopes: `stars`, `nebulas`, `asteroids`, `black-holes`, `metadata`, `docs`, `ci`

Examples:
- `feat(stars): add Dune star names (~70 entries)`
- `fix(nebulas): correct typo in "Crab Nebula" entry`
- `docs: update repository-structure.md for new file`
- `chore(metadata): update supported_version to 4.5.*`

### 6. Pull Request

1. Open PR from your fork's branch to `hmlendea/stellaris-ui-star-names:master`
2. PR title: Same as commit message (or summary for multiple commits)
3. PR description:
   - **What**: Brief summary of changes
   - **Why**: Rationale / issue reference
   - **Testing**: How verified (count script, in-game, etc.)
   - **Entry counts**: Before/after from `count-additions.sh`

4. Labels: Auto-assigned from branch name or add manually

### 7. Review Process

#### Automated Checks

- GitHub Actions validates workflow syntax (no code tests)
- No linting, formatting, or unit tests for data files

#### Manual Review

Maintainer checks:
- [ ] File follows naming convention
- [ ] Format is valid Clausewitz script
- [ ] Category field matches file category
- [ ] Entries are quoted strings (stars/nebulas/black holes)
- [ ] No obvious duplicates within file
- [ ] Source attribution clear (filename + optional comment)
- [ ] `count-additions.sh` output reasonable

#### Review Outcomes

| Outcome | Action |
|---------|--------|
| Approve | Merge to master |
| Request changes | Contributor updates branch |
| Reject | Close with explanation |

### 8. Merge and Release

1. Maintainer merges PR (squash or merge commit)
2. Changes now in `master`
3. Maintainer creates release tag when ready:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```
4. Automated workflows publish to Steam and Nexus
5. Maintainer manually uploads to Paradox Mods

## Quality Standards

### Name List Files

- **Encoding**: UTF-8
- **Line endings**: LF (Unix)
- **Indentation**: 4 spaces (Clausewitz standard)
- **Quoting**: Double quotes for `name` entries
- **Comments**: `#` for comments, use sparingly
- **Ordering**: Alphabetical preferred
- **Duplicates**: Avoid within file; cross-file duplicates allowed (increase weight)

### Metadata Files

- Both descriptor files **must** be identical
- `supported_version` uses wildcard: `4.5.*`
- `tags` must include `Galaxy Generation`

### Documentation

- Follow existing markdown structure
- Update `docs/INDEX.md` if adding new docs
- Verify repository-relative links work

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Wrong category in `name_list` | Match category to filename prefix |
| Missing quotes on names | Always use `name = "Name"` |
| Windows line endings | Configure editor for LF |
| Duplicate file (e.g., `copy.txt`) | Check before committing |
| Descriptor files out of sync | Edit both simultaneously |
| Tag format wrong | Use `vX.Y.Z` exactly |

## Tools

| Tool | Purpose |
|------|---------|
| `./count-additions.sh` | Count unique entries per category |
| Text editor | Edit `.txt` files (VS Code, Notepad++, etc.) |
| Stellaris launcher | Test mod in-game |
| Git/GitHub | Version control and PR workflow |

## Onboarding Checklist for New Contributors

- [ ] Read README.md
- [ ] Read CONTRIBUTING.md
- [ ] Read this document
- [ ] Fork repository
- [ ] Run `./count-additions.sh` to see baseline
- [ ] Make a small test change (fix typo)
- [ ] Submit first PR

## Maintainer Checklist for Merging

- [ ] PR passes automated checks
- [ ] Manual review criteria met
- [ ] No merge conflicts
- [ ] Commit message follows convention
- [ ] Squash/merge appropriately
- [ ] Delete branch after merge
- [ ] Consider if release tag needed