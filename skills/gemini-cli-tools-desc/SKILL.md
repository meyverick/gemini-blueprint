---
name: gemini-cli-tools-desc
description: Introspects Gemini CLI tools using the /tools desc command. Returns validated tool schemas, argument requirements, and usage constraints.
---

# Gemini CLI Tool Introspection

This skill enables the extraction of structural definitions for available tools within the Gemini CLI environment via the `/tools desc` command.

## Phase 1: Discovery

**Trigger:** Use this skill when asked to determine the capabilities, required arguments, or return types of a specific Gemini CLI tool, or when a previous tool execution fails due to schema mismatch.
**Target:** Extracts structured metadata (JSON) rather than raw text.

## Phase 2: Activation (Pre-flight)

1. Verify `gemini` is in the system `$PATH`.
2. Verify the target tool name is known (e.g., `File Fetcher`, `Google Search`).
3. If the tool name is unknown, first run a general tool discovery (not covered by this skill).

## Phase 3: Execution

Do not execute the CLI command directly via bash. Always use the provided Python wrapper to guarantee cross-platform execution, standard error capture, and JSON schema validation.

**Command:**

```bash
python scripts/run_tools_desc.py --tool <tool_name>
```
