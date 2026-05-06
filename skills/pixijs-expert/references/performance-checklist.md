# PixiJS Performance & Optimization Checklist

This document details empirical benchmarks and optimization triggers for PixiJS v8+ WebGPU and WebGL architectures.

## 1. WebGPU / WebGL Backend Selection

- **WebGPU-First**: PixiJS v8 defaults to WebGPU. Ensure fallback architectures (WebGL2) are maintained for wider compatibility.
- **Trigger**: Write custom WGSL shaders natively. Always supply GLSL variants if mobile or legacy browser support is within the project scope.

## 2. Draw Call Optimization & Batching

- **Empirical Limit**: Aim for fewer than 100 draw calls per frame on mobile, and 500 on desktop. Use Spector.js or WebGPU tracing to audit.
- **Batch Breakage**: Avoid alternating distinct textures or blend modes in the display list.
- **Texture Atlasing**: Group assets into spritesheets. A single atlas allows the renderer to batch thousands of sprites into a single draw call.

## 3. Culling & Visibility

- **Trigger**: If a scene contains >2,000 objects, but <20% are visible on screen.
- **Action**: Implement explicit bounds-checking or spatial hashing (e.g., QuadTree).
- **Pixi API**: Set `cullable = true` on display objects that frequently exit the viewport. Note that PixiJS only processes culling if a culling mechanism is explicitly executed in the ticker loop.

## 4. Texture and Memory Management

- **Compressed Textures**: Use Basis Universal (`.basis` / `.ktx2`) or ASTC/ETC2 formats for high-resolution assets to reduce VRAM footprint by up to 80%.
- **Garbage Collection**: VRAM does not auto-collect efficiently. 
  - Call `Assets.unload('bundleId')` when navigating away from scenes.
  - Call `texture.destroy(true)` for dynamically generated textures (e.g., from `RenderTexture` or HTML Canvas).

## 5. Ticker & Loop Optimization

- Disable `Ticker.shared.autoStart` if rendering static scenes. Manually call `renderer.render(stage)` only when reactive state dictates a visual change.
- Limit CPU-side math within the render loop. Pre-compute trigonometric values and matrices where applicable.
