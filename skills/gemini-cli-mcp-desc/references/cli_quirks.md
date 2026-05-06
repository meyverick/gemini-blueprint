# Gemini CLI MCP Quirks

## Stale Process Locks

If the `run_mcp_desc.py` script consistently fails with a `Connection Refused` error despite the user claiming the server is running, the local MCP process may be zombie/orphaned. The agent should advise the user to run `pkill -f mcp` (on Unix/Linux/macOS) or kill the relevant node/python process via Task Manager (Windows) before restarting the connection.

## Unsupported Schema Types

Occasionally, experimental MCP servers return JSON Schemas (Draft 2020-12) containing arbitrary `$defs` or `$ref` pointers that the Gemini CLI cannot fully resolve inline. If the returned JSON contains unresolved `$ref` strings, do NOT hallucinate the parameters. Inform the user that the MCP server's schema formatting is strictly incompatible with the current agent capability.
