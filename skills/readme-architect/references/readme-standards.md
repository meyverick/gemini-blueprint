# readme Technical Standards & Structural Taxonomy

## 1. Foundational Philosophies

### Readme-Driven Development (RDD)

The methodology dictating that readme documentation must precede source code. It acts as a cognitive forcing function for public API design and architectural boundaries.

### ASCII Sorting & functional Capitalization

Historical lineage (PDP-10, UNIX) where capitalized filenames (readme.md) prioritized documentation at the top of directory listings via ASCII character sorting.

## 2. Cognitive Funneling (Consensus-Driven Anatomy)

| Level | Section Nomenclature | Cognitive Purpose and Funnel Position | Structural Contents and Execution Requirements |
| :---- | :---- | :---- | :---- |
| **L1** | **Project Title & Banner** | Instant Identification (Top of Funnel) | Clear H1 heading and brand logo/banner for immediate visual anchoring. |
| **L1** | **Status Badges** | Metadata Telemetry (Top of Funnel) | Dynamic SVG indicators (Shields.io) for build health, versioning, and coverage. |
| **L1** | **Description (The "Why")** | Value Proposition (Top of Funnel) | Succinct paragraph articulating the problem (Tension) and target demographic. |
| **L1** | **Visual Demonstrations** | Proof of Concept (Top of Funnel) | Animated GIFs or theme-responsive UI captures to reduce functional ambiguity. |
| **L2** | **Table of Contents** | Navigational Efficacy (Mid Funnel) | Anchor tags to facilitate non-linear reading and rapid context switching. |
| **L2** | **Installation** | Dependency Resolution (Mid Funnel) | Deterministic, copy-paste instructions with explicit prerequisites. |
| **L2** | **Usage / Quickstart** | Time to Value (Mid Funnel) | Minimal executable code snippet for verifiable output. |
| **L3** | **Architecture / API** | Deep Integration (Lower Funnel) | Parameter definitions, return types, and C4 Model diagrams. |
| **L4** | **Contributing** | Community Governance (Bottom of Funnel) | Directives for local development, linting, testing, and PR conventions. |
| **L4** | **Changelog** | Historical Context (Bottom of Funnel) | Direct link to `changelog.md` and summary of significance. |
| **L4** | **Contacts** | Support & Interaction (Bottom of Funnel) | GitHub issues/discussions. Programmatic `[project_id]` replacement. |
| **L4** | **Sponsorship** | Community Support (Bottom of Funnel) | Advocacy for the project and sponsorship links (GitHub Sponsors). |
| **L4** | **Credits** | Dynamic Attribution (Bottom of Funnel) | Placeholder `[[CREDITS]]` for contributor population. |
| **L4** | **License** | Legal Distribution (Bottom of Funnel) | Authoritative link to `license.md` and binding legal language. |

## 3. Linguistic Directives & Zero-Pronoun Enforcement

| Element | Professional Practice | Prohibited Antipatterns |
| :---- | :---- | :---- |
| **Perspective** | Objective Third-Person / Direct Action. | Avoid "I", "We", "You", "Our", "My". |
| **Voice** | Active Voice (identifies actor). | Avoid Passive Voice. |
| **Tense** | Present Tense (immediate state). | Avoid Future Tense. |
| **Imperative** | Direct commands (pronoun-free). | Avoid "Simply", "Just", "Obviously", "Easily". |
| **Tone** | Conversational and empathetic (peer-to-peer). | Avoid academic elitism or excessive formality. |
| **Inclusivity** | Gender-neutral, universally comprehensible terms. | Prohibit slang, idioms, or cultural pop-references. |
| **Narrative** | Tension, Pacing, Harmony, Hero's Journey. | Avoid dry lists without contextual utility. |

## 4. Formatting & Visual Hygiene

- **Line Length**: 80-100 characters max to prevent horizontal visual fatigue.
- **GFM Alerts**: Standardized urgency stratification (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`).
- **Emoji Pragmatics**: Consistent visual anchors semantically congruent with text valence.
- **Diagrams**: Mermaid.js following C4 Model hierarchy (Context, Container, Component, Code).
- **Theme Awareness**: Dynamic serving of graphics via HTML `<picture>` and `prefers-color-scheme`.
- **Bento UI**: Grid-based modular layouts for high-density information.
- **Progressive Disclosure**: `<details>` for secondary technical depth.

## 5. Domain Specializations

- **Research Data**: Provenance ledgers, ISO date formats, instrument models. Avoid proprietary formats.
- **Utility Frameworks**: Prescriptive class ordering handbook.
- **AI Agents**: `agents.md` behavior programming, persona mapping, repository constraints.

## 6. Operational Maintenance Limits

- **Pruning**: Max 5,000 branches.
- **Storage**: Max 10 GB on-disk size.
- **Density**: Max 3,000 files/directory; max 50 levels of depth.
