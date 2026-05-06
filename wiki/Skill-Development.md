# Skill Development

Skills are specialized procedural packages that extend the Gemini CLI with structured workflows, validation scripts, and reference materials. They are activated on-demand to provide expert guidance for specific tasks.

## Anatomy of a Skill

A skill is a directory located in `skills/` containing:

-   **`SKILL.md`:** The primary instruction file. It defines the persona, procedures, and resources for the skill.
-   **`references/`:** (Optional) Support documentation or technical standards.
-   **`scripts/`:** (Optional) Python or shell scripts for automated validation or processing.
-   **`assets/`:** (Optional) Templates, icons, or static resources.

## Built-in Skills

The Blueprint includes several state-of-the-art skills:

-   **`readme-architect`:** Generates documentation following the Stripe Benchmark.
-   **`changelog-architect`:** Manages `CHANGELOG.md` per Keep a Changelog v1.1.0.
-   **`github-wiki-master`:** Orchestrates and synchronizes repository wikis.
-   **`forensic-git-historian`:** Drafts high-fidelity, architectural commit messages.

## Creating a New Skill

1.  **Scaffold:** Create a new directory in `skills/` (e.g., `skills/my-skill/`).
2.  **Draft `SKILL.md`:** Define the activation criteria and the expert procedural guidance.
3.  **Implement Validation:** Add scripts in `scripts/` to ensure the skill's outputs meet technical standards.
4.  **Reference Assets:** Include any necessary templates or checklists.

## Usage Workflow

1.  **Activation:** The user or the main agent calls `activate_skill(name="skill-name")`.
2.  **Instruction Ingestion:** The content of `SKILL.md` is loaded into the agent's context.
3.  **Expert Execution:** The agent follows the specialized instructions within the `<instructions>` tags.
4.  **Verification:** Automated scripts are run to validate the results before completion.
