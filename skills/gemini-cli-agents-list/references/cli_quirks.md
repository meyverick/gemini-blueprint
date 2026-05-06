# Gemini CLI Agent Registry Quirks

## Offline Mode Truncation

If the user's environment is disconnected from the network, `/agents list` will only return locally cached agents. The JSON payload will include an `offline_mode: true` flag. If this flag is present, DO NOT attempt to route tasks to agents that require cloud-based tool execution (e.g., search agents).

## Delegated Auth Failures

If you attempt to route a task to an agent found via this skill, and it immediately fails with a `403 Forbidden`, the user's current session lacks the scope to invoke that specific agent persona. Do not attempt to force execution; request user intervention to update permissions.
