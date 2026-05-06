---
name: gemini-cli-mcp-desc
description: Introspects connected Model Context Protocol (MCP) servers and their exposed tools using the /mcp desc command. Returns validated schema payloads to ensure reliable remote tool execution.
---

# Gemini CLI MCP Introspection

This skill enables the extraction of structural definitions for available MCP servers and their specific tools within the Gemini CLI environment via the `/mcp desc` command.

## Phase 1: Discovery

**Trigger:** Use this skill when asked to determine the capabilities, connection status, or required tool arguments of a connected MCP server (e.g., a local database connector, a remote enterprise API).
**Target:** Extracts structured metadata (JSON) defining the remote capabilities.

## Phase 2: Activation (Pre-flight)

1. Verify `gemini` is in the system `$PATH`.
2. Verify the target MCP server name (and optional tool name) is known.
3. If the user request does not specify an MCP server, first run a general MCP discovery (not covered by this skill).

## Phase 3: Execution

Do not execute the CLI command directly via bash. Always use the provided Python wrapper to guarantee cross-platform execution, handle network latency gracefully, and enforce JSON schema validation.

**Command:**

```bash
# To describe the entire MCP server:
python scripts/run_mcp_desc.py --target <mcp_server_name>

# To describe a specific tool on an MCP server:
python scripts/run_mcp_desc.py --target <mcp_server_name> --tool <tool_name>
```
