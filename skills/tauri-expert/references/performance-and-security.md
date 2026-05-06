# Tauri 2.0 Performance & Security Architecture

## Capability Management

Tauri v2 shifts away from the monolithic `tauri.conf.json` allowlist to granular capabilities defined in `src-tauri/capabilities/`.
- Capabilities must be scoped to specific windows or webviews.
- Strict definitions minimize the attack surface by enforcing default-deny semantics.

## The Law of Demeter in Tauri State Management

When accessing managed state via `tauri::State`, deep property access must be strictly avoided.

**Anti-pattern:**
```rust
state.get_database().get_connection().query()
```

**State-of-the-art practice:**
```rust
crate::database::execute_query(&state, payload)
```
Encapsulate the interactions within the domain module to maintain strict boundary separation.

## Inter-Process Communication (IPC)

- Strongly typed schemas must be utilized for all `invoke` calls.
- IPC payloads exceeding 10MB must bypass JSON serialization. Utilize `RawBuffer` or custom streaming protocols to minimize memory overhead.
- For high-frequency telemetry or real-time state synchronization, emit events using `app.emit_to()` rather than continuous polling from the frontend.
