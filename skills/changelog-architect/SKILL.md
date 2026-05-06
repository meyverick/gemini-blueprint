---
name: changelog-architect
description: Maintains project changelog.md according to Keep a Changelog (v1.1.0) and SemVer. Parses repository history to generate human-centric, zero-pronoun release notes.
metadata:
  dependencies: python>=3.9
---

# Changelog Architect Skill (v1.1.0)

Principal Architect skill for maintaining the project `changelog.md`.

## Core Mandates

- **Human-Centric & Zero-Pronoun Policy:** Content must be technical, objective, and devoid of pronouns (e.g., "Add feature X" instead of "We added feature X"). Focus on *intent* and user impact.
- **Strict Categorization:** Group changes strictly into: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.
- **Chronological Order:** Maintain the latest version at the top using ISO-8601 Dates (`YYYY-MM-DD`).
- **Unreleased Tracking:** Always maintain an `## [Unreleased]` header.

## Operational Workflow

### Phase 1: Deterministic History Ingestion

1. **Execute Script:** Run `python <this-skill-folder>/scripts/parse_history.py` (resolving the path relative to this `SKILL.md` file) to deterministically extract and auto-categorize commits since the last tagged release.
2. **Contextualize:** Review the JSON output from the script. Cross-reference `git diff` for any ambiguous commits to accurately determine their architectural impact.

### Phase 2: Rationale Translation

1. Translate raw developer commit messages into human-centric changelog entries.
2. **Sanitize:** Aggressively strip out internal PII, API keys, or environment-specific file paths.
3. Merge duplicate or related commits into single, high-density bullet points.

### Phase 3: SemVer Resolution & Formatting

1. Evaluate the categorized payload to suggest the next version bump:
   - **Major:** Breaking API changes or removed features.
   - **Minor:** New backward-compatible features (`Added`).
   - **Patch:** Backward-compatible bug fixes (`Fixed`, `Security`).
2. Move items from `## [Unreleased]` to the newly designated `## [vX.Y.Z] - YYYY-MM-DD` section.
3. Update the Markdown reference links at the bottom of the document to point to the new git tag comparisons (e.g., `[Unreleased]: https://.../compare/vX.Y.Z...HEAD`).

### Phase 4: Validation

1. Verify no pronouns exist in the final drafted entries.
2. Ensure the `changelog.md` file is strictly formatted according to the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standard before writing to disk.
