# Gemini CLI Skills Registry Quirks

## "Broken" Skill States

If a skill appears in the JSON output under a `status: broken` flag, the agent MUST NOT attempt to execute it. This usually indicates a malformed `SKILL.md` frontmatter in that specific skill's directory.

- **Remediation:** Inspect the target skill's `SKILL.md` file directly to fix YAML frontmatter errors before re-running `/skills list`.

## Stale Registry Cache

The Gemini CLI caches skill manifests locally. If a skill was manually deleted from the filesystem but still appears in the `/skills list` output, the agent should ignore the phantom skill. Do not attempt to run a command to clear the cache unless specifically instructed by the user.
