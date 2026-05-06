---
name: gemini-cli-skills-list
description: Introspects available Gemini CLI agent skills using the /skills list command. Returns validated JSON representing active, available, and broken skills to optimize workflow selection.
---

# Gemini CLI Skill Introspection

This skill enables the extraction of all currently installed, active, and available agent skills within the Gemini CLI environment via the `/skills list` command.

## Phase 1: Discovery

**Trigger:** Use this skill when asked to list your current capabilities, verify if a specific skill is installed, or when you need to audit the active environment before attempting a complex, multi-step workflow.
**Target:** Extracts structured metadata (JSON) categorizing skills by their operational state (`active`, `inactive`, `broken`).

## Phase 2: Activation (Pre-flight)

1. Verify `gemini` is in the system `$PATH`.
2. Do not attempt to guess skill names before running this command if the user request is ambiguous.

## Phase 3: Execution

Do not execute the CLI command directly via bash. Always use the provided Python wrapper to guarantee cross-platform execution, standard error capture, and strict JSON schema validation.

**Command:**

```bash
python scripts/run_skills_list.py
```
