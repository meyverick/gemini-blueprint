---
name: threlte-expert
description: Use this skill when engineering 3D web applications requiring Threlte (v8+) and Svelte 5 (Runes). Applies strict SOLID and SoC principles to 3D scene graphs, enforces Law of Demeter in state management, and implements high-scale performance techniques.
compatibility: Requires Threlte v8+ and Svelte 5.
metadata:
  gemini_temperature: 1.0
---

# Threlte Expert Operations

## Core Architectural Directives

1. **Svelte 5 Runes Integration**: State management within the 3D scene graph must exclusively utilize Svelte 5 Runes (`$state`, `$derived`, `$effect`). Legacy reactive declarations (`$:`) are strictly prohibited.
2. **Performance & Scaling**: Applications targeting high entity counts (>1000) must implement `InstancedMesh` with manual matrix updates. Individual mesh instancing within loops is prohibited.
3. **Law of Demeter in 3D Context**: Components must not deeply traverse the Three.js scene graph. Access to objects must occur via explicit, direct references or immediate parent-child prop passing. Avoid `scene.getObjectByName().children[0].material.color.set()`.
4. **Separation of Concerns (SoC)**: Logic defining physics, rendering pipelines, and user interaction must exist in separate components or TypeScript modules. Monolithic Threlte components are strictly prohibited.

## Procedural Workflow: Plan-Validate-Execute

When tasked with creating or modifying a Threlte component, execute the following procedure:

### 1. Plan

- Define the entity hierarchy (Scene, Camera, Lighting, Meshes).
- Determine performance requirements (Standard Mesh vs. InstancedMesh).
- Identify required state variables and their optimal Rune assignment.

### 2. Validate

- Execute `uv run <this-skill-folder>/scripts/validate_threlte_setup.py` to confirm the environment dependencies meet v8+ requirements.
- Ensure no legacy Svelte APIs are utilized in the proposed design.

### 3. Execute

- Implement the component using the approved templates.
- Run static analysis checks if available.

## Gotchas & Failure Modes

- **Reactivity in Render Loops**: Accessing `$state` Runes directly within a high-frequency `useTask` loop can cause severe frame drops if it triggers Svelte re-renders. Always read state at the task initialization, or decouple visual updates from Svelte's DOM update cycle by mutating Three.js object properties directly within the frame loop.
- **InstancedMesh Updates**: When updating matrices for an `InstancedMesh` via a `useTask` loop, the developer must explicitly set `mesh.instanceMatrix.needsUpdate = true`. Failure to do so will result in static instances.
- **Material Mutability**: Sharing materials across meshes implies global modification. If a single entity requires a distinct material property (e.g., color tinting), clone the material or use instance colors.
- **Post-Processing Overdraw**: Stacking multiple passes (e.g., Bloom, SSR) requires careful order-of-operations mapping. Always place antialiasing (SMAA/FXAA) at the end of the chain unless depth-dependent.

## Templates

### High-Performance InstancedMesh Component

```svelte
<script lang="ts">
  import { T, useTask } from '@threlte/core';
  import { InstancedMesh, Matrix4, Vector3 } from 'three';

  let { count = 1000 } = $props<{ count?: number }>();

  let meshRef = $state<InstancedMesh>();
  const dummy = new Matrix4();
  const position = new Vector3();

  useTask((delta) => {
    if (!meshRef) return;
    
    for (let i = 0; i < count; i++) {
      // Direct mutation pattern bypassing Svelte reactivity for performance
      position.set(
        Math.sin(delta + i) * 10,
        Math.cos(delta + i) * 10,
        Math.sin(delta * i) * 10
      );
      dummy.setPosition(position);
      meshRef.setMatrixAt(i, dummy);
    }
    
    meshRef.instanceMatrix.needsUpdate = true;
  });
</script>

<T.InstancedMesh bind:ref={meshRef} args={[undefined, undefined, count]}>
  <T.BoxGeometry />
  <T.MeshPhysicalMaterial color="#ffffff" transmission={1} roughness={0} thickness={0.5} />
</T.InstancedMesh>
```

## Validation Loops

Before concluding execution, the generated output must be validated:

1. Verify the presence of `bind:ref` instead of deprecated bindings.
2. Confirm that matrix updates within `useTask` include `.needsUpdate = true`.
3. Ensure no interactive prompts or shell configurations exist within bundled scripts.

## File References

Load detailed technical references only when specific domain knowledge is required. You must check both the extension's and the workspace's `references/` folders for the following:

- Review deep performance metrics: `<this-skill-folder>/references/performance.md`
- Review exact Rune integration techniques: `<this-skill-folder>/references/runes-integration.md`
