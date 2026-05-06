---
name: svelte-expert
description: Use this skill when architecting, generating, refactoring, or optimizing Svelte 5 components and SvelteKit applications. Triggers on requests involving Svelte Runes, SvelteKit load functions, form actions, or component state management.
compatibility: Requires Svelte 5+ and SvelteKit 2+.
---

# Svelte Expert Architecture Directives

This skill enforces elite-level Svelte 5 and SvelteKit development standards, reflecting state-of-the-art 2026 ecosystem trends. All generated code must be production-ready, highly performant, and maintainable.

## Core Architectural Principles

- **SOLID & SoC**: Isolate distinct behaviors. Components must have a single responsibility. Extract complex logic into external `.ts` or `.svelte.ts` files.
- **Law of Demeter**: Enforce strict boundary encapsulation. Components must only interact with immediate dependencies via `$props()` and snippets. Deep prop drilling is strictly prohibited; utilize Context API or shared `$state` modules for deeply nested state.
- **DRY & YAGNI**: Prevent speculative engineering. Abstract redundant logic into single sources of truth.
- **KISS**: Prioritize cognitive simplicity over convoluted abstractions.

## Decoding Compliance

- **Temperature Constraint**: Temperature MUST be locked at `1.0` for all Gemini 3 models to ensure optimal reasoning paths. Tuning temperature is strictly prohibited.

## Svelte 5 Implementation Mandates

1. **Runes over Legacy Reactivity**:
    - Must use `$props()` for component inputs. Legacy `export let` is strictly prohibited.
    - Must use `$state()` for reactive variables.
    - Must use `$derived()` for computed values.
    - Must use `$effect()` strictly for side effects (e.g., DOM manipulation, subscriptions, canvas operations), not for state derivation.
2. **Event Handling**:
    - Must use modern event attributes (e.g., `onclick`, `onkeydown`). Legacy `on:click` directives are prohibited.
    - Must pass callback functions as props instead of utilizing `createEventDispatcher`.
3. **Snippets**:
    - Must utilize snippets (`{#snippet ...}`) for reusable markup within components instead of legacy `<slot>` elements.

## SvelteKit Architecture Mandates

1. **Load Functions**:
    - Distinguish strictly between Universal Load (`+page.ts` - runs on server and client) and Server Load (`+page.server.ts` - runs only on server).
    - Always return serializable JSON from load functions.
2. **Form Actions**:
    - Implement progressive enhancement using `use:enhance` for form actions in `+page.server.ts`.
3. **Environment Variables**:
    - Strictly separate public (`$env/static/public`) and private (`$env/static/private`) variables. Never expose private variables to the client.

## Gotchas

- **Reactivity Loss**: Destructuring `$props()` without the `bind:` directive or deep reactive tracking can cause reactivity loss. Always access properties directly from the destructured object if reactivity is required, or use `$derived()`.
- **Effect Loops**: Overusing `$effect()` to update `$state()` values can cause infinite render loops. Derive state using `$derived()` whenever possible.
- **Server-Side State Bleed**: Never define global `$state()` outside of the component context in server-rendered environments without request-scoping (e.g., using SvelteKit's `locals`), as this causes cross-request state pollution.
- **Prop Fallbacks**: Default values in `$props()` destructuring are evaluated upon initialization. If a prop is bound, changes do not re-evaluate the fallback.

## Procedural Workflow: Execution Loop

Follow the phased disclosure protocol strictly when scaffolding or refactoring Svelte modules.

1. **Plan & Discovery**:
    - Identify the single responsibility of the component and define required `$props()`.
    - If specific architectural patterns or APIs are unknown, consult the index in `references/docs-index.md` to find relevant documentation paths.
    - Use the `get-documentation` MCP tool on those paths *only* when specific domain knowledge is required. Minimize document requests to conserve token limits.
2. **Architect**:
    - Determine if external state modules (`.svelte.ts`) are necessary to respect the Law of Demeter and decouple logic from the view.
3. **Act**:
    - Implement the component using Svelte 5 Runes and modern event handlers.
4. **Validate**:
    - Invoke the `svelte-autofixer` tool immediately passing the generated code.
    - Resolve any findings (e.g., deprecated Svelte 4 reactivity patterns, missing accessible attributes).
    - Repeat the autofix validation loop until the tool returns zero issues. Do not finalize code until this validation passes.
5. **Finalize**:
    - Once the code passes the validation loop, provide it to the user.
    - Ask the user if they would like a Svelte playground link generated. If affirmed, format the output into an `App.svelte` entry point and invoke the `playground-link` tool.

## Validation Loops

Execute the following steps to verify implementation correctness before invoking the autofixer:

1. Run the local validation script against the target file: `uv run <this-skill-folder>/scripts/validate_svelte5.py --file <path/to/component.svelte>`
2. Run environment validation: `uv run <this-skill-folder>/scripts/validate_env.py`
3. Address any emitted errors regarding legacy syntax or architectural violations.

## References

Load detailed technical references only when specific domain knowledge is required. You must check both the extension's and the workspace's `references/` folders for the following:

- `<this-skill-folder>/references/svelte-5-runes.md`: Comprehensive guide on Rune mechanics and migration strategies.
- `<this-skill-folder>/references/docs-index.md`: Massive index of available Svelte MCP documentation paths.
