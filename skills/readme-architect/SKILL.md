---
name: readme-architect
description: An elite skill for generating high-fidelity, Stripe-benchmark repository documentation. Enforces Readme-Driven Development (RDD), C4 architectural diagrams, and cognitive funneling.
metadata:
  dependencies: python>=3.9
---

# Readme Architect Skill

## Core Mission

Transform the static readme into a "Digital Handshake" and "Operational Blueprint" that maximizes Developer Experience (DX). You must strictly adhere to the principles of Readme-Driven Development (RDD), cognitive funneling, and technical storytelling.

## Foundational Mandates

1. **Zero-Pronoun Policy:** Maintain an objective, third-person perspective. The use of personal pronouns (I, we, you, our, my) is strictly prohibited. Utilize the active voice and present tense.
2. **Eradication of Fluff:** Do not use belittling or subjective words such as "simply", "just", "obviously", or "easily".
3. **Progressive Disclosure:** Implement standard HTML/Markdown elements (`<details>`, GFM Alerts) for secondary information depth.

## Operational Workflow

### Phase 1: Environment & Constraint Audit

1. **Repository Audit:** Execute `python <this-skill-folder>/scripts/audit_repo_limits.py` (resolving the path relative to this `SKILL.md` file). This script deterministically verifies that the repository is within operational bounds (branch count < 5000, storage < 10GB, depth < 50 levels). **Do not proceed if this script throws a critical violation.**
2. **Ingestion:** Analyze the project tech stack, functional goals, existing source code, and current documentation state.

### Phase 2: Structural Drafting & Funneling

1. Establish the underlying problem ("Tension") that the repository solves.
2. Consult **[readme-standards.md](<this-skill-folder>/references/readme-standards.md)** to map out the Cognitive Funnel.
3. Ensure all mandatory L1 (Top of Funnel) to L4 (Bottom of Funnel) sections are accounted for, from Status Badges down to License & Attribution.

### Phase 3: Visual Synthesis (Architecture as Code)

1. Treat architectural visualizations as version-controlled source code.
2. Generate **Mermaid.js** diagrams adhering to the **C4 Model** (Context, Container, Component, Code).
3. Wrap all visualizations in theme-aware `<picture>` tags using `prefers-color-scheme` to support Light/Dark modes.

### Phase 4: Formatting Hygiene & Linguistic Audit

1. Ensure strict compliance with formatting limits: wrap lines at 80-100 characters.
2. Standardize GFM Alerts (`> [!NOTE]`, `> [!TIP]`, etc.) for urgency stratification.
3. Execute a final sweep for zero-pronoun compliance. (e.g., translate "connect with me" to "connect with the project maintainers").

### Phase 5: Execution & Delivery

1. Compile the final `readme.md` file.
2. Ensure the authoritative License clause is embedded exactly as dictated by the domain standards.
