# Gemini CLI Environment Quirks

## Authentication Expiry

If `run_tools_desc.py` returns a 401 Unauthorized equivalent in its stderr payload:

1. The agent must pause introspection.
2. Execute `gemini auth login --refresh`.
3. Retry the target script.

## Shell Escaping

If passing complex tool names (e.g., nested or namespaced tools like `google:search`), the Python script's `subprocess.run` list-based execution mitigates bash injection. Do not attempt to manually escape tool names in the python call.