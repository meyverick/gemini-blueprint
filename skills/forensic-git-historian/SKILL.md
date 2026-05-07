---
name: forensic-git-historian
description: Transforms code changes into high-fidelity, architectural commit messages using semantic AST diffing. Execute semantic version control operations (impact analysis, history, context) to avoid line-level noise. Use when committing changes, reviewing code, or analyzing blast radius.
metadata:
  dependencies: python>=3.9, sem-cli
---

# Forensic Git Historian & Semantic Ledger

## Core Mission

Architect the **Epistemological Ledger** of the workspace. You do not merely summarize syntactical changes; you document the **Technical Rationale (Why)** and business logic shifts. Every commit must be a "testable unit of intent" satisfying the `git bisect` standard. You achieve this by fundamentally shifting from line-oriented reasoning (`git diff`) to structural, entity-oriented reasoning (`sem diff`).

## 1. Semantic Execution Protocols

### A. Semantic Diffing & Code Reviews
Always prefer semantic diffs over standard `git diff` to eliminate line-level noise.
* **Default execution:** `sem diff`
* **Machine-readable execution:** `sem diff --format json` (Mandatory for commit generation).
* **Specific commit range:** `sem diff --from HEAD~3 --to HEAD --format json`

### B. Impact Analysis (Blast Radius)
Map dependencies before recommending refactors or generating rationale.
* **Default execution:** `sem impact <entity_name>` (append `--file <path>` for disambiguation).
* **JSON Pipeline:** `sem impact <entity_name> --json` (Parses direct dependencies and dependents).

### C. Token-Budgeted Context Extraction
When loading context for complex refactors, restrict output to stay within context windows.
* **Default execution:** `sem context <entity_name> --budget 8000 --json`

### D. Semantic Blame & History
Track authors and historical changes at the structural level.
* **Entity evolution:** `sem log <entity_name> -v --json`
* **File-level entity blame:** `sem blame <file_path> --json`

## 2. The Semantic-Forensic Commit Workflow

### Phase 1: Structural Discovery & Deterministic Security
1. **Mandatory Watchtower Audit**: Execute `python <this-skill-folder>/scripts/security_audit.py` to programmatically verify `.gitignore` integrity. **Do not proceed if this exits with an error code.**
2. **Semantic Ingestion**: Execute `sem diff --format json` (never `git diff`) to extract exact structural and logical changes (e.g., added parameters, changed return types, new classes).
3. **Validation Loop**: Verify the `entityType` in JSON outputs. If it reads `chunk`, semantic extraction failed for that file. Explicitly check for `renamed` or `moved` tags before assuming an entity was deleted.

### Phase 2: Rationale Extraction & Blast Radius
1. Automatically trigger `sem impact <entity_name> --json` for critical modified entities to determine the "Blast Radius."
2. Extract the "Why" from the structural impact analysis, developer comments, and user hints. Focus purely on logical entity changes.
3. Apply the **Zero-Pronoun Policy**: Use explicit noun repetition instead of "it", "this", or "they".

### Phase 3: Version Calibration & Synthesis
1. Consult **[commit-standards.md](<this-skill-folder>/references/commit-standards.md)** for formatting rules.
2. Analyze the `sem diff` output to automatically determine SemVer impact (e.g., a breaking signature change triggers a `!` prefix).
3. Apply the **Conventional Commits v1.0.0** typology.
4. Ensure the Subject Line completes the construct: "If applied, the commit will...".

### Phase 4: Quality Assurance
1. Ensure periods and commas are placed **OUTSIDE** quotation marks.
2. Wrap the final commit message in `<commit_message>` tags.

### Phase 5: Post-Commit Synchronization (Mandatory)
1. **Trigger**: Immediately after successfully executing the `git commit` command.
2. **Action**: Invoke the **changelog-architect** skill.
