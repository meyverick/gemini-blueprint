---
name: pixijs-expert
description: Use this skill when architecting, generating, refactoring, or optimizing PixiJS v8+ rendering logic, scene graphs, or WebGPU/WebGL shaders. Triggers on requests involving PixiJS application setup, asset loading, performance tuning, or reactive framework integration.
compatibility: Requires PixiJS 8+ and modern WebGPU/WebGL2 browser environments.
---

# PixiJS Expert Architecture Directives

This skill enforces elite-level PixiJS v8+ development standards, targeting WebGPU-first architectures. All generated code must be production-ready, highly performant, and maintainable, reflecting the state-of-the-art 2026 ecosystem.

## Core Architectural Principles

- **SOLID & SoC**: Isolate rendering logic from business logic and state management. PixiJS components must be exclusively responsible for visual representation.
- **Law of Demeter**: Enforce strict boundary encapsulation within the Scene Graph. A component must only manipulate its immediate children. Deep scene graph traversals (e.g., `parent.getChildByName('x').getChildAt(0)`) are strictly prohibited. Pass dependencies explicitly or use event-driven communication.
- **DRY & YAGNI**: Abstract redundant rendering logic (e.g., common filter setups) into reusable modules. Do not implement complex culling or custom batching until empirical performance data necessitates it.
- **KISS**: Prioritize native PixiJS v8 API features (e.g., built-in Asset loader, WebGPU batcher) over custom, convoluted implementations.

## Decoding Compliance

- **Temperature Constraint**: Temperature MUST be locked at `1.0` for all Gemini 3 models to ensure optimal reasoning paths. Tuning temperature is strictly prohibited.

## PixiJS v8 Implementation Mandates

### 1. Scene Graph Mastery

- Extend `Container` for custom entities. Encapsulate all child creation and destruction within the class lifecycle.
- Maintain a flat scene graph hierarchy where possible to optimize the transform update loop.
- Use `cullable = true` on containers heavily populated out-of-bounds to allow the renderer to skip processing.

### 2. Rendering Optimization

- **WebGPU-First**: Assume WebGPU backend is preferred. Ensure custom shaders are provided in WGSL alongside GLSL fallbacks.
- **Batching**: Maximize batching efficiency by grouping items with identical textures and blend modes. Avoid arbitrary z-index sorting that breaks batches.
- **Tickers**: Avoid anonymous functions in `Ticker.shared.add()`. Always bind explicit methods and ensure `Ticker.shared.remove()` is called during component destruction to prevent memory leaks.

### 3. Shader Development

- Utilize the PixiJS v8 `Filter` API. Provide WGSL source for `gpuProgram` and GLSL for `glProgram`.
- Ensure uniform updates occur only when data mutates, not continuously on every frame, to minimize CPU-to-GPU overhead.

### 4. Asset Management

- Always use `Assets.load()` and `Assets.addBundle()` for asynchronous loading. Avoid synchronous texture creation during runtime.
- Implement lazy loading for non-critical assets.
- Unload unused assets using `Assets.unload()` when transitioning major scenes. Always call `.destroy({ children: true, texture: true })` on defunct containers.

### 5. Reactive Patterns (e.g., Svelte 5 Integration)

- Maintain strict SoC: Reactive state (e.g., Svelte `$state`) drives the data model. PixiJS observes state changes and interpolates visual updates.
- Do not store PixiJS DisplayObjects in reactive proxies (e.g., Svelte `$state` or Vue `ref`), as proxying complex WebGL objects causes severe performance degradation and memory leaks. Store raw data only.

## Gotchas

- **Proxy Object Bloat**: Injecting PixiJS instances into reactive framework state managers (like Svelte Runes or Redux) causes catastrophic recursion and memory leaks. Always unwrap or store references externally.
- **Texture Memory Leaks**: Destroying a `Sprite` or `Container` does NOT destroy the underlying base texture. Base textures must be explicitly destroyed or managed via the Assets cache.
- **Event Listener Accumulation**: Failing to remove `.on()` interaction listeners or Ticker callbacks upon container destruction is the primary cause of zombie objects in PixiJS.
- **Law of Demeter Violations**: Relying on deep `.parent` or `.getChildAt()` chains makes the scene graph brittle. If the UI structure changes, the code breaks. Use signals or custom events for inter-component communication.

## Templates

### Custom Component Boilerplate

Use this template when architecting custom PixiJS display objects to guarantee proper lifecycle management and encapsulation.

```typescript
import { Container, Sprite, Assets, Ticker } from 'pixi.js';

export class CustomEntity extends Container {
    private sprite!: Sprite;
    private boundUpdate: (ticker: Ticker) => void;

    constructor() {
        super();
        this.boundUpdate = this.update.bind(this);
        this.initialize();
    }

    private async initialize() {
        // Enforce asynchronous loading
        const texture = await Assets.load('path/to/asset.png');
        this.sprite = new Sprite(texture);
        this.addChild(this.sprite);

        // Explicitly bind ticker events
        Ticker.shared.add(this.boundUpdate);
    }

    private update(ticker: Ticker) {
        // Implement rotation or movement
        if (this.sprite) {
            this.sprite.rotation += 0.01 * ticker.deltaTime;
        }
    }

    override destroy(options?: any) {
        // Prevent memory leaks
        Ticker.shared.remove(this.boundUpdate);
        
        // Destroy children and textures explicitly if necessary
        super.destroy({ children: true, ...options });
    }
}
```

## Procedural Workflow: Feature Implementation

1. **Plan**: Define the visual requirement. Identify required assets, shaders, and the necessary container hierarchy.
2. **Architect**: Design the Scene Graph structure. Ensure strict encapsulation (Law of Demeter) and separate rendering state from application state.
3. **Execute**: Implement the rendering logic. Utilize the `Assets` module for loading, set up `Ticker` bindings properly, and apply WGSL/GLSL filters if needed.
4. **Validate**: Verify memory management by checking `.destroy()` methods and confirming Ticker callbacks are removed.

## Validation Loops

Execute the following steps to verify implementation correctness:

1. Run the validation script against the target file:
   `uv run <this-skill-folder>/scripts/validate_pixi_patterns.py --file <path/to/component.ts>`
2. Analyze the emitted JSON for Law of Demeter violations, missing destroy methods, or reactive state bloat.
3. Refactor any flagged code to adhere strictly to encapsulation and memory management protocols.

## References

Load detailed technical references only when specific domain knowledge is required. You must check both the extension's and the workspace's `references/` folders for the following:

- `<this-skill-folder>/references/performance-checklist.md`: Empirical benchmarks, WebGPU optimization triggers, and memory management guidelines.
