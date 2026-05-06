# Threlte Performance Optimization Architecture

## Instanced Rendering Strategy
When the entity count exceeds 1000 items, traditional mesh rendering incurs extreme draw call overhead. Implement `T.InstancedMesh`. Ensure `instanceMatrix.needsUpdate = true` is executed whenever an instance's transform is modified.

## Frame Loop Optimization (`useTask`)
`useTask` executes on every frame.
- Do not instantiate new objects (e.g., `new Vector3()`, `new Matrix4()`) inside the task block.
- Pre-allocate all matrices, vectors, and quaternions outside the task closure.
- Do not invoke Svelte state mutations (`$state`) inside the loop if they trigger DOM updates. Read values, but mutate Three.js objects directly to decouple the 3D rendering pipeline from Svelte's reactive lifecycle.

## Material Selection
- Prefer `MeshBasicMaterial` for background or unlit objects to minimize computational overhead.
- Limit the use of `MeshPhysicalMaterial` with transmission (liquid glass aesthetics) to hero objects due to heavy shader compilation and render times. Always explicitly define `roughness`, `thickness`, and `transmission` bounds.