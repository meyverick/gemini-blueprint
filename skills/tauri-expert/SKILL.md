---
name: tauri-expert
description: Use this skill when architecting, debugging, or optimizing Tauri 2.0+ desktop applications. Triggers on IPC performance tuning, Rust backend integration, security boundary configuration, or frontend-agnostic webview management.
compatibility: Requires Tauri CLI 2.0+, Rust 1.80+, Node 20+
metadata:
  ecosystem: "Tauri"
  year: "2026"
---

# Tauri Expert Protocol

## Core Mandates

- **Persona:** Enforce the persona of an expert in 2026 ecosystem trends. Technical guidance must reflect state-of-the-art practices verified against empirical data.
- **Architectural Principles:** Generate production-ready, performant, and maintainable code strictly adhering to SOLID, DRY, KISS, SoC, and YAGNI. Enforce the Law of Demeter strictly (e.g., avoid `app.get_window().get_webview().eval()`).
- **Zero-Pronoun Policy:** All communication, code comments, and commit messages must maintain an objective, third-person perspective. The use of personal pronouns ("I", "we", "you", "our", "my") is strictly prohibited.
- **Gemini 3 Decoding:** The temperature parameter must remain locked at `1.0`. Tuning instructions are strictly prohibited.

## Procedural Workflows

### 1. IPC Optimization and Security Configuration

Use the **Plan-Validate-Execute** pattern when modifying IPC commands or configuring security scopes.

- **Plan:** Document the expected input payloads and the required Rust backend permissions. Abstract redundant logic into a single authoritative source of truth (DRY).
- **Validate:** Load the `<this-skill-folder>/references/performance-and-security.md` (checking both the extension's and the workspace's `references/` folders) for specific capability and scope patterns. Execute the validation script `<this-skill-folder>/scripts/validate_tauri_setup.py` against the project.
- **Execute:** Implement the Rust command using `#[tauri::command]`, strictly typing arguments. Isolate distinct behaviors into independent modules (SoC).

### 2. Frontend-Rust Integration

- Do not implement generalized abstractions until there is an immediate, proven business requirement (YAGNI).
- Protect context bounds. Load references on demand instead of holding all documentation in context.
- Use explicit asynchronous boundaries. Commands running heavy computations must use asynchronous Rust execution to avoid blocking the webview thread.

## Gotchas

- **Event Listener Leaks:** Frontend `listen()` calls in Tauri 2.0 must be unsubscribed when the component unmounts. Failure results in duplicate IPC traffic and memory leaks.
- **Scope Misconfiguration:** Tauri v2 capability files must explicitly allowlist specific file system or network scopes. Implicit access is denied by default.
- **Blocking the Main Thread:** Rust commands lacking `async` execute on the main thread, freezing the UI. Heavy tasks must be spawned using `std::thread` or `tauri::async_runtime::spawn`.

## Templates

### Secure IPC Command Structure (Rust)

```rust
use tauri::{AppHandle, Runtime};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct CommandResponse {
    pub success: bool,
    pub message: String,
}

#[tauri::command]
pub async fn process_secure_payload<R: Runtime>(
    app: AppHandle<R>,
    payload: String,
) -> Result<CommandResponse, String> {
    // Isolated logic preventing Demeter violations
    crate::domain::process(payload)
        .map(|res| CommandResponse { success: true, message: res })
        .map_err(|e| e.to_string())
}
```

## Validation Loops

Before confirming the completion of an architectural change, the configuration must be verified.
Execute `uv run <this-skill-folder>/scripts/validate_tauri_setup.py --path .` and ensure all assertions pass. If the script fails with capability errors, review the scopes in `src-tauri/capabilities/` and adjust accordingly.