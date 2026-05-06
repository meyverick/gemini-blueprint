---
name: sem-version-control
description: Execute semantic version control operations using the sem CLI. Perform entity-level diffing, cross-file impact analysis, semantic blame, and token-budgeted context extraction across 23+ supported languages. Use this to avoid line-level diff noise and understand structural code changes.
---

# Semantic Version Control (sem) Execution Protocol

This skill dictates the procedures for interacting with `sem`, a tree-sitter-based semantic version control tool. You will shift from line-oriented reasoning (`git diff`) to structural, entity-oriented reasoning (`sem diff`).

## 1. Activation Conditions (When to use)

Engage this skill when the user requests:

* **Code Reviews:** Understanding what logical units (functions, classes, traits) changed, ignoring whitespace/formatting.
* **Blast Radius Analysis:** Determining what breaks if a specific function/class is modified.
* **Semantic History:** Tracking the evolution of a specific entity over time, regardless of file moves or renames.
* **Context Generation:** Gathering token-budgeted LLM context around an entity and its dependencies.

## 2. Execution Procedures & Clear Defaults

### A. Semantic Diffing

Always prefer semantic diffs over standard `git diff` to eliminate line-level noise.

* **Default execution:** `sem diff`
* **Machine-readable execution:** `sem diff --format json` (Use this for reliable parsing).
* **Verbose word-level:** `sem diff -v`
* **Specific commit range:** `sem diff --from HEAD~3 --to HEAD --format json`

### B. Impact Analysis (Blast Radius)

Map dependencies before recommending or executing refactors.

* **Default execution:** `sem impact <entity_name>`
* **Disambiguation:** If an entity name exists in multiple files, strictly append `--file <path/to/file>`.
* **JSON Pipeline:** `sem impact <entity_name> --json` (Parses direct dependencies and dependents).

### C. Semantic Blame & History

Track authors and historical changes at the structural level.

* **Entity evolution:** `sem log <entity_name> -v --json` (Shows content diffs between versions).
* **File-level entity blame:** `sem blame <file_path> --json`

### D. Token-Budgeted Context Extraction

When loading context for complex refactors, restrict output to stay within context windows.

* **Default execution:** `sem context <entity_name> --budget 8000 --json`

## 3. Validation Loops & Gotchas

* **Unrecognized Entities Fallback:** `sem` defaults to chunk-based diffing if the language is unsupported. Always verify the `entityType` in JSON outputs. If it reads `chunk`, semantic extraction failed for that file.
* **Rename Detection Verification:** `sem` utilizes a 3-phase matching system (Exact ID -> Structural Hash -> Fuzzy >80%). When reviewing changes, explicitly check if the `changeType` is marked as `renamed` or `moved` before assuming an entity was deleted.
* **Execution Environment:** Ensure `sem` operates within a valid Git repository root unless explicitly diffing two standalone files (`sem diff file1.ts file2.ts`).

## 4. MCP Server Integration (Optional)

If running inside an MCP-enabled environment, fallback to the provided MCP tools (`sem_entities`, `sem_diff`, `sem_blame`, `sem_impact`, `sem_log`, `sem_context`) rather than spawning shell commands.
