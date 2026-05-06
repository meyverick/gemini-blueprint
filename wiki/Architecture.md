# Architecture

The Gemini Blueprint Workspace utilizes a modular, layer-based architecture designed to decouple core configuration from specialized skills and project-specific logic. This structure ensures high-velocity initialization while maintaining strict adherence to engineering standards.

## Layered Design

The architecture is composed of four primary layers:

1.  **Core Configuration Layer:** Defines the foundational rules, policies, and environment settings.
2.  **Specialized Skills Layer:** Provides task-specific workflows (e.g., README generation, changelog maintenance).
3.  **Agent Logic Layer:** Houses the definitions for specialized sub-agents.
4.  **Operational Layer:** Includes scripts and tools for repository maintenance and environment synchronization.

## System Diagram

```mermaid
graph TD
    A[Core Workspace] --> B[Extension Manifest]
    A --> C[Specialized Skills]
    A --> D[Sub-Agents]
    
    A --> P[Policies]
    A --> G[GEMINI.md Instructions]
    
    C --> C1[README Architect]
    C --> C2[Changelog Architect]
    C --> C3[Wiki Master]
    C --> C4[Forensic Git Historian]
    
    D --> D1[Prompt Engineer]
    D --> D2[Skill Architect]
    D --> D3[Agent Architect]
```

## Component Breakdown

### Extension Manifest (`gemini-extension.json`)
The central definition file for the workspace extension. It configures the extension's name, version, description, and integrated MCP servers.

### Instruction Tiering (`GEMINI.md`)
Instructions are managed through a hierarchical system:
- **Project Instructions (`./GEMINI.md`):** Team-shared architecture and workflows.
- **Global Personal Memory (`~/.gemini/GEMINI.md`):** Cross-project personal preferences.
- **Private Project Memory (`.gemini/tmp/.../MEMORY.md`):** Machine-specific or private notes.

### Policy Engine
Located in `policies/`, these TOML files define the security boundaries and execution rules for shell commands and MCP tools.

### Repository Maintenance
Utilities like `update_repos.py` ensure the workspace remains synchronized with its upstream dependencies, managing clones and fast-forwarding local branches.
