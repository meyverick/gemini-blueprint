---
name: forensic-git-historian
description: Transforms code changes into high-fidelity, architectural commit messages. Use when the user needs to commit changes, or requires atomic, bisect-compatible, and rationale-first version control documentation.
metadata:
  dependencies: python>=3.9
---

# Forensic Git Historian & Commit Architect

## Core Mission

Architect the **Epistemological Ledger** of the workspace. You do not merely summarize syntactical changes; you document the **Technical Rationale (Why)** and business logic shifts. Every commit must be a "testable unit of intent" satisfying the `git bisect` standard.

## Operational Workflow

### Phase 1: Forensic Discovery & Deterministic Security

1. **Change Ingestion**: Execute `git status` and `git diff HEAD` (or `git diff --staged`) to identify the modified scope.
2. **Mandatory Watchtower Audit**: Execute `python <this-skill-folder>/scripts/security_audit.py` (resolving the path relative to this `SKILL.md` file) to programmatically verify `.gitignore` integrity and ensure no sensitive credentials or environment metadata (`.env`, `.pem`, `node_modules`) are staged. **Do not proceed if this script exits with an error code.**
3. **Historical Alignment**: Execute `git log -n 3` to align with the existing repository style and verbosity.

### Phase 2: Rationale Extraction & Environment Sanitization

1. Extract the "Why" from code patterns, developer comments, and user hints.
2. **Environment Gotchas (CRLF vs LF)**: When analyzing diffs, aggressively filter out whitespace or line-ending noise caused by Windows (CRLF) vs. Unix (LF) environment transitions. Never document line-ending normalizations as logic changes unless explicitly requested.
3. Identify architectural trade-offs and underlying business requirements.
4. Apply the **Zero-Pronoun Policy**: Use explicit noun repetition instead of "it", "this", or "they".

### Phase 3: Message Synthesis

1. Consult **[commit-standards.md](<this-skill-folder>/references/commit-standards.md)** for strict formatting rules (Subject line ≤ 50 chars, 72-char body wrap).
2. Apply the **Conventional Commits v1.0.0** typology.
3. Ensure the Subject Line completes the semantic construct: "If applied, the commit will...".
4. Draft the message with an absolute focus on rationale-first content.

### Phase 4: Quality Assurance

1. Perform a final audit against the checklist in **[commit-standards.md](<this-skill-folder>/references/commit-standards.md)**.
2. Ensure periods and commas are placed **OUTSIDE** quotation marks.
3. Wrap the final commit message in `<commit_message>` tags.

### Phase 5: Post-Commit Synchronization (Mandatory)

1. **Trigger**: Immediately after successfully executing the `git commit` command.
2. **Action**: Invoke the **changelog-architect** skill.
3. **Objective**: Synchronize `changelog.md` with the newly created commit to ensure historical continuity.

## Mandatory Output Format

```xml
<commit_message>
<type>(<scope>)<!>: <description>

<rationale_body>
</commit_message>
```
