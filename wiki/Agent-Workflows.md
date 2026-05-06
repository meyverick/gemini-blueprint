# Agent Workflows

The Gemini Blueprint Workspace leverages specialized sub-agents to perform complex, domain-specific tasks efficiently. This delegation model keeps the main agent's context clean and focuses its reasoning on high-level orchestration.

## Sub-Agents Overview

Sub-agents are independent agents with their own system prompts, tools, and context windows. They are invoked by the main agent as tools.

### Core Sub-Agents

- **`prompt-engineer`:** Audits project files and transforms vague requests into high-efficiency prompts.
- **`agent-architect`:** Specialized in designing and configuring new sub-agents.
- **`skill-architect`:** Focused on creating and optimizing specialized agent skills.

## How Delegation Works

1.  **Detection:** The main agent analyzes the user's request.
2.  **Matching:** If the task aligns with a sub-agent's expertise (e.g., "design a new agent"), the main agent selects the relevant specialist.
3.  **Invocation:** The main agent calls the sub-agent tool with a comprehensive prompt.
4.  **Execution:** The sub-agent performs the task in an isolated context.
5.  **Synthesis:** The sub-agent returns a structured report or artifact to the main agent.

## Creating Custom Agents

Custom agents are defined as Markdown files in the `agents/` directory.

### Agent Definition Format

Agent files must include a YAML frontmatter:

```markdown
---
name: my-agent
description: Description of the agent's expertise.
tools:
  - list_of_tools
model: gemini-3-flash-preview
---

System instructions for the sub-agent...
```

### Best Practices

- **Clear Descriptions:** The `description` field is critical for the main agent to know when to delegate.
- **Minimal Tools:** Grant only the tools necessary for the specific domain to ensure security and reliability.
- **Isolated Context:** Use sub-agents for turn-intensive tasks (e.g., batch refactoring) to preserve the main session's context window.
