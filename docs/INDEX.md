# Stellaris - Universum Infinitum - Star Names Documentation

## Repository Summary

This repository contains a pure data mod for the game Stellaris that adds thousands of new names for stars, nebulas, asteroids, and black holes. The mod consists entirely of static text files in Clausewitz script format that the Stellaris game engine reads during galaxy generation. There is no executable code, build step, or runtime.

## Root Document Map

- [ARCHITECTURE.md](../ARCHITECTURE.md) — System context, data architecture, deployment model, compatibility contracts, and source map
- [SECURITY.md](../SECURITY.md) — Security policy, supported versions, vulnerability reporting, and disclosure process
- [ROADMAP.md](../ROADMAP.md) — Project roadmap and planned enhancements
- [PRIVACY.md](../PRIVACY.md) — Privacy and data handling statement (no personal data processed)
- [LICENSE](../LICENSE) — GNU General Public License v3 terms
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) — Community conduct standards and reporting process
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Contribution guidelines, development setup, and pull request process
- [README.md](../README.md) — Project overview, installation, usage, and contribution guidelines

## Documentation Catalogue

### Architecture & Design

| File | Description |
|------|-------------|
| [architecture.md](./architecture.md) | High-level architecture complementing root ARCHITECTURE.md with implementation detail |
| [repository-overview.md](./repository-overview.md) | Repository purpose, scope, and entry points |
| [repository-structure.md](./repository-structure.md) | Source tree layout and module organisation |
| [data-model.md](./data-model.md) | Domain entities, relationships, and persistence model |

### Components

| File | Description |
|------|-------------|
| [components/name-list-data.md](./components/name-list-data.md) | Name list data files: stars, nebulas, asteroids, black holes |
| [components/mod-metadata.md](./components/mod-metadata.md) | Mod descriptor files and their contracts |
| [components/release-automation.md](./components/release-automation.md) | GitHub Actions workflows for Steam Workshop, Nexus Mods, and GitHub Releases |

### Flows

| File | Description |
|------|-------------|
| [flows/mod-loading-and-galaxy-generation.md](./flows/mod-loading-and-galaxy-generation.md) | End-to-end flow from mod installation to name application |
| [flows/release-and-distribution.md](./flows/release-and-distribution.md) | Release automation flow from tag push to platform publication |

### Behaviour

| File | Description |
|------|-------------|
| [behaviour/name-selection-and-application.md](./behaviour/name-selection-and-application.md) | How Stellaris selects and applies names from the mod |
| [behaviour/contribution-workflow.md](./behaviour/contribution-workflow.md) | Contributor workflow from fork to merged pull request |

### Configuration

| File | Description |
|------|-------------|
| [config/mod-descriptor-schema.md](./config/mod-descriptor-schema.md) | Mod descriptor file schema and validation rules |
| [config/name-list-format.md](./config/name-list-format.md) | Name list file format specification |

### Testing

| File | Description |
|------|-------------|
| [testing/test-strategy.md](./testing/test-strategy.md) | Test strategy, organisation, and coverage |

### Operations

| File | Description |
|------|-------------|
| [operations/deployment.md](./operations/deployment.md) | Deployment process across all platforms |
| [operations/troubleshooting.md](./operations/troubleshooting.md) | Common issues and solutions |

### API Reference

| File | Description |
|------|-------------|
| [api-reference/name-list-api.md](./api-reference/name-list-api.md) | Engine internal API for name list registration and selection |
| [api-reference/mod-descriptor-api.md](./api-reference/mod-descriptor-api.md) | Mod descriptor interface for launcher and Steam |

### Logging

| File | Description |
|------|-------------|
| [logging.md](./logging.md) | Engine logging behaviour relevant to mod debugging |

## Navigation Aids

- **Start here** (newcomers): [repository-overview.md](./repository-overview.md) → [repository-structure.md](./repository-structure.md) → [architecture.md](./architecture.md)
- **Deep dive** (component owners): [components/](./components/) → [data-model.md](./data-model.md) → [flows/](./flows/)
- **Debugging** (operators): [logging.md](./logging.md) → [operations/troubleshooting.md](./operations/troubleshooting.md)
- **Contributing** (contributors): [behaviour/contribution-workflow.md](./behaviour/contribution-workflow.md) → [config/](./config/) → [testing/](./testing/)
- **Releasing** (maintainers): [flows/release-and-distribution.md](./flows/release-and-distribution.md) → [operations/deployment.md](./operations/deployment.md)

## Maintenance Metadata

- Last reviewed: 2026-11-03
- Owner: Repository maintainers
- Coverage status: Initial generation — comprehensive coverage of all repository areas
- Total documents: 18 (including this index)