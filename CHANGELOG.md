# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2026-05-08

### Changed
- Consolidate semantic versioning and commit generation by natively integrating the `sem-version-control` skill into the `forensic-git-historian` skill workflow.

### Removed
- The standalone `sem-version-control` skill has been removed to enforce a unified semantic ledger boundary.

## [2.1.11] - 2026-05-08

## [2.1.10] - 2026-05-07

### Changed
- Synchronized `README.md` and technical wiki with the current codebase state, adding 9 missing specialized skills (PixiJS, Svelte, Tauri, Threlte, SemVer, and CLI Introspection).
- Updated architectural diagrams in `README.md` and `wiki/Architecture.md` to reflect the expanded skills layer.
- Corrected legacy references to the `policies/` directory in `README.md` and `wiki/Architecture.md`, redirecting to the current `commands/` and `hooks/` implementation.
- Refined `wiki/Skill-Development.md` with a categorized breakdown of Core, Framework Expert, and Utility skills.
- Updated `wiki/Repository-Maintenance.md` to reflect that `update_repos.py` now only synchronizes existing repositories and no longer performs auto-cloning.

## [2.1.9] - 2026-05-06

### Changed
- Disabled ANSI escape sequence colorization in `update_repos.py`, `release.py`, and `package.py` while ensuring mandatory emoji preservation in script outputs.
- Refined the `/audit` command prompt in `commands/audit.toml` for enhanced architectural mapping and contextual depth.
- Updated `GEMINI.md` to formally codify Output Presentation Standards, prohibiting ANSI colorization and mandating emoji utilization in plain text environments.

## [2.1.8] - 2026-05-06

## [2.1.7] - 2026-05-06

## [2.1.6] - 2026-05-06

### Fixed
- Enabled ANSI escape sequence support on Windows in `update_repos.py` and `release.py` to prevent raw escape codes from appearing in the console.

## [2.1.5] - 2026-05-06

## [2.1.4] - 2026-05-06

## [2.1.3] - 2026-05-06

## [2.1.2] - 2026-05-06

## [2.1.1] - 2026-05-06

## [2.1.0] - 2026-05-06

### Added
- Automated release orchestrator script (`release.py`) for streamlined versioning and tagging.
- GitHub Actions workflow for automated creation of formal GitHub Releases upon tag pushes.
- Integrated release notes extraction logic for automated deployment.

## [2.0.0] - 2026-05-06

### Added
- Repository manifest `references/repositories/.repos` for automated workspace restoration.
- Modern Python implementation of `update_repos.py` for cross-platform repository synchronization.
- `Maintenance and Backups` section in technical wiki documenting restoration procedures.
- Comprehensive technical wiki structure (Architecture, Agent-Workflows, Skill-Development) initialized for independent wiki repository management.

### Changed
- Optimized `backup_sync.py` with a lightweight strategy that harvests repository URLs into a manifest while excluding bulky source folders.
- Hardcoded backup destination to `D:/Files/development/backups/` to ensure structural consistency and machine portability.
- Updated `.gitignore` to explicitly exclude repository subfolders while preserving manifest files.

### Removed
- Legacy `update_repos.js` in favor of the new Python implementation.

### Fixed
- 7-Zip exclusion logic in `backup_sync.py` to ensure reliable folder skipping on Windows environments.
- Corrected `hooks.json` structure by wrapping hook events in a required `"hooks"` property to ensure compliance with Gemini CLI extension standards.
