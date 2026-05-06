# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
