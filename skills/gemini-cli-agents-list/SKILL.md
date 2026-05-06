---
name: gemini-cli-agents-list
description: Introspects the registry of available Gemini CLI agents using the /agents list command. Returns validated JSON representing active profiles to optimize task delegation and routing.
---

# Gemini CLI Agent Introspection

This skill enables the extraction of all currently installed and active agent profiles within the Gemini CLI environment via the `/agents list` command.

## Phase 1: Discovery

**Trigger:** Use this skill when asked to list available agent personas, verify if a specific agent type exists before delegation, or audit the multi-agent environment prior to launching a distributed workflow.
**Target:** Extracts structured metadata (JSON) detailing agent names, capabilities, and system readiness.

## Phase 2: Activation (Pre-flight)

1. Verify `gemini` is available in the system `$PATH`.
2. Determine if the user request implies filtering (e.g., "Find an agent good at Python"). Note that filtering happens *after* execution by parsing the JSON payload in your context window.

## Phase 3: Execution

Do not execute the raw CLI command directly via a shell. Always use the provided Python wrapper to guarantee cross-platform execution, standard error capture, and strict JSON schema validation.

**Command:**

```bash
python scripts/run_agents_list.py
```
